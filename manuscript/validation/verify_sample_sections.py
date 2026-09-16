"""Run the expanded sections' actual examples and check their local links.

Run with Qiskit 2.5.2, qiskit-ibm-runtime 0.49.0 and NumPy installed:
    python manuscript/validation/verify_sample_sections.py

This executes trusted Python fences from the repository, not downloaded input.
It checks examples and selected mathematical consequences, not teaching quality.
"""
from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from importlib.metadata import version
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import numpy as np
import qiskit
from qiskit.quantum_info import Pauli, Statevector


ROOT = Path(__file__).resolve().parents[2]
SAMPLES = (
    ("01-quantum-operations.md", "state-amplitude", '<a id="matrix-order"></a>', 1),
    ("01-quantum-operations.md", "matrix-order", '<a id="phase"></a>', 2),
    ("01-quantum-operations.md", "phase", '<a id="basic-gates"></a>', 2),
    ("01-quantum-operations.md", "basic-gates", '<a id="multi-entanglement"></a>', 1),
    ("01-quantum-operations.md", "multi-entanglement", '<a id="bit-pauli-order"></a>', 2),
    ("01-quantum-operations.md", "bit-pauli-order", '<a id="expectation"></a>', 4),
    ("01-quantum-operations.md", "expectation", "\n## 章末チェック\n", 2),
    ("06-estimator.md", "estimator-purpose", '<a id="estimator-pub"></a>', 1),
    ("06-estimator.md", "estimator-pub", '<a id="estimator-broadcasting"></a>', 2),
    ("06-estimator.md", "estimator-broadcasting", '<a id="estimator-options"></a>', 2),
    ("06-estimator.md", "estimator-options", '<a id="estimator-result"></a>', 3),
    ("06-estimator.md", "estimator-result", "\n## 章末チェック\n", 1),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def close(actual, expected) -> None:
    np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-12)


def run_examples() -> dict[str, dict]:
    namespaces = {}
    for filename, anchor, end, expected_count in SAMPLES:
        path = ROOT / "manuscript/ja" / filename
        source = path.read_text(encoding="utf-8")
        start = f'<a id="{anchor}"></a>\n'
        require(source.count(start) == 1 and source.count(end) == 1,
                f"Missing or duplicate section boundary: {filename}")
        section = source.split(start, 1)[1].split(end, 1)[0]
        examples = list(re.finditer(
            r"```python\n(.*?)\n```\s*出力:\s*```text\n(.*?)\n```",
            section, re.S,
        ))
        require(len(examples) == expected_count, f"Example count changed: {filename}")
        require(len(re.findall(r"^```python$", section, re.M)) == expected_count,
                f"Python example without a checked output: {filename}")
        namespace = {"__name__": "__main__"}
        for index, example in enumerate(examples, 1):
            # Only broadcasting explicitly continues a preceding example.
            execution_scope = namespace if anchor == "estimator-broadcasting" else {"__name__": "__main__"}
            output = StringIO()
            with redirect_stdout(output):
                exec(compile(example[1], str(path), "exec"), execution_scope)
            namespace.update(execution_scope)
            require(output.getvalue().strip() == example[2].strip(),
                    f"Output differs: {filename} example {index}\n{output.getvalue()}")
            print(f"PASS printed output: {filename} #{anchor} example {index}")
        namespaces[anchor] = namespace
    return namespaces


