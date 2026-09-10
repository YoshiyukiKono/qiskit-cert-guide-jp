# Topic Test 03 — Circuit Construction

全10問。各問1つ選択してください。

## Questions

### Q1
2量子ビット・2古典ビットの回路を最も簡潔に作るコードはどれか。

A. `QuantumCircuit(2, 2)`  
B. `QuantumCircuit(4)`  
C. `QuantumCircuit("2,2")`  
D. `QuantumCircuit.measure(2,2)`

### Q2
量子ビット0を古典ビット1へ測定する正しい呼び出しはどれか。

A. `qc.measure(0, 1)`  
B. `qc.measure(1, 0)`  
C. `qc.measure_all(0, 1)`  
D. `qc.read(0, 1)`

### Q3
パラメータ化された回転角を作る代表的なクラスはどれか。

A. `Parameter`  
B. `Sampler`  
C. `Target`  
D. `Counts`

### Q4
回路 `other` の操作を既存回路 `qc` に結合する用途として適切なのはどれか。

A. `qc.compose(other)`  
B. `qc.sample(other)`  
C. `qc.compile(other)`  
D. `qc.counts(other)`

### Q5
ある回路の逆ユニタリを構成したい。最も直接的なのはどれか。

A. `qc.inverse()`  
B. `qc.reverse_bits()`  
C. `qc.measure_all()`  
D. `qc.decompose()`

### Q6
単一量子ビットゲート X を制御付きゲートに変換する考え方として正しいものはどれか。

A. X の `control()` を利用できる  
B. X を classical register に変換する  
C. X に測定を追加する  
D. X の global phase を削除する

### Q7
`barrier()` の主な意味として適切なのはどれか。

A. 量子状態を測定する  
B. 回路上の論理的な区切りを示し、特定の最適化をまたがせないために使える  
C. 量子ビットを追加する  
D. ノイズを除去する

### Q8
`qc.append(gate, [0, 1])` の第2引数が表すものはどれか。

A. gate を適用する量子ビットの対応  
B. shot数  
C. transpiler optimization level  
D. measurement counts

### Q9
`QuantumRegister(3, "q")` が表すものはどれか。

A. 3量子ビットの名前付き量子レジスタ  
B. 3古典ビットのレジスタ  
C. 3shotの実行設定  
D. 3つのbackend

### Q10
parameterized circuit に数値を代入する用途として適切なのはどれか。

A. `assign_parameters(...)`  
B. `draw(...)`  
C. `measure_all(...)`  
D. `reverse_bits(...)`

---

# Answers & Explanations

### A1 — A
`QuantumCircuit(2, 2)` は2量子ビットと2古典ビットを持つ回路を作る標準的な簡略形。

### A2 — A
`measure(qubit, cbit)` の順。`qc.measure(0,1)` は q0 の結果を c1 に格納する。

### A3 — A
`qiskit.circuit.Parameter` は未束縛の記号パラメータを回路に持たせるために使う。Sampler/Estimator へ値の配列を渡す学習にもつながる。

### A4 — A
`compose` は回路同士を合成するためのAPI。引数や `inplace` の扱いは最新版APIを確認すること。

### A5 — A
`inverse()` は各可逆操作を逆順・逆操作へ変換して逆回路を構成する。測定など非ユニタリ操作を含む場合には単純な逆ユニタリとして扱えない。

### A6 — A
Gate/Instruction の制御版を構成できるAPIがあり、X の制御版はCXに対応する考え方になる。

### A7 — B
barrier は物理的な量子操作として情報を変換するためのものではなく、回路構造・コンパイル上の境界として使われる。

### A8 — A
`append` では instruction/gate と、それをどの qargs/cargs に割り当てるかを指定する。

### A9 — A
`QuantumRegister(3,"q")` は3つの quantum bits を束ねる名前付きレジスタ。

### A10 — A
`assign_parameters` は Parameter を数値や別Parameterへ束縛する。V2 Primitives では回路自体を事前束縛せず PUB としてparameter valuesを渡す場面もある。
