# Mock Exam 01 — Answers & Explanations

対応問題: `../../mock-exams/mock-01.md`

この解説は、正答だけでなく各distractorがなぜ不適切かを確認するためのものです。API依存事項は2026-09-10時点のIBM Quantum Documentationを基準にしています。2026-09-11の訂正・再検証範囲は`../../validation/revision-report-2026-09-11.md`を参照してください。

## Answer Key

1 C / 2 D / 3 C / 4 B / 5 D / 6 B / 7 C / 8 D / 9 D / 10 C  
11 C / 12 A / 13 D / 14 C / 15 B / 16 A / 17 D / 18 A / 19 A / 20 C  
21 B / 22 B / 23 A / 24 A / 25 D / 26 D / 27 D / 28 B / 29 B / 30 D  
31 C / 32 A / 33 B / 34 C / 35 A / 36 B / 37 D / 38 A / 39 A / 40 B  
41 C / 42 D / 43 C / 44 D / 45 B / 46 D / 47 B / 48 B / 49 C / 50 C  
51 C / 52 B / 53 A / 54 D / 55 D / 56 A / 57 A / 58 A / 59 D / 60 A  
61 C / 62 B / 63 C / 64 C / 65 B / 66 A / 67 B / 68 A

正答位置: **A=17 / B=17 / C=17 / D=17**。

---

## Detailed Explanations

### Q1 — C

**問題**

`H Z H` と等価なoperatorはどれか。

**解説**

Hadamard conjugationでXとZは交換されるため`HZH=X`。
- A: Yにはならない。
- B: Hで挟む前のoperatorのままではない。
- C: 正解。
- D: identityではない。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#matrix-order)

### Q2 — D

**問題**

`Rz(pi)` をglobal phaseも含む**厳密な行列等式**として表すとどれか。

**解説**

`Rz(theta)=exp(-i theta Z/2)`なので`Rz(pi)=diag(-i,i)=-iZ`。
- A: global phaseを無視したphysical actionとしてZ相当だが、設問は厳密な行列等式を要求する。
- B: phaseの符号が逆。
- C: `-Z`ではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#phase)

### Q3 — C

**問題**

global phaseを省略せず、**厳密な状態ベクトルとして** `Z|+>` と等しいものはどれか。

**解説**

`|+>=(|0>+|1>)/sqrt(2)`の`|1>`成分をZが反転し`|->`になる。
- A: `-|+>`は両成分を反転するglobal phaseでありZの作用ではない。
- B: Zはprojective measurementではない。
- C: 正解。
- D: Cと同じphysical stateを表すが、余分なglobal phaseが付いており、設問の要求する厳密なstatevector等式ではない。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#phase)

### Q4 — B

**問題**

`|+i>=(|0>+i|1>)/sqrt(2)` に `S†` を作用させた結果はどれか。

**解説**

`S†=diag(1,-i)`で、`i(-i)=1`。したがって`|+>`。
- A: `|-i>`にはならない。
- B: 正解。
- C: `|1>`成分の符号はマイナスにならない。
- D: `|0>`成分も残る。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#basic-gates)

### Q5 — D

**問題**

pure stateに対するglobal phaseについて正しいものはどれか。

**解説**

global phaseはstatevector全体への共通因子で、同じray/physical stateを表す。
- A: Born ruleの絶対値二乗では共通位相は消える。
- B: relative phaseは成分間の位相差であり別概念。
- C: Qiskit circuitはglobal phaseを保持できる。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#phase)

### Q6 — B

**問題**

computational basisでcontrol=`1`, target=`0` にCXを作用させた出力はどれか。

**解説**

CXはcontrol=1のときtargetを反転するので`10 -> 11`（ここではcontrol, targetの順で記載）。
- A: targetを反転していない。
- B: 正解。
- C/D: control/targetのbit patternと一致しない。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#multi-entanglement)

### Q7 — C

**問題**

Qiskitの2-qubit Pauli label `"XZ"` のqubit対応として正しいものはどれか。

**解説**

QiskitのPauli labelは右端がq0なので`XZ`ではZがq0、Xがq1。
- A: orderingが逆。
- B: tensor-product operatorを単一qubitへの逐次操作と誤解している。
- C: 正解。
- D: Pauli stringには明確なorderingがある。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#bit-pauli-order)

