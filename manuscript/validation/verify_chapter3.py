"""Execute Chapter 3 examples and independently check circuit design decisions.

Requires manuscript/validation/requirements.txt (Python 3.12).
    python -X utf8 -B manuscript/validation/verify_chapter3.py
    python -X utf8 -B manuscript/validation/verify_chapter3.py --write-figures

Trusted repository examples run in temporary working directories. Dynamic circuits
are inspected and their branches checked with projectors, not submitted to a QPU.
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

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "qiskit-manuscript-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from qiskit import QuantumCircuit
from qiskit.circuit import Gate, Instruction, Parameter, ParameterVector
from qiskit.circuit.exceptions import CircuitError
from qiskit.exceptions import QiskitError
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Operator, Statevector

from verify_sample_sections import ROOT, anchors, check_links, close, require

SOURCE = ROOT / "manuscript/ja/03-circuit-construction.md"
ASSETS = SOURCE.parent / "figures/03"
NAMES = (
    "registers", "measurement_mapping", "measure_all", "compose", "append_gate",
    "append_instruction", "inverse", "control", "parameter_sweep", "parameter_order",
    "feedforward", "feedforward_branches", "if_else", "circuit_loop",
)
ORIGINAL_ANCHORS = {
    "construct-registers", "measure-mapping", "compose-control", "parameters",
    "dynamic-circuits", "sdk-hardware-boundary",
}
X = np.array([[0, 1], [1, 0]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j])


def rejects(error_type, action, message: str) -> None:
    try:
        action()
    except error_type:
        return
    raise AssertionError(message)


def run_examples(directory: Path) -> dict[str, dict]:
    source = SOURCE.read_text(encoding="utf-8")
    require(ORIGINAL_ANCHORS <= anchors(source), "An original Chapter 3 anchor was removed")
    examples = list(re.finditer(r"```python\n(.*?)\n```\s*出力:\s*```text\n(.*?)\n```", source, re.S))
    require(len(examples) == len(re.findall(r"^```python$", source, re.M)) == len(NAMES),
            "Every Chapter 3 Python example must have a checked output")
    namespaces = {}
    with chdir(directory):
        for name, example in zip(NAMES, examples, strict=True):
            namespace = {"__name__": "__main__"}
            stdout = StringIO()
            with redirect_stdout(stdout):
                exec(compile(example[1], str(SOURCE), "exec"), namespace)
            require(stdout.getvalue().strip() == example[2].strip(),
                    f"Output differs for {name}:\n{stdout.getvalue()}")
            namespaces[name] = namespace
            plt.close("all")
            print(f"PASS Chapter 3 printed output: {name}")
    images = {Path(link).name for link in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)}
    require(images == {p.name for p in directory.glob("*.png")}, "Generated figures and references differ")
    for name in images:
        with Image.open(directory / name) as img:
            require(img.format == "PNG" and min(img.size) >= 180, f"Invalid figure: {name}")
            require(any(lo < hi for lo, hi in img.convert("RGB").getextrema()), f"Blank figure: {name}")
        with Image.open(directory / name) as img:
            img.verify()
    print(f"PASS {len(images)} circuit figures and {len(ORIGINAL_ANCHORS)} preserved anchors")
    return namespaces


def measurement_pairs(circuit: QuantumCircuit) -> list[tuple[int, int]]:
    return [(circuit.find_bit(item.qubits[0]).index, circuit.find_bit(item.clbits[0]).index)
            for item in circuit.data if item.operation.name == "measure"]


def check_measurement(ns: dict[str, dict]) -> None:
    require(measurement_pairs(ns["registers"]["qc"]) == [(1, 0)], "First example saves q1")
    require(measurement_pairs(ns["measurement_mapping"]["qc"]) == [(2, 0), (0, 1)], "Subset mapping")
    require(measurement_pairs(ns["measurement_mapping"]["swapped"]) == [(2, 1), (0, 0)], "Swapped mapping")
    sample = ns["measure_all"]
    require(sample["base"].num_clbits == 2 and measurement_pairs(sample["base"]) == [], "Original changed")
    require(sample["added"].num_clbits == 4, "Default measure_all must add storage")
    require(measurement_pairs(sample["added"]) == [(0, 2), (1, 3)], "New register mapping")
    require(measurement_pairs(sample["reused"]) == [(0, 0), (1, 1)], "Existing storage mapping")
    rejects(CircuitError, lambda: QuantumCircuit(3, 1).measure_all(add_bits=False), "Insufficient storage accepted")
    question = QuantumCircuit(4, 2)
    question.x(3)
    question.measure([3, 1], [0, 1])
    result = StatevectorSampler().run([question], shots=16).result()[0]
    require(result.data.c.get_counts() == {"01": 16}, "Chapter question mapping")
    print("PASS registers, partial measurement, storage reuse, insufficient storage and changed mapping")


def cx_matrix(width: int, control: int, target: int) -> np.ndarray:
    # Construct from the bit-level truth table, independently of Qiskit circuits.
    matrix = np.zeros((2**width, 2**width), dtype=complex)
    for column in range(2**width):
        row = column ^ (1 << target) if column & (1 << control) else column
        matrix[row, column] = 1
    return matrix


def check_composition(ns: dict[str, dict]) -> None:
    mapped = ns["compose"]
    expected = cx_matrix(3, 2, 0) @ np.kron(H, np.eye(4)) @ np.kron(np.eye(2), np.kron(X, np.eye(2)))
    close(Operator(mapped["combined"]).data, expected)
    close(Operator(mapped["updated"]).data, expected)
    require(mapped["returned"] is None and len(mapped["base"].data) == 1, "compose mutation contract")

    hc, sc = QuantumCircuit(1), QuantumCircuit(1)
    hc.h(0)
    sc.s(0)
    close(Operator(hc.compose(sc)).data, S @ H)
    close(Operator(hc.compose(sc, front=True)).data, H @ S)
    zc = QuantumCircuit(1)
    zc.z(0)
    require(Statevector.from_instruction(hc.compose(zc)).equiv(Statevector.from_label("-")), "H then Z")
    require(Statevector.from_instruction(hc.compose(zc, front=True)).equiv(Statevector.from_label("+")), "Z then H")

    close(Operator(ns["append_gate"]["qc"]).data, np.kron(S @ H, np.eye(4)))
    require(measurement_pairs(ns["append_instruction"]["expanded"]) == [(1, 0)], "Instruction cargs mapping")
    read_z = ns["append_instruction"]["read_z"]
    base = QuantumCircuit(3, 2)
    base.x(2)
    composed = base.compose(read_z, qubits=[2], clbits=[1])
    require(measurement_pairs(composed) == [(2, 1)], "compose clbits question")
    require(StatevectorSampler().run([composed], shots=16).result()[0].data.c.get_counts() == {"10": 16},
            "compose clbits saved value")

    inverse = ns["inverse"]
    close(Operator(inverse["backward"]).data, (S @ H).conj().T)
    close(Operator(inverse["round_trip"]).data, np.eye(2))
    require(not np.allclose(S @ H @ S @ H, np.eye(2)), "Reversing order alone is not inversion")
    for name in ("measure", "reset"):
        circuit = QuantumCircuit(1, 1) if name == "measure" else QuantumCircuit(1)
        circuit.measure(0, 0) if name == "measure" else circuit.reset(0)
        rejects(CircuitError, circuit.inverse, f"{name} unexpectedly invertible")
        rejects(QiskitError, circuit.to_gate, f"{name} unexpectedly converted to Gate")

    controlled = ns["control"]
    close(Operator(controlled["controlled_x"]).data, cx_matrix(2, 0, 1))
    close(Operator(controlled["qc"]).data, cx_matrix(2, 0, 1) @ np.kron(np.eye(2), H))
    reversed_control = QuantumCircuit(2)
    reversed_control.append(controlled["controlled_x"], [1, 0])
    close(Operator(reversed_control).data, cx_matrix(2, 1, 0))
    require(hasattr(Gate, "control") and not hasattr(Instruction, "control"), "Gate/Instruction distinction")
    print("PASS full composition matrices, order, qargs/cargs, inversion and both CX directions")


def check_parameters(ns: dict[str, dict]) -> None:
    sample = ns["parameter_sweep"]
    for angle in (-np.pi, 0, np.pi / 3, np.pi / 2, 2 * np.pi / 3, np.pi):
        bound = sample["pqc"].assign_parameters({sample["theta"]: angle})
        state = Statevector.from_instruction(bound)
        close(state.data, [np.cos(angle / 2), np.sin(angle / 2)])
        close(state.probabilities()[1], np.sin(angle / 2) ** 2)
    require(sample["pqc"].num_parameters == 1, "Sweep must preserve template")
    ordered = ns["parameter_order"]
    close(Operator(ordered["by_name"]).data, Operator(ordered["correct_list"]).data)
    require(not np.allclose(Operator(ordered["by_name"]).data, Operator(ordered["by_list"]).data), "Order should matter")
    require(ordered["partial"].num_parameters == 1, "Partial binding")
    completed = ordered["partial"].assign_parameters({ordered["a_angle"]: 0})
    close(Operator(completed).data, Operator(ordered["by_name"]).data)

    theta, phi = Parameter("theta"), Parameter("phi")
    shared = QuantumCircuit(1)
    shared.ry(theta, 0)
    shared.rz(2 * theta, 0)
    require(shared.num_parameters == 1, "Shared symbol count")
    bound = shared.assign_parameters({theta: np.pi / 3})
    close([float(item.operation.params[0]) for item in bound.data], [np.pi / 3, 2 * np.pi / 3])
    renamed = shared.assign_parameters({theta: phi / 2})
    require(list(renamed.parameters) == [phi], "Expression substitution remains symbolic")
    close(Operator(renamed.assign_parameters({phi: 2 * np.pi / 3})).data, Operator(bound).data)
    vector = ParameterVector("v", 12)
    circuit = QuantumCircuit(1)
    for item in reversed(vector):
        circuit.ry(item, 0)
    require(list(circuit.parameters) == list(vector), "ParameterVector element order")
    print("PASS analytic rotations, changed angles, binding order, partial binding and shared expressions")


def evolve_branch(state: Statevector, circuit: QuantumCircuit, branch_index: int) -> Statevector:
    """Evaluate the selected unitary block of the example's single if_else operation."""
    instructions = [item for item in circuit.data if item.operation.name == "if_else"]
    require(len(instructions) == 1, "Expected one if_else")
    enclosing = instructions[0]
    block = enclosing.operation.blocks[branch_index]
    for item in block.data:
        require(isinstance(item.operation, Gate), "Example branch must contain only gates")
        qargs = [circuit.find_bit(enclosing.qubits[block.find_bit(bit).index]).index for bit in item.qubits]
        state = state.evolve(item.operation, qargs=qargs)
    return state


