# exercises/ex10_vqe_minimal.py
"""
Exercise 10: VQE最小例

学習目標:
- VQE = パラメータ付き回路 + Estimator + 古典最適化
- Estimatorは期待値を返す
- ここでは H = Z の期待値を最小化する

理論:
Zの期待値は、
|0> で +1
|1> で -1

したがって最小値は -1。
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp


def ansatz(theta: float) -> QuantumCircuit:
    """
    1量子ビットのパラメータ付き回路。

    Ry(theta)により、
    |0> から |1> まで連続的に状態を動かす。
    """
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    return qc


def estimate_energy(theta: float) -> float:
    """
    H = Z の期待値を計算する。

    Estimatorは「回路」と「observable」を受け取り、
    期待値を返す。
    """
    qc = ansatz(theta)
    observable = SparsePauliOp.from_list([("Z", 1.0)])

    estimator = StatevectorEstimator()
    job = estimator.run([(qc, observable)])
    result = job.result()[0]

    # result.data.evs に期待値が入る
    return float(result.data.evs)


# 本格的な最適化ライブラリを使わず、
# 資格対策として分かりやすくgrid searchする
candidates = np.linspace(0, 2 * np.pi, 101)

best_theta = None
best_energy = None

for theta in candidates:
    energy = estimate_energy(theta)

    if best_energy is None or energy < best_energy:
        best_energy = energy
        best_theta = theta

print("Best theta:", best_theta)
print("Best energy:", best_energy)

print("\nExpected:")
print("Minimum energy should be close to -1.")
