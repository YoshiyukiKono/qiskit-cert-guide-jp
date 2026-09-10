"""Local, credential-free checks for the Qiskit v2.x practice bank.

These checks deliberately cover claims that can be verified with the Qiskit SDK
alone. IBM Quantum Compute / Runtime claims are checked against current official
documentation instead of requiring account credentials in this script.
"""

from math import isclose, pi, sqrt

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RXGate, XGate, ZGate
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.qasm3 import dumps
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector


def assert_close_complex(actual, expected, tol=1e-9):
    assert abs(actual - expected) < tol, (actual, expected)


def check_basic_states():
    qc = QuantumCircuit(1)
    qc.h(0)
    sv = Statevector.from_instruction(qc)
    assert_close_complex(sv.data[0], 1 / sqrt(2))
    assert_close_complex(sv.data[1], 1 / sqrt(2))

    qc.z(0)
    sv = Statevector.from_instruction(qc)
    assert_close_complex(sv.data[0], 1 / sqrt(2))
    assert_close_complex(sv.data[1], -1 / sqrt(2))


def check_operator_identities():
    """Compare operators exactly, not basis-state rays up to global phase."""

    x = Operator(XGate()).data
    z = Operator(ZGate()).data

    hzh = QuantumCircuit(1)
    hzh.h(0)
    hzh.z(0)
    hzh.h(0)
    assert np.allclose(Operator(hzh).data, x)

    hxh = QuantumCircuit(1)
    hxh.h(0)
    hxh.x(0)
    hxh.h(0)
    assert np.allclose(Operator(hxh).data, z)

    rx_pi = Operator(RXGate(pi)).data
    assert np.allclose(rx_pi, -1j * x)


def check_bell_state():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    probs = Statevector.from_instruction(qc).probabilities_dict()
    assert isclose(probs.get("00", 0.0), 0.5, abs_tol=1e-9)
    assert isclose(probs.get("11", 0.0), 0.5, abs_tol=1e-9)
    assert isclose(probs.get("01", 0.0), 0.0, abs_tol=1e-9)
    assert isclose(probs.get("10", 0.0), 0.0, abs_tol=1e-9)


def check_compose_semantics():
    qc = QuantumCircuit(1)
    other = QuantumCircuit(1)
    other.x(0)

    composed = qc.compose(other)
    assert len(qc.data) == 0, "compose() default should not mutate qc"
    assert len(composed.data) == 1

    qc.compose(other, inplace=True)
    assert len(qc.data) == 1


def check_sampler():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    sampler = StatevectorSampler(seed=1234)
    result = sampler.run([qc], shots=1000).result()[0]
    counts = result.data.c.get_counts()
    assert sum(counts.values()) == 1000
    p0 = counts.get("0", 0) / 1000
    assert 0.40 < p0 < 0.60, counts


def check_estimator():
    qc = QuantumCircuit(1)
    qc.h(0)
    estimator = StatevectorEstimator()

    x = SparsePauliOp.from_list([("X", 1.0)])
    z = SparsePauliOp.from_list([("Z", 1.0)])

    x_result = np.asarray(estimator.run([(qc, x)]).result()[0].data.evs).item()
    z_result = np.asarray(estimator.run([(qc, z)]).result()[0].data.evs).item()

    assert isclose(float(x_result), 1.0, abs_tol=1e-9)
    assert isclose(float(z_result), 0.0, abs_tol=1e-9)


def check_qasm3_export():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    text = dumps(qc)
    assert "OPENQASM 3.0;" in text
    assert 'include "stdgates.inc";' in text
    assert "qubit[2]" in text
    assert "bit[2]" in text
    assert "measure" in text


def main():
    check_basic_states()
    check_operator_identities()
    check_bell_state()
    check_compose_semantics()
    check_sampler()
    check_estimator()
    check_qasm3_export()
    print("practice-bank smoke checks: OK")


if __name__ == "__main__":
    main()