def check_math(namespaces: dict[str, dict]) -> None:
    gates = namespaces["matrix-order"]
    h, z, x = (gates[name] for name in ("h", "z", "x"))

    # Exact integer arithmetic: H = A / sqrt(2), so A Z A = 2 X.
    a = np.array([[1, 1], [1, -1]], dtype=np.int64)
    zi = np.array([[1, 0], [0, -1]], dtype=np.int64)
    xi = np.array([[0, 1], [1, 0]], dtype=np.int64)
    np.testing.assert_array_equal(a @ zi @ a, 2 * xi)
    np.testing.assert_array_equal(a @ xi @ a, 2 * zi)

    zero, one = np.array([1, 0]), np.array([0, 1])
    plus, minus = (zero + one) / np.sqrt(2), (zero - one) / np.sqrt(2)
    for initial, after_h, after_z, final in (
        (zero, plus, minus, one), (one, minus, plus, zero),
    ):
        close(h @ initial, after_h)
        close(z @ after_h, after_z)
        close(h @ after_z, final)
    close(z @ h @ zero, minus)
    close(h @ z @ zero, plus)
    close(h @ x @ h, z)
    state = Statevector([np.sqrt(1 / 3), 1j * np.sqrt(2 / 3)])
    close(state.evolve(gates["qc"]).data, x @ state.data)
    print("PASS HZH/HXH exact integer identities, intermediate states and complex input")

    sample = namespaces["estimator-broadcasting"]
    pqc, theta = sample["pqc"], sample["theta"]
    angles, evs = sample["angles"], sample["evs"]
    require(evs.shape == (2, 3), "Expected a 2 by 3 result")
    close(evs, np.vstack([np.cos(angles), np.sin(angles)]))
    # Check each cell against an independently bound single-state evaluation.
    for column, angle in enumerate(angles):
        state = Statevector.from_instruction(pqc.assign_parameters({theta: angle}))
        close(state.data, [np.cos(angle / 2), np.sin(angle / 2)])
        for row, label in enumerate(("Z", "X")):
            close(evs[row, column], state.expectation_value(Pauli(label)))

    estimator = sample["estimator"]
    swapped = estimator.run([
        (pqc, [["X"], ["Z"]], sample["values"])
    ], precision=0.0).result()[0].data.evs
    close(swapped, evs[::-1])
    require(sample["pair_evs"].shape == (2,), "Expected two paired results")
    close(sample["pair_evs"], [1, 1])
    outer = estimator.run([
        (pqc, [["Z"], ["X"]], sample["pair_values"])
    ], precision=0.0).result()[0].data.evs
    require(outer.shape == (2, 2), "Expected four combinations")
    close(outer, [[1, 0], [0, 1]])
    try:
        estimator.run([(pqc, ["Z", "X"], sample["values"])], precision=0.0).result()
    except ValueError:
        pass
    else:
        raise AssertionError("Incompatible shapes (2,) and (3,) should be rejected")
    binding_shape = np.zeros((5, 2)).shape[:-1]
    require(binding_shape == (5,), "Wrong binding shape in question 1")
    require(np.broadcast_shapes((3, 1), binding_shape) == (3, 5), "Question 2")
    require(np.broadcast_shapes((3,), (3,)) == (3,), "Question 4")
    print("PASS six cells, analytic expectations, pairing, row order and invalid shapes")


