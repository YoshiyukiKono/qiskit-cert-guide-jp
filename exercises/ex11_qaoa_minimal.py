# exercises/ex11_qaoa_minimal.py
"""
Exercise 11: QAOA最小例

学習目標:
- QAOA = cost Hamiltonian + mixer Hamiltonian
- MaxCutを2ノードで理解する
- gamma はcost回転、beta はmixer回転

問題:
2ノード1エッジのMaxCut。

最適解:
01 または 10

理由:
2つのノードが異なるグループに分かれると、辺がcutされる。
"""

from math import pi
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def qaoa_2node_maxcut(gamma: float, beta: float) -> QuantumCircuit:
    """
    2ノードMaxCut用のp=1 QAOA回路。

    初期状態:
    |++>

    cost evolution:
    ZZ相互作用で問題のコストを位相に埋め込む

    mixer evolution:
    RX回転で探索空間を移動する
    """
    qc = QuantumCircuit(2, 2)

    # 初期状態 |++>
    qc.h([0, 1])

    # Cost Hamiltonian: Z0 Z1 に対応する位相回転
    # RZZを使うとZZ相互作用を簡潔に表現できる
    qc.rzz(2 * gamma, 0, 1)

    # Mixer Hamiltonian: X0 + X1
    qc.rx(2 * beta, 0)
    qc.rx(2 * beta, 1)

    qc.measure([0, 1], [0, 1])
    return qc


# 2ノードMaxCutでは、このあたりの値で 01/10 が出やすくなる
gamma = pi / 4
beta = pi / 8

qc = qaoa_2node_maxcut(gamma, beta)

print(qc.draw("text"))

sim = AerSimulator()
compiled = transpile(qc, sim)

result = sim.run(compiled, shots=1000).result()
counts = result.get_counts()

print("\nCounts:")
print(counts)

print("\nExpected good answers:")
print("01 and 10")
