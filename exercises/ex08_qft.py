# exercises/ex08_qft.py
"""
Exercise 08: QFT

学習目標:
- QFT = H + Controlled Phase + SWAP
- Controlled Phase の角度が π/2, π/4... と小さくなる
- 最後に bit reversal 補正として SWAP が必要になる

補足:
Qiskitには QFT / QFTGate もありますが、
資格対策では「手で書ける」ことが重要です。
"""

from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def qft_3qubits() -> QuantumCircuit:
    qc = QuantumCircuit(3)

    # q0にHadamard
    qc.h(0)

    # q0をcontrolとして、q1/q2へ位相を与える
    qc.cp(pi / 2, 0, 1)
    qc.cp(pi / 4, 0, 2)

    # q1にHadamard
    qc.h(1)

    # q1をcontrolとして、q2へ位相を与える
    qc.cp(pi / 2, 1, 2)

    # q2にHadamard
    qc.h(2)

    # QFTでは出力ビット順が逆になるため補正する
    qc.swap(0, 2)

    return qc


qc = qft_3qubits()

print(qc.draw("text"))

state = Statevector.from_instruction(qc)
print("\nStatevector:")
print(state)
