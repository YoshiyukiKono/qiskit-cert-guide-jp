# exercises/ex14_parameter_sweep.py
"""
Exercise 14: parameter sweep

学習目標:
- Parameter を使うとパラメータ付き回路を作れる
- 同じ回路で角度だけ変えて結果を比較できる
- VQE/QAOAの前提になる
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector

theta = Parameter("θ")

qc = QuantumCircuit(1)
qc.ry(theta, 0)

print("Parameterized circuit:")
print(qc.draw("text"))

for value in np.linspace(0, np.pi, 5):
    bound_qc = qc.assign_parameters({theta: value})
    state = Statevector.from_instruction(bound_qc)
    probs = state.probabilities_dict()

    print(f"\nθ = {value:.3f}")
    print(probs)