### Q8 — D

**問題**

`SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])` の意味として正しいものはどれか。

**解説**

`SparsePauliOp`はPauli stringsと係数からなる疎な線形結合を表す。
- A: measurement countsではない。
- B: circuit compositionではない。
- C: eigenvalueだけを保存するcontainerではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#bit-pauli-order)

### Q9 — D

**問題**

Pauli XとZの積について正しいものはどれか。

**解説**

Pauli XとZはanticommuteし、`XZ=-ZX`。
- A: commuteしない。
- B/C: operator productの等式として誤り。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#basic-gates)

### Q10 — C

**問題**

global phaseを省略せず、行列積として厳密な `Y|0>` はどれか。

**解説**

Pauli-Y行列から`Y|0>=i|1>`。
- A/B/D: physical rayとしてglobal phaseの違いを無視する文脈はあり得るが、設問は厳密な行列積を問う。
- C: 正解。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#basic-gates)

### Q11 — C

**問題**

`|++>` に対するobservable `XX` の期待値はどれか。

**解説**

`|+>`はXの+1 eigenstateなので、`|++>`は`X⊗X`のeigenvalue `(+1)(+1)=+1`。
- A/B: eigenstate propertyと一致しない。
- C: 正解。
- D: Pauli observableのeigenvalue範囲を超える。

