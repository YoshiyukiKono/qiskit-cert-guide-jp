"""Credential-free SDK/client regression checks; no Runtime service or QPU calls.

Numerical comparisons retain global phase and use explicit tolerances. Passing
these selected checks is not a proof of all 148 questions or hardware support.
"""
from __future__ import annotations
from io import StringIO
from math import pi, sqrt
from pathlib import Path
import tempfile
import unittest

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Gate, Instruction, Parameter
from qiskit.circuit.library import RXGate, RZGate, XGate, YGate, ZGate
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.primitives.containers import BitArray
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.qasm3 import dump, dumps, load, loads
from qiskit.quantum_info import Operator, Pauli, SparsePauliOp, Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.options import EstimatorOptions, SamplerOptions


def close(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-12)


class SDKChecks(unittest.TestCase):
    def test_hzh_hxh_and_rotations(self):
        # Expected matrices are constructed independently of the gate classes.
        x = np.array([[0, 1], [1, 0]], dtype=complex)
        z = np.diag([1, -1]).astype(complex)
        for middle, expected in (("z", x), ("x", z)):
            qc = QuantumCircuit(1)
            qc.h(0)
            getattr(qc, middle)(0)
            qc.h(0)
            close(Operator(qc).data, expected)
        close(Operator(RXGate(pi)).data, -1j * x)
        close(Operator(RZGate(pi)).data, -1j * z)

    def test_vectors_and_global_phase(self):
        plus = np.array([1, 1], dtype=complex) / sqrt(2)
        minus = np.array([1, -1], dtype=complex) / sqrt(2)
        close(Operator(ZGate()).data @ plus, minus)
        close(Operator(YGate()).data @ np.array([1, 0]), [0, 1j])
        close(np.diag([1, -1j]) @ (np.array([1, 1j]) / sqrt(2)), plus)
        self.assertFalse(np.allclose(minus, 1j * minus))
        close(np.outer(minus, minus.conj()), np.outer(1j * minus, (1j * minus).conj()))

    def test_bell_amplitudes_probabilities_and_phase(self):
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        state = Statevector.from_instruction(qc)
        close(state.data, np.array([1, 0, 0, 1]) / sqrt(2))
        close(state.probabilities(), [0.5, 0, 0, 0.5])
        qc.z(0)
        changed = Statevector.from_instruction(qc)
        close(changed.probabilities(), state.probabilities())
        self.assertFalse(state.equiv(changed))

    def test_pauli_label_order(self):
        x = np.array([[0, 1], [1, 0]])
        z = np.diag([1, -1])
        close(Pauli("XZ").to_matrix(), np.kron(x, z))
        close(Pauli("XZ").to_matrix() @ [0, 1, 0, 0], [0, 0, 0, -1])

    def test_compose_and_parameter_binding(self):
        qc, other = QuantumCircuit(1), QuantumCircuit(1)
        other.x(0)
        composed = qc.compose(other)
        self.assertEqual(len(qc.data), 0)
        close(Operator(composed).data, [[0, 1], [1, 0]])
        self.assertIsNone(qc.compose(other, inplace=True))
        self.assertEqual(len(qc.data), 1)
        angle = Parameter("theta")
        parameterized = QuantumCircuit(1)
        parameterized.ry(angle, 0)
        bound = parameterized.assign_parameters({angle: pi})
        self.assertEqual(parameterized.num_parameters, 1)
        self.assertEqual(bound.num_parameters, 0)
        close(Statevector.from_instruction(bound).data, [0, 1])

    def test_gate_control_not_generic_instruction(self):
        self.assertTrue(hasattr(Gate, "control"))
        self.assertFalse(hasattr(Instruction, "control"))
        expected = QuantumCircuit(2)
        expected.cx(0, 1)
        close(Operator(XGate().control()).data, Operator(expected).data)

    def test_sampler_counts_and_shot_precedence(self):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        result = StatevectorSampler(seed=1234).run([qc], shots=1000).result()[0]
        counts = result.data.c.get_counts()
        self.assertEqual(sum(counts.values()), 1000)
        self.assertTrue(400 < counts.get("0", 0) < 600)
        deterministic = QuantumCircuit(1, 1)
        deterministic.x(0)
        deterministic.measure(0, 0)
        sampler = StatevectorSampler(default_shots=500, seed=1234)
        pubs = sampler.run([deterministic, (deterministic, None, 32)], shots=128).result()
        self.assertEqual(pubs[0].data.c.get_counts(), {"1": 128})
        self.assertEqual(pubs[1].data.c.get_counts(), {"1": 32})

    def test_bitarray_expectation_and_counts(self):
        bits = BitArray.from_counts({"0": 3, "1": 1})
        self.assertEqual(bits.get_counts(), {"0": 3, "1": 1})
        close(bits.expectation_values("Z"), 0.5)
        with self.assertRaises(TypeError):
            bits.expectation_values()
        with self.assertRaises(ValueError):
            bits.expectation_values("X")

    def test_register_and_measurement_order(self):
        from qiskit import ClassicalRegister, QuantumRegister
        q = QuantumRegister(2, "q")
        left, right = ClassicalRegister(1, "left"), ClassicalRegister(1, "right")
        qc = QuantumCircuit(q, left, right)
        qc.x(q[0])
        qc.measure(q[0], right[0])
        qc.measure(q[1], left[0])
        result = StatevectorSampler().run([qc], shots=16).result()[0]
        self.assertEqual(result.data.right.get_counts(), {"1": 16})
        self.assertEqual(result.data.left.get_counts(), {"0": 16})

    def test_estimator_expectations_and_broadcasting(self):
        parameter = Parameter("theta")
        qc = QuantumCircuit(1)
        qc.ry(parameter, 0)
        # Parameter-binding axis is excluded: (3,1) values -> binding shape (3,).
        values = np.array([[0], [pi / 2], [pi]])
        result = StatevectorEstimator().run([(qc, [["Z"], ["X"]], values)]).result()[0]
        self.assertEqual(result.data.evs.shape, (2, 3))
        close(result.data.evs, [[1, 0, -1], [0, 1, 0]])
        close(result.data.stds, np.zeros((2, 3)))
        bell = QuantumCircuit(2)
        bell.h([0, 1])
        close(StatevectorEstimator().run([(bell, SparsePauliOp("XX"))]).result()[0].data.evs, 1)

    def test_target_and_observable_layout(self):
        backend = GenericBackendV2(3, basis_gates=["cx", "id", "rz", "sx", "x"],
                                   coupling_map=[[0, 1], [1, 0], [1, 2], [2, 1]], seed=123)
        qc = QuantumCircuit(2)
        qc.x(0)
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1,
                                          initial_layout=[2, 0], seed_transpiler=123)
        isa = pm.run(qc)
        obs = SparsePauliOp("IZ")
        mapped = obs.apply_layout(isa.layout)
        self.assertEqual(mapped.num_qubits, isa.num_qubits)
        close(Statevector.from_instruction(qc).expectation_value(obs), -1)
        close(Statevector.from_instruction(isa).expectation_value(mapped), -1)

    def test_if_test_representation_and_local_sampler_limit(self):
        qc = QuantumCircuit(2, 1)
        qc.h(0)
        qc.measure(0, 0)
        with qc.if_test((qc.clbits[0], 1)):
            qc.x(1)
        operation = qc.data[-1].operation
        self.assertEqual(operation.name, "if_else")
        self.assertEqual(operation.condition, (qc.clbits[0], 1))
        # This tests SDK representation, not execution on IBM hardware.
        mid = QuantumCircuit(1, 1)
        mid.h(0)
        mid.measure(0, 0)
        mid.x(0)
        mid.measure(0, 0)
        with self.assertRaises(ValueError):
            StatevectorSampler().run([mid]).result()

    def test_runtime_client_option_objects_only(self):
        sampler = SamplerOptions(default_shots=500)
        sampler.dynamical_decoupling.enable = True
        self.assertEqual(sampler.default_shots, 500)
        self.assertTrue(sampler.dynamical_decoupling.enable)
        for level in (0, 1, 2):
            self.assertEqual(EstimatorOptions(resilience_level=level).resilience_level, level)
        options = EstimatorOptions(resilience_level=0)
        options.resilience.zne_mitigation = True
        self.assertTrue(options.resilience.zne_mitigation)
        # Object acceptance is not proof of the server's mitigation execution.

    def test_qasm3_export_import_roundtrip(self):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [1, 0])
        text = dumps(qc)
        self.assertIn("OPENQASM 3.0;", text)
        self.assertIn('include "stdgates.inc";', text)
        stream = StringIO()
        dump(qc, stream)
        self.assertEqual(stream.getvalue(), text)
        imported = loads(text)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "circuit.qasm"
            path.write_text(text, encoding="utf-8")
            from_file = load(str(path))
        self.assertEqual(imported, from_file)
        self.assertEqual(imported.count_ops(), qc.count_ops())
        def measurements(circuit):
            return [(circuit.find_bit(item.qubits[0]).index, circuit.find_bit(item.clbits[0]).index)
                    for item in circuit.data if item.operation.name == "measure"]
        self.assertEqual(measurements(imported), measurements(qc))
        close(Operator(imported.remove_final_measurements(inplace=False)).data,
              Operator(qc.remove_final_measurements(inplace=False)).data)

    def test_explicit_qasm_reset_prepares_plus_before_measurement(self):
        source = 'OPENQASM 3.0;\ninclude "stdgates.inc";\nqubit q;\nreset q;\nh q;\n'
        circuit = loads(source)
        self.assertEqual([item.operation.name for item in circuit.data], ["reset", "h"])
        # Try two possible incoming states; reset, not declaration, prepares zero.
        for initial in ("0", "1"):
            state = Statevector.from_label(initial).evolve(circuit)
            close(state.data, np.array([1, 1]) / sqrt(2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
