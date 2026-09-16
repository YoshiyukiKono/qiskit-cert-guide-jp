"""Verify Chapter 8 OpenQASM text, conversion, semantics and one circuit figure.

Uses manuscript/validation/requirements.txt; no credentials or QPU required.
    python -X utf8 -B manuscript/validation/verify_chapter8.py
    python -X utf8 -B manuscript/validation/verify_chapter8.py --write-figures

Parsers do not prove all language semantics; unsupported classical expressions
are checked against the language specification and independent arithmetic.
"""
from __future__ import annotations

import argparse
from contextlib import chdir, redirect_stdout
from importlib.metadata import version
from io import StringIO
import os
from pathlib import Path
import re
import shutil
import tempfile
from unittest.mock import patch

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "qiskit-manuscript-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import openqasm3
from PIL import Image
from qiskit import QuantumCircuit, qasm2, qasm3
from qiskit.exceptions import QiskitError
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import DensityMatrix, Operator, Statevector
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import UnrollForLoops
from verify_sample_sections import ROOT, anchors, check_links, close, require

SOURCE = ROOT / "manuscript/ja/08-openqasm3.md"
ASSETS = SOURCE.parent / "figures/08"
NAMES = ("bell", "reset_density", "feedback", "branches", "loop", "export_text",
         "files", "parameters", "phase", "classical", "qasm2_conversion")
ORIGINAL_ANCHORS = {"qasm-types", "qasm-semantics", "qasm-qiskit-interop",
                    "qasm-support-boundary", "qasm-version-differences"}
ORIGINAL_HEADINGS = ["version、量子型、古典型", "programを意味で追う", "Qiskitとのimport/export",
                     "仕様、SDK、QPU、RESTの境界", "OpenQASM 2と3を見分ける", "章末チェック"]


def run_examples(directory: Path) -> dict[str, dict]:
    source = SOURCE.read_text(encoding="utf-8")
    require(ORIGINAL_ANCHORS <= anchors(source), "Original anchor removed")
    require(re.findall(r"^## (.+)$", source, re.M) == ORIGINAL_HEADINGS, "H2 headings changed")
    prose = re.sub(r"```.*?```", "", source, flags=re.S)
    require(not any("（" in s or "）" in s for s in re.findall(r"\*\*([^*\n]+)\*\*", prose)),
            "Parenthesis inside bold")
    require(not re.search(r"mock|practice-bank|PLACEHOLDER", source, re.I), "Unexpected reference or placeholder")
    examples = list(re.finditer(r"```python\n(.*?)\n```", source, re.S))
    require(len(examples) == len(NAMES), "Unclassified Python example")
    namespaces = {}
    with chdir(directory):
        for name, example in zip(NAMES, examples, strict=True):
            namespace = {"__name__": "__main__"}
            stdout = StringIO()
            with redirect_stdout(stdout):
                exec(compile(example[1], str(SOURCE), "exec"), namespace)
            expected = re.match(r"\s*出力:\s*```text\n(.*?)\n```", source[example.end():], re.S)
            require(expected is not None, f"Missing output: {name}")
            require(stdout.getvalue().strip() == expected[1].strip(), f"Output differs: {name}\n{stdout.getvalue()}")
            namespaces[name] = namespace
            plt.close("all")
            print(f"PASS Chapter 8 printed output: {name}")
    # Every standalone QASM example must match the independently runnable Python
    # example that embeds it, including the intentionally unsupported program.
    qasm_blocks = re.findall(r"<!-- validation: qasm (\w+) -->\n```qasm\n(.*?)\n```", source, re.S)
    require(len(qasm_blocks) == len(re.findall(r"^```qasm$", source, re.M)) == 4, "Unclassified QASM block")
    for name, program in qasm_blocks:
        require(program.strip() == namespaces[name]["program"].strip(), f"QASM/Python source drift: {name}")
        require(openqasm3.parse(program).version == "3.0", "QASM version")
    for name in ["parameters", "export_text"]:
        require(openqasm3.parse(namespaces[name]["program"]).version == "3.0", "Embedded/exported QASM")
    require(openqasm3.parse(namespaces["qasm2_conversion"]["source_v3"]).version == "3.0", "Converted QASM version")
    images = {Path(p).name for p in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)}
    require(images == {"08-qasm-feedback.png"} == {p.name for p in directory.glob("*.png")}, "Figure links/outputs")
    with Image.open(directory / "08-qasm-feedback.png") as img:
        require(img.format == "PNG" and min(img.size) >= 150, "Invalid figure")
        require(any(a < b for a, b in img.convert("RGB").getextrema()), "Blank figure")
    print("PASS 4 QASM blocks, 1 figure, 5 preserved anchors and 6 preserved H2 headings")
    return namespaces


def measurements(qc: QuantumCircuit) -> list[tuple[int, int]]:
    return [(qc.find_bit(i.qubits[0]).index, qc.find_bit(i.clbits[0]).index)
            for i in qc.data if i.operation.name == "measure"]


