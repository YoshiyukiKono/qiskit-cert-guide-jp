# exercises/ex02_pauli.py
"""
Exercise 02: Pauliゲート

学習目標:
- Xはビット反転
- Zは位相反転
- HXH = Z
- HZH = X
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from common import show_state


# X|0> = |1>
qc_x = QuantumCircuit(1)
qc_x.x(0)

print("X gate:")
print(qc_x.draw("text"))
show_state(qc_x)


# H Z H = X
qc_hzh = QuantumCircuit(1)
qc_hzh.h(0)
qc_hzh.z(0)
qc_hzh.h(0)

print("\nH-Z-H operator:")
print(Operator(qc_hzh))


# H X H = Z
qc_hxh = QuantumCircuit(1)
qc_hxh.h(0)
qc_hxh.x(0)
qc_hxh.h(0)

print("\nH-X-H operator:")
print(Operator(qc_hxh))