def check_feedforward(ns: dict[str, dict]) -> None:
    dynamic = ns["feedforward"]["dynamic"]
    two_branches = ns["if_else"]["qc"]
    require(measurement_pairs(dynamic) == [(0, 0), (1, 1)], "Distinct flag and readout storage")
    for circuit in (dynamic, two_branches):
        op = [item.operation for item in circuit.data if item.operation.name == "if_else"][0]
        require(op.condition == (circuit.clbits[0], 1), "Condition must read first classical bit")

    initial = np.kron([1, 0], [1, 1]) / np.sqrt(2)
    mixed = np.zeros((4, 4), dtype=complex)
    distribution = {"00": 0.0, "01": 0.0, "10": 0.0, "11": 0.0}
    for bit in (0, 1):
        projector = np.kron(np.eye(2), np.diag([int(bit == 0), int(bit == 1)]))
        projected = projector @ initial
        probability = float(np.vdot(projected, projected).real)
        close(probability, 0.5)
        state = Statevector(projected / np.sqrt(probability))
        final = evolve_branch(state, dynamic, 0) if bit == 1 else state
        close(final.probabilities(), np.eye(4)[3 * bit])
        mixed += probability * np.outer(final.data, final.data.conj())
        either = evolve_branch(state, two_branches, 0 if bit == 1 else 1)
        for out, conditional_probability in enumerate(either.probabilities([1])):
            distribution[f"{out}{bit}"] += probability * float(conditional_probability)
        # Changed-condition question: substitute Z for the X correction on q1.
        correction = QuantumCircuit(2)
        if bit:
            correction.z(1)
        close(state.evolve(correction).probabilities([1]), [1, 0])
    close(mixed, np.diag([0.5, 0, 0, 0.5]))
    close(list(distribution.values()), [0.25, 0, 0.25, 0.5])
    bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
    require(not np.allclose(mixed, np.outer(bell, bell)), "Classical mixture must differ from coherent Bell state")
    close(np.trace(mixed @ np.kron(X, X)), 0)
    close(np.vdot(bell, np.kron(X, X) @ bell), 1)

    loop = ns["circuit_loop"]["loop_operation"]
    require(list(loop.params[0]) == [0, 1, 2], "Loop range")
    body = Operator(loop.blocks[0]).data
    close(np.linalg.matrix_power(body, 3), Operator(ns["circuit_loop"]["unrolled"]).data)
    close(np.linalg.matrix_power(body, 3), X)
    mid = QuantumCircuit(1, 1)
    mid.h(0)
    mid.measure(0, 0)
    mid.x(0)
    mid.measure(0, 0)
    rejects(QiskitError, lambda: StatevectorSampler().run([mid]).result(), "Mid-circuit measurement accepted")
    rejects(QiskitError, lambda: StatevectorSampler().run([dynamic]).result(), "Control flow accepted")
    print("PASS projected branches, conditional target mapping, joint probabilities, mixture, loops and sampler limits")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-figures", action="store_true")
    args = parser.parse_args()
    require(version("qiskit") == "2.5.2", "Use Qiskit 2.5.2")
    print(" / ".join(f"{pkg} {version(pkg)}" for pkg in ("qiskit", "numpy", "matplotlib", "pylatexenc")))
    with tempfile.TemporaryDirectory(prefix="qiskit-chapter3-") as directory:
        temporary = Path(directory)
        namespaces = run_examples(temporary)
        check_measurement(namespaces)
        check_composition(namespaces)
        check_parameters(namespaces)
        check_feedforward(namespaces)
        if args.write_figures:
            ASSETS.mkdir(parents=True, exist_ok=True)
            for image in temporary.glob("*.png"):
                shutil.copyfile(image, ASSETS / image.name)
            print(f"WROTE figures to {ASSETS.relative_to(ROOT)}")
    check_links()


if __name__ == "__main__":
    main()
