# Mock Exam 01 — Qiskit v2.X Developer Associate

**68 questions / 90 minutes**

- 各問1つ選択。
- 資料を見ずに解くことを推奨。
- 分からない問題は印を付けて先へ進む。
- 解答は `../answers/mock-exams/mock-01-answers.md`。
- 本模試はオリジナル問題であり、IBM実試験問題の再現ではない。

---

## Q1
`X` を `|1>` に適用するとどうなるか。

A. `|0>`  B. `|1>`  C. `|+>`  D. `i|0>`

## Q2
`H|0>` はどれか。

A. `(|0>+|1>)/sqrt(2)`  B. `(|0>-|1>)/sqrt(2)`  C. `|1>`  D. `i|0>`

## Q3
`Z|1>` はどれか。

A. `|1>`  B. `-|1>`  C. `|0>`  D. `i|0>`

## Q4
`S` ゲートの `|1>` 成分への位相はどれか。

A. 1  B. -1  C. i  D. -i

## Q5
`T†` は何の逆ゲートか。

A. H  B. T  C. X  D. CX

## Q6
`HXH` と等価なのはどれか。

A. X  B. Y  C. Z  D. S

## Q7
`Rz(theta)` の主な効果はどれか。

A. Z軸周りの回転  B. X軸周りの回転  C. qubit追加  D. 測定

## Q8
control=`1`, target=`0` に CX を適用した computational basis 出力はどれか。

A. `00`  B. `01`  C. `10`  D. `11`

## Q9
状態全体に `-1` を掛けたとき、同一基底での測定確率はどうなるか。

A. すべて反転  B. 変わらない  C. 0になる  D. 2倍になる

## Q10
`|1>` の Bloch 球上の標準的位置はどこか。

A. +Z  B. -Z  C. +X  D. +Y

## Q11
`|+>` を X basis で測定した理想結果に相当するのはどれか。

A. +1 が確定  B. -1 が確定  C. 50/50  D. 測定不能

## Q12
次の回路の理想的な測定分布はどれか。

```python
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0,1], [0,1])
```

A. 00と11が約半々  B. 01と10が約半々  C. 4通り均等  D. 常に00

## Q13
`Statevector.from_label("0")` が表す状態はどれか。

A. `|0>`  B. `|1>`  C. `|+>`  D. 混合状態

## Q14
振幅 `-i/sqrt(2)` の絶対値二乗はどれか。

A. -1/2  B. 1/2  C. i/2  D. 1

## Q15
回路のテキスト描画を得る基本操作はどれか。

A. `qc.draw()`  B. `qc.run()`  C. `qc.counts()`  D. `qc.qasm3()`

## Q16
`|+i>=(|0>+i|1>)/sqrt(2)` を computational basis で測るとどうなるか。

A. 0/1が約半々  B. 常に0  C. 常に1  D. iが出る

## Q17
Qiskitの複数bit文字列の表示で、通常 bit 0 はどこか。

A. 左端  B. 右端  C. 表示されない  D. 中央

## Q18
3量子ビットだけの回路を作るコードはどれか。

A. `QuantumCircuit(3)`  B. `QuantumCircuit(0,3)`  C. `QuantumCircuit("3")`  D. `QuantumCircuit.qubits(3)`

## Q19
回路に Hadamard を q2 へ追加するコードはどれか。

A. `qc.h(2)`  B. `qc.h[2]`  C. `qc.H(2,2)`  D. `h.qc(2)`

## Q20
`Parameter("theta")` を使う主な理由はどれか。

A. 後から値を束縛できる記号角を作る  B. shotを固定する  C. backendを選ぶ  D. countsを保存する

## Q21
回路をその場で合成して元の `qc` を更新したい場合に関連する `compose` の引数はどれか。

A. `inplace=True`  B. `shots=True`  C. `measure=True`  D. `backend=True`

## Q22
`qc.measure_all()` の効果として最も近いものはどれか。

A. 回路の全量子ビットを測定するための命令を追加する  B. 量子状態を返すだけ  C. transpileする  D. observableを生成する

## Q23
`qc.inverse()` を適用する対象として最も自然なのはどれか。

A. 可逆なユニタリ回路  B. counts辞書  C. backend  D. classical-only program

## Q24
`QuantumRegister(2,"data")` の `data` は何か。

