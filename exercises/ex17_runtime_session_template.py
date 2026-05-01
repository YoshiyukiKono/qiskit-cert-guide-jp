# exercises/ex17_runtime_session_template.py
"""
Exercise 17: IBM Runtime Session template

学習目標:
- Runtime Sessionの基本形を理解する
- 実機実行では qiskit-ibm-runtime を使う
- SamplerV2 / EstimatorV2 はRuntime用primitive

注意:
このファイルはテンプレートです。
実行にはIBM QuantumアカウントとAPI設定が必要です。
"""

from qiskit import QuantumCircuit

# 実行環境がある場合のみ有効化してください
# from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

print(qc.draw("text"))

"""
実機実行テンプレート:

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

with Session(backend=backend) as session:
    sampler = Sampler(mode=session)
    job = sampler.run([qc], shots=1000)
    result = job.result()

print(result)
"""
