# exercises/ex15_sampler_parameterized.py
"""
Exercise 15: StatevectorSampler with parameterized circuit

学習目標:
- Samplerは測定結果のサンプルを返す
- パラメータ付き回路を複数の値で評価できる
- V2 primitivesではPUB形式を意識する
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorSampler

theta = Parameter("θ")

qc = QuantumCircuit(1, 1)
qc.ry(theta, 0)
qc.measure(0, 0)

parameter_values = np.array([[0.0], [np.pi / 2], [np.pi]])

sampler = StatevectorSampler(seed=42)

# PUB: (circuit, parameter_values)
job = sampler.run([(qc, parameter_values)], shots=1000)
result = job.result()[0]

print(qc.draw("text"))
print("\nSampler result:")
print(result)
