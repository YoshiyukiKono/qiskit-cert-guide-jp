# Mock Exam 01 — Qiskit v2.X Developer Associate

**68 questions / 90 minutes**

- 各問1つ選択してください。
- 資料を見ずに解くことを推奨します。
- 分からない問題は印を付けて先へ進んでください。
- 解答は `../answers/mock-exams/mock-01-answers.md` に分離しています。
- 本模試は公開Exam Objectivesを基にしたオリジナル問題であり、IBM実試験問題の再現ではありません。

Domain allocation: 11 / 8 / 12 / 10 / 8 / 8 / 7 / 4 = 68 questions.

各問のHTMLコメントは教材側のprimary domain割当です。validatorは割当の整合性を確認しますが、内容の妥当性は独立レビューで確認してください。

---

## Q1
<!-- domain: 1 -->
`H Z H` と等価なoperatorはどれか。

A. Y  
B. Z  
C. X  
D. I

## Q2
<!-- domain: 1 -->
`Rz(pi)` をglobal phaseも含む**厳密な行列等式**として表すとどれか。

A. `Z`  
B. `iZ`  
C. `-Z`  
D. `-iZ`

## Q3
<!-- domain: 1 -->
global phaseを省略せず、**厳密な状態ベクトルとして** `Z|+>` と等しいものはどれか。

A. `-|+>`  
B. `|0>`  
C. `|->`  
D. `i|->`

## Q4
<!-- domain: 1 -->
`|+i>=(|0>+i|1>)/sqrt(2)` に `S†` を作用させた結果はどれか。

A. `|-i>`  
B. `|+>`  
C. `|->`  
D. `|1>`

## Q5
<!-- domain: 1 -->
pure stateに対するglobal phaseについて正しいものはどれか。

A. computational-basis probabilityだけを変える  
B. relative phaseと同じ情報を表す  
C. Qiskitのcircuitでは表現できない  
D. 状態全体に同じ`e^{iφ}`を掛けても同じphysical stateを表す

## Q6
<!-- domain: 1 -->
computational basisでcontrol=`1`, target=`0` にCXを作用させた出力はどれか。

A. `10`  
B. `11`  
C. `01`  
D. `00`

## Q7
<!-- domain: 1 -->
Qiskitの2-qubit Pauli label `"XZ"` のqubit対応として正しいものはどれか。

A. Xがq0、Zがq1  
B. XとZを両方q0へ順番に適用する  
C. Zがq0、Xがq1  
D. Pauli labelにはqubit orderingがない

## Q8
<!-- domain: 1 -->
`SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])` の意味として正しいものはどれか。

A. 2つのcountsを結合する  
B. 2つのQuantumCircuitをcomposeする  
C. ZとXのeigenvalueだけを保存する  
D. Pauli stringsの線形結合 `0.5 ZI - XX` を表す

## Q9
<!-- domain: 1 -->
Pauli XとZの積について正しいものはどれか。

A. `XZ=ZX`  
B. `XZ=I`  
C. `XZ=Z`  
D. `XZ=-ZX`

## Q10
<!-- domain: 1 -->
global phaseを省略せず、行列積として厳密な `Y|0>` はどれか。

A. `|1>`  
B. `-i|1>`  
C. `i|1>`  
D. `-|1>`

## Q11
<!-- domain: 1 -->
`|++>` に対するobservable `XX` の期待値はどれか。

A. -1  
B. 0  
C. +1  
D. 2

## Q12
<!-- domain: 2 -->
QuantumCircuitをMatplotlib形式で描画する代表的な呼び出しはどれか。

A. `qc.draw("mpl")`  
B. `plot_histogram(qc)`  
C. `Statevector(qc)`  
D. `qc.measure_all()`

## Q13
<!-- domain: 2 -->
`counts = {"00": 500, "11": 524}` を測定分布として可視化する代表的な関数はどれか。

A. `plot_state_city(counts)`  
B. `plot_bloch_multivector(counts)`  
C. `circuit_drawer(counts)`  
D. `plot_histogram(counts)`

## Q14
<!-- domain: 2 -->
Qiskitの通常の2-bit result string `"10"` では、もっとも右の文字はどのclassical bitに対応するか。

A. bit 1  
B. physical qubit 0に必ず固定  
C. bit 0  
D. backendごとに未定義

## Q15
<!-- domain: 2 -->
`plot_state_qsphere` の表現について正しいものはどれか。

