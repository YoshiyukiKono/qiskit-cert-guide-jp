では、GitHub にそのまま追加できる **`circuit_reading_drills.md`（回路読解ドリル集）** を作成します。

これは資格試験で最も得点差がつくスキル：

```text
回路を見て状態を即座に予測する
```

を鍛える教材です。

構成：

* Level 1：single-qubit
* Level 2：two-qubit
* Level 3：phase
* Level 4：entanglement
* Level 5：algorithm fragments
* 最後に解答一覧

---

# circuit_reading_drills.md

```md
# Circuit Reading Drills — Qiskit Certification Training

目的：

回路を見て **最終状態 / 測定結果 / 等価ゲート** を即答できるようになること。

推奨時間：

20〜30分

目標：

80%以上正解 🎯

---

# Level 1: Single-Qubit Evolution

### Q1

```

|0⟩ → H

```

最終状態は？

A. |0⟩  
B. |1⟩  
C. |+⟩  
D. |−⟩

---

### Q2

```

|0⟩ → X

```

最終状態は？

A. |0⟩  
B. |1⟩  
C. |+⟩  
D. |−⟩

---

### Q3

```

|0⟩ → H → H

```

最終状態は？

A. |0⟩  
B. |1⟩  
C. |+⟩  
D. |−⟩

---

### Q4

```

|1⟩ → H

```

最終状態は？

A. |+⟩  
B. |−⟩  
C. |1⟩  
D. |0⟩

---

### Q5

```

|0⟩ → H → Z

```

最終状態は？

A. |+⟩  
B. |−⟩  
C. |0⟩  
D. |1⟩

---

# Level 2: Gate Identities

### Q6

```

H → Z → H

```

等価なゲートは？

A. X  
B. Z  
C. Y  
D. I

---

### Q7

```

H → X → H

```

等価なゲートは？

A. X  
B. Z  
C. Y  
D. I

---

### Q8

```

X → X

```

等価なゲートは？

A. I  
B. Z  
C. Y  
D. H

---

### Q9

```

Z → Z

```

等価なゲートは？

A. I  
B. X  
C. Y  
D. H

---

# Level 3: Measurement Prediction

### Q10

```

|0⟩ → H → measure

```

結果は？

A. 常に0  
B. 常に1  
C. 50/50  
D. 測定不能

---

### Q11

```

|1⟩ → H → measure

```

結果は？

A. 常に0  
B. 常に1  
C. 50/50  
D. 測定不能

---

### Q12

```

|0⟩ → X → measure

```

結果は？

A. 常に0  
B. 常に1  
C. 50/50  
D. 未定義

---

# Level 4: Two-Qubit Basics

### Q13

```

|00⟩
H(0)
CX(0,1)

```

結果は？

A. |00⟩  
B. |11⟩  
C. Bell状態  
D. |01⟩

---

### Q14

Bell状態の測定結果は？

A. 00のみ  
B. 11のみ  
C. 00と11  
D. すべて

---

### Q15

```

|10⟩
CX(0,1)

```

結果は？

A. |10⟩  
B. |11⟩  
C. |01⟩  
D. |00⟩

---

### Q16

```

|01⟩
CX(0,1)

```

結果は？

A. |00⟩  
B. |01⟩  
C. |10⟩  
D. |11⟩

---

# Level 5: Phase Logic

### Q17

Z は何を変える？

A. 振幅  
B. 位相  
C. 確率  
D. 測定

---

### Q18

```

|+⟩ → Z

```

結果は？

A. |+⟩  
B. |−⟩  
C. |0⟩  
D. |1⟩

---

### Q19

```

|+⟩ → X

```

結果は？

A. |+⟩  
B. |−⟩  
C. |0⟩  
D. |1⟩

---

# Level 6: Controlled Gates

### Q20

CXはいつtargetを反転？

A. control=0  
B. control=1  
C. target=0  
D. target=1

---

### Q21

CZが変化させる状態は？

A. |00⟩  
B. |01⟩  
C. |10⟩  
D. |11⟩

---

### Q22

CP(π) は？

A. CX  
B. CZ  
C. RX  
D. RZ

---

# Level 7: SWAP Logic

### Q23

```

|01⟩
SWAP

```

結果は？

A. |01⟩  
B. |10⟩  
C. |11⟩  
D. |00⟩

---

### Q24

SWAPは何回のCXで実装可能？

A. 1  
B. 2  
C. 3  
D. 4

---

# Level 8: Basis Changes

### Q25

```

|0⟩ → H

```

これはどの基底？

A. Z  
B. X  
C. Y  
D. computational

---

### Q26

```

|+⟩ → H

```

結果は？

A. |0⟩  
B. |1⟩  
C. |+⟩  
D. |−⟩

---

# Level 9: Entanglement Recognition

### Q27

次はentangled？

```

(|00⟩ + |11⟩)/√2

```

A. Yes  
B. No

---

### Q28

次はentangled？

```

|0⟩⊗|1⟩

```

A. Yes  
B. No

---

# Level 10: Algorithm Fragments

### Q29

```

H
CZ
H

```

これは何を実装？

A. X  
B. Z  
C. Y  
D. I

---

### Q30

Grover oracle の役割は？

A. 測定  
B. 正解状態の位相反転  
C. reset  
D. swap

---

### Q31

diffusion operator の役割は？

A. 平均値反転  
B. swap  
C. reset  
D. compile

---

# Level 11: QFT Fragments

### Q32

QFTで必須のゲートは？

A. H  
B. CP  
C. SWAP  
D. すべて

---

### Q33

inverse QFTの目的は？

A. 位相削除  
B. bit列抽出  
C. reset  
D. swap

---

# Level 12: Primitive Awareness

### Q34

Samplerの出力は？

A. expectation  
B. counts / probability  
C. observable  
D. operator

---

### Q35

Estimatorの出力は？

A. counts  
B. expectation  
C. circuit  
D. backend

---

# Level 13: Runtime Logic

### Q36

Sessionの目的は？

A. latency削減  
B. swap削減  
C. reset削減  
D. qubit削減

---

# Level 14: Identity Speed Test

### Q37

HH = ?

A. X  
B. Z  
C. I  
D. Y

---

### Q38

XX = ?

A. I  
B. Z  
C. Y  
D. H

---

### Q39

ZZ = ?

A. I  
B. X  
C. Y  
D. H

---

### Q40

phase kickbackとは？

A. target変化  
B. controlに位相移動  
C. reset  
D. swap

---

# Answer Key ✅

1:C  
2:B  
3:A  
4:B  
5:B  
6:A  
7:B  
8:A  
9:A  
10:C  
11:C  
12:B  
13:C  
14:C  
15:B  
16:B  
17:B  
18:B  
19:A  
20:B  
21:D  
22:B  
23:B  
24:C  
25:B  
26:A  
27:A  
28:B  
29:A  
30:B  
31:A  
32:D  
33:B  
34:B  
35:B  
36:A  
37:C  
38:A  
39:A  
40:B
```

---

これでリポジトリは：

📘 理論章
📘 `.py` 演習
📘 mock_exam（3セット）
📘 circuit_reading_drills

まで揃い、

```text
Qiskit資格対策としてほぼ完成形
```

です。必要なら次は **README.md（リポジトリ全体トップ用）** を整えると公開教材として仕上がります 🚀