def check_bell_and_reset(ns: dict[str, dict]) -> None:
    qc = ns["bell"]["qc"]
    prep = qc.remove_final_measurements(inplace=False)
    target = np.array([1, 0, 0, 1]) / np.sqrt(2)
    close(Statevector(prep).data, target)
    require(measurements(qc) == [(0, 0), (1, 1)], "Register measurement expansion")
    # Explicit resets must prepare the Bell state even from another input.
    arbitrary = np.array([1, 2j, -1j, 3], dtype=complex) / np.sqrt(15)
    close(DensityMatrix(arbitrary).evolve(prep).data, np.outer(target, target.conj()))
    changed = QuantumCircuit(2)
    changed.h(1)
    changed.cx(0, 1)
    close(Statevector(changed).probabilities(), [0.5, 0, 0.5, 0])
    # Independent Kraus calculation: reset q0 discards its value and prepares 0.
    before = ns["reset_density"]["before"].data
    k0 = np.kron(np.eye(2), [[1, 0], [0, 0]])
    k1 = np.kron(np.eye(2), [[0, 1], [0, 0]])
    expected = k0 @ before @ k0.conj().T + k1 @ before @ k1.conj().T
    close(ns["reset_density"]["after"].data, expected)
    close(expected, np.diag([0.5, 0, 0.5, 0]))
    reset = QuantumCircuit(1)
    reset.reset(0)
    for input_state in [Statevector.from_label("0"), Statevector.from_label("1"), Statevector.from_label("+")]:
        close(DensityMatrix(input_state).evolve(reset).data, [[1, 0], [0, 0]])
    print("PASS Bell preparation, explicit initialization, changed control/target example and reset channel")


def check_feedback_and_loops(ns: dict[str, dict]) -> None:
    qc = ns["feedback"]["qc"]
    branch = qc.data[3].operation
    require(measurements(qc) == [(0, 0), (0, 1)], "Past and final measurement destinations")
    require(qc.find_bit(branch.condition[0]).index == 0 and branch.condition[1] == 1, "Wrong condition")
    require(len(branch.blocks) == 1 and branch.blocks[0].data[0].operation.name == "x", "Wrong branch")
    require(branch.blocks[0].num_qubits == 1, "Wrong quantum branch width")
    # Follow both projected branches, including the changed-condition question.
    projected = [np.array([1, 0]), np.array([0, 1])]
    x = np.array([[0, 1], [1, 0]])
    original_records, changed_records = {}, {}
    for bit, state in enumerate(projected):
        after = x @ state if bit else state
        close(after, [1, 0])
        original_records[f"0{bit}"] = 0.5
        changed = x @ state if bit == 0 else state
        close(changed, [0, 1])
        changed_records[f"1{bit}"] = 0.5
    require(original_records == {"00": .5, "01": .5} and changed_records == {"10": .5, "11": .5},
            "Changed feedback question")
    # The importer's actual block implements the same X checked above.
    close(Operator(branch.blocks[0]).data, x)
    restored = qasm3.loads(qasm3.dumps(qc))
    require(measurements(restored) == measurements(qc), "Feedback roundtrip measurement mapping")
    require(restored.find_bit(restored.data[3].operation.condition[0]).index == 0, "Feedback roundtrip condition")
    try:
        StatevectorSampler().run([qc], shots=4).result()
    except QiskitError as error:
        require("cannot handle ControlFlowOp" in str(error), "Unexpected Sampler rejection")
    else:
        raise AssertionError("StatevectorSampler unexpectedly accepted feedback")
    loop = ns["loop"]
    require(list(loop["looped"].data[1].operation.params[0]) == [0, 1, 2], "Inclusive range")
    for stop, expected in [(1, "0"), (2, "1"), (3, "0")]:
        program = loop["program"].replace("[0:2]", f"[0:{stop}]")
        circuit = PassManager(UnrollForLoops()).run(qasm3.loads(program))
        require(circuit.count_ops()["x"] == stop+1, "Unrolled iteration count")
        data = StatevectorSampler(seed=7).run([circuit], shots=8).result()[0].data.readout
        require(data.get_counts() == {expected: 8}, "Parity of repeated X gates")
    question = qasm3.loads(loop["program"].replace("[0:2]", "[1:3]"))
    require(list(question.data[1].operation.params[0]) == [1, 2, 3], "Changed inclusive lower bound")
    print("PASS feedback structure/branches and round trip, local simulator limit, inclusive loops and unrolling")