A. circuit depthとgate countだけを描く  
B. basis componentのprobabilityとphaseを視覚化できる  
C. backend coupling map専用である  
D. sampled countsだけを表示しstate informationは扱わない

## Q16
<!-- domain: 2 -->
複数量子ビットのstateをqubitごとのBloch sphereとして表示する代表的な関数はどれか。

A. `plot_bloch_multivector`  
B. `plot_histogram`  
C. `circuit_drawer`  
D. `plot_distribution`

## Q17
<!-- domain: 2 -->
Bell state `(|00>+|11>)/sqrt(2)` をcomputational basisで測定した理想分布はどれか。

A. 01と10が約50%ずつ  
B. 4通りが約25%ずつ  
C. 常に00  
D. 00と11が約50%ずつ

## Q18
<!-- domain: 2 -->
測定を含まない `qc` を初期`|0...0>`へ作用させたstatevectorを直接得る方法はどれか。

A. `Statevector.from_instruction(qc)`  
B. `qc.draw()`  
C. `plot_histogram(qc)`  
D. `transpile(qc).result()`

## Q19
<!-- domain: 2 -->
`|->=(|0>-|1>)/sqrt(2)` にHを作用させ、その後computational basisで測定すると理想的にはどうなるか。

A. 1が確定  
B. 0が確定  
C. 0/1が50%ずつ  
D. `-1`というbitが出る

## Q20
<!-- domain: 3 -->
2 quantum bitsと2 classical bitsを持つcircuitを作る正しいコードはどれか。

A. `QuantumCircuit(4)`  
B. `QuantumCircuit(0, 4)`  
C. `QuantumCircuit(2, 2)`  
D. `QuantumCircuit("2,2")`

## Q21
<!-- domain: 3 -->
q0のmeasurement resultをc1へ保存する呼び出しはどれか。

A. `qc.measure(1, 0)`  
B. `qc.measure(0, 1)`  
C. `qc.measure_all(0, 1)`  
D. `qc.read(0, 1)`

## Q22
<!-- domain: 3 -->
`new_qc = qc.compose(other)` のdefault behaviorについて正しいものはどれか。

A. `qc`をin-place変更し戻り値は`None`  
B. 合成した新しいcircuitを返し、defaultでは`qc`自体を変更しない  
C. `other`のmeasurementだけを`qc`へ移す  
D. Qiskit v2.xでは`compose`はdeprecatedで使用できない

## Q23
<!-- domain: 3 -->
symbolic rotation angleを作る代表的なclassはどれか。

A. `Parameter`  
B. `Target`  
C. `SamplerV2`  
D. `ClassicalRegister`

## Q24
<!-- domain: 3 -->
parameterized circuitへ事前に数値を代入する代表的なAPIはどれか。

A. `assign_parameters(...)`  
B. `bind_runtime(...)`  
C. `measure_parameters(...)`  
D. `draw_parameters(...)`

## Q25
<!-- domain: 3 -->
X gateからcontrolled-X相当のgateを構成する方法として適切なのはどれか。

A. X gateをclassical registerへ変換する  
B. X gateへ`measure()`を追加する  
C. X gateを`reverse_bits()`する  
D. gateの`control()`を使う

## Q26
<!-- domain: 3 -->
次のようなclassical feedforwardをQiskit circuitへ追加する現在の代表的構文はどれか。

A. `if qc.measure(0): qc.x(1)`  
B. `qc.classical_if(0, qc.x(1))`  
C. `qc.x(1).condition = 1`  
D. `with qc.if_test((c0, 1)): qc.x(q1)`

## Q27
<!-- domain: 3 -->
「dynamic circuit」の説明として最も適切なのはどれか。

A. parameterをPython loopで変更するだけのcircuit  
B. transpilationのたびにgate orderが変わるcircuit  
C. shots数をrunごとに変更するcircuit  
D. mid-circuit measurementとclassical resultに基づくcontrol flow等を含み得るcircuit

## Q28
<!-- domain: 3 -->
Qiskit SDKのcontrol-flow supportと実QPU executionについて正しいものはどれか。

A. SDKで表現できるcontrol flowはすべてのQPUで必ず実行できる  
B. SDKは`if_test`, `switch`, loops等を表現できるが、実QPUで利用できるfeatureはcurrent backend/service supportを別に確認する  
C. Qiskit SDKはmid-circuit measurementを表現できない  
D. QPUではclassical feedforwardという概念自体が存在しない

## Q29
<!-- domain: 3 -->
backend向けのstandard staged transpilation pipelineを作る代表的な方法はどれか。

