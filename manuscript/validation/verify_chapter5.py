"""Verify Chapter 5 samples, parameter axes, registers, shot settings and DD model.

Uses manuscript/validation/requirements.txt; no credentials or QPU required.
    python -X utf8 -B manuscript/validation/verify_chapter5.py
    python -X utf8 -B manuscript/validation/verify_chapter5.py --write-figures

Runs trusted manuscript examples in a temporary directory. Runtime examples use
GenericBackendV2 locally. DD's physical effectiveness and service scheduling are
not simulated by these Runtime calls. Socket connections are forbidden in checks.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from contextlib import chdir, redirect_stdout
from importlib.metadata import version
from io import StringIO
import os
from pathlib import Path
import re
import shutil
import tempfile
from unittest.mock import patch
import warnings

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "qiskit-manuscript-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.primitives.containers import SamplerPub
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.quantum_info import Operator, Statevector
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2, SamplerV2

from verify_sample_sections import ROOT, anchors, check_links, close, require

SOURCE = ROOT / "manuscript/ja/05-sampler.md"
ASSETS = SOURCE.parent / "figures/05"
NAMES = (
    "shot_records", "shot_counts", "parameter_sweep", "parameter_order", "local_shots",
    "submit_shot_comparison", "named_register", "multiple_registers", "dd_model", "submit_with_dd",
)
FUNCTIONS = {"submit_shot_comparison", "submit_with_dd"}
ORIGINAL_ANCHORS = {
    "sampler-purpose", "sampler-pub", "sampler-result-registers",
    "sampler-options", "sampler-compatibility",
}
ORIGINAL_HEADINGS = [
    "何を計算するか", "Sampler PUBとshots優先順位", "result fieldはregister名から来る",
    "Runtime optionsとdynamical decoupling", "feature compatibilityは都度確認する",
    "典型的な誤答", "章末チェック",
]


def run_examples(directory: Path) -> dict[str, dict]:
    source = SOURCE.read_text(encoding="utf-8")
    require(ORIGINAL_ANCHORS <= anchors(source), "Original anchor removed")
    require(re.findall(r"^## (.+)$", source, re.M) == ORIGINAL_HEADINGS, "H2 headings changed")
    prose = re.sub(r"```.*?```", "", source, flags=re.S)
    require(not any("（" in span or "）" in span for span in re.findall(r"\*\*([^*\n]+)\*\*", prose)),
            "Parenthesis inside bold")
    require(not re.search(r"mock|practice-bank|PLACEHOLDER", source, re.I), "Unexpected placeholder/reference")
    examples = list(re.finditer(r"```python\n(.*?)\n```", source, re.S))
    require(len(examples) == len(NAMES), "Unclassified Python block")
    namespaces = {}
    with chdir(directory):
        for name, example in zip(NAMES, examples, strict=True):
            namespace = {"__name__": "__main__"}
            tree = ast.parse(example[1])
            if name in FUNCTIONS:
                require(len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef),
                        "Runtime block must only define a function")
                function = tree.body[0]
                require(function.name == name and not function.decorator_list, "Unexpected definition")
                require(all(isinstance(d, ast.Constant) for d in function.args.defaults), "Executable default")
                require(source[:example.start()].rstrip().endswith("<!-- validation: runtime-function -->"),
                        "Missing function validation marker")
            stdout = StringIO()
            with redirect_stdout(stdout):
                exec(compile(tree, str(SOURCE), "exec"), namespace)
            if name in FUNCTIONS:
                require(not stdout.getvalue(), "Definition produced output")
            else:
                output = re.match(r"\s*出力:\s*```text\n(.*?)\n```", source[example.end():], re.S)
                require(output is not None, f"Missing output: {name}")
                require(stdout.getvalue().strip() == output[1].strip(),
                        f"Output differs for {name}:\n{stdout.getvalue()}")
                print(f"PASS Chapter 5 printed output: {name}")
            namespaces[name] = namespace
            plt.close("all")
    images = {Path(link).name for link in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)}
    require(images == {p.name for p in directory.glob("*.png")}, "Figure outputs and links differ")
    for name in images:
        with Image.open(directory / name) as img:
            require(img.format == "PNG" and min(img.size) >= 180, "Invalid PNG")
            require(any(lo < hi for lo, hi in img.convert("RGB").getextrema()), "Blank PNG")
        with Image.open(directory / name) as img:
            img.verify()
    print("PASS 2 figures, 5 preserved explicit anchors and 7 preserved H2 headings")
    return namespaces


def check_samples_and_axes(ns: dict[str, dict]) -> None:
    sample = ns["shot_records"]
    close(Statevector(sample["qc"].remove_final_measurements(inplace=False)).data,
          np.array([1, 0, 0, 1]) / np.sqrt(2))
    require(Counter(sample["bits"].get_bitstrings()) == sample["counts"], "Shot records/counts mismatch")
    require(sum(sample["counts"].values()) == 8, "Total shots mismatch")
    require(sample["counts"].get("01", 0) == 0, "Absent outcome handling")
    plus = np.array([1, 0, 0, 1]) / np.sqrt(2)
    minus = np.array([1, 0, 0, -1]) / np.sqrt(2)
    close(abs(plus)**2, abs(minus)**2)
    require(not np.allclose(plus, minus), "Same probabilities do not imply same state")

    sweep = ns["parameter_sweep"]
    bits = sweep["bits"]
    require(bits.shape == (3,) and bits.num_shots == 32 and bits.num_bits == 1, "Result axes")
    require(bits.array.shape == (3, 32, 1), "Packed bytes versus logical shape")
    combined = Counter()
    for index, angle in enumerate(sweep["values"][:, 0]):
        records = bits.get_bitstrings(index)
        counts = bits.get_counts(index)
        require(len(records) == 32 and Counter(records) == counts, "Condition selection")
        combined.update(counts)
        bound = sweep["qc"].assign_parameters({sweep["theta"]: angle})
        close(Statevector(bound.remove_final_measurements(inplace=False)).probabilities(),
              [np.cos(angle/2)**2, np.sin(angle/2)**2])
    require(dict(combined) == bits.get_counts() and sum(combined.values()) == 96, "Pooled conditions")
    # Change both parameter count and number of conditions (chapter question).
    sample = ns["parameter_order"]
    values = np.array([[0, 0], [0, np.pi], [np.pi, 0], [np.pi, np.pi], [0.4, 1.2]])
    result = StatevectorSampler(seed=7).run([(sample["qc"], values)], shots=100).result()[0].data.meas
    require(result.shape == (5,) and result.num_shots == 100, "Five conditions/two parameters")
    require(sum(result.get_counts().values()) == 500 and result.get_counts(2) == {"10": 100},
            "Chapter question result location/denominator")
    for a, z in values:
        bound = sample["qc"].assign_parameters({sample["a"]: a, sample["z"]: z})
        expected = np.kron([np.cos(a/2), np.sin(a/2)], [np.cos(z/2), np.sin(z/2)])
        close(Statevector(bound.remove_final_measurements(inplace=False)).data, expected)
    qc = ns["local_shots"]["qc"]
    try:
        SamplerPub.coerce((qc, 128))
    except ValueError:
        pass
    else:
        raise AssertionError("Shots in parameter slot accepted")
    try:
        StatevectorSampler().run([qc], precision=0.01)
    except TypeError:
        pass
    else:
        raise AssertionError("Sampler accepted precision")
    print("PASS raw samples, finite counts, phase ambiguity, parameter axes/order, pooled counts and PUB slots")


def check_registers(ns: dict[str, dict]) -> None:
    named = ns["named_register"]
    qc, bits = named["qc"], named["bits"]
    pairs = [(qc.find_bit(item.qubits[0]).index, qc.find_bit(item.clbits[0]).index)
             for item in qc.data if item.operation.name == "measure"]
    require(pairs == [(2, 0), (0, 1)], "Named-register measurement mapping")
    require(bits.shape == () and bits.num_bits == 2, "No condition axis is not empty data")
    require(bits.slice_bits([1]).get_counts() == {"0": 8}, "Second classical bit")
    question = QuantumCircuit(4, 2)
    question.x(1)
    question.measure([3, 1], [0, 1])
    data = StatevectorSampler(seed=7).run([question], shots=8).result()[0].data.c
    require(data.get_counts() == {"10": 8} and data.slice_bits([0]).get_counts() == {"0": 8},
            "Changed measurement destination question")
    multi = ns["multiple_registers"]
    require(all(a != b for a, b in multi["pairs"]), "Anticorrelation lost")
    require(multi["joint_counts"] == {"01": 5, "10": 3}, "Explicit left-right string order")
    same = ["00", "11"]
    different = ["01", "10"]
    require(all(Counter(s[index] for s in same) == Counter(s[index] for s in different)
                for index in [0, 1]), "Equal marginals counterexample")
    require(Counter(same) != Counter(different), "Equal marginals must not fix joint distribution")
    print("PASS register names, classical-bit order, bit slicing and joint-vs-marginal records")


def check_dd_model(ns: dict[str, dict]) -> None:
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    def rz(angle):
        return np.diag([np.exp(-1j*angle/2), np.exp(1j*angle/2)])
    for angle in [-np.pi, -0.7, 0, 0.23, np.pi/2, np.pi, 2*np.pi]:
        close(x @ rz(angle) @ x, rz(-angle))
        close(rz(angle/4) @ x @ rz(angle/2) @ x @ rz(angle/4), np.eye(2))
        state = h @ rz(angle) @ h @ np.array([1, 0])
        close(state, [np.cos(angle/2), -1j*np.sin(angle/2)])
        close(abs(state[0])**2, np.cos(angle/2)**2)
    sample = ns["dd_model"]
    close(Operator(sample["echo"]).data, np.eye(2))
    close(Operator(sample["idle"]).data, rz(np.pi/2))
    # Without the interleaved timing, the X pair leaves the unwanted rotation.
    close(rz(np.pi/2) @ x @ x, rz(np.pi/2))
    require(not np.allclose(rz(np.pi/2) @ x @ x, np.eye(2)), "Adjacent X pair cancels idle drift")
    # Unequal drift accumulated before/between/after pulses breaks cancellation.
    varied = rz(0.1) @ x @ rz(0.9) @ x @ rz(0.2)
    close(varied, rz(-0.6))
    require(not np.allclose(varied, np.eye(2)), "Time-dependent drift counterexample")
    close(-1j*x, np.cos(np.pi/2)*np.eye(2) - 1j*np.sin(np.pi/2)*x)
    close(1j*x, np.cos(-np.pi/2)*np.eye(2) - 1j*np.sin(-np.pi/2)*x)
    plotted = sample["axes"][1].lines
    close(plotted[0].get_ydata(), np.cos(sample["angles"]/2)**2)
    close(plotted[1].get_ydata(), np.ones_like(sample["angles"]))
    print("PASS DD matrix derivation, X-basis readout, pulse directions, timing counterexamples and plotted curves")


def check_runtime(ns: dict[str, dict]) -> None:
    backend = GenericBackendV2(2, seed=7, noise_info=False)
    circuit = ns["shot_records"]["qc"].copy()
    original = circuit.copy()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        jobs = ns["submit_shot_comparison"]["submit_shot_comparison"](backend)
        results = [job.result()[0].data.meas for job in jobs]
        require([data.num_shots for data in results] == [128, 256, 500], "Runtime shot precedence")
        require([data.get_counts() for data in results] == [{"1": n} for n in [128, 256, 500]],
                "Runtime deterministic outputs")
        job = ns["submit_with_dd"]["submit_with_dd"](circuit, backend, shots=32)
        data = job.result()[0].data.meas
        require(data.num_shots == 32 and set(data.get_counts()) <= {"00", "11"}, "DD request local flow")
        require(circuit == original, "Input circuit mutated")
    require(not any(issubclass(w.category, DeprecationWarning) for w in caught),
            "Published Runtime examples must avoid deprecated calls")
    for message in sorted({str(w.message) for w in caught}):
        print(f"LOCAL RUNTIME WARNING: {message}")

    # Inspect the actual Sampler options at the submission boundary.
    def inspect_submission(sampler, pubs, *, shots):
        require(sampler.options.dynamical_decoupling.enable is True, "DD disabled")
        require(sampler.options.dynamical_decoupling.sequence_type == "XY4", "Wrong DD sequence")
        require(shots == 24 and len(pubs) == 1, "Wrong submission arguments")
        isa = pubs[0]
        for item in isa.data:
            if item.operation.name == "barrier":
                continue
            indices = tuple(isa.find_bit(q).index for q in item.qubits)
            require(backend.target.instruction_supported(item.operation.name, indices), "Non-ISA instruction")
        return "recorded-local-request"
    with patch.object(SamplerV2, "run", autospec=True, side_effect=inspect_submission):
        require(ns["submit_with_dd"]["submit_with_dd"](circuit, backend, shots=24)
                == "recorded-local-request", "Function must return the submitted job")
    # Verify the 0.48+ warning itself without submitting the deprecated workload.
    isa = generate_preset_pass_manager(backend=backend, optimization_level=1, seed_transpiler=7).run(circuit)
    sampler = SamplerV2(mode=backend)
    with patch.object(sampler, "_run", return_value=None), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        sampler.run([(isa, None, 16), (isa, None, 32)])
    require(any(issubclass(w.category, DeprecationWarning) and "different 'shots'" in str(w.message)
                for w in caught), "Missing mixed-shots deprecation warning")
    # Chapter 6's adjacent clarification concerns the same Runtime release change.
    preparation = isa.remove_final_measurements(inplace=False)
    estimator = EstimatorV2(mode=backend)
    with patch.object(estimator, "_run", return_value=None), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        estimator.run([(preparation, "ZZ", None, 0.01), (preparation, "ZZ", None, 0.02)])
    require(any(issubclass(w.category, DeprecationWarning) and "different 'precision'" in str(w.message)
                for w in caught), "Missing mixed-precision deprecation warning")
    print("PASS Runtime local execution, shot precedence, DD request options and shots/precision deprecations")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-figures", action="store_true")
    args = parser.parse_args()
    require(version("qiskit") == "2.5.2" and version("qiskit-ibm-runtime") == "0.49.0", "Use baseline versions")
    print("Versions:", ", ".join(f"{package}={version(package)}" for package in
                                 ["qiskit", "qiskit-ibm-runtime", "numpy", "matplotlib"]))
    with tempfile.TemporaryDirectory(prefix="qiskit-chapter5-") as temporary:
        directory = Path(temporary)
        with patch("socket.socket.connect", side_effect=AssertionError("Network forbidden in Chapter 5 checks")):
            ns = run_examples(directory)
            check_samples_and_axes(ns)
            check_registers(ns)
            check_dd_model(ns)
            check_runtime(ns)
        if args.write_figures:
            ASSETS.mkdir(parents=True, exist_ok=True)
            for figure in directory.glob("*.png"):
                shutil.copy2(figure, ASSETS / figure.name)
            print("WROTE Chapter 5 figures")
    check_links()
    print("PASS Chapter 5: 8 printed examples and 2 Runtime functions; no QPU submissions")


if __name__ == "__main__":
    main()