[正本で深掘り](../../../manuscript/ja/01-quantum-operations.md#expectation)

### Q12 — A

**問題**

QuantumCircuitをMatplotlib形式で描画する代表的な呼び出しはどれか。

**解説**

`QuantumCircuit.draw("mpl")`はMatplotlib-based circuit drawerを選ぶ。
- A: 正解。
- B: sampled distributionのvisualization。
- C: circuit drawing APIではない。
- D: measurement命令を追加する。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#circuit-drawing)

### Q13 — D

**問題**

`counts = {"00": 500, "11": 524}` を測定分布として可視化する代表的な関数はどれか。

**解説**

countsの棒グラフには`plot_histogram`が代表的。
- A/B: quantum-state visualizationでありcounts用途とは異なる。
- C: circuit drawer。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#measurement-plots)

### Q14 — C

**問題**

Qiskitの通常の2-bit result string `"10"` では、もっとも右の文字はどのclassical bitに対応するか。

**解説**

Qiskitの通常のbitstring表記ではbit 0が右端。
- A: orderingが逆。
- B: classical bitとphysical qubit mappingを混同している。
- C: 正解。
- D: Qiskitの表示規約は定義されている。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#bitstrings-counts)

### Q15 — B

**問題**

`plot_state_qsphere` の表現について正しいものはどれか。

**解説**

Q-sphereはbasis componentの大きさ/確率とphaseを視覚化できる。
- A: circuit metricsのplotではない。
- B: 正解。
- C: coupling map visualizationではない。
- D: statevector由来のphase情報も扱える。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#state-plots)

### Q16 — A

**問題**

複数量子ビットのstateをqubitごとのBloch sphereとして表示する代表的な関数はどれか。

**解説**

`plot_bloch_multivector`はstateをqubitごとのBloch sphereとして描く代表的関数。
- A: 正解。
- B/D: sampled distributions用。
- C: circuit drawing用。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#state-plots)

### Q17 — D

**問題**

Bell state `(|00>+|11>)/sqrt(2)` をcomputational basisで測定した理想分布はどれか。

**解説**

Bell stateの非零amplitudeは00と11だけで各`1/sqrt(2)`。
- A/B/C: statevectorの非零成分と一致しない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#measurement-basis)

### Q18 — A

**問題**

測定を含まない `qc` を初期`|0...0>`へ作用させたstatevectorを直接得る方法はどれか。

**解説**

`Statevector.from_instruction(qc)`は測定のないcircuitを初期stateへ作用させたstatevectorを構成できる。
- A: 正解。
- B: visualizationだけ。
- C: countsが必要なplot用途。
- D: `transpile`の戻り値に`result()`を呼ぶものではない。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#statevector)

### Q19 — A

**問題**

`|->=(|0>-|1>)/sqrt(2)` にHを作用させ、その後computational basisで測定すると理想的にはどうなるか。

**解説**

`H|->=|1>`なのでcomputational basis measurementは1が確定する。
- A: 正解。
- B/C: H transformの結果と不一致。
- D: measurement bitは0/1。

[正本で深掘り](../../../manuscript/ja/02-visualization-measurement.md#measurement-basis)

### Q20 — C

**問題**

2 quantum bitsと2 classical bitsを持つcircuitを作る正しいコードはどれか。

**解説**

`QuantumCircuit(2,2)`は2 qubitsと2 clbitsを作る。
- A: 4 qubitsのみ。
- B: 0 qubits + 4 clbits。
- C: 正解。
- D: 有効なconstructor指定ではない。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#construct-registers)

### Q21 — B

**問題**

q0のmeasurement resultをc1へ保存する呼び出しはどれか。

**解説**

`measure(qubit, clbit)`の順なのでq0→c1は`qc.measure(0,1)`。
- A: q1→c0。
- B: 正解。
- C: `measure_all`は個別mapping指定ではない。
- D: 対応するstandard APIではない。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#measure-mapping)

### Q22 — B

**問題**

`new_qc = qc.compose(other)` のdefault behaviorについて正しいものはどれか。

**解説**

`compose`のdefaultは`inplace=False`で、新しいcircuitを返す。
- A: `inplace=True`の場合の説明。
- B: 正解。
- C: measurementだけを合成するAPIではない。
- D: current Qiskit v2.xで利用できる。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#compose-control)

### Q23 — A

**問題**

symbolic rotation angleを作る代表的なclassはどれか。

**解説**

`qiskit.circuit.Parameter`がsymbolic parameterを作る。
- A: 正解。
- B: transpiler target表現。
- C: execution primitive。
- D: classical bits container。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#parameters)

### Q24 — A

**問題**

parameterized circuitへ事前に数値を代入する代表的なAPIはどれか。

**解説**

`assign_parameters`でParameterを数値や別Parameterへ置換できる。
- A: 正解。
- B/C/D: current standard APIではない。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#parameters)

### Q25 — D

**問題**

X gateからcontrolled-X相当のgateを構成する方法として適切なのはどれか。

**解説**

`Gate.control()`でcontrolled versionを構成できる。例えば`XGate().control()`でcontrolled-Xを得る。基底`Instruction`にはこのmethodはなく、測定等を含む任意のInstructionへ一般化しない。
- A/B/C: controlled-Xを生成する方法ではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#compose-control)

### Q26 — D

**問題**

次のようなclassical feedforwardをQiskit circuitへ追加する現在の代表的構文はどれか。

**解説**

current control-flow builderでは`with qc.if_test((c0, 1)):`のようにclassical conditionを表せる。
- A: Pythonのruntime `if`でquantum measurementを直接評価する構文ではない。
- B/C: current recommended control-flow builder APIではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#dynamic-circuits)

### Q27 — D

**問題**

「dynamic circuit」の説明として最も適切なのはどれか。

**解説**

dynamic circuitはmid-circuit measurementとclassical feedforward/control flowなどを含み得る。
- A: parameter sweepだけではdynamic circuitとは限らない。
- B: transpiler variabilityの名称ではない。
- C: shots変更だけではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#dynamic-circuits)

### Q28 — B

**問題**

Qiskit SDKのcontrol-flow supportと実QPU executionについて正しいものはどれか。

**解説**

SDKが表現できるcontrol flowとhardware/serviceが実行できるfeature setは区別する。
- A: 全QPUで全constructが実行可能とは限らない。
- B: 正解。
- C: SDKはmid-circuit measurementを表現できる。
- D: IBM hardwareにはclassical feedforward supportがあるが制約を確認する。

[正本で深掘り](../../../manuscript/ja/03-circuit-construction.md#sdk-hardware-boundary)

### Q29 — B

**問題**

backend向けのstandard staged transpilation pipelineを作る代表的な方法はどれか。

**解説**

`generate_preset_pass_manager(..., backend=backend)`がstandard staged transpilation pipelineを生成する代表的方法。
- A/C/D: pass manager生成APIではない。
- B: 正解。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#transpile-preset)

### Q30 — D

**問題**

preset pass managerの`optimization_level`について正しい説明はどれか。

**解説**

preset optimization levelは0–3。高いlevelは一般により積極的なoptimizationを試みるが、特定のdepth削減を保証しない。
- A: level範囲が不足。
- B: optimization outcomeは保証されない。
- C: shots設定ではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#transpile-preset)

### Q31 — C

**問題**

IBM Quantum ComputeのRuntime primitiveへQPU用circuitを送る際の重要な境界はどれか。

**解説**

QPU Runtime workflowではtarget backendのISA/layoutに適合するcircuitを準備する。
- A: QASM2 conversionは必須要件ではない。
- B: Samplerではclassical outputsのためmeasurementが必要。
- C: 正解。
- D: abstract circuitをtarget-independentにそのまま送れるという理解は誤り。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#isa-layout)

### Q32 — A

**問題**

IBM Quantum Compute Serviceの3つのexecution modesはどれか。

**解説**

IBM Quantum Computeのexecution modesはJob, Session, Batch。
- A: 正解。
- B/C/D: official execution-mode namesではない。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#execution-modes)

### Q33 — B

**問題**

Session modeが最も適する代表的なworkloadはどれか。

**解説**

Sessionはquantum/classical間でresult-dependent iterationを行うmulti-job workloadに向く。
- A: independent jobsならBatchが自然。
- B: 正解。
- C/D: Runtime scheduling modeを必要としない。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#execution-modes)

### Q34 — C

**問題**

Batch modeの代表的な用途として最も適切なのはどれか。

**解説**

Batchは互いにconditional dependencyのない複数jobsをまとめるworkload向け。
- A: iterative dependencyはSession寄り。
- B: single-job専用modeではない。
- C: 正解。
- D: circuit内control flowとjob schedulingを混同している。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#execution-modes)

### Q35 — A

**問題**

Job modeでRuntime Samplerを使う代表的な初期化はどれか。

**解説**

Job modeではprimitiveを`mode=backend`で作る代表的workflowがある。
- A: 正解。
- B: local reference primitiveにQPU modeを付けるAPIではない。
- C/D: valid mode objectではない。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#execution-modes)

### Q36 — B

**問題**

利用可能なQPUから比較的空いているbackendを選ぶ代表的なservice APIはどれか。

**解説**

`QiskitRuntimeService().least_busy(...)`は条件に合う比較的空いているbackendを選ぶ代表API。
- A/C/D: current service backend-selection APIではない。
- B: 正解。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#backend-selection)

### Q37 — D

**問題**

IBM Quantum Compute ServiceのV2 Samplerをimportする現在の代表的な形はどれか。

**解説**

IBM Runtime implementationは`qiskit_ibm_runtime.SamplerV2`。
- A/B: current import pathではない。
- C: V1-style generic Samplerを指し、IBM Runtime V2 classではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#runtime-local)

### Q38 — A

**問題**

Estimator V2のPUBとして正しい一般形はどれか。

**解説**

Estimator PUBはcircuit + observablesを核に、parameter valuesとprecisionを追加できる。
- A: 正解。
- B: Sampler PUBの形。
- C/D: Estimator PUBではない。

位置引数の順序は変わらない。未parameter化回路でprecisionだけを指定する例は`(qc, observable, None, 0.01)`であり、`None`の位置を省いて値を前へ詰めない。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#pub-job)

### Q39 — A

**問題**

Estimator V2でobservablesとparameter valuesをarrayとして渡す場合のbroadcastingについて正しいものはどれか。

**解説**

Estimator V2はobservable arraysとparameter arraysにNumPy-style broadcastingを使う。
- A: 正解。
- B: exact同長listだけに限定されない。
- C: Estimator V2の重要な機能。
- D: broadcast shapeに応じてarray resultを返し得る。

parameter values配列の最後の軸は回路parameterの軸で、broadcastingのshapeから除かれる。例えばparameterが1個ならvalues shape `(3,1)`のbinding shapeは`(3,)`。observables shape `(2,1)`と組み合わせると結果shapeは`(2,3)`になる。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-broadcasting)

### Q40 — B

**問題**

`job = estimator.run(pubs)` の戻り値について正しいものはどれか。

**解説**

Runtime V2 `run()`はsubmitted job objectを返し、`job.result()`でPrimitiveResultを得る。
- A: direct scalar returnではない。
- B: 正解。
- C/D: runのreturn typeではない。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#pub-job)

### Q41 — C

**問題**

local `StatevectorEstimator` とRuntime `EstimatorV2` の違いとして最も適切なのはどれか。

**解説**

local statevector reference implementationはQPU target/schedulingを必要としないが、Runtime QPU executionではISAとexecution modeを考慮する。
- A: local implementationはIBM QPU必須ではない。
- B: Estimatorはobservableを受け取る。
- C: 正解。
- D: execution environmentは異なる。

[正本で深掘り](../../../manuscript/ja/04-transpile-execution.md#runtime-local)

### Q42 — D

**問題**

Sampler V2の中心的な出力はどれか。

**解説**

Samplerの目的はclassical output dataをsampleすること。
- A/C: exact spectral analysisではない。
- B: transpilerではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-purpose)

### Q43 — C

**問題**

Qiskit SDKのlocal statevector-based V2 Sampler reference implementationはどれか。

**解説**

`qiskit.primitives.StatevectorSampler`がlocal statevector-based V2 reference implementation。
- A/B: Estimator側。
- C: 正解。
- D: service access class。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-purpose)

### Q44 — D

**問題**

IBM Quantum Compute ServiceでQPU等へSampler workloadを送るclassはどれか。

**解説**

IBM Quantum Compute用は`qiskit_ibm_runtime.SamplerV2`。
- A/B: current APIではない。
- C: local statevector reference implementation。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-purpose)