def check_chapter_one(namespaces: dict[str, dict]) -> None:
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import RXGate, RYGate, RZGate, UnitaryGate
    from qiskit.primitives import StatevectorSampler
    from qiskit.quantum_info import Operator, partial_trace
    from scipy.linalg import expm

    zero, one = np.eye(2, dtype=complex)
    identity = np.eye(2)
    x, y, z = (Pauli(label).to_matrix() for label in ("X", "Y", "Z"))
    h = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    amplitude = namespaces["state-amplitude"]
    close(amplitude["normalized"].data, [1 / np.sqrt(2), 1j / np.sqrt(2)])
    close(abs((1 + 1j) / 2) ** 2, 0.5)
    raw = np.array([2, 1j])
    close(abs(raw / np.linalg.norm(raw)) ** 2, [4 / 5, 1 / 5])

    # Probe unequal complex amplitudes and several phases, not just the printed example.
    state = Statevector([np.sqrt(0.3), 1j * np.sqrt(0.7)])
    for phase in (0, np.pi / 2, np.pi, -0.73):
        shifted = Statevector(np.exp(1j * phase) * state.data)
        require(state.equiv(shifted), "Common phase must preserve the physical state")
        for gate in (h, RXGate(0.81), RYGate(-0.42)):
            close(state.evolve(gate).probabilities(), shifted.evolve(gate).probabilities())
        relative = Statevector([1, np.exp(1j * phase)] / np.sqrt(2))
        close(relative.evolve(h).probabilities(),
              [(1 + np.cos(phase)) / 2, (1 - np.cos(phase)) / 2])
    print("PASS normalization, common phase invariance and phase-dependent interference")

    close(x @ z, -z @ x)
    close(y @ zero, 1j * one)
    close(y @ one, -1j * zero)
    close(y @ y, identity)
    for factory, pauli in ((RXGate, x), (RYGate, y), (RZGate, z)):
        for angle in (0, -0.71, np.pi / 3, np.pi, 2 * np.pi):
            matrix = Operator(factory(angle)).data
            close(matrix, expm(-1j * angle * pauli / 2))
            close(Operator(factory(-angle)).data @ matrix, identity)
            close(Operator(factory(0.29)).data @ matrix, Operator(factory(angle + 0.29)).data)
        close(Operator(factory(np.pi)).data, -1j * pauli)
        close(Operator(factory(2 * np.pi)).data, -identity)
    angle = 0.83
    close(np.exp(1j * angle / 2) * Operator(RZGate(angle)).data,
          np.diag([1, np.exp(1j * angle)]))
    close(namespaces["basic-gates"]["t"] @ namespaces["basic-gates"]["t"],
          namespaces["basic-gates"]["s"])
    close(np.linalg.matrix_power(namespaces["basic-gates"]["t"], 4), z)
    print("PASS Pauli products, rotation exponentials, inverses, composition and phase gates")

    cx = QuantumCircuit(2)
    cx.cx(0, 1)
    basis = np.eye(4)
    for source, destination in enumerate((0, 3, 2, 1)):
        close(Statevector(basis[source]).evolve(cx).data, basis[destination])
    reverse = QuantumCircuit(2)
    reverse.cx(1, 0)
    close(Statevector.from_label("01").evolve(reverse).data, basis[1])
    bell = namespaces["multi-entanglement"]["bell"]
    close(bell.data, (basis[0] + basis[3]) / np.sqrt(2))
    close(bell.evolve(cx).data, np.kron(zero, (zero + one) / np.sqrt(2)))
    # A pure product state has a rank-one coefficient matrix. Bell has rank two.
    require(np.linalg.matrix_rank(bell.data.reshape(2, 2)) == 2, "Bell must not factor")
    plus_pair = Statevector.from_label("++")
    require(np.linalg.matrix_rank(plus_pair.data.reshape(2, 2)) == 1, "++ must factor")
    close(plus_pair.evolve(cx).data, plus_pair.data)
    for discarded in ([0], [1]):
        close(partial_trace(bell, discarded).data, identity / 2)
    mixture = (np.outer(basis[0], basis[0]) + np.outer(basis[3], basis[3])) / 2
    readout = np.kron(h, h)
    close(np.diag(mixture), bell.probabilities())
    close(np.diag(readout @ mixture @ readout.conj().T), namespaces["multi-entanglement"]["mixed_x"])
    close(namespaces["multi-entanglement"]["bell_x"], [0.5, 0, 0, 0.5])
    close(bell.expectation_value(Pauli("YY")), -1)  # Same basis does not always mean equal outcomes.
    control_phase = QuantumCircuit(2)
    control_phase.append(UnitaryGate(-identity).control(1), [0, 1])
    close(Statevector.from_label("0+").evolve(control_phase).data,
          Statevector.from_label("0-").data)
    print("PASS CX truth table, tensor factors, Bell marginals, classical mixture and controlled phase")

    order = namespaces["bit-pauli-order"]
    # Check the new circuits against their action on each computational basis
    # column, not just against each other: equal circuits could target wrong qubits.
    expected_xz = np.array([[0, 0, 1, 0], [0, 0, 0, -1],
                            [1, 0, 0, 0], [0, -1, 0, 0]])
    for name in ("u_x_then_z", "u_z_then_x", "tensor_xz"):
        close(order[name], expected_xz)
    for initial in (bell.data, np.array([1, 2j, -3, 4j]) / np.sqrt(30)):
        expected = [initial[2], -initial[3], initial[0], -initial[1]]
        for name in ("x_then_z", "z_then_x"):
            close(Statevector(initial).evolve(order[name]).data, expected)
    # Changed-condition question: H/Y on disjoint qubits versus the same qubit.
    close(np.kron(h, identity) @ np.kron(identity, y), np.kron(h, y))
    close(np.kron(identity, y) @ np.kron(h, identity), np.kron(h, y))
    close(h @ y, -y @ h)
    require(not np.allclose(h @ y, y @ h), "H/Y must not commute on one qubit")
    close(np.kron(identity, h) @ np.kron(identity, y),
          -np.kron(identity, y) @ np.kron(identity, h))
    print("PASS local gate order, all basis columns, entangled inputs and H/Y question")
    close(order["op"].to_matrix(), 0.5 * np.kron(z, identity) - np.kron(x, x))
    close(Pauli("XZ").to_matrix(), np.kron(x, z))
    close(Statevector.from_label("10").evolve(Pauli("XZ")).data, basis[0])
    close(Statevector.from_label("00").evolve(Pauli("IY")).data, 1j * basis[1])
    close(Pauli("ZIX").to_matrix(), np.kron(np.kron(z, identity), x))
    mapped = QuantumCircuit(2, 2)
    mapped.x(1)
    mapped.measure(0, 1)
    mapped.measure(1, 0)
    counts = StatevectorSampler(seed=11).run([mapped], shots=8).result()[0].data.c.get_counts()
    require(counts == {"01": 8}, "Changed input must follow the classical measurement map")
    chapter_state = Statevector([1, 2j] / np.sqrt(5))
    close(chapter_state.probabilities(), [1 / 5, 4 / 5])
    close(chapter_state.expectation_value(Pauli("Z")), -3 / 5)
    close(Statevector.from_label("+-").expectation_value(Pauli("XX")), -1)
    close(Statevector.from_label("+-").expectation_value(Pauli("ZZ")), 0)
    close(Statevector(zero).evolve(RYGate(np.pi / 2)).data, (zero + one) / np.sqrt(2))
    print("PASS qubit and classical-bit order, Pauli labels and changed-condition chapter questions")


