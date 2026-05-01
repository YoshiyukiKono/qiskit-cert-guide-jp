# exercises/ex09_grover.py
"""
Exercise 09: Grover最小例

学習目標:
- oracle = 正解状態の位相を反転する
- diffusion = 平均値に対する反転
- 2量子ビット探索では1回のGrover iterationで正解確率が高くなる

ここでは |11> を正解として探索する。
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def oracle_mark_11(qc: QuantumCircuit) -> None:
    """
    |11> だけに -1 の位相を付ける。

    CZは |11> にだけ -1 を付けるので、
    |11> を正解にするoracleとしてそのまま使える。
    """
    qc.cz(0, 1)


def diffusion_2qubits(qc: QuantumCircuit) -> None:
    """
    2量子ビット用diffusion operator。

    流れ:
    H
    X
    CZ
    X
    H

    これは「平均値に対する反転」を回路で実装したもの。
    """
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])


qc = QuantumCircuit(2, 2)

# 全状態の均等重ね合わせを作る
qc.h([0, 1])

# Grover iteration = oracle + diffusion
oracle_mark_11(qc)
diffusion_2qubits(qc)

# 測定
qc.measure([0, 1], [0, 1])

print(qc.draw("text"))

sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1000).result()

print("\nCounts:")
print(result.get_counts())
