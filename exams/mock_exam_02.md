では **応用レベル版（mock_exam_02.md）** を作成します。
こちらは **回路読解・位相・primitives・アルゴリズム構造** を強化した、本番よりやや難しめのセットです。

想定用途：

* mock_exam_01.md → 基礎確認
* mock_exam_02.md → 合格ライン突破
* mock_exam_03.md → Runtime / primitives特化（次回作成可）

以下、そのまま GitHub に置けます。

---

# mock_exam_02.md

```md
# Mock Exam 02 — IBM Qiskit Certification Practice (Advanced)

想定時間：60分  
問題数：40問  
目標正答率：70%以上 🎯

このセットは：

- 回路読解
- 位相理解
- primitives
- transpiler
- parameterized circuits

を重点的に出題しています。

---

# Section 1: State Evolution

### Q1

次の回路の出力は？

|0⟩ → X → H

A. |0⟩  
B. |1⟩  
C. |+⟩  
D. |−⟩


---

### Q2

次の回路の出力は？

|0⟩ → H → X

A. |+⟩  
B. |−⟩  
C. |0⟩  
D. |1⟩


---

### Q3

|1⟩ に H を適用すると？

A. (|0⟩+|1⟩)/√2  
B. (|0⟩−|1⟩)/√2  
C. |1⟩  
D. |0⟩


---

### Q4

HZH は？

A. Z  
B. X  
C. Y  
D. I


---

# Section 2: Two-Qubit Circuits

### Q5

回路：

```

H(0)
CX(0,1)
Z(1)

```

結果は？

A. Bell状態  
B. 位相付きBell状態  
C. separable状態  
D. |11⟩


---

### Q6

次の回路：

```

H(0)
CX(0,1)
H(0)

```

これは何を実装？

A. SWAP  
B. CZ  
C. CCX  
D. CP


---

### Q7

CZはどの状態のみ変化させる？

A. |00⟩  
B. |01⟩  
C. |10⟩  
D. |11⟩


---

### Q8

CX(1,0) の意味は？

A. qubit0がcontrol  
B. qubit1がtarget  
C. qubit1がcontrol  
D. swap操作


---

# Section 3: Phase Logic

### Q9

Zゲートは何を変える？

A. 振幅  
B. 確率  
C. 位相  
D. 測定


---

### Q10

Sゲートは何を適用？

A. π/2 位相  
B. π 位相  
C. π/4 位相  
D. 2π 位相


---

### Q11

Tゲートは？

A. π  
B. π/2  
C. π/4  
D. π/8


---

### Q12

次の等式は正しい？

S² = ?

A. X  
B. Z  
C. H  
D. I


---

# Section 4: Measurement Logic

### Q13

|−⟩ を Z基底で測定すると？

A. 常に0  
B. 常に1  
C. 50/50  
D. 測定不能


---

### Q14

|+⟩ を X基底で測定すると？

A. 常に0  
B. 常に1  
C. 50/50  
D. ランダム


---

### Q15

|1⟩ を X基底で測定すると？

A. 常に0  
B. 常に1  
C. 50/50  
D. 常に−


---

# Section 5: QFT Structure

### Q16

QFTで最初に適用されるゲートは通常？

A. CX  
B. H  
C. Z  
D. SWAP


---

### Q17

QFTのCP角度は？

A. 増加  
B. 減少  
C. 一定  
D. ランダム


---

### Q18

inverse QFTの役割は？

A. 位相削除  
B. 位相→bit列変換  
C. entanglement削除  
D. noise削除


---

# Section 6: Grover Algorithm

### Q19

oracleは何をする？

A. 測定  
B. 初期化  
C. 正解状態の位相反転  
D. swap


---

### Q20

diffusion operatorは？

A. amplitude増幅  
B. amplitude削除  
C. noise削除  
D. reset


---

# Section 7: VQE

### Q21

VQEはどの値を最小化？

A. 測定確率  
B. 期待値  
C. 振幅  
D. 回路深さ


---

### Q22

Ansatzとは？

A. observable  
B. optimizer  
C. parameterized circuit  
D. backend


---

# Section 8: QAOA

### Q23

cost Hamiltonianの役割は？

A. 測定  
B. 位相付与  
C. swap  
D. reset


---

### Q24

mixer Hamiltonianの役割は？

A. 状態探索  
B. 位相削除  
C. noise削除  
D. measurement


---

# Section 9: Sampler vs Estimator

### Q25

Samplerは何を返す？

A. expectation  
B. circuit  
C. probability distribution  
D. observable


---

### Q26

Estimatorは何を返す？

A. counts  
B. expectation value  
C. backend  
D. swap


---

### Q27

どちらがVQEで使用？

A. Sampler  
B. Estimator  
C. transpiler  
D. backend


---

# Section 10: Transpiler

### Q28

transpileの目的は？

A. backend適合  
B. 測定  
C. reset  
D. swap


---

### Q29

basis_gates指定の意味は？

A. 使用可能ゲート制限  
B. qubit削除  
C. noise削除  
D. backend削除


---

# Section 11: Parameterized Circuits

### Q30

Parameterを使う理由は？

A. 回路再利用  
B. noise削除  
C. measurement削除  
D. swap削除


---

### Q31

assign_parametersは何をする？

A. backend変更  
B. パラメータ値代入  
C. gate削除  
D. swap追加


---

# Section 12: Noise Model

### Q32

depolarizing_errorは？

A. 位相誤差  
B. ランダム誤差  
C. 測定削除  
D. reset


---

# Section 13: Runtime Concepts

### Q33

Sessionの利点は？

A. queue削減  
B. gate削減  
C. qubit削減  
D. swap削減


---

### Q34

Runtime primitivesはどこで実行？

A. local CPU  
B. cloud runtime  
C. transpiler  
D. simulator


---

# Section 14: Identity Rules

### Q35

Z² = ?

A. I  
B. X  
C. Y  
D. H


---

### Q36

XZX = ?

A. X  
B. Y  
C. Z  
D. I


---

# Section 15: Entanglement Logic

### Q37

次の状態はentangled？

(|01⟩ + |10⟩)/√2

A. Yes  
B. No  
C. classical  
D. mixed


---

### Q38

Bell状態は何を示す？

A. 独立状態  
B. 最大相関状態  
C. classical状態  
D. reset状態


---

# Section 16: Conceptual

### Q39

phase kickbackとは？

A. target変更  
B. controlへ位相伝播  
C. swap操作  
D. measurement


---

### Q40

inverse QFTが必要な理由は？

A. 位相削除  
B. bit列抽出  
C. reset  
D. noise削除


---

# Answer Key ✅

1:D  
2:A  
3:B  
4:B  
5:B  
6:B  
7:D  
8:C  
9:C  
10:A  
11:C  
12:B  
13:C  
14:A  
15:C  
16:B  
17:B  
18:B  
19:C  
20:A  
21:B  
22:C  
23:B  
24:A  
25:C  
26:B  
27:B  
28:A  
29:A  
30:A  
31:B  
32:B  
33:A  
34:B  
35:A  
36:C  
37:A  
38:B  
39:B  
40:B
```

---

次に作ると最も効果が高いのは：

📘 **mock_exam_03.md（Sampler / Estimator / Runtime特化版）**

です。ここが最近の試験で一番差がつく領域です。