def check_interop(ns: dict[str, dict], directory: Path) -> None:
    sample = ns["files"]
    require(sample["written"] is None and (directory / "08-roundtrip.qasm").is_file(), "Stream output")
    close(Operator(sample["preparation"]).data, Operator(sample["restored_preparation"]).data)
    require(measurements(sample["restored"]) == [(0, 1), (1, 0)], "Swapped classical destinations")
    require(qasm3.loads((directory / "08-roundtrip.qasm").read_text(encoding="utf-8")) == sample["restored"],
            "File/string load mismatch")
    # Test incorrect interface arguments while suppressing parser diagnostics.
    from contextlib import redirect_stderr
    with redirect_stderr(StringIO()):
        try:
            qasm3.loads("saved.qasm")
        except openqasm3.parser.QASM3ParsingError:
            pass
        else:
            raise AssertionError("Filename accepted as QASM body")
    try:
        qasm3.dump(sample["qc"], "unused.qasm")
    except AttributeError:
        pass
    else:
        raise AssertionError("dump filename unexpectedly accepted")
    parameters = ns["parameters"]
    restored, theta = parameters["restored"], parameters["theta"]
    for angle in [-0.4, 0, .7, np.pi/2, np.pi]:
        bound = restored.assign_parameters({theta: angle}).remove_final_measurements(inplace=False)
        close(Statevector(bound).probabilities(), [np.cos(angle/2)**2, np.sin(angle/2)**2])
    original_param = next(iter(parameters["qc"].parameters))
    require(original_param.name == theta.name and original_param != theta, "Names need not preserve Parameter identity")
    try:
        StatevectorSampler().run([restored], shots=4).result()
    except ValueError:
        pass
    else:
        raise AssertionError("Unbound parameter accepted")
    phase = ns["phase"]
    u, v = phase["original_operator"].data, phase["restored_operator"].data
    close(u, np.exp(.3j)*v)
    require(not np.allclose(u, v) and phase["restored"].metadata == {}, "Baseline export phase/metadata behavior")
    # Add a control: the lost global phase becomes relative between branches.
    controlled_u = Operator(phase["qc"].to_gate().control()).data
    controlled_v = Operator(phase["restored"].to_gate().control()).data
    require(not Operator(controlled_u).equiv(Operator(controlled_v)), "Controlled phase must matter")
    # The language/importer can represent an explicit gphase in this scope.
    gphase = qasm3.loads('OPENQASM 3.0; include "stdgates.inc"; qubit q; gphase(0.3); h q;')
    close(Operator(gphase).data, u)
    print("PASS string/stream/file interfaces, unitary and wiring round trip, parameter binding, phase and metadata limits")


def check_language_and_versions(ns: dict[str, dict]) -> None:
    program = ns["classical"]["program"]
    require(len(openqasm3.parse(program).statements) == 4, "Classical syntax")
    try:
        qasm3.loads(program)
    except qasm3.QASM3ImporterError as error:
        require("initialisation of classical bits is not supported" in str(error), "Expected importer boundary")
    else:
        raise AssertionError("Classical initialization unexpectedly supported")
    # Independent arithmetic for the specified classical example; not a general interpreter.
    bits = [1, 0, 1, 0]
    value = sum(bit * 2**i for i, bit in enumerate(bits))
    require(value == 5 and bool(bits[0]) is True and value+1 == 6, "Classical cast arithmetic")
    require(int("1010", 2) == 10 and int("1010"[-1]) == 0, "Changed bit pattern")
    close(np.arange(8)*2*np.pi/(2**3), np.arange(8)*np.pi/4)
    legacy = qasm3.loads('OPENQASM 3.0; qreg q[1]; creg c[1]; measure q -> c;')
    require(legacy.num_qubits == legacy.num_clbits == 1 and measurements(legacy) == [(0, 0)], "3.0 legacy syntax")
    converted = ns["qasm2_conversion"]
    original, restored = converted["qc"], converted["restored"]
    require(measurements(original) == measurements(restored), "QASM2/3 measurement mapping")
    close(DensityMatrix(original.remove_final_measurements(inplace=False)).data,
          DensityMatrix(restored.remove_final_measurements(inplace=False)).data)
    physical = qasm3.loads('OPENQASM 3.0; include "stdgates.inc"; x $2;', num_qubits=4)
    require(physical.num_qubits == 4 and physical.find_bit(physical.data[0].qubits[0]).index == 2,
            "Physical index parsed, not a hardware capability check")
    print("PASS classical syntax/import boundary and arithmetic, angle representation, QASM2 conversion and legacy syntax")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-figures", action="store_true")
    args = parser.parse_args()
    baseline = {"qiskit": "2.5.2", "qiskit-qasm3-import": "0.6.0", "openqasm3": "1.0.1",
                "antlr4-python3-runtime": "4.13.2"}
    for name, expected in baseline.items():
        require(version(name) == expected, f"Use baseline {name}={expected}")
    print("Versions:", ", ".join(f"{name}={version(name)}" for name in baseline))
    with tempfile.TemporaryDirectory(prefix="qiskit-chapter8-") as temporary:
        directory = Path(temporary)
        with patch("socket.socket.connect", side_effect=AssertionError("Network forbidden in Chapter 8 checks")):
            ns = run_examples(directory)
            check_bell_and_reset(ns)
            check_feedback_and_loops(ns)
            check_interop(ns, directory)
            check_language_and_versions(ns)
        if args.write_figures:
            ASSETS.mkdir(parents=True, exist_ok=True)
            shutil.copy2(directory / "08-qasm-feedback.png", ASSETS / "08-qasm-feedback.png")
            print("WROTE Chapter 8 figure")
    check_links()
    print("PASS Chapter 8: 11 printed examples, 4 QASM blocks; no service connection or QPU submissions")


if __name__ == "__main__":
    main()
