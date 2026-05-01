# Mock Exam 03 — IBM Qiskit Certification Practice (Runtime & Primitives Focus)

想定時間：60分  
問題数：40問  
目標正答率：75%以上 🎯

対象範囲：

- Sampler
- Estimator
- Runtime Session
- Observable
- Parameterized circuits
- Transpiler
- Noise
- Algorithm primitives

---

# Section 1: Sampler Basics

### Q1

Samplerが返すものは？

A. expectation value  
B. statevector  
C. probability distribution  
D. observable


---

### Q2

Samplerはどの操作を抽象化する？

A. measurement sampling  
B. transpile  
C. optimization  
D. compilation


---

### Q3

Sampler.run() の入力は？

A. observable  
B. backend  
C. circuit  
D. parameter


---

### Q4

Samplerは主にどの用途？

A. VQE  
B. Grover  
C. Hamiltonian最小化  
D. 固有値計算


---

# Section 2: Estimator Basics

### Q5

Estimatorが返す値は？

A. counts  
B. expectation value  
C. probability  
D. statevector


---

### Q6

Estimator.run() に必要な入力は？

A. circuitのみ  
B. observableのみ  
C. circuitとobservable  
D. backendのみ


---

### Q7

Estimatorはどのアルゴリズムで使われる？

A. QFT  
B. VQE  
C. SWAP  
D. RESET


---

### Q8

observableとは？

A. 測定対象演算子  
B. backend  
C. parameter  
D. circuit


---

# Section 3: Observable Logic

### Q9

Z observable の期待値は？

|0⟩ → ?

A. 0  
B. 1  
C. −1  
D. 未定義


---

### Q10

Z observable の期待値は？

|1⟩ → ?

A. 0  
B. 1  
C. −1  
D. 未定義


---

### Q11

|+⟩ 状態で Z observable の期待値は？

A. 0  
B. 1  
C. −1  
D. 2


---

### Q12

|+⟩ 状態で X observable の期待値は？

A. 0  
B. 1  
C. −1  
D. 2


---

# Section 4: Parameterized Circuits

### Q13

Parameter の目的は？

A. 回路削除  
B. 回路再利用  
C. noise削除  
D. swap削除


---

### Q14

assign_parameters() の役割は？

A. parameter削除  
B. 値代入  
C. backend変更  
D. reset


---

### Q15

Parameter sweep の目的は？

A. observable削除  
B. 角度依存解析  
C. qubit削除  
D. swap削除


---

# Section 5: Runtime Concepts

### Q16

Runtime Sessionの利点は？

A. queue削減  
B. gate削減  
C. qubit削減  
D. noise削減


---

### Q17

Runtime primitivesはどこで実行？

A. local CPU  
B. transpiler  
C. cloud runtime  
D. notebook


---

### Q18

Session内で複数jobを実行する利点は？

A. backend削除  
B. latency削減  
C. qubit削除  
D. reset削除


---

# Section 6: Primitive V2 Concepts

### Q19

Primitive V2 の入力単位は？

A. circuit  
B. observable  
C. PUB  
D. backend


---

### Q20

PUBとは？

A. parameterized unit batch  
B. primitive unified block  
C. primitive unified bloc  
D. primitive unit bundle


---

### Q21

SamplerV2 は何を扱う？

A. expectation  
B. sampling  
C. observable  
D. transpile


---

### Q22

EstimatorV2 は何を扱う？

A. measurement sampling  
B. expectation evaluation  
C. transpilation  
D. reset


---

# Section 7: Transpiler

### Q23

transpile の役割は？

A. backend適合  
B. measurement削除  
C. reset追加  
D. swap削除


---

### Q24

basis_gates 指定の目的は？

A. 使用ゲート制限  
B. qubit削除  
C. backend削除  
D. measurement削除


---

# Section 8: Optimization Levels

### Q25

optimization_level=3 は？

A. 最低最適化  
B. 中程度  
C. 高度最適化  
D. 無効


---

### Q26

optimization_level を上げると？

A. 回路短縮可能  
B. qubit削除  
C. backend削除  
D. measurement削除


---

# Section 9: Noise

### Q27

depolarizing_errorとは？

A. ランダム誤差  
B. 位相削除  
C. measurement削除  
D. reset


---

### Q28

noise model を使う理由は？

A. 実機近似  
B. 回路削除  
C. backend削除  
D. swap削除


---

# Section 10: Algorithm + Primitive Integration

### Q29

VQEでEstimatorを使う理由は？

A. sampling  
B. expectation評価  
C. transpile  
D. reset


---

### Q30

Groverで主に使うprimitiveは？

A. Estimator  
B. Sampler  
C. Transpiler  
D. Backend


---

### Q31

QAOAでEstimatorが必要な理由は？

A. expectation評価  
B. swap  
C. reset  
D. measurement削除


---

# Section 11: StatevectorSampler

### Q32

StatevectorSampler の特徴は？

A. 実機実行  
B. statevector sampling  
C. observable評価  
D. transpile


---

### Q33

StatevectorEstimator は？

A. sampling  
B. expectation評価  
C. reset  
D. swap


---

# Section 12: Multi Observable Logic

### Q34

同一回路で複数observableを評価可能？

A. Yes  
B. No  
C. 部分的  
D. runtimeのみ


---

### Q35

SparsePauliOp は何を表す？

A. circuit  
B. observable  
C. backend  
D. transpiler


---

# Section 13: Runtime Execution Model

### Q36

Runtimeが高速な理由は？

A. gate削減  
B. cloud内反復処理  
C. qubit削除  
D. reset削除


---

### Q37

Session終了後に起こることは？

A. backend削除  
B. queue再接続  
C. job独立化  
D. measurement削除


---

# Section 14: Conceptual Understanding

### Q38

SamplerとEstimatorの違いは？

A. sampling vs expectation  
B. reset vs swap  
C. measurement vs transpile  
D. backend vs circuit


---

### Q39

Observableを変えると何が変化？

A. circuit  
B. expectation値  
C. backend  
D. swap


---

### Q40

Primitive APIの目的は？

A. backend削除  
B. 抽象化された量子計算インターフェース  
C. measurement削除  
D. swap削除


---

# Answer Key ✅

1:C  
2:A  
3:C  
4:B  
5:B  
6:C  
7:B  
8:A  
9:B  
10:C  
11:A  
12:B  
13:B  
14:B  
15:B  
16:A  
17:C  
18:B  
19:C  
20:D  
21:B  
22:B  
23:A  
24:A  
25:C  
26:A  
27:A  
28:A  
29:B  
30:B  
31:A  
32:B  
33:B  
34:A  
35:B  
36:B  
37:C  
38:A  
39:B  
40:B