### Q45 — B

**問題**

Sampler V2 PUBの一般形として最も適切なのはどれか。

**解説**

Sampler PUBはcircuitとoptional parameter values/shots。
- A: Estimator PUBに近い。
- B: 正解。
- C/D: valid Sampler PUB structureではない。

parameter valuesを省略してPUBのshotsを指定する例は`(qc, None, 128)`。`(qc, 128)`では2番目の要素がshotsになるわけではない。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-pub)

### Q46 — D

**問題**

`sampler.options.default_shots = 500` の後、PUB-specific shotsを指定していないcircuitを今回だけ128 shotsでrunしたい。最も直接的なのはどれか。

**解説**

`SamplerV2.run(pubs, shots=128)`のrun-level shotsは、PUB-specific shotsがないPUBについてcurrent runの`default_shots`をoverrideする。
- A: Estimator-side precision概念。
- B: Sampler `run()`のinterfaceは`shots`。
- C: Sampler shots設定ではない。
- D: 正解。PUB-specific shotsがあればそちらがさらに優先される。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-pub)

### Q47 — B

**問題**

Runtime Samplerのdynamical decouplingを有効にするcurrent option pathに最も近いものはどれか。

**解説**

current Sampler optionsでは`dynamical_decoupling.enable=True`。
- A: Estimator resilience設定との混同。
- B: 正解。
- C/D: current option pathではない。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-options)

