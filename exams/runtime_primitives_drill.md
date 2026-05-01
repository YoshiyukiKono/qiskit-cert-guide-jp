了解しました。
以下は **IBM Qiskit Certification 試験で最頻出の Runtime / Primitive 領域だけに特化した演習セット**です。

対象：

* Sampler
* Estimator
* Observable
* Parameterized circuits
* Runtime Session
* Job object
* Primitive V2 概念
* Transpile との関係

試験の得点に直結する部分だけ集めています 📈

そのまま `runtime_primitives_drill.md` として保存できます。

---

# Runtime / Primitive 集中演習セット

想定時間：45分
問題数：30問
目標正答率：80%以上 🎯

---

# Section 1：Sampler 基本理解

Q1
Sampler が返すものはどれ？

A statevector
B counts / probability distribution
C expectation value
D observable

---

Q2
Sampler はどの操作を抽象化している？

A measurement sampling
B transpilation
C optimization
D noise reduction

---

Q3
Sampler.run() に必要な入力は？

A observable
B circuit
C backend
D parameter

---

Q4
Sampler の主用途は？

A VQE
B Grover
C Hamiltonian最小化
D 固有値計算

---

Q5
Sampler の出力形式として正しいものは？

A expectation values
B bitstring distribution
C matrix
D operator

---

# Section 2：Estimator 基本理解

Q6
Estimator が返すものは？

A counts
B expectation value
C probability
D statevector

---

Q7
Estimator.run() に必要な入力は？

A circuit のみ
B observable のみ
C circuit と observable
D backend

---

Q8
Estimator が主に使われるアルゴリズムは？

A Grover
B QFT
C VQE
D teleportation

---

Q9
Observable とは何か？

A backend
B operator
C circuit
D parameter

---

Q10
Estimator は何を評価する？

A measurement counts
B expectation values
C sampling noise
D transpilation depth

---

# Section 3：Observable 理解

Q11
Z observable の期待値：

|0⟩ のとき？

A 0
B +1
C −1
D 2

---

Q12
Z observable の期待値：

|1⟩ のとき？

A 0
B +1
C −1
D 2

---

Q13
|+⟩ 状態に対する Z observable の期待値は？

A 0
B +1
C −1
D 未定義

---

Q14
|+⟩ 状態に対する X observable の期待値は？

A 0
B +1
C −1
D 未定義

---

Q15
Observable を変更すると変わるものは？

A circuit
B expectation value
C backend
D transpiler

---

# Section 4：Parameterized circuits

Q16
Parameter の目的は？

A 回路削除
B 回路再利用
C backend変更
D observable削除

---

Q17
assign_parameters() の役割は？

A parameter削除
B 値の代入
C measurement追加
D backend設定

---

Q18
parameter sweep の目的は？

A observable削除
B 角度依存評価
C measurement削除
D swap削除

---

Q19
parameterized circuit は主にどのアルゴリズムで使う？

A VQE
B teleportation
C QFT
D SWAP test

---

# Section 5：Runtime Session

Q20
Runtime Session の利点は？

A queue待ち削減
B qubit削除
C measurement削除
D transpile削除

---

Q21
Session 内で複数 job を実行すると何が改善する？

A latency
B qubit数
C measurement精度
D transpiler速度

---

Q22
Runtime Session は何を共有する？

A backend context
B observable
C circuit
D transpiler設定

---

# Section 6：Job Object

Q23
job.result() は何をする？

A job送信
B job削除
C result取得
D backend変更

---

Q24
job.status() が返すものは？

A circuit depth
B job state
C observable
D transpiler level

---

Q25
job.cancel() の役割は？

A backend停止
B job停止
C circuit削除
D measurement削除

---

# Section 7：Primitive V2

Q26
Primitive V2 の入力単位は？

A circuit
B observable
C PUB
D backend

---

Q27
PUB とは何か？

A parameterized unit batch
B primitive unified bundle
C primitive utility block
D parameter usage block

---

Q28
SamplerV2 が扱うものは？

A expectation values
B sampling distributions
C operators
D transpilation

---

Q29
EstimatorV2 が扱うものは？

A measurement sampling
B expectation evaluation
C circuit visualization
D reset operations

---

# Section 8：Runtime アーキテクチャ理解

Q30
Python SDK と Runtime REST API の関係は？

A SDK は REST API を抽象化している
B REST API は SDK を抽象化している
C 無関係
D backendのみ使用する

---

# 解答

1 B
2 A
3 B
4 B
5 B
6 B
7 C
8 C
9 B
10 B
11 B
12 C
13 A
14 B
15 B
16 B
17 B
18 B
19 A
20 A
21 A
22 A
23 C
24 B
25 B
26 C
27 B
28 B
29 B
30 A

---

必要なら次に：

「試験で必ず出る回路変換（HXH＝Z など）だけを集めた高速暗記ドリル」

も作れます。これは合格率をさらに押し上げます 🚀
