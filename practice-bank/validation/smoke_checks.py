"""Small local checks for the v2.x practice bank.

This is intentionally not a complete test suite for every question.  It checks a
few facts that are easy to regress when examples are edited.
"""

from math import isclose, sqrt

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.qasm3 import dumps
from qiskit.quantum_info import SparsePauliOp, Statevector


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


def check_hzh_and_hxh():
    hzh = QuantumCircuit(1)
    hzh.h(0)
    hzh.z(0)
    hzh.h(0)
    out = Statevector.from_instruction(hzh)
    assert out.equiv(Statevector.from_label("1"))

    hxh = QuantumCircuit(1)
    hxh.x(0)
    hxh.h(0)  # prepare |-> from |1>, then complete explicit HXH below differently

    # Direct matrix-free checks on computational basis for HXH = Z.
    qc0 = QuantumCircuit(1)
    qc0.h(0)
    qc0.x(0)
    qc0.h(0)
    assert Statevector.from_instruction(qc0).equiv(Statevector.from_label("0"))

    qc1 = QuantumCircuit(1)
    qc1.x(0)  # prepare |1>
    qc1.h(0)
    qc1.x(0)
    qc1.h(0)
    expected = Statevector([0, -1])
    assert Statevector.from_instruction(qc1).equiv(expected)


def check_bell_state():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    probs = Statevector.from_instruction(qc).probabilities_dict()
    assert isclose(probs.get("00", 0.0), 0.5, abs_tol=1e-9)
    assert isclose(probs.get("11", 0.0), 0.5, abs_tol=1e-9)
    assert isclose(probs.get("01", 0.0), 0.0, abs_tol=1e-9)
    assert isclose(probs.get("10", 0.0), 0.0, abs_tol=1e-9)


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

    x_result = estimator.run([(qc, x)]).result()[0].data.evs
    z_result = estimator.run([(qc, z)]).result()[0].data.evs

    assert isclose(float(x_result), 1.0, abs_tol=1e-9)
    assert isclose(float(z_result), 0.0, abs_tol=1e-9)


def check_qasm3_export():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    text = dumps(qc)
    assert "OPENQASM 3.0;" in text
    assert "qubit[2]" in text
    assert "bit[2]" in text
    assert "measure" in text


def main():
    check_basic_states()
    check_hzh_and_hxh()
    check_bell_state()
    check_sampler()
    check_estimator()
    check_qasm3_export()
    print("practice-bank smoke checks: OK")


if __name__ == "__main__":
    main()
