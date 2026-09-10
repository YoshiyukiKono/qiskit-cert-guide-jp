# Mock Exam 01 — Answers & Explanations

対応問題: `../../mock-exams/mock-01.md`

## Answer Key

1 A / 2 A / 3 B / 4 C / 5 B / 6 C / 7 A / 8 D / 9 B / 10 B  
11 A / 12 A / 13 A / 14 B / 15 A / 16 A / 17 B / 18 A / 19 A / 20 A  
21 A / 22 A / 23 A / 24 A / 25 A / 26 A / 27 A / 28 A / 29 A / 30 A  
31 A / 32 A / 33 A / 34 A / 35 A / 36 A / 37 A / 38 A / 39 A / 40 A  
41 A / 42 A / 43 A / 44 A / 45 C / 46 B / 47 A / 48 A / 49 A / 50 A  
51 A / 52 A / 53 A / 54 A / 55 A / 56 A / 57 A / 58 A / 59 A / 60 A  
61 A / 62 A / 63 A / 64 A / 65 A / 66 A / 67 A / 68 A

> 選択肢位置の偏りは内容理解を優先した初版設計によるものです。本番の選択肢分布を模倣する意図はありません。次版ではランダム化候補です。

---

## Detailed Explanations

### Q1 — A
Pauli-X は computational basis を反転するので `X|1>=|0>`。`i|0>` ではなく、行列としても係数は1。

### Q2 — A
`H|0>=(|0>+|1>)/sqrt(2)=|+>`。符号がマイナスの選択肢は `H|1>=|->`。

### Q3 — B
Zは`|0>`に+1、`|1>`に-1を与える。したがって `Z|1>=-|1>`。

### Q4 — C
`S=diag(1,i)`。`|1>` 成分に90度の相対位相 `i` を掛ける。

### Q5 — B
dagger は随伴で、unitary gateではinverse。したがって `T†T=I`。

### Q6 — C
Hadamard conjugation は X と Z を交換するので `HXH=Z`、`HZH=X`。

### Q7 — A
`Rz(theta)=exp(-i theta Z/2)` で Bloch 球上のZ軸回転に対応する。

### Q8 — D
CX はcontrolが1ならtargetを反転する。`|10>` を control first の論理記法で考えればtarget 0→1で `|11>`。

### Q9 — B
状態全体への `-1=e^{iπ}` はglobal phase。Born則の絶対値二乗で消えるため同じ基底の測定確率は不変。

### Q10 — B
標準Bloch球では `|0>`=+Z、`|1>`=-Z。

### Q11 — A
`|+>` はPauli-Xの+1固有状態。X basis measurementでは+1が確定する。

### Q12 — A
Hでq0を重ね合わせにし、CXでBell state `( |00>+|11> )/sqrt(2)` を作る。computational basis measurementは00/11が各約1/2。

### Q13 — A
`Statevector.from_label("0")` はbasis labelから `|0>` を作る。混合状態ではなくpure state。

### Q14 — B
確率は複素振幅の絶対値二乗。`|-i/sqrt(2)|^2=1/2`。

### Q15 — A
`QuantumCircuit.draw()` は回路を描画する。実行・sampling・serializationとは別機能。

### Q16 — A
0と1の振幅の大きさはともに `1/sqrt(2)`。相対位相 `i` はcomputational basisの直接確率を変えない。

### Q17 — B
Qiskitの通常のbitstring表示ではbit 0が右端。複数量子ビット問題で頻出の取り違えポイント。

### Q18 — A
`QuantumCircuit(3)` は3 quantum bits、classical bitsなしの回路を作る。

### Q19 — A
Qiskitの回路メソッドでは `qc.h(2)` でq2へHadamardを追加する。

### Q20 — A
`Parameter` はsymbolic parameterを作り、後で値を束縛したりPrimitiveへparameter valuesを渡したりできる。

### Q21 — A
`compose(..., inplace=True)` は合成結果を新規回路として返すのではなく対象回路へ反映する用途で使う。

### Q22 — A
`measure_all()` は原則として全qubitを測定する命令を追加する便利メソッド。実行そのものではない。

### Q23 — A
`inverse()` はunitary/reversible circuitに対して自然な操作。測定など非可逆命令を含む回路では単純な逆ユニタリとして扱えない。

### Q24 — A
`QuantumRegister(2,"data")` の第2引数はregister name。

### Q25 — A
`append` はinstructionと、それを割り当てるqargs/cargsを指定する。2-qubit gateなら2つの対象qubitが必要。

### Q26 — A
barrierは主に論理的区切り・transpilation上の境界として使う。量子情報を測定・resetする操作ではない。

### Q27 — A
routing は論理2-qubit interactionをhardware connectivityへ割り当てる工程。

### Q28 — A
ターゲットが高水準gateを直接持たなければ、transpilerがbasis gate setへ分解・変換する。

### Q29 — A
coupling mapは主に2-qubit operationが可能な物理qubit間接続を表す。

### Q30 — A
transpilationは表現を変えても理想的な論理作用を保つことを目的とする。gate列やdepthが同一である必要はない。

### Q31 — A
高いoptimization levelは一般により多く/積極的な最適化passを試す。特定のdepth削減を保証するものではない。

