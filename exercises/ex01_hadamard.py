# exercises/ex01_hadamard.py
"""
Exercise 01: Hadamardゲート

学習目標:
- H|0> = (|0> + |1>) / sqrt(2)
- Hを2回かけると元に戻る
"""

from qiskit import QuantumCircuit
from common import show_state, show_probabilities


# 1量子ビット回路
qc = QuantumCircuit(1)

# |0> に H を適用
qc.h(0)

print("Circuit:")
print(qc.draw("text"))

print("\nStatevector:")
show_state(qc)

print("\nProbabilities:")
show_probabilities(qc)


# Hを2回適用
qc2 = QuantumCircuit(1)
qc2.h(0)
qc2.h(0)

print("\nH twice:")
print(qc2.draw("text"))
show_state(qc2)