A. `Statevector.from_instruction(backend)`  
B. `generate_preset_pass_manager(optimization_level=..., backend=backend)`  
C. `SamplerV2(optimization_level=...)`  
D. `QuantumCircuit.compile(backend)`

## Q30
<!-- domain: 3 -->
preset pass managerの`optimization_level`について正しい説明はどれか。

A. 0と1しか指定できない  
B. levelが高いほど必ずcircuit depthが厳密に小さくなる  
C. shotsのoptimization levelを意味する  
D. 0–3のlevelがあり、高いlevelは一般により積極的なoptimizationを試みるが特定の改善を保証しない

## Q31
<!-- domain: 3 -->
IBM Quantum ComputeのRuntime primitiveへQPU用circuitを送る際の重要な境界はどれか。

A. circuitを必ずOpenQASM 2へ変換する  
B. measurementをすべて削除する  
C. target backendのISAへ適合したcircuitを用意する  
D. abstract circuitならtargetに関係なく必ずそのまま受理される

## Q32
<!-- domain: 4 -->
IBM Quantum Compute Serviceの3つのexecution modesはどれか。

A. Job / Session / Batch  
B. Local / Cloud / Hybrid  
C. Sampler / Estimator / Transpiler  
D. Queue / Run / Result

## Q33
<!-- domain: 4 -->
Session modeが最も適する代表的なworkloadはどれか。

A. 相互依存のないjobsを最初に全部投入するworkload  
B. 前のquantum job resultを使って次のjobを決めるiterative workload  
C. OpenQASM sourceをlocal fileへexportする処理  
D. 1回だけのStatevector simulation

## Q34
<!-- domain: 4 -->
Batch modeの代表的な用途として最も適切なのはどれか。

A. 前jobのresult待ちが必須のadaptive workload  
B. 1つのjobだけをexclusive accessで実行する  
C. 互いに独立して実行できる複数jobsをまとめて効率良く投入する  
D. dynamic circuit内部の`if`を評価する

## Q35
<!-- domain: 4 -->
Job modeでRuntime Samplerを使う代表的な初期化はどれか。

A. `SamplerV2(mode=backend)`  
B. `StatevectorSampler(mode="qpu")`  
C. `SamplerV2(mode=QuantumCircuit)`  
D. `SamplerV2(mode="statevector")`

## Q36
<!-- domain: 4 -->
利用可能なQPUから比較的空いているbackendを選ぶ代表的なservice APIはどれか。

A. `QuantumCircuit.least_busy()`  
B. `QiskitRuntimeService().least_busy(operational=True, simulator=False)`  
C. `SamplerV2.random_backend()`  
D. `Statevector.from_backend()`

## Q37
<!-- domain: 4 -->
IBM Quantum Compute ServiceのV2 Samplerをimportする現在の代表的な形はどれか。

A. `from qiskit import RuntimeSampler`  
B. `from qiskit.quantum_info import SamplerV2`  
C. `from qiskit.primitives import Sampler`  
D. `from qiskit_ibm_runtime import SamplerV2`

## Q38
<!-- domain: 4 -->
Estimator V2のPUBとして正しい一般形はどれか。

A. `(circuit, observables, optional parameter_values, optional precision)`  
B. `(circuit, optional parameter_values, optional shots)`  
C. `(counts, backend)`  
D. `(session, qasm_version)`

## Q39
<!-- domain: 4 -->
Estimator V2でobservablesとparameter valuesをarrayとして渡す場合のbroadcastingについて正しいものはどれか。

A. NumPy-style broadcasting rulesにより互換なshapeを組み合わせられる  
B. 両者は必ず同じ1次元list長でなければならない  
C. broadcastingはSampler V1だけの機能である  
D. shapeは常に無視されscalar resultになる

## Q40
<!-- domain: 4 -->
`job = estimator.run(pubs)` の戻り値について正しいものはどれか。

A. expectation valueそのものの`float`  
B. submitted job objectで、結果は通常`job.result()`から取得する  
C. transpiled `QuantumCircuit`  
D. backendのcoupling map

## Q41
<!-- domain: 4 -->
local `StatevectorEstimator` とRuntime `EstimatorV2` の違いとして最も適切なのはどれか。

A. `StatevectorEstimator`も必ずIBM QPUを使う  
B. Runtime `EstimatorV2`はobservableを受け取らない  
C. local reference implementationはhardware targetを必要としない一方、QPU Runtime workflowではbackend ISAやexecution modeを考慮する  
D. 両者はclass名以外すべて同じexecution environmentである