### Q48 — B

**問題**

dynamical decouplingの主目的として最も適切なのはどれか。

**解説**

dynamical decouplingはidle periodsへpulse sequencesを挿入し、decoherence等の影響を抑える方向で使う。
- A: result conversionではない。
- B: 正解。
- C: serializationとは無関係。
- D: hardware connectivityは変わらない。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-options)

### Q49 — C

**問題**

2026-09時点のIBM documentationにおけるdynamic circuitsとdynamical decouplingのcompatibilityとして正しいものはどれか。

**解説**

2026-09時点のIBM feature compatibilityではdynamic circuitsとdynamical decouplingはincompatibleとして扱われる。
- A/B: current documentationと一致しない。
- C: 正解。version-sensitiveなので直前に再確認する。
- D: DDはSampler optionsで設定できる。

[正本で深掘り](../../../manuscript/ja/05-sampler.md#sampler-compatibility)

### Q50 — C

**問題**

Estimator V2の中心的な目的はどれか。

**解説**

Estimatorはobservable expectation valuesを評価するprimitive。
- A: Samplerの役割。
- B/D: Estimatorの役割ではない。
- C: 正解。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-purpose)

### Q51 — C

**問題**

Qiskit SDKのlocal statevector-based V2 Estimator reference implementationはどれか。

**解説**

local reference implementationは`qiskit.primitives.StatevectorEstimator`。
- A/B/D: Estimatorのlocal statevector reference classではない。
- C: 正解。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-purpose)

### Q52 — B

**問題**

