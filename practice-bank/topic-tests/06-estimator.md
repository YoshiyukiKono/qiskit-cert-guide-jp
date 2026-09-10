# Topic Test 06 — Estimator Primitive

全10問。local V2 reference implementationとIBM Quantum Compute `EstimatorV2`、precisionとresilience optionsを区別して扱います。

## Questions

### Q1
Estimator V2の中心的な役割として最も適切なのはどれか。

A. circuitのclassical bitstringだけをsampleする  
B. transpiler routingを実行する  
C. circuitとobservableから期待値を求める  
D. OpenQASM sourceを構文解析する

### Q2
Qiskit SDKのローカルV2 reference Estimatorはどれか。

A. `StatevectorSampler`  
B. `BackendSamplerV2`  
C. `EstimatorV2`  
D. `StatevectorEstimator`

### Q3
IBM Quantum Compute Serviceで使うEstimator implementationはどれか。

A. `qiskit.quantum_info.EstimatorV2`  
B. `qiskit_ibm_runtime.EstimatorV2`  
C. `QuantumCircuit.estimator()`  
D. `qiskit.primitives.StatevectorSampler`

### Q4
Estimator PUBの一般的なtuple構造として最も適切なのはどれか。

A. `(circuit, observables, optional parameter_values, optional precision)`  
B. `(circuit, optional parameter_values, optional shots)`  
C. `(counts, observable)`  
D. `(backend, qasm_version)`

### Q5
`|+>` に対するPauli-Zの期待値 `<Z>` はいくつか。

A. +1  
B. -1  
C. 0  
D. 1/2

### Q6
2026-09時点のIBM Quantum Compute `EstimatorV2` で指定できる `resilience_level` の組として正しいものはどれか。

A. 1, 2, 3, 4  
B. 0, 1, 2  
C. 0, 1だけ  
D. 任意の0以上の整数

### Q7
個別のresilience optionsで上書きしない場合、`resilience_level=0` のpresetとして最も適切なのはどれか。

A. ZNEだけを有効にする  
B. TREXだけを必ず有効にする  
C. shotsを0にする  
D. Estimatorが提供するresilience mitigationを適用しない

### Q8
個別のresilience optionsで上書きしない場合、2026-09時点の `resilience_level=2` のpresetについて最も適切なのはどれか。

A. level 1の測定error mitigationに加え、ZNE等を用いたより強いmitigationを有効にする設定である  
B. Qiskit transpilerのoptimization level 2と同一である  
C. circuitを2回だけ実行する指定である  
D. observableを2個に制限する指定である

### Q9
Estimatorの `precision` について最も適切な説明はどれか。

A. qubitの浮動小数点bit幅を指定する  
B. observableのPauli string長を指定する  
C. expectation-value estimateに要求するtarget precisionを表し、より小さい値は一般により多くのsampling resourceを必要とし得る  
D. circuit depthの上限を指定する

### Q10
Estimator V2のPUB resultで `data.evs` が典型的に表すものはどれか。

A. error vectors  
B. event bitstrings  
C. execution versions  
D. expectation values

---

# Answers & Explanations

### A1 — C
- A: sampled classical outputはSamplerの中心目的。
- B: routingはtranspilerの役割。
- C: 正解。Estimatorはcircuitとobservableを評価してexpectation valueを返す。
- D: OpenQASM parserではない。

### A2 — D
- A: local Sampler implementation。
- B: backend-based Sampler implementation。
- C: IBM Runtime側のclass名として使われるが、Qiskit SDKのlocal statevector reference classではない。
- D: 正解。`qiskit.primitives.StatevectorEstimator`。

### A3 — B
- A/C: 現行の標準import pathではない。
- B: 正解。`qiskit_ibm_runtime.EstimatorV2`を使う。
- D: SamplerでありEstimatorではない。

### A4 — A
- A: 正解。Estimator PUBはsingle circuitとobservablesを核にし、parameter valuesとprecisionを加えられる。
- B: Sampler PUBの形。
- C/D: V2 Estimator PUBではない。

### A5 — C
`|+>`はZ basisでは0/1が等確率で、Z固有値+1/-1の平均は0。
- A: `|+>`に対するXの期待値なら+1だが、ここはZ。
- B: `|1>`に対するZの期待値は-1だが、ここは`|+>`。
- C: 正解。
- D: `P(0)=1/2`と、固有値を重み付けした期待値を混同している。

### A6 — B
- A/C/D: current Runtime optionsと一致しない。
- B: 正解。2026-09時点では0, 1, 2。

### A7 — D
- A/B: 上書きのないlevel 0 presetはこれらのmitigationを有効にしない。
- C: shot count設定ではない。
- D: 正解。resilience mitigationを適用しないbaseline。

個別optionsはpresetを上書きできる。例えばlevel 0と`resilience.zne_mitigation=True`を組み合わせるとZNEを有効にできるため、数値levelだけから最終設定を断定しない。

### A8 — A
- A: 正解。上書きのないlevel 2 presetはlevel 1の測定mitigationにZNEやgate twirlingを加える。精度の改善量を保証する値ではない。
- B: transpiler optimization levelとは別概念。
- C/D: execution countやobservable数の指定ではない。

### A9 — C
- A/B/D: precisionの意味ではない。
- C: 正解。Estimatorが返すexpectation-value estimateのtarget precision。実装・optionsによって必要resourceとの関係は変わり得るのでcurrent docsを確認する。

### A10 — D
- A/B/C: `evs`の意味ではない。
- D: 正解。expectation valuesを保持する。

## Official references

- Estimator V2: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/estimator-v2
- Estimator options: https://quantum.cloud.ibm.com/docs/en/guides/estimator-options
- Estimator inputs/outputs: https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output
- Local SDK primitives: https://quantum.cloud.ibm.com/docs/en/guides/simulate-with-qiskit-sdk-primitives
- Presets and explicit overrides: https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management
