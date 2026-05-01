# exercises/ex04_bell_state.py
"""
Exercise 04: Bell状態

学習目標:
- H + CX でエンタングルメントを作る
- 測定結果は 00 と 11 のみになる
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from common import show_state


qc = QuantumCircuit(2)

# Bell状態を作る
qc.h(0)
qc.cx(0, 1)

print("Bell circuit:")
print(qc.draw("text"))

print("\nStatevector:")
show_state(qc)


# 測定用回路
measured = QuantumCircuit(2, 2)
measured.h(0)
measured.cx(0, 1)
measured.measure([0, 1], [0, 1])

sim = AerSimulator()
compiled = transpile(measured, sim)

result = sim.run(compiled, shots=1000).result()
print("\nCounts:")
print(result.get_counts())