IBM Quantum Compute Serviceで使うRuntime Estimator implementationはどれか。

**解説**

IBM Quantum Compute用Runtime classは`qiskit_ibm_runtime.EstimatorV2`。
- A/C: current import path/APIではない。
- B: 正解。
- D: Sampler implementation。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-purpose)

### Q53 — A

**問題**

Estimator PUBの核となる入力はどれか。

**解説**

Estimator PUBはcircuitとobservable(s)を核にする。
- A: 正解。
- B: Sampler/result conceptsとの混同。
- C/D: primitive scientific inputではない。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-pub)

### Q54 — D

**問題**

`|+>` に対するPauli-Zの期待値はどれか。

**解説**

`|+>`をZ basisで見れば+1/-1が等重みなので`<Z>=0`。
- A: `<X>`なら+1。
- B: `|1>`の`<Z>`に対応。
- C: eigenvalue-weighted averageとして不適切。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-purpose)

### Q55 — D

**問題**

2026-09時点でRuntime Estimatorの`resilience_level`として用意されているlevelはどれか。

**解説**

2026-09時点のRuntime Estimator resilience levelsは0,1,2。
- A/B/C: current official optionsと一致しない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-options)

### Q56 — A

**問題**

個別のresilience optionsで上書きしない場合、`resilience_level=0` のpresetについて正しいものはどれか。

**解説**

個別optionsによる上書きがない場合、`resilience_level=0`はEstimatorのresilience mitigationを適用しないbaseline。
- A: 正解。
- B/C: 上書きのないlevel 0 presetでは有効にしない。
- D: shotsの値ではない。

個別optionsはpresetを上書きできる。level 0でも`resilience.zne_mitigation=True`を設定すればZNEを有効にできるため、levelだけで最終設定を断定しない。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-options)

### Q57 — A

**問題**

Estimator V2のPUB resultで`data.evs`が表すものはどれか。

**解説**

`data.evs`はestimated expectation values。
- A: 正解。
- B: sampled bitsはSampler result側。
- C/D: field名の意味ではない。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-result)

### Q58 — A

**問題**

既知のRuntime job ID `job_id` からjob objectを取得する代表的なAPIはどれか。

**解説**

過去job IDからは`QiskitRuntimeService.job(job_id)`でjob objectを取得できる。
- A: 正解。
- B/C/D: current representative retrieval APIではない。

