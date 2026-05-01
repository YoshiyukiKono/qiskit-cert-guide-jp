# exercises/ex05_phase.py
"""
Exercise 05: 位相ゲート

学習目標:
- Z, S, T は確率ではなく位相を変える
- 位相は測定だけでは見えにくい
- Hで挟むと干渉として見える
"""

from qiskit import QuantumCircuit
from common import show_state, show_probabilities


qc = QuantumCircuit(1)

# |+> を作る
qc.h(0)

# 位相反転
qc.z(0)

print("After H then Z:")
print(qc.draw("text"))
show_state(qc)
show_probabilities(qc)


# HZH = X を確認
qc2 = QuantumCircuit(1)
qc2.h(0)
qc2.z(0)
qc2.h(0)

print("\nAfter H-Z-H:")
print(qc2.draw("text"))
show_state(qc2)
show_probabilities(qc2)
