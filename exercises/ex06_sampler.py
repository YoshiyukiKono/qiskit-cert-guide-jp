# exercises/ex06_sampler.py
"""
Exercise 06: StatevectorSampler

学習目標:
- Samplerは測定結果のサンプルを返す
- Qiskit 2.x系では StatevectorSampler がローカル演習に便利
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


qc = QuantumCircuit(2, 2)

qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

sampler = StatevectorSampler(seed=42)

# V2 primitiveでは、runにはPUBのリストを渡す
job = sampler.run([qc], shots=1000)
result = job.result()[0]

print(qc.draw("text"))
print(result)