def check_conjugation(namespaces: dict[str, dict]) -> None:
    from qiskit.quantum_info import Operator

    sample = namespaces["matrix-order"]
    h, x, z = (sample[name] for name in ("h", "x", "z"))
    y = Pauli("Y").to_matrix()
    s = np.diag([1, 1j])
    sdg = s.conj().T
    a = np.array([[1, 1], [1, -1]], dtype=np.int64)
    # Exact arithmetic for the additional entries in the conjugation table.
    np.testing.assert_array_equal(a @ y @ a, -2 * y)
    for original, expected in ((x, y), (y, -x), (z, z)):
        close(s @ original @ sdg, expected)
    close(h.conj().T, h)
    close(s @ sdg, np.eye(2))

    mx = Operator(sample["x_readout"]).data
    my = Operator(sample["y_readout"]).data
    close(mx, h)
    close(my, h @ sdg)
    close(my.conj().T, s @ h)
    close(mx.conj().T @ z @ mx, x)
    close(my.conj().T @ z @ my, y)

    bases = (
        (mx, x, (np.array([1, 1]), np.array([1, -1]))),
        (my, y, (np.array([1, 1j]), np.array([1, -1j]))),
    )
    states = [Statevector.from_label(label).data for label in ("0", "1", "+", "-", "r", "l")]
    states.append(sample["psi"].data)
    for measurement, observable, vectors in bases:
        projectors = [np.outer(v, v.conj()) / 2 for v in vectors]
        for state in states:
            # Direct projections onto the requested eigenbasis, independently of
            # the gate sequence used in the manuscript to compute probabilities.
            probabilities = np.array([np.vdot(state, p @ state).real for p in projectors])
            close(np.abs(measurement @ state) ** 2, probabilities)
            close(probabilities @ [1, -1], np.vdot(state, observable @ state))
    close(sample["x_probabilities"], [0.5, 0.5])
    close(sample["y_probabilities"], [(2 + np.sqrt(3)) / 4, (2 - np.sqrt(3)) / 4])

    zero, one = np.array([1, 0]), np.array([0, 1])
    plus_i = np.array([1, 1j]) / np.sqrt(2)
    close(s @ x @ s @ zero, y @ zero)
    close(s @ x @ s @ one, 1j * zero)
    close(y @ one, -1j * zero)
    close(np.abs(my @ plus_i) ** 2, [1, 0])
    close(np.abs(sdg @ h @ plus_i) ** 2, [0.5, 0.5])

    # Check both directions of the general change of basis with a unitary
    # whose inverse differs from itself, and a non-Pauli conjugation result.
    t = np.diag([1, np.exp(1j * np.pi / 4)])
    close(t @ x @ t.conj().T, (x + y) / np.sqrt(2))
    u = h @ t
    for original in (x, y, z):
        transformed = u @ original @ u.conj().T
        in_new_basis = u.conj().T @ original @ u
        for coordinates in states:
            close(transformed @ (u @ coordinates), u @ (original @ coordinates))
            close(original @ (u @ coordinates), u @ (in_new_basis @ coordinates))
    print("PASS H/S conjugation, inverse order, X/Y measurement projections and changed-condition questions")


