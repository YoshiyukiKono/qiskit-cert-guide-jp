# exercises/ex12_transpile.py
"""
Exercise 12: transpile

学習目標:
- transpile = 回路をbackend向けに変換する処理
- basis_gates により使用ゲートを制限できる
- optimization_level により回路が簡約される
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(1)

# Hを2回かけると恒等変換
qc.h(0)
qc.h(0)

print("Original circuit:")
print(qc.draw("text"))

sim = AerSimulator()

compiled_0 = transpile(qc, sim, optimization_level=0)
compiled_3 = transpile(qc, sim, optimization_level=3)

print("\nTranspiled optimization_level=0:")
print(compiled_0.draw("text"))

print("\nTranspiled optimization_level=3:")
print(compiled_3.draw("text"))