## Q42
<!-- domain: 5 -->
Sampler V2の中心的な出力はどれか。

A. observableのeigenvectors  
B. transpiler pass list  
C. exact Hamiltonian spectrum  
D. circuitのclassical output registerから得るsampled bitstrings/data

## Q43
<!-- domain: 5 -->
Qiskit SDKのlocal statevector-based V2 Sampler reference implementationはどれか。

A. `StatevectorEstimator`  
B. `BackendEstimatorV2`  
C. `StatevectorSampler`  
D. `QiskitRuntimeService`

## Q44
<!-- domain: 5 -->
IBM Quantum Compute ServiceでQPU等へSampler workloadを送るclassはどれか。

A. `qiskit.quantum_info.SamplerV2`  
B. `QuantumCircuit.sampler()`  
C. `qiskit.primitives.StatevectorSampler`  
D. `qiskit_ibm_runtime.SamplerV2`

## Q45
<!-- domain: 5 -->
Sampler V2 PUBの一般形として最も適切なのはどれか。

A. `(circuit, observable, precision)`  
B. `(circuit, optional parameter_values, optional shots)`  
C. `(counts, shots)`  
D. `(backend, observables)`

## Q46
<!-- domain: 5 -->
`sampler.options.default_shots = 500` の後、PUB-specific shotsを指定していないcircuitを今回だけ128 shotsでrunしたい。最も直接的なのはどれか。

A. `sampler.options.default_precision = 128`  
B. `sampler.run(pubs, precision=128)`  
C. `sampler.options.resilience_level = 128`  
D. `sampler.run(pubs, shots=128)`

## Q47
<!-- domain: 5 -->
Runtime Samplerのdynamical decouplingを有効にするcurrent option pathに最も近いものはどれか。

A. `sampler.options.resilience_level = 1`  
B. `sampler.options.dynamical_decoupling.enable = True`  
C. `sampler.dynamic = "DD"`  
D. `sampler.options.shots.dynamical = True`

## Q48
<!-- domain: 5 -->
dynamical decouplingの主目的として最も適切なのはどれか。

A. measurement resultをexpectation valueへ変換する  
B. idle periodへpulse sequencesを挿入しdecoherence等の影響を抑える方向で使う  
C. circuitをOpenQASM 3へserializeする  
D. coupling mapをall-to-allへ変更する

## Q49
<!-- domain: 5 -->
2026-09時点のIBM documentationにおけるdynamic circuitsとdynamical decouplingのcompatibilityとして正しいものはどれか。

A. dynamic circuitではDDが自動的に必須になる  
B. 両者は常に同時利用できる  
C. current feature compatibilityではincompatibleとして扱われる  
D. DDはSampler optionsではないので関係しない

## Q50
<!-- domain: 6 -->
Estimator V2の中心的な目的はどれか。

A. classical bitstringsだけをsampleする  
B. OpenQASM parserを提供する  
C. circuitとobservableからexpectation valueを推定する  
D. routingだけを実行する

## Q51
<!-- domain: 6 -->
Qiskit SDKのlocal statevector-based V2 Estimator reference implementationはどれか。

A. `StatevectorSampler`  
B. `BackendSamplerV2`  
C. `StatevectorEstimator`  
D. `SamplerV2`

## Q52
<!-- domain: 6 -->
IBM Quantum Compute Serviceで使うRuntime Estimator implementationはどれか。

A. `qiskit.quantum_info.EstimatorV2`  
B. `qiskit_ibm_runtime.EstimatorV2`  
C. `QuantumCircuit.estimator()`  
D. `qiskit.primitives.StatevectorSampler`

## Q53
<!-- domain: 6 -->
Estimator PUBの核となる入力はどれか。

A. circuitとobservable(s)  
B. countsとshotsだけ  
C. circuit drawingとPNG file  
D. backend passwordとAPI token

## Q54
<!-- domain: 6 -->
`|+>` に対するPauli-Zの期待値はどれか。

A. +1  
B. -1  
C. 1/2  
D. 0

## Q55
<!-- domain: 6 -->
2026-09時点でRuntime Estimatorの`resilience_level`として用意されているlevelはどれか。

A. 0と1だけ  
B. 1, 2, 3, 4  
C. 任意の0以上の整数  
D. 0, 1, 2