[正本で深掘り](../../../manuscript/ja/07-results-analysis.md#job-lifecycle)

### Q59 — D

**問題**

条件を指定しながら複数の過去Runtime jobsを一覧取得する代表的なAPIはどれか。

**解説**

`QiskitRuntimeService.jobs(...)`は過去jobsをlist/filterするAPI。
- A: single job result取得とは異なる。
- B/C: jobs retrieval APIではない。
- D: 正解。

[正本で深掘り](../../../manuscript/ja/07-results-analysis.md#job-lifecycle)

### Q60 — A

**問題**

Runtime jobの現在のstatusを確認する代表的なmethodはどれか。

**解説**

`job.status()`がRuntime jobの現在状態を取得する代表method。
- A: 正解。
- B/C/D: job lifecycle status methodではない。

[正本で深掘り](../../../manuscript/ja/07-results-analysis.md#job-lifecycle)

### Q61 — C

**問題**

Sampler resultの`pub_result.data.meas`が`BitArray`であるとき、outcome count辞書を得る代表的なmethodはどれか。

**解説**

Sampler resultの`BitArray.get_counts()`でoutcome countsを得られる。
- A: `BitArray.expectation_values(observables)`は実在し、対角observableの期待値を求めるAPIである。ただしcounts辞書を返すAPIではなく、この選択肢の呼び出しには必須の`observables`引数もない。
- B: sampled dataからexact probabilitiesを返すmethodではない。
- C: 正解。
- D: observableを返すものではない。

[正本で深掘り](../../../manuscript/ja/07-results-analysis.md#bitarray-counts)

### Q62 — B

**問題**

Estimator resultの`data.stds`について最も適切なのはどれか。

**解説**

Estimator `data.stds`は`evs`に対応するstandard deviation/uncertainty情報を持つ。error-mitigation settingsにより追加fieldsもあり得る。
- A: bitstringsではない。
- B: 正解。
- C/D: result uncertainty fieldではない。

[正本で深掘り](../../../manuscript/ja/06-estimator.md#estimator-result)

### Q63 — C

**問題**

1000 shotsのcountsが `{'0': 760, '1': 240}` のとき、経験的な `P(1)` はどれか。

**解説**

経験確率は`240/1000=0.24`。
- A: P(0)に相当する。
- B/D: countsから導かれない。
- C: 正解。

[正本で深掘り](../../../manuscript/ja/07-results-analysis.md#empirical-analysis)

### Q64 — C

**問題**

Primitive resultのmetadataについて正しい説明はどれか。

**解説**

Primitive result metadataにはshots、target precision、resilience/execution関連情報等が含まれ得る。
- A: metadataはquantum stateそのものではない。
- B: 常に空ではない。
- C: 正解。
- D: metadata readingはjob resubmissionではない。

[正本で深掘り](../../../manuscript/ja/07-results-analysis.md#metadata)

### Q65 — B

**問題**

OpenQASM 3で2 quantum bitsと2 classical bitsを宣言する正しい組み合わせはどれか。

**解説**

OpenQASM 3では`qubit[2] q;`と`bit[2] c;`。
- A/C/D: OpenQASM 3のdeclaration syntaxではない。
- B: 正解。

[正本で深掘り](../../../manuscript/ja/08-openqasm3.md#qasm-types)

### Q66 — A

**問題**

次のOpenQASM 3 programの意味として正しいものはどれか。

```qasm
OPENQASM 3.0;
include "stdgates.inc";
bit c;
qubit q;
h q;
c = measure q;
```

**解説**

version declarationと`stdgates.inc`を読み、qへHを作用させ、measurement resultをcへ格納する。
- A: 正解。ここでは初期状態やH後の特定の状態ベクトルを断定していない。
- B: cはclassical bitでqubitへ変換しない。
- C: measurementを明示的に実行している。
- D: gate definitionをcへ保存するコードではない。

[正本で深掘り](../../../manuscript/ja/08-openqasm3.md#qasm-semantics)

### Q67 — B

**問題**

QiskitのOpenQASM 3 import/exportについて正しいものはどれか。

**解説**

`dumps`はOpenQASM 3 string export、`loads`はprogram string import。current importには`qiskit-qasm3-import` optional packageが必要。
- A: import/export方向が逆。
- B: 正解。
- C: `qiskit.qasm3`はOpenQASM 3用。
- D: circuit serialization/import APIでありSampler result専用ではない。

[正本で深掘り](../../../manuscript/ja/08-openqasm3.md#qasm-qiskit-interop)

### Q68 — A

**問題**

OpenQASM 3とIBM Quantum Compute Serviceについて最も適切な説明はどれか。

**解説**

language/specification、Qiskit parse/representation、IBM QPU executable supportは別レイヤー。IBM Quantum Compute REST APIでもprimitive workloadsをJob/Session/Batchで扱える。
- A: 正解。
- B: specification featureが全てhardware executableとは限らない。
- C: RESTでも3 execution modesがある。
- D: REST APIでもEstimator/Sampler primitive workloadという構造を使う。

[正本で深掘り](../../../manuscript/ja/08-openqasm3.md#qasm-support-boundary)

---

## Review by Domain

- Q1–Q11: Performing quantum operations — 11 questions
- Q12–Q19: Visualization / measurements / states — 8 questions
- Q20–Q31: Creating quantum circuits — 12 questions
- Q32–Q41: Running quantum circuits — 10 questions
- Q42–Q49: Sampler — 8 questions
- Q50–Q57: Estimator — 8 questions
- Q58–Q64: Results / jobs — 7 questions
- Q65–Q68: OpenQASM — 4 questions

## Official references

- Certification: https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- Qiskit documentation: https://quantum.cloud.ibm.com/docs/
- Bit ordering: https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering
- Dynamic circuits: https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- Primitive I/O: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Sampler options: https://quantum.cloud.ibm.com/docs/en/guides/sampler-options
- Estimator options: https://quantum.cloud.ibm.com/docs/en/guides/estimator-options
- Runtime service API: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service
- OpenQASM 3 interop: https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3
- REST execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api
- Gate control: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Gate
- BitArray methods: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray
- Resilience presets and overrides: https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management