### Q32 — A
実機にはgate/readout error等のnoiseがあり、さらに有限shotの統計揺らぎもある。理想statevector simulationとの差の代表要因。

### Q33 — A
preset pass managerは標準的なtranspilation stagesをまとめたpipelineを構成するための仕組み。

### Q34 — A
physical connectivityを満たすためのroutingでSWAP相当操作が挿入されることがある。

### Q35 — A
shots増加はsampling errorを小さくする方向に働くが、systematic hardware noiseを自動で除去するわけではない。

### Q36 — A
Samplerはclassical output samples、Estimatorはobservable expectation values。この対比はV2 Primitives理解の中心。

### Q37 — A
`qiskit.primitives.StatevectorSampler` がlocal statevector-based V2 Sampler reference implementation。

### Q38 — A
Sampler PUBはcircuitを中心に、optional parameter valuesやshotsを含められる実行単位。

### Q39 — A
`|0>` をcomputational basisで理想測定すれば0が確定するので100 shotsなら0が100に近い。

### Q40 — A
parameter sweepは同じ回路構造を異なる角度・parameter setsで繰り返し評価するとき有効。

### Q41 — A
`StatevectorSampler` はpure-state statevectorを基礎にするため、mid-circuit measurementを一般的にはサポートしない。

### Q42 — A
理論0.5/0.5でも1000回なら509/491程度のずれは自然なbinomial fluctuation。

### Q43 — A
PUB=Primitive Unified Bloc。V2 Primitivesで入力をまとめる基本単位。

### Q44 — A
Estimatorはcircuitとobservableの組を評価する。parameterized circuitならparameter values等も伴い得る。

### Q45 — C
`Z|1>=-|1>` なので `|1>` はZの-1固有状態、期待値は-1。

### Q46 — B
`|0>` をX basisで見ると+/-が等重みなので `<X>=0`。行列計算 `⟨0|X|0⟩=0` でも確認できる。

### Q47 — A
`SparsePauliOp` はPauli stringsの疎な線形結合を表し、Hamiltonianやobservableに使える。

### Q48 — A
`StatevectorEstimator` はfull statevector simulationを用いて期待値を計算するlocal reference implementation。

### Q49 — A
`|+>` はXの+1固有状態なので、`|++>` に対する `X⊗X` の固有値は(+1)(+1)=+1。

### Q50 — A
`ZI` のどちら側をどのqubitと読むかはQiskit orderingに注意が必要だが、`|00>` ではどちらのZも+1なので結果は+1。

### Q51 — A
V2 Estimator resultの `evs` はexpectation valuesを表す命名。

### Q52 — A
600+400=1000 shots。

### Q53 — A
経験確率は400/1000=0.4。

### Q54 — A
expectation 0は+1/-1寄与の平均が相殺したことを意味するだけで、状態を一意に決めない。`|+>`以外にも多くの状態があり得る。

### Q55 — A
複数registerではspaceを含む表示やbit orderingが結果解釈に影響する。measurement mappingと合わせて確認する。

### Q56 — A
shot数増加は統計精度を改善するが、gate biasやreadout errorなどsystematic noiseをそれだけで消さない。

### Q57 — A
histogramはoutcome frequency/distributionを視覚化する。unitary matrixやcoupling mapそのものではない。

### Q58 — A
有限標本のrelative frequencyは母確率から揺らぐ。独立samplingならshots増加に伴い経験分布が理論分布へ近づくことを期待する。

### Q59 — A
expectation valueはobservableの固有値を確率重み付きで平均した量。単純なevent countではない。

### Q60 — A
OpenQASM 3のversion declarationは `OPENQASM 3.0;`。

### Q61 — A
`qubit[3] q;` は3要素のqubit array/registerを宣言する代表的構文。

### Q62 — A
`bit` はclassical bit type。`bit[4] c;` は4 classical bitsを宣言する。

### Q63 — A
`qiskit.qasm3.dumps(qc)` はQuantumCircuitをOpenQASM 3 stringとしてexportする。

### Q64 — A
`dump(qc, stream)` は文字列を返す `dumps` と異なりfile-like streamへ書く。

### Q65 — A
`loads(program)` はOpenQASM 3 program文字列からQuantumCircuitをimportする高水準関数。`load(filename)` はfile名を受ける。

### Q66 — A
2026-09時点のQiskit docsではOpenQASM 3 importに `qiskit-qasm3-import` packageが必要。exportはcore APIに含まれる。

### Q67 — A
OpenQASM 3ではmeasurement resultをclassical bitへassignmentできる。ここではqの測定結果がcに入る。

### Q68 — A
QiskitのOpenQASM 3 interoperabilityは発展中。資格対策でも古いsyntax/APIを固定的に暗記せず、最新版のIBM/Qiskit docsと仕様を基準にする。

---

## Review by Domain

- Q1–Q9: quantum operations
- Q10–Q17: visualization / measurement / states
- Q18–Q26: circuit construction
- Q27–Q35: running / transpilation
- Q36–Q43: Sampler
- Q44–Q51: Estimator
- Q52–Q59: results analysis
- Q60–Q68: OpenQASM 3

間違いが2問以上まとまった領域は、対応する `topic-tests/` を再度解いてから次の模試へ進んでください。