def check_expectation(namespaces: dict[str, dict]) -> None:
    sample = namespaces["expectation"]
    z, x = Pauli("Z"), Pauli("X")
    for name, expected in (
        ("z_value", 0.5), ("plus_z", 0), ("plus_x", 1),
        ("xx_value", 1), ("zz_value", 0), ("sum_value", -1),
    ):
        close(sample[name], expected)

    for label, operator, eigenvalue in (
        ("0", z, 1), ("1", z, -1), ("+", x, 1), ("-", x, -1),
    ):
        state = Statevector.from_label(label)
        close(operator.to_matrix() @ state.data, eigenvalue * state.data)

    # Check conjugation with unequal complex amplitudes, not only real states.
    complex_state = Statevector([np.sqrt(3) / 2, 1j / 2])
    close(complex_state.probabilities(), [0.75, 0.25])
    for state in (sample["psi"], sample["plus"], complex_state):
        p0, p1 = state.probabilities()
        close(state.expectation_value(z), p0 - p1)
        close(np.vdot(state.data, z.to_matrix() @ state.data), p0 - p1)
    close(complex_state.expectation_value(z), 0.5)

    # For product states, the two-qubit eigenvalue is the product of the signs.
    xx = Pauli("XX")
    for label, eigenvalue in (("++", 1), ("+-", -1), ("-+", -1), ("--", 1)):
        state = Statevector.from_label(label)
        close(xx.to_matrix() @ state.data, eigenvalue * state.data)
    close(sample["pair"].probabilities(), [0.25] * 4)
    close(np.dot(sample["pair"].probabilities(), [1, -1, -1, 1]), 0)
    observable = sample["observable"].to_matrix()
    expected_matrix = 0.5 * np.kron(z.to_matrix(), np.eye(2)) - xx.to_matrix()
    close(observable, expected_matrix)
    close(observable, observable.conj().T)
    close(np.vdot(sample["pair"].data, observable @ sample["pair"].data), -1)
    eigenvalues, eigenvectors = np.linalg.eigh(observable)
    probabilities = np.abs(eigenvectors.conj().T @ sample["pair"].data) ** 2
    close(np.dot(eigenvalues, probabilities), sample["sum_value"])
    # An asymmetric state catches swapped Pauli ordering hidden by |++>.
    ordered = Statevector.from_label("10")
    close(ordered.expectation_value(Pauli("ZI")), -1)
    close(ordered.expectation_value(Pauli("IZ")), 1)

    # Correlated states need not factor into individual expectation values.
    bell = Statevector([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)])
    close(bell.expectation_value(xx), 1)
    close(bell.expectation_value(Pauli("XI")), 0)
    close(bell.expectation_value(Pauli("IX")), 0)
    close((740 - 260) / 1000, 0.48)
    close((300 - 700) / 1000, -0.4)
    print("PASS expectation averages, eigenstates, complex conjugation, tensor products and sums")


