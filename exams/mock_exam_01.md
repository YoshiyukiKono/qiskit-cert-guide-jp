では、GitHub にそのまま追加できる **`mock_exam_01.md`（本番レベル40問セット）** を作成します。
構成は実際の IBM Qiskit Associate 試験に近い形：

* 回路理解
* ゲート恒等式
* Sampler / Estimator
* entanglement
* phase
* primitives
* algorithms

でバランスさせています。

**形式：**

* Q1〜Q40：問題
* 最後に解答一覧（別セクション）
* GitHub教材としてそのまま使える構造

---

# mock_exam_01.md

```md
# Mock Exam 01 — IBM Qiskit Certification Practice

想定時間：60分  
問題数：40問  
目標正答率：70%以上 🎯

---

# Section 1: Single-Qubit Gates

### Q1

H|0⟩ = ?

A. |0⟩  
B. |1⟩  
C. (|0⟩+|1⟩)/√2  
D. (|0⟩−|1⟩)/√2


---

### Q2

H を2回適用すると何になる？

A. X  
B. Z  
C. I  
D. Y


---

### Q3

HZH は何と等価？

A. I  
B. X  
C. Y  
D. Z


---

### Q4

HXH は何と等価？

A. Z  
B. X  
C. Y  
D. I


---

### Q5

Z|1⟩ = ?

A. |0⟩  
B. −|0⟩  
C. |1⟩  
D. −|1⟩


---

# Section 2: Measurement

### Q6

H|0⟩ を測定すると？

A. 常に0  
B. 常に1  
C. 50%で0、50%で1  
D. 測定不能


---

### Q7

測定は何を行う操作？

A. 位相変更  
B. ユニタリ変換  
C. 古典ビットへの射影  
D. 回路削除


---

### Q8

shots の意味は？

A. qubit数  
B. 測定回数  
C. gate数  
D. backend数


---

# Section 3: Entanglement

### Q9

次の回路の結果は？

```

H(0)
CX(0,1)

```

A. |00⟩  
B. Bell状態  
C. |11⟩  
D. |01⟩


---

### Q10

Bell状態の測定結果は？

A. 00のみ  
B. 11のみ  
C. 00と11  
D. すべて


---

### Q11

CZが位相反転する状態は？

A. |00⟩  
B. |01⟩  
C. |10⟩  
D. |11⟩


---

### Q12

CXのtargetが反転する条件は？

A. control=0  
B. control=1  
C. target=0  
D. target=1


---

# Section 4: Phase

### Q13

位相は直接測定できる？

A. できる  
B. できない  
C. 常にできる  
D. 常にできない


---

### Q14

phaseを観測可能にする方法は？

A. 測定  
B. 干渉  
C. reset  
D. swap


---

### Q15

CP(π) は何と等価？

A. CX  
B. CZ  
C. RX  
D. RZ


---

# Section 5: Multi-Qubit Logic

### Q16

SWAPは何回のCXで実装可能？

A. 1  
B. 2  
C. 3  
D. 4


---

### Q17

CNOTは何を生成できる？

A. 位相  
B. entanglement  
C. 測定  
D. reset


---

# Section 6: Basis

### Q18

|+⟩ はどの基底？

A. Z  
B. X  
C. Y  
D. computational


---

### Q19

|+⟩ = ?

A. (|0⟩+|1⟩)/√2  
B. (|0⟩−|1⟩)/√2  
C. |0⟩  
D. |1⟩


---

# Section 7: QFT

### Q20

QFTの基本構造は？

A. H + CP + SWAP  
B. X + CX  
C. Z + H  
D. RXのみ


---

### Q21

QFTでSWAPが必要な理由は？

A. 位相修正  
B. bit順序反転  
C. entanglement削除  
D. noise補正


---

# Section 8: Grover

### Q22

oracleの役割は？

A. 正解状態の位相反転  
B. 測定  
C. 初期化  
D. swap


---

### Q23

diffusion operatorの役割は？

A. noise削除  
B. 平均値反転  
C. reset  
D. swap


---

# Section 9: VQE

### Q24

VQEが求めるものは？

A. 最大固有値  
B. 最小固有値  
C. 測定値  
D. 確率


---

### Q25

VQEはどのタイプ？

A. 古典  
B. 量子のみ  
C. ハイブリッド  
D. ランダム


---

# Section 10: QAOA

### Q26

QAOAの対象は？

A. FFT  
B. 最適化問題  
C. 分解問題  
D. ソート


---

### Q27

QAOAのパラメータは？

A. θ  
B. γとβ  
C. λ  
D. φ


---

# Section 11: Sampler

### Q28

Samplerが返すものは？

A. expectation  
B. statevector  
C. probability distribution  
D. operator


---

### Q29

Samplerの用途は？

A. VQE  
B. Grover  
C. Hamiltonian分解  
D. ノイズ削除


---

# Section 12: Estimator

### Q30

Estimatorが返すものは？

A. counts  
B. expectation value  
C. circuit  
D. backend


---

### Q31

Estimatorが必要なアルゴリズムは？

A. VQE  
B. swap  
C. reset  
D. barrier


---

# Section 13: Runtime

### Q32

Runtime Sessionの目的は？

A. queue削減  
B. gate削減  
C. qubit削減  
D. swap削減


---

# Section 14: Transpiler

### Q33

transpileの目的は？

A. 測定  
B. backend適合  
C. reset  
D. noise削除


---

### Q34

optimization_level=3 の意味は？

A. 最低最適化  
B. 中間  
C. 高度最適化  
D. 無効


---

# Section 15: Parameterized Circuits

### Q35

Parameterの用途は？

A. 回路削除  
B. 回路再利用  
C. qubit削除  
D. swap削除


---

# Section 16: Noise

### Q36

実機で確率が変化する理由は？

A. compile  
B. noise  
C. reset  
D. swap


---

# Section 17: Identity Rules

### Q37

HH = ?

A. X  
B. Z  
C. I  
D. Y


---

### Q38

X² = ?

A. I  
B. Z  
C. Y  
D. H


---

# Section 18: Concept

### Q39

entanglementとは？

A. 独立状態  
B. 相関状態  
C. classical状態  
D. noise状態


---

### Q40

phase kickbackとは？

A. targetが変化  
B. controlに位相移動  
C. reset操作  
D. swap操作


---

# Answer Key ✅

1:C  
2:C  
3:B  
4:A  
5:D  
6:C  
7:C  
8:B  
9:B  
10:C  
11:D  
12:B  
13:B  
14:B  
15:B  
16:C  
17:B  
18:B  
19:A  
20:A  
21:B  
22:A  
23:B  
24:B  
25:C  
26:B  
27:B  
28:C  
29:B  
30:B  
31:A  
32:A  
33:B  
34:C  
35:B  
36:B  
37:C  
38:A  
39:B  
40:B
```

---

必要なら次に：

* mock_exam_02.md（応用レベル）
* mock_exam_03.md（Runtime / primitives重点）
* 回路読み取り特化版

も追加できます 📘
