# exercises/ex13_noise_simulation.py
"""
Exercise 13: noise simulation

学習目標:
- 実機は理想シミュレータと違いノイズを持つ
- depolarizing_error で簡単なノイズを追加できる
- Bell状態の 00/11 以外が出る理由を理解する
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# ノイズモデルを作る
noise_model = NoiseModel()

# 1量子ビットゲート用ノイズ
one_qubit_error = depolarizing_error(0.01, 1)

# 2量子ビットゲート用ノイズ
two_qubit_error = depolarizing_error(0.05, 2)

noise_model.add_all_qubit_quantum_error(one_qubit_error, ["h", "x"])
noise_model.add_all_qubit_quantum_error(two_qubit_error, ["cx"])

sim = AerSimulator(noise_model=noise_model)
compiled = transpile(qc, sim)

result = sim.run(compiled, shots=1000).result()

print(qc.draw("text"))
print("\nCounts with noise:")
print(result.get_counts())
