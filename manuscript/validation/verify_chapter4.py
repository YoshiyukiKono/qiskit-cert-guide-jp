"""Run Chapter 4 examples and check routing, layouts and Runtime control flow.

Requires manuscript/validation/requirements.txt. No credentials or QPU needed.
    python -X utf8 -B manuscript/validation/verify_chapter4.py --write-figures

Trusted repository examples run in temporary directories. Runtime functions use
GenericBackendV2 locally; service selection uses a recording test double. A socket
guard prevents accidental network connections during all example execution.
"""
from __future__ import annotations

import argparse
import ast
from contextlib import chdir, redirect_stdout
from importlib.metadata import version
from io import StringIO
import os
from pathlib import Path
import re
import shutil
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import warnings

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "qiskit-manuscript-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from qiskit.transpiler import generate_preset_pass_manager

from verify_sample_sections import ROOT, anchors, check_links, close, require

SOURCE = ROOT / "manuscript/ja/04-transpile-execution.md"
ASSETS = SOURCE.parent / "figures/04"
NAMES = (
    "target", "transpile", "optimization", "layout", "readout", "observable",
    "submit_one", "run_independent", "run_adaptive", "choose_backend",
    "local_primitives", "sampler_pubs", "estimator_pub",
)
FUNCTIONS = {"submit_one", "run_independent", "run_adaptive", "choose_backend"}
ORIGINAL_ANCHORS = {
    "transpile-preset", "isa-layout", "execution-modes", "backend-selection",
    "runtime-local", "pub-job", "broadcasting-preview",
}
ORIGINAL_HEADINGS = [
    "preset pass manager", "ISA circuitとlayout", "Job / Session / Batch",
    "serviceとbackend選択", "local primitivesとRuntime primitives", "PUB、run、job",
    "Estimator broadcasting予告", "章末チェック",
]


def run_examples(directory: Path) -> dict[str, dict]:
    source = SOURCE.read_text(encoding="utf-8")
    require(ORIGINAL_ANCHORS <= anchors(source), "An original anchor was removed")
    require(re.findall(r"^## (.+)$", source, re.M) == ORIGINAL_HEADINGS, "H2 headings changed")
    prose = re.sub(r"```.*?```", "", source, flags=re.S)
    bold_spans = re.findall(r"\*\*([^*\n]+)\*\*", prose)
    require(not any("（" in span or "）" in span for span in bold_spans), "Parenthesis inside bold")
    require(not re.search(r"mock|practice-bank", source, re.I), "Mock reference in standalone chapter")
    examples = list(re.finditer(r"```python\n(.*?)\n```", source, re.S))
    require(len(examples) == len(NAMES), "Unclassified Python example")
    namespaces = {}
    with chdir(directory):
        for name, example in zip(NAMES, examples, strict=True):
            namespace = {"__name__": "__main__"}
            tree = ast.parse(example[1])
            if name in FUNCTIONS:
                require(len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef),
                        f"Runtime example {name} must only define a function")
                function = tree.body[0]
                require(function.name == name and not function.decorator_list, "Unexpected function")
                require(all(isinstance(d, ast.Constant) for d in function.args.defaults),
                        "Function default may execute a call")
                marker = "service-function" if name == "choose_backend" else "runtime-function"
                require(source[:example.start()].rstrip().endswith(f"<!-- validation: {marker} -->"),
                        "Function example needs a validation marker")
            stdout = StringIO()
            with redirect_stdout(stdout):
                exec(compile(tree, str(SOURCE), "exec"), namespace)
            if name in FUNCTIONS:
                require(not stdout.getvalue(), "Function definition produced output")
            else:
                output = re.match(r"\s*出力:\s*```text\n(.*?)\n```", source[example.end():], re.S)
                require(output is not None, f"Missing printed output for {name}")
                require(stdout.getvalue().strip() == output[1].strip(),
                        f"Output differs for {name}:\n{stdout.getvalue()}")
                print(f"PASS Chapter 4 printed output: {name}")
            namespaces[name] = namespace
            plt.close("all")
    images = {Path(link).name for link in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)}
    require(images == {p.name for p in directory.glob("*.png")}, "Generated figures and links differ")
    for name in images:
        with Image.open(directory / name) as img:
            require(img.format == "PNG" and min(img.size) >= 180, f"Invalid figure: {name}")
            require(any(lo < hi for lo, hi in img.convert("RGB").getextrema()), f"Blank figure: {name}")
        with Image.open(directory / name) as img:
            img.verify()
    print(f"PASS {len(images)} circuit figures, {len(ORIGINAL_ANCHORS)} anchors and 8 H2 headings")
    return namespaces


def permutation(mapping: list[int]) -> np.ndarray:
    """Construct the little-endian permutation from a bit-index mapping."""
    width = len(mapping)
    matrix = np.zeros((2**width, 2**width), dtype=complex)
    for basis in range(2**width):
        destination = sum(((basis >> bit) & 1) << physical for bit, physical in enumerate(mapping))
        matrix[destination, basis] = 1
    return matrix


