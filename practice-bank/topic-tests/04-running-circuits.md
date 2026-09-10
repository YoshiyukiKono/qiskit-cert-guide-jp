# Topic Test 04 — Running Quantum Circuits

全10問。IBM Quantum Compute execution modes、Runtime V2 primitives、PUBとISA boundaryを中心に扱います。

## Questions

### Q1
`SamplerV2` / `EstimatorV2` を単発のJob modeで実行するとき、`mode` に渡す代表的なものはどれか。

A. `QuantumCircuit`  
B. `Session`だけ  
C. target `BackendV2` object  
D. `Statevector`

### Q2
2026-09時点のSession modeについて最も適切な説明はどれか。

A. 相互依存のない多数jobをまとめるだけのBatchと同義である  
B. 複数jobを扱うdedicated/exclusive execution windowで、activeなsession内workloadはscheduling上priorityを得る。result-dependentな反復workloadにも向く  
C. 1つのlocal Statevector計算だけを指す  
D. OpenQASM textのserialization modeである

### Q3
Batch modeの説明として最も適切なのはどれか。

A. 互いに独立して実行できる複数jobをまとめて扱うexecution mode  
B. 1つのjob内部のshotsを1に固定する機能  
C. statevectorだけを保存するlocal mode  
D. dynamic circuit内のif文そのもの

### Q4
Job / Session / Batchについて正しいものはどれか。

A. SessionとBatchは同じ意味で名前だけ異なる  
B. Job modeではPrimitiveを使えない  
C. Batchではjob同士が前の結果を待って逐次依存することが前提  
D. scheduling/workload特性に応じて3つのexecution modeを使い分ける

### Q5
IBM Quantum Compute用backendを選ぶ処理として現在の代表例に最も近いものはどれか。

A. `Statevector.from_backend()`  
B. `QiskitRuntimeService().least_busy(operational=True, simulator=False)`  
C. `QuantumCircuit.least_busy()`  
D. `SamplerV2.random_backend()`

### Q6
IBM Quantum ComputeのV2 Samplerをimportする現在の代表的な形はどれか。

A. `from qiskit.primitives import Sampler`  
B. `from qiskit import RuntimeSampler`  
C. `from qiskit_ibm_runtime import SamplerV2`  
D. `from qiskit_aer import SamplerV2`

### Q7
Runtime primitiveへQPU用circuitを送る前のtranspilationについて正しいものはどれか。

A. backendのISAへ適合したcircuitを用意する  
B. Runtime V2は任意のabstract instructionを必ずserver側で自動変換するので不要  
C. measurementを全部削除する必要がある  
D. QASM2へ必ず変換する

### Q8
Estimator PUBの構造として最も適切なのはどれか。

A. `(counts, backend)`  
B. `(circuit, observables, optional parameter_values, optional precision)`  
C. `(circuit, shots)`だけ  
D. `(session, qasm_version)`

### Q9
次のlocal V2 EstimatorのPUBを評価したとき、`evs.shape`はどれか。必要なimportは完了しているとする。

```python
theta = Parameter("theta")
qc = QuantumCircuit(1)
qc.ry(theta, 0)
values = np.array([[0.0], [np.pi / 2], [np.pi]])
observables = [["Z"], ["X"]]
evs = StatevectorEstimator().run([(qc, observables, values)]).result()[0].data.evs
```

A. `(3, 2)`  
B. `(2, 3, 1)`  
C. shapeが2と3で異なるため必ず例外になる  
D. `(2, 3)`

### Q10
`job = estimator.run(pubs)` の後の一般的な関係として正しいものはどれか。

A. `run()`はexpectation valueのPython floatだけを直接返す  
B. `run()`はQuantumCircuitを書き換えて戻す  
C. `run()`はjob objectを返し、完了後の結果は`job.result()`で取得する  
D. `run()`は必ず同期的に全結果をlistとして返す

---

# Answers & Explanations

### A1 — C
- A/D: execution modeではない。
- B: Sessionもmodeに使えるが、単発Job modeではbackend objectを指定する。
- C: 正解。

### A2 — B
- A: SessionとBatchは用途が異なる。independent multi-job workloadはBatchが自然。
- B: 正解。current docsではSessionはdedicated/exclusive execution windowで、activeなsession内workloadはpriorityを得る。前job結果を次jobへ反映するiterative workloadにも適する。
- C/D: IBM Quantum execution scheduling modeの説明ではない。

### A3 — A
- A: 正解。Batchはindependently executable jobsを効率よくまとめる。
- B: shots設定ではない。
- C: local simulation modeではない。
- D: circuit control flowとexecution schedulingを混同している。

### A4 — D
- A: Sessionはdedicated/priorityなmulti-job window、Batchはindependent multi-job向けで目的が異なる。
- B: Job modeもprimitive request。
- C: 逐次依存はSession側の代表ユースケース。
- D: 正解。

### A5 — B
- A/C/D: 現行の代表APIではない。
- B: 正解。serviceから利用可能backendを選択する代表例。

### A6 — C
- A: V1 `Sampler`を選ぶ形ではなく、またIBM Runtime implementationでもない。
- B/D: 現行の標準import pathではない。
- C: 正解。

### A7 — A
- A: 正解。target backendのsupported instructions / connectivityへ合わせたISA circuitが必要。
- B: local reference primitivesとの混同。
- C: Samplerではclassical outputを得るmeasurementが必要になる。
- D: QASM2変換は要件ではない。

### A8 — B
- A: Estimator入力ではない。
- B: 正解。PUBはsingle circuit + observablesを核にする。
- C: `(circuit, shots)`はそのまま正しいSampler PUBでもない。Samplerでparameter valuesなしにshotsを渡すなら`(circuit, None, shots)`。Estimatorではさらにobservableが必要。
- D: PUBの構造ではない。

### A9 — D
`values`の最後の軸は1個のcircuit parameterに対応するため、broadcastするbinding shapeは`(3,)`。observable shape `(2,1)`とbroadcastして`(2,3)`になる。
- A: observableの軸とparameter-setの軸を逆にしている。
- B: 最後のparameter軸は出力に残らない。
- C: size 1の軸を利用できるため、この2つのshapeは互換である。
- D: 正解。2種類のobservableを3つのparameter setで評価する。

理想的な`evs`は、Zの行が`[1,0,-1]`、Xの行が`[0,1,0]`（数値誤差を除く）。このbroadcasting規則はV2 PUBのものであり、Runtime QPUへ送る際には別途ISA circuit / observable layoutを整える。このlocalコードをQPU上で実行したという意味ではない。

### A10 — C
- A/D: `run()`はjob handleを返す。
- B: circuit mutation APIではない。
- C: 正解。`job.result()`は完了までblockし得る。

## Official references

- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- Primitive input/output: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Estimator inputs/outputs: https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output
- Transpilation/ISA: https://quantum.cloud.ibm.com/docs/en/guides/defaults-and-configuration-options
