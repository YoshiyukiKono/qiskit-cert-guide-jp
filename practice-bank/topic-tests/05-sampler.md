# Topic Test 05 — Sampler Primitive

全10問。local V2 reference implementationとIBM Quantum Compute `SamplerV2` を区別して扱います。

## Questions

### Q1
Sampler V2の中心的な役割はどれか。

A. observableの期待値だけを返す  
B. circuitのclassical output registerからbitstring samplesを得る  
C. Hamiltonianを厳密対角化する  
D. transpiler passを生成する

### Q2
Qiskit SDKのローカルV2 reference Samplerはどれか。

A. `BackendEstimatorV2`  
B. `EstimatorV2`  
C. `StatevectorSampler`  
D. `QiskitRuntimeService`

### Q3
IBM Quantum Compute Serviceで使うSampler implementationはどれか。

A. `qiskit_ibm_runtime.SamplerV2`  
B. `qiskit.primitives.StatevectorEstimator`  
C. `qiskit.quantum_info.Sampler`  
D. `QuantumCircuit.sampler()`

### Q4
Sampler PUBの一般的なtuple構造として最も適切なのはどれか。

A. `(circuit, observable, precision)`  
B. `(counts, shots)`  
C. `(backend, circuit, observable)`  
D. `(circuit, optional parameter_values, optional shots)`

### Q5
`StatevectorSampler` とmid-circuit measurementについて正しいものはどれか。

A. local `StatevectorSampler` は一般のmid-circuit measurementをサポートしない。Runtime側のdynamic-circuit supportとは分けて考える  
B. Sampler V2という名前なら全implementationが同じdynamic-circuit機能を持つ  
C. `StatevectorSampler`ではterminal measurementも禁止  
D. measurementがあると自動的に`StatevectorEstimator`へ切り替わる

### Q6
IBM Quantum Compute `SamplerV2` のshotsを既定値として設定するoptionとして最も直接的なのはどれか。

A. `resilience_level`  
B. `default_shots`  
C. `default_precision`  
D. `optimization_level`

### Q7
Sampler optionsのdynamical decouplingを有効化する現在の形に最も近いものはどれか。

A. `sampler.options.resilience_level = 2`  
B. `sampler.options.shots.dynamic = True`  
C. `sampler.options.dynamical_decoupling.enable = True`  
D. `sampler.dynamic_circuit = "DD"`

### Q8
dynamical decouplingの目的として最も適切なのはどれか。

A. idle periodにpulse sequenceを挿入し、decoherence等の影響を抑える方向で使う  
B. shotsを必ず1に減らす  
C. classical registerをobservableへ変換する  
D. OpenQASM parserを高速化する

### Q9
2026-09時点のIBM Quantum documentationで、dynamic circuitsとdynamical decouplingのfeature compatibilityについて正しいものはどれか。

A. 常に併用必須  
B. dynamic circuitsではDDが自動でONになる  
C. feature compatibilityはSamplerと無関係  
D. 現行documentationでは互いにincompatibleとして記載されている

### Q10
Sampler resultで `pub_result.data.meas` のようなfieldを得た場合、その典型的な意味はどれか。

A. Estimatorのexpectation-value array  
B. `meas`というclassical output registerに対応する`BitArray`等のresult data  
C. backendのcoupling map  
D. circuitのglobal phase

---

# Answers & Explanations

### A1 — B
- A: expectation valuesはEstimatorの中心目的。
- B: 正解。Samplerは測定されたclassical outputsをsampleする。
- C/D: primitiveの役割ではない。

### A2 — C
- A: Estimator implementation。
- B: IBM Runtime Estimator側の名称。
- C: 正解。`qiskit.primitives.StatevectorSampler`はlocal reference V2 implementation。
- D: IBM Quantum service access class。

### A3 — A
- A: 正解。IBM Quantum Compute用V2 Sampler。
- B: local Estimator。
- C/D: 現行APIではない。

### A4 — D
- A: Estimator PUBに近い。
- B/C: Sampler V2 PUBの構造ではない。
- D: 正解。Sampler PUBはsingle circuitとoptional parameter values/shots。

### A5 — A
- A: 正解。implementation-specific constraintを明示している。
- B: V2 interfaceと実装能力を混同している。
- C: terminal measurementはSamplerのclassical outputに必要。
- D: primitiveが自動切替されることはない。

### A6 — B
- A: Estimatorのnoise mitigation設定。
- B: 正解。SamplerOptionsの`default_shots`。
- C: Estimator側のprecision概念。
- D: transpiler設定で、Sampler execution shotsではない。

### A7 — C
- A: SamplerにEstimator resilience levelを設定する問題ではない。
- B/D: 現行option pathではない。
- C: 正解。

### A8 — A
- A: 正解。idle qubitへのsequenceでnoise suppressionを狙う。
- B/C/D: DDの目的ではない。

### A9 — D
- A/B/C: current feature tableと一致しない。
- D: 正解。これはversion-sensitiveなので試験直前にcurrent docsを再確認する。

### A10 — B
- A: `evs`はEstimator result側。
- B: 正解。V2 Sampler resultはclassical register名に対応するdataを持ち、BitArrayからbitstrings/countsを取得できる。
- C/D: result classical dataの意味ではない。

## Official references

- Primitives: https://quantum.cloud.ibm.com/docs/en/guides/primitives
- Sampler quickstart: https://quantum.cloud.ibm.com/docs/en/guides/get-started-with-sampler
- Sampler options: https://quantum.cloud.ibm.com/docs/en/guides/sampler-options
- Local SDK primitives: https://quantum.cloud.ibm.com/docs/en/guides/simulate-with-qiskit-sdk-primitives