def check_target(circuit: QuantumCircuit, backend) -> None:
    for item in circuit.data:
        if item.operation.name == "barrier":
            continue
        indices = tuple(circuit.find_bit(q).index for q in item.qubits)
        require(backend.target.instruction_supported(item.operation.name, indices),
                f"Unsupported instruction: {item.operation.name} {indices}")


def check_math_and_layouts(ns: dict[str, dict]) -> None:
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    sx = np.array([[1+1j, 1-1j], [1-1j, 1+1j]]) / 2
    rz = np.diag([np.exp(-1j*np.pi/4), np.exp(1j*np.pi/4)])
    close(sx @ sx, x)
    close(np.exp(1j*np.pi/4) * rz @ sx @ rz, h)
    swap = QuantumCircuit(2)
    swap.cx(0, 1)
    swap.cx(1, 0)
    swap.cx(0, 1)
    close(Operator(swap).data, permutation([1, 0]))

    sample = ns["layout"]
    backend, qc = sample["backend"], sample["qc"]
    rng = np.random.default_rng(7)
    vector = rng.normal(size=8) + 1j*rng.normal(size=8)
    vector /= np.linalg.norm(vector)
    observable = SparsePauliOp.from_list([("IIZ", 0.3), ("XYI", -0.7), ("ZZX", 0.4)])
    for initial in [[0, 1, 2], [2, 0, 1], [0, 2, 1]]:
        pm = generate_preset_pass_manager(backend=backend, optimization_level=0,
                                         initial_layout=initial, routing_method="basic", seed_transpiler=7)
        circuit = pm.run(qc)
        check_target(circuit, backend)
        final = circuit.layout.final_index_layout()
        start, finish = permutation(initial), permutation(final)
        # Includes a non-identity initial placement and routing, not merely |000>.
        close(Operator(circuit).data, finish @ Operator(qc).data @ start.conj().T)
        close(Operator.from_circuit(circuit).data, Operator(qc).data)
        mapped = observable.apply_layout(circuit.layout).to_matrix()
        close(mapped, finish @ observable.to_matrix() @ finish.conj().T)
        close(np.vdot(finish @ vector, mapped @ (finish @ vector)),
              np.vdot(vector, observable.to_matrix() @ vector))
    require(SparsePauliOp("IIZ").apply_layout(sample["isa_circuit"].layout).paulis.to_labels()
            == ["IZI"], "Routing observable mapping")
    require(SparsePauliOp("IIZ").apply_layout([2, 0, 1]).paulis.to_labels() == ["ZII"],
            "Chapter check observable mapping")

    expanded = ns["observable"]
    close(expanded["isa_observable"].to_matrix(), np.kron(np.diag([1, -1]), np.eye(4)))
    # Change the preparation and observable, including a complex Pauli term.
    varied = QuantumCircuit(2)
    varied.ry(0.71, 0)
    varied.s(0)
    varied.h(1)
    varied.cx(0, 1)
    compiled = expanded["pm"].run(varied)
    op = SparsePauliOp.from_list([("IZ", 0.3), ("XY", -0.7), ("ZZ", 0.4)])
    close(Statevector(varied).expectation_value(op),
          Statevector(compiled).expectation_value(op.apply_layout(compiled.layout)))

    for level in range(4):
        optimized = generate_preset_pass_manager(backend=backend, optimization_level=level,
                    initial_layout=[0, 1, 2], seed_transpiler=7).run(ns["optimization"]["qc"])
        close(Operator.from_circuit(optimized).data, np.eye(8))
        check_target(optimized, backend)
    print("PASS SX/H identities, SWAP, full operators, initial/final layouts, observable width and optimization")


def check_readout_and_pubs(ns: dict[str, dict]) -> None:
    sample = ns["readout"]
    circuit = sample["isa_circuit"]
    check_target(circuit, sample["backend"])
    final = circuit.layout.final_index_layout()
    pairs = {circuit.find_bit(item.clbits[0]).index: circuit.find_bit(item.qubits[0]).index
             for item in circuit.data if item.operation.name == "measure"}
    require(pairs == dict(enumerate(final)), "Classical destination no longer preserves logical bits")
    # Compare complete probability distributions after mapping physical -> classical.
    probabilities = Statevector(circuit.remove_final_measurements(inplace=False)).probabilities()
    classical = np.zeros_like(probabilities)
    for physical, probability in enumerate(probabilities):
        key = sum(((physical >> p) & 1) << c for c, p in pairs.items())
        classical[key] += probability
    close(classical, Statevector(sample["qc"].remove_final_measurements(inplace=False)).probabilities())
    late = ns["layout"]["isa_circuit"].copy()
    late.measure_all()
    counts = StatevectorSampler(seed=7).run([late], shots=32).result()[0].data.meas.get_counts()
    require(set(counts) == {"000", "110"}, "Late measure_all physical order counterexample")
    result = ns["sampler_pubs"]["result"]
    require(len(result) == 2 and all(p.data.meas.num_shots == 16 for p in result), "PUB/shot hierarchy")
    qc = ns["estimator_pub"]["qc"]
    op = ns["estimator_pub"]["observable"]
    good = StatevectorEstimator(seed=7).run([(qc, op, None, 0.01)]).result()[0]
    require(good.metadata["target_precision"] == 0.01, "Precision occupies slot 4")
    try:
        StatevectorEstimator().run([(qc, op, 0.01)]).result()
    except ValueError:
        pass
    else:
        raise AssertionError("Precision accidentally accepted in parameter slot")
    for angle in [0, np.pi/4, np.pi/2, np.pi]:
        varied = QuantumCircuit(1)
        varied.ry(angle, 0)
        close(Statevector(varied).probabilities()[1], np.sin(angle/2)**2)
    print("PASS readout distributions, late-measurement counterexample, PUB/shot hierarchy and precision slots")