A. register名  B. backend名  C. observable  D. shot数

## Q25
2量子ビットgateを q1,q3 に割り当てる操作として最も適切なのはどれか。

A. `qc.append(gate, [1,3])`  B. `qc.draw(gate,[1,3])`  C. `qc.measure(gate)`  D. `gate.shots(1,3)`

## Q26
barrierについて正しいものはどれか。

A. 主に回路構造/最適化境界として使う  B. 必ずqubitをresetする  C. probabilityを正規化する  D. Estimatorの別名

## Q27
transpilerがハードウェア接続制約を処理する工程として最も関係するのはどれか。

A. routing  B. sampling  C. plotting  D. serialization

## Q28
basis gate set に含まれない高水準gateを実行可能にする典型的方法はどれか。

A. basis gateへ分解/変換する  B. gate名を文字列で短くする  C. shotを0にする  D. classical bitへ移す

## Q29
coupling map が主に表すものはどれか。

A. 量子ビット間の許可された接続関係  B. probability table  C. parameter dictionary  D. QASM version

## Q30
transpile前後の理想的な論理動作について期待されるものはどれか。

A. 意味的に等価  B. 常に完全に同じgate列  C. 必ず同じdepth  D. 必ず同じphysical qubit番号

## Q31
より高い optimization level について一般に言えるものはどれか。

A. より積極的な最適化を試みることがある  B. 結果を必ず反転する  C. measurementを削除する  D. qubitを必ず1個にする

## Q32
実機結果が理想simulationと異なる理由として自然なのはどれか。

A. noiseと有限shot  B. Python文字列  C. Markdown  D. Git branch

## Q33
preset pass manager の役割として適切なのはどれか。

A. 標準的transpilation pipelineを構成する  B. Credly badgeを発行する  C. probabilityを手計算する  D. QASMを暗号化する

## Q34
非隣接な2量子ビットを相互作用させるためSWAPが増えた。これは何の影響か。

A. routing  B. visualization  C. state normalization  D. global phase

## Q35
shotsを増やしたときに通常期待されることはどれか。

A. 経験分布の統計誤差が小さくなる  B. circuit depthが0になる  C. qubit数が増える  D. すべてのnoiseが消える

## Q36
SamplerとEstimatorの違いとして正しいものはどれか。

A. Samplerは古典出力サンプル、Estimatorは期待値  B. 完全に同じ  C. Samplerはobservableだけを受ける  D. Estimatorは回路を受けない

## Q37
ローカルのV2 sampler参照実装はどれか。

A. `StatevectorSampler`  B. `StatevectorEstimator`  C. `Pauli`  D. `PassManager`

## Q38
Sampler PUB に含め得るものはどれか。

A. circuit, parameter values, shots  B. PNG, CSS, HTML  C. git SHAだけ  D. observableだけでcircuitなし

## Q39
`|0>`を100 shotsでSampler実行した理想的なcountsはどれに近いか。

A. 0が100  B. 1が100  C. 0/1が50ずつ  D. -1が100

## Q40
Samplerのparameter sweepが便利なのはどんな場合か。

A. 同一回路を複数の角度で評価する  B. register名を変更する  C. QASM versionを切り替える  D. Git履歴を比較する

## Q41
`StatevectorSampler` の制約として注意すべきものはどれか。

A. mid-circuit measurementを一般には扱えない  B. H gateを扱えない  C. 1qubitしか扱えない  D. parameterを扱えない

## Q42
Samplerで得た509/491の分布を理論50/50と比較した判断として適切なのはどれか。

A. 有限shotの自然な揺らぎ  B. 必ずバグ  C. probabilityが509  D. phaseが491度

## Q43
V2 Primitives の PUB は何の略か。

A. Primitive Unified Bloc  B. Python User Backend  C. Physical Unit Basis  D. Public Universal Bit

## Q44
Estimatorで必要になる中心的な入力はどれか。

A. circuitとobservable  B. countsだけ  C. PNGだけ  D. coupling mapだけ

## Q45
`|1>` に対する `<Z>` はいくつか。

A. +1  B. 0  C. -1  D. 1/2

## Q46
`|0>` に対する `<X>` はいくつか。

A. +1  B. 0  C. -1  D. 2

## Q47
`SparsePauliOp` が便利なのはどれか。

