# exercises/ex03_measurement.py
"""
Exercise 03: Measurement

学習目標:
- 測定は量子状態を古典ビットへ変換する
- shotsは回路実行回数
- countsは測定結果の回数
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


qc = QuantumCircuit(1, 1)

# 重ね合わせを作る
qc.h(0)

# qubit 0 を classical bit 0 に測定
qc.measure(0, 0)

print(qc.draw("text"))

sim = AerSimulator()
compiled = transpile(qc, sim)

result = sim.run(compiled, shots=1000).result()
counts = result.get_counts()

print(counts)