def check_runtime_functions(ns: dict[str, dict]) -> None:
    backend = GenericBackendV2(3, seed=7, noise_info=False)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        job = ns["submit_one"]["submit_one"](backend, shots=32)
        require(job.result()[0].data.meas.get_counts() == {"1": 32}, "Runtime Job local result")
        results = ns["run_independent"]["run_independent"](backend, shots=32)
        require(results == [{"0": 32}, {"1": 32}], "Runtime Batch local result")
        adaptive = ns["run_adaptive"]["run_adaptive"](backend, shots=128)
        require(len(adaptive) == 2 and all(sum(c.values()) == 128 for _, c in adaptive),
                "Runtime Session local result")
        expected = np.pi/2 if adaptive[0][1].get("1", 0) / 128 < 0.5 else 0
        close(adaptive[1][0], expected)
    for message in sorted({str(w.message) for w in caught}):
        print(f"LOCAL RUNTIME WARNING: {message}")
    print("PASS actual Runtime Job/Batch/Session calls with GenericBackendV2 (local execution only)")

    # Verify the ordering of submissions/results, both feedback paths and mode binding.
    def record_run(function_name: str, first_counts: dict[str, int]):
        events, circuits = [], []

        class Scope:
            def __init__(self, **kwargs):
                require(kwargs["backend"] is backend, "Wrong scoped backend")
            def __enter__(self):
                events.append("enter")
                return self
            def __exit__(self, *_):
                events.append("close")

        class Sampler:
            def __init__(self, *, mode):
                require(isinstance(mode, Scope), "Primitive not bound to scope")
            def run(self, pubs, *, shots):
                circuit, = pubs
                require(circuit.num_parameters == 0, "Submitted parameters are unbound")
                check_target(circuit, backend)
                number = len(circuits)
                circuits.append(circuit)
                events.append(f"run{number}")
                counts = first_counts if number == 0 else {"0": shots}
                def result():
                    events.append(f"result{number}")
                    return [SimpleNamespace(data=SimpleNamespace(meas=SimpleNamespace(get_counts=lambda: counts)))]
                return SimpleNamespace(result=result)

        with patch("qiskit_ibm_runtime.SamplerV2", Sampler), \
             patch("qiskit_ibm_runtime.Batch", Scope), patch("qiskit_ibm_runtime.Session", Scope):
            result = ns[function_name][function_name](backend, shots=8)
        return events, circuits, result

    events, _, _ = record_run("run_independent", {"0": 8})
    require(events == ["enter", "run0", "run1", "close", "result0", "result1"], "Batch must submit before waiting")
    for counts, angle in [({"0": 8}, np.pi/2), ({"0": 4, "1": 4}, 0), ({"1": 8}, 0)]:
        events, circuits, result = record_run("run_adaptive", counts)
        require(events == ["enter", "run0", "result0", "run1", "result1", "close"], "Session feedback order")
        close(result[1][0], angle)
        second = circuits[1].remove_final_measurements(inplace=False)
        logical = Operator.from_circuit(second).data
        close(abs(logical[1, 0])**2, np.sin(angle/2)**2)
    with patch("qiskit_ibm_runtime.QiskitRuntimeService") as service:
        service.return_value.least_busy.return_value = backend
        require(ns["choose_backend"]["choose_backend"](5) is backend, "Selection return value")
        service.assert_called_once_with()
        service.return_value.least_busy.assert_called_once_with(
            operational=True, simulator=False, min_num_qubits=5)
    print("PASS Batch submission order, Session result dependency/both branches and service selection arguments")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-figures", action="store_true")
    args = parser.parse_args()
    print("Versions:", ", ".join(f"{package}={version(package)}" for package in
                                 ["qiskit", "qiskit-ibm-runtime", "numpy", "matplotlib"]))
    with tempfile.TemporaryDirectory(prefix="qiskit-chapter4-") as temporary:
        directory = Path(temporary)
        with patch("socket.socket.connect", side_effect=AssertionError("Network access forbidden in Chapter 4 checks")):
            ns = run_examples(directory)
            check_math_and_layouts(ns)
            check_readout_and_pubs(ns)
            check_runtime_functions(ns)
        if args.write_figures:
            ASSETS.mkdir(parents=True, exist_ok=True)
            for figure in directory.glob("*.png"):
                shutil.copy2(figure, ASSETS / figure.name)
            print("WROTE Chapter 4 circuit figures")
    check_links()
    print("PASS Chapter 4: 9 printed examples, 4 function examples; no QPU submissions")


if __name__ == "__main__":
    main()
