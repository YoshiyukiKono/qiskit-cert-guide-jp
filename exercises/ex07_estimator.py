# exercises/ex07_estimator.py
"""
Exercise 07: StatevectorEstimator

学習目標:
- Estimatorは期待値を計算する
- VQE/QAOAでは Estimator が重要
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp


# |0> 状態
qc = QuantumCircuit(1)

# Z observable
observable = SparsePauliOp.from_list([("Z", 1.0)])

estimator = StatevectorEstimator()

job = estimator.run([(qc, observable)])
result = job.result()[0]

print(qc.draw("text"))
print(result)
