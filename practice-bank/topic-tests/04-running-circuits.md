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
Session modeが最も適するworkloadはどれか。

A. 相互依存のない多数jobをまとめて効率良く投入するだけのworkload  
B. 前のjob結果を使って次のjobを決める反復的workload  
C. 1つのlocal Statevector計算  
D. OpenQASM textのserialization

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
Estimator V2のbroadcastingについて正しいものはどれか。

A. observablesとparameter valuesは必ず同一Python list長でなければならない  
B. broadcastingはSamplerだけの機能  
C. array形状は無視され常にscalar resultになる  
D. observablesとparameter valuesはNumPy型のbroadcasting rulesに従って組み合わせられる

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
- A: independent multi-job workloadはBatchが自然。
- B: 正解。iterative workloadでSessionが有効。
- C/D: IBM Quantum execution scheduling modeを必要としない。

### A3 — A
- A: 正解。Batchはindependently executable jobsを効率よくまとめる。
- B: shots設定ではない。
- C: local simulation modeではない。
- D: circuit control flowとexecution schedulingを混同している。

### A4 — D
- A: Sessionはiterative、Batchはindependent multi-job向けで目的が異なる。
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
- C: Sampler PUBに近いがEstimatorではobservableが必要。
- D: PUBの構造ではない。

### A9 — D
- A: size 1 dimensions等を使ったbroadcastingが可能。
- B: Estimatorで重要な機能。
- C: broadcasted shapeに応じてarray resultを返し得る。
- D: 正解。

### A10 — C
- A/D: `run()`はjob handleを返す。
- B: circuit mutation APIではない。
- C: 正解。`job.result()`は完了までblockし得る。

## Official references

- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- Primitive input/output: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Estimator inputs/outputs: https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output
- Transpilation/ISA: https://quantum.cloud.ibm.com/docs/en/guides/defaults-and-configuration-options
