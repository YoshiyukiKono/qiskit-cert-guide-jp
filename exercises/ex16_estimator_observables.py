# exercises/ex16_estimator_observables.py
"""
Exercise 16: Estimator with multiple observables

学習目標:
- Estimatorは期待値を計算する
- observableを変えると同じ状態でも評価値が変わる
- VQE/QAOAではこの考え方が中心になる
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(1)

# |+> 状態を作る
qc.h(0)

observables = [
    SparsePauliOp.from_list([("X", 1.0)]),
    SparsePauliOp.from_list([("Y", 1.0)]),
    SparsePauliOp.from_list([("Z", 1.0)]),
]

estimator = StatevectorEstimator()

for observable in observables:
    job = estimator.run([(qc, observable)])
    result = job.result()[0]

    print("\nObservable:")
    print(observable)
    print("Expectation value:")
    print(result.data.evs)