def check_estimator_chapter(namespaces: dict[str, dict]) -> None:
    from qiskit.primitives.containers import EstimatorPub
    from qiskit.quantum_info import Operator, SparsePauliOp

    purpose = namespaces["estimator-purpose"]
    close(purpose["result"][0].data.evs, 0)
    plus = Statevector.from_instruction(purpose["qc"])
    weighted = SparsePauliOp.from_list([("Z", 0.5), ("X", -1.0)])
    close(plus.expectation_value(weighted), -1)

    pub = namespaces["estimator-pub"]
    # The asymmetric input distinguishes the intended qubit from an idle one.
    close(pub["result"][0].data.evs, -1)
    close(pub["result"][1].data.evs, -1)
    mapped_state = Statevector.from_instruction(pub["isa_circuit"])
    close(mapped_state.expectation_value(Pauli("IIZ")), 1)
    require(pub["isa_observable"].num_qubits == pub["isa_circuit"].num_qubits,
            "Observable width must match the ISA circuit")
    single_pub = EstimatorPub.coerce((purpose["qc"], "Z", None, 0.02))
    close(single_pub.precision, 0.02)
    try:
        EstimatorPub.coerce((purpose["qc"], "Z", 0.02))
    except ValueError:
        pass
    else:
        raise AssertionError("A third tuple element is not a precision")

    options = namespaces["estimator-options"]
    result = options["result"]
    close([p.metadata["target_precision"] for p in result], [0.02, 0.03])
    runtime = options["estimator"]
    require(runtime.options.resilience_level == 0, "Level 0 must be preserved")
    require(runtime.options.resilience.zne_mitigation is True, "Explicit ZNE is enabled")
    close(runtime.options.resilience.zne.noise_factors, [1, 3, 5])
    require(runtime.options.resilience.zne.extrapolator == "linear", "Linear fit requested")

    # Independently derive the fitted intercept from two data points.
    x, y = options["noise_factors"], options["measured_evs"]
    slope = (y[-1] - y[0]) / (x[-1] - x[0])
    intercept = y[0] - slope * x[0]
    close([options["slope"], options["intercept"]], [slope, intercept])
    close(slope * x + intercept, y)
    close(intercept, 0.8)
    close(0.6 - (0.2 - 0.6) / (3 - 1), 0.8)  # Changed-condition question.
    # Folding preserves the ideal operation, including a non-self-inverse gate.
    from qiskit import QuantumCircuit
    folding = QuantumCircuit(2)
    folding.ry(0.37, 0)
    folding.cx(0, 1)
    u = Operator(folding).data
    close(u @ u.conj().T @ u, u)
    close(Pauli("X").to_matrix() @ Pauli("X").to_matrix(), np.eye(2))

    # Derive the variance and readout correction from explicit probabilities.
    signs = np.array([1, -1])
    for p0 in (0.0, 0.25, 0.5, 0.8, 1.0):
        probabilities = np.array([p0, 1 - p0])
        mean = probabilities @ signs
        variance = probabilities @ (signs - mean) ** 2
        close(variance, 1 - mean**2)
        close(np.sqrt(variance / 400), np.sqrt(variance / 100) / 2)
        readout_channel = np.array([[0.9, 0.1], [0.1, 0.9]])
        observed_mean = (readout_channel @ probabilities) @ signs
        close(observed_mean, 0.8 * mean)
        close(observed_mean / 0.8, mean)
    close(1 / np.sqrt([100, 10000]), [0.1, 0.01])
    close(1 / 0.02**2, 2500)
    close((60 - 40) / 100, 0.2)

    output = namespaces["estimator-result"]["result"]
    require(len(output) == 2 and output[0].data.evs.shape == (), "One scalar in PUB 1")
    require(output[1].data.evs.shape == (2,), "Two values in PUB 2")
    close(output[1].data.evs, [0, 1])
    close(output[1].data.stds, [0, 0])
    close(plus.expectation_value(Pauli("Z")), 0)
    close(plus.expectation_value(Pauli("Z").compose(Pauli("Z"))), 1)
    close(namespaces["estimator-broadcasting"]["result"][0].data.evs[1, 2], 0)
    print("PASS Estimator PUBs, layout, options, precision, ZNE arithmetic, shot variance and results")


def outside_fences(text: str) -> str:
    return re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", "", text, flags=re.M | re.S)


def anchors(text: str) -> set[str]:
    text = outside_fences(text)
    result = set(re.findall(r'<a\s+id="([^"]+)"', text))
    seen: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6} (.+)$", text, re.M):
        # GitHub-compatible for the headings targeted by this manuscript.
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def check_links(extra_files: tuple[Path, ...] = ()) -> None:
    files = sorted((ROOT / "manuscript").rglob("*.md"))
    files.append(ROOT / "practice-bank/answers/mock-exams/mock-01-answers.md")
    files.extend(extra_files)
    checked = 0
    for path in files:
        source = outside_fences(path.read_text(encoding="utf-8"))
        for link in re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", source):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            require(target.is_file(), f"Missing link target: {path.name}: {link}")
            if parsed.fragment:
                require(unquote(parsed.fragment) in anchors(target.read_text(encoding="utf-8")),
                        f"Missing anchor: {path.name}: {link}")
            checked += 1
    print(f"PASS {checked} local links in {len(files)} Markdown files")


def main() -> None:
    print(f"Python {sys.version.split()[0]} / Qiskit {qiskit.__version__} / NumPy {np.__version__}")
    require(qiskit.__version__ == "2.5.2", "Use the manuscript baseline Qiskit 2.5.2")
    runtime_version = version("qiskit-ibm-runtime")
    print(f"qiskit-ibm-runtime {runtime_version}")
    require(runtime_version == "0.49.0", "Use the manuscript baseline qiskit-ibm-runtime 0.49.0")
    namespaces = run_examples()
    check_math(namespaces)
    check_chapter_one(namespaces)
    check_conjugation(namespaces)
    check_expectation(namespaces)
    check_estimator_chapter(namespaces)
    check_links()


if __name__ == "__main__":
    main()
