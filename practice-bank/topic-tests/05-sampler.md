# Topic Test 05 — Sampler Primitive

全10問。各問1つ選択してください。

## Questions

### Q1
Sampler primitive の役割として最も適切なのはどれか。

A. 回路の古典出力をサンプリングする  
B. Hamiltonian の固有値を厳密対角化する  
C. transpiler pass を生成する  
D. OpenQASMを構文解析する

### Q2
Qiskit SDK のローカル V2 Sampler 実装として代表的なのはどれか。

A. `StatevectorSampler`  
B. `StatevectorEstimator`  
C. `SparsePauliOp`  
D. `CouplingMap`

### Q3
Sampler を使う回路に classical output register / measurement が重要なのはなぜか。

A. Sampler は古典出力レジスタからサンプルを返すから  
B. 測定がないと transpile が禁止されるから  
C. 測定がないと量子ビットが作れないから  
D. classical bit が observable になるから

### Q4
V2 primitive でいう PUB の説明として最も適切なのはどれか。

A. 1つの実行単位をまとめた Primitive Unified Bloc  
B. Python Universal Backend  
C. Physical Utility Bit  
D. Public User Bus

### Q5
Sampler で shots を増やす主目的はどれか。

A. サンプリング統計のばらつきを減らす  
B. 回路を自動的に短くする  
C. observableを追加する  
D. qubit数を増やす

### Q6
parameterized circuit を Sampler V2 に渡す利点として適切なのはどれか。

A. 同じ回路構造に複数の parameter values を与えて評価できる  
B. Parameterを使うと測定が不要になる  
C. Parameterはhardware calibrationだけに使う  
D. Parameterを使うとshotsが必ず1になる

### Q7
`StatevectorSampler` について正しい説明はどれか。

A. 純粋状態の statevector simulation を使う参照実装である  
B. 必ず実IBM QPUを使う  
C. Estimator専用のobservableを返す  
D. OpenQASM 2しか受け付けない

### Q8
mid-circuit measurement を含む回路と `StatevectorSampler` の関係について正しいものはどれか。

A. pure statevector ベースのため制約があり、一般的なmid-circuit measurementとは非互換  
B. あらゆるdynamic circuitを完全サポートする  
C. mid-circuit measurementが必須  
D. 測定があると自動的にEstimatorへ切り替わる

### Q9
Sampler の結果を expectation value と混同してはいけない理由はどれか。

A. Sampler は主に測定された古典サンプルを返し、Estimator はobservableの期待値を扱うから  
B. 両者は完全に同じAPI名だから  
C. Samplerは量子回路を受け付けないから  
D. Estimatorはclassical registerだけを受け付けるから

### Q10
1000 shots の理想的な `|+>` 測定で counts が 487/513 になった。最も適切な解釈はどれか。

A. 50/50分布と整合する有限shotの統計変動  
B. Hゲートは壊れている  
C. `|+>` は48.7%だけ存在する混合状態  
D. global phaseが変化した証拠

---

# Answers & Explanations

### A1 — A
Sampler は回路の classical outputs をサンプリングする primitive。Estimator の expectation value と役割を区別する。

### A2 — A
Qiskit v2.x の参照 V2 implementation として `qiskit.primitives.StatevectorSampler` がある。

### A3 — A
Sampler は測定から得る classical data を扱う。回路設計時に、どの classical register に何を測るかが結果解釈に直結する。

### A4 — A
PUB は Primitive Unified Bloc。Sampler では circuit と optional parameter values / shots などを1実行単位としてまとめる。

### A5 — A
shots を増やすと経験頻度の統計誤差は通常小さくなるが、回路そのものが変わるわけではない。

### A6 — A
同じ ansatz/circuit を複数パラメータで評価するとき、parameterized circuit と V2 PUB の組み合わせが有効。

### A7 — A
`StatevectorSampler` は `Statevector` を使うローカル参照実装。IBM QPUを必須としない。

### A8 — A
pure-state statevector でサンプルを生成する設計上、mid-circuit measurements には制約がある。実装ごとの差を意識する。

### A9 — A
Sampler=sampled classical outcomes、Estimator=expectation values と整理すると試験問題を切り分けやすい。

### A10 — A
理論確率が0.5でも有限標本では正確に500/500になる必要はない。487/513は十分自然な揺らぎ。