A. Pauli項の線形結合でobservableを表す  B. classical registerを描く  C. shotsを数える  D. backend loginする

## Q48
`StatevectorEstimator` は何を基礎にするか。

A. statevector simulation  B. CSV file  C. OpenQASM parserのみ  D. hardware calibrationのみ

## Q49
`|++>` に対する `XX` の期待値はどれか。

A. +1  B. 0  C. -1  D. +2

## Q50
`|00>` に対する `ZI` の期待値はどれか。

A. +1  B. 0  C. -1  D. 不定

## Q51
Estimator result の `evs` は通常何か。

A. expectation values  B. event strings  C. environment variables  D. error versions

## Q52
counts `{'00': 600, '11': 400}` の総shotsはいくつか。

A. 1000  B. 600  C. 400  D. 200

## Q53
上記countsの経験的 `P(11)` はどれか。

A. 0.4  B. 0.6  C. 1.0  D. 0.2

## Q54
Pauli-Z expectation value が0という事実だけから何が言えるか。

A. Zの+1/-1寄与が平均で相殺している  B. 状態は必ず`|+>`  C. qubitは存在しない  D. probabilityが負

## Q55
複数classical registerがある結果のbitstringを読むとき重要なのはどれか。

A. register/bit orderingを確認する  B. 色を確認する  C. CPU温度だけを見る  D. ファイル名を見る

## Q56
8192 shotsに増やしても実機noiseそのものはどうなるか。

A. shot増加だけでは系統的noiseは自動消滅しない  B. 必ずゼロになる  C. 逆符号になる  D. qubit数になる

## Q57
histogramが主に表すものはどれか。

A. outcome frequencies/distribution  B. unitary matrixそのもの  C. coupling map  D. source code diff

## Q58
有限shotの経験確率と理論確率の関係として正しいのはどれか。

A. 一致しないことが普通にあり、shots増加で収束が期待される  B. 1回でも必ず一致  C. 経験確率は複素数  D. 理論確率は整数だけ

## Q59
Estimatorの値 `0.72` を counts の72回と読むのが誤りなのはなぜか。

A. expectation valueは固有値の平均でありshot countそのものではない  B. 0.72は文字列だから  C. Estimatorは常に100shotだから  D. 72は素数でないから

## Q60
OpenQASM 3のversion宣言はどれか。

A. `OPENQASM 3.0;`  B. `QASM3;`  C. `version=3;`  D. `open qasm(3)`

## Q61
3量子ビット宣言として正しいものはどれか。

A. `qubit[3] q;`  B. `qbit(3) q;`  C. `quantum q[3];`  D. `qubits=3;`

## Q62
`bit[4] c;` は何を宣言するか。

A. 4 classical bits  B. 4 qubits  C. 4 shots  D. 4 observables

## Q63
Qiskit circuitをOpenQASM 3文字列へ変換するのはどれか。

A. `qiskit.qasm3.dumps(qc)`  B. `qc.measure_all()`  C. `transpile(qc)`  D. `Statevector(qc)`

## Q64
Qiskit circuitをOpenQASM 3としてstreamに書くのはどれか。

A. `qiskit.qasm3.dump(qc, stream)`  B. `qiskit.qasm3.loads(qc)`  C. `qc.draw(stream)`  D. `Sampler(stream)`

## Q65
OpenQASM 3文字列をQiskitへ読み込む高水準関数はどれか。

A. `qiskit.qasm3.loads(...)`  B. `qiskit.qasm3.dumps(...)`  C. `qc.inverse()`  D. `StatevectorSampler()`

## Q66
現在のQiskitでQASM3 importを使う際に必要になり得る追加packageはどれか。

A. `qiskit-qasm3-import`  B. `matplotlib-qasm`  C. `numpy-runtime`  D. `git-qiskit`

## Q67
`c = measure q;` の意味として正しいものはどれか。

A. qを測定し古典結果をcへ代入  B. cを量子化  C. qを削除  D. cをHadamard変換

## Q68
OpenQASM 3を学ぶ際の最も安全な方針はどれか。

A. supportが発展中なので最新版Qiskit docsと仕様を確認する  B. 2021年の文法だけ暗記する  C. OpenQASM 2と完全同一と考える  D. Python構文と同一と考える