## Q56
<!-- domain: 6 -->
個別のresilience optionsで上書きしない場合、`resilience_level=0` のpresetについて正しいものはどれか。

A. Estimatorが提供するresilience mitigationを適用しないbaseline  
B. ZNEを必ず有効にする  
C. measurement mitigationを必ず有効にする  
D. shotsを0にする

## Q57
<!-- domain: 6 -->
Estimator V2のPUB resultで`data.evs`が表すものはどれか。

A. expectation values  
B. event bitstrings  
C. execution versions  
D. error vectors

## Q58
<!-- domain: 7 -->
既知のRuntime job ID `job_id` からjob objectを取得する代表的なAPIはどれか。

A. `QiskitRuntimeService().job(job_id)`  
B. `RuntimeJobV2.from_id(job_id)`  
C. `SamplerV2.job(job_id)`  
D. `QuantumCircuit.load_job(job_id)`

## Q59
<!-- domain: 7 -->
条件を指定しながら複数の過去Runtime jobsを一覧取得する代表的なAPIはどれか。

A. `job.result(all=True)`  
B. `Statevector.jobs()`  
C. `QuantumCircuit.jobs()`  
D. `QiskitRuntimeService().jobs(...)`

## Q60
<!-- domain: 7 -->
Runtime jobの現在のstatusを確認する代表的なmethodはどれか。

A. `job.status()`  
B. `job.statevector()`  
C. `job.measure()`  
D. `job.transpile()`

## Q61
<!-- domain: 7 -->
Sampler resultの`pub_result.data.meas`が`BitArray`であるとき、outcome count辞書を得る代表的なmethodはどれか。

A. `meas.expectation_values()`  
B. `meas.probabilities_exact()`  
C. `meas.get_counts()`  
D. `meas.observable()`

## Q62
<!-- domain: 7 -->
Estimator resultの`data.stds`について最も適切なのはどれか。

A. sampled bitstringsのlist  
B. `evs`に対応するstandard-deviation / uncertainty information  
C. backendのinstruction schedule  
D. circuitのglobal phases

## Q63
<!-- domain: 7 -->
1000 shotsのcountsが `{'0': 760, '1': 240}` のとき、経験的な `P(1)` はどれか。

A. 0.76  
B. 0.50  
C. 0.24  
D. 0.32

## Q64
<!-- domain: 7 -->
Primitive resultのmetadataについて正しい説明はどれか。

A. metadataだけがquantum stateそのものである  
B. metadataは常に空である  
C. shots、target precision、execution/error-mitigation情報などの補助情報を実装に応じて含み得る  
D. metadataへアクセスするとjobが再実行される

## Q65
<!-- domain: 8 -->
OpenQASM 3で2 quantum bitsと2 classical bitsを宣言する正しい組み合わせはどれか。

A. `qbit[2] q; cbit[2] c;`  
B. `qubit[2] q; bit[2] c;`  
C. `quantum[2] q; classical[2] c;`  
D. `qubits q(2); bits c(2);`

## Q66
<!-- domain: 8 -->
次のOpenQASM 3 programの意味として正しいものはどれか。

```qasm
OPENQASM 3.0;
include "stdgates.inc";
bit c;
qubit q;
h q;
c = measure q;
```

A. qへHを作用させ、measurement resultをclassical bit cへ格納する  
B. cをqubitへ変換してHを作用させる  
C. statevectorを測定せずcへ代入する  
D. H gate definitionをcへ保存する

## Q67
<!-- domain: 8 -->
QiskitのOpenQASM 3 import/exportについて正しいものはどれか。

A. `loads()`はexport、`dumps()`はimportである  
B. `dumps()`はOpenQASM 3 stringをexportし、`loads()`はprogram stringをimportする。current importにはoptional packageが必要である  
C. `qiskit.qasm3`はOpenQASM 2だけを扱う  
D. `dump()`と`load()`はいずれもSampler result専用である

## Q68
<!-- domain: 8 -->
OpenQASM 3とIBM Quantum Compute Serviceについて最も適切な説明はどれか。

A. Qiskitでparse/representできるOpenQASM 3 featureとQPUで実行可能なfeatureは同一とは限らず、REST APIでもprimitive workloadsをjob/session/batchで扱えるためcurrent support table/docsを確認する  
B. OpenQASM 3 specificationに存在するfeatureはすべてIBM QPUで必ず実行できる  
C. REST APIではjob modeしか使えない  
D. REST APIを使う場合Sampler/Estimatorというprimitive conceptはなくなる
