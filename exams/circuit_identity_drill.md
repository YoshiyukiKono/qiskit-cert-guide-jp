了解しました。
以下は **Qiskit 資格試験で頻出の「回路変換・等価変換」だけを集めた高速暗記ドリル**です。
そのまま `circuit_identity_drill.md` として保存できます。

目的：

* 回路を見て即座に状態を判断できるようにする
* 等価変換を暗記する
* 試験時間を短縮する ⏱️
* 正答率を底上げする 📈

---

# 回路等価変換 高速暗記ドリル

推奨時間：20分
目標：即答できるまで繰り返す

---

# Section 1：Hadamard 恒等変換

Q1

H H = ?

---

Q2

H X H = ?

---

Q3

H Z H = ?

---

Q4

H Y H = ?

---

Q5

H |0⟩ = ?

---

Q6

H |1⟩ = ?

---

# Section 2：Pauli 基本変換

Q7

X X = ?

---

Q8

Z Z = ?

---

Q9

Y Y = ?

---

Q10

X Z = ?

（順序重要）

---

Q11

Z X = ?

（順序重要）

---

# Section 3：位相ゲート

Q12

S S = ?

---

Q13

T T = ?

---

Q14

S† S = ?

---

Q15

Z = ?

（S を使って表現）

---

# Section 4：Basis 変換

Q16

H Z H = ?

---

Q17

H X H = ?

---

Q18

|+⟩ を Z basis で測定すると？

---

Q19

|0⟩ を X basis で測定すると？

---

# Section 5：CNOT の基本性質

Q20

control = |0⟩

CNOT の結果は？

---

Q21

control = |1⟩

CNOT の結果は？

---

Q22

CNOT を 2回適用すると？

---

Q23

CNOT(control,target)

target = |0⟩ のとき何が起こる？

---

Q24

CNOT(control,target)

target = |1⟩ のとき何が起こる？

---

# Section 6：Bell 状態生成

Q25

次の回路の結果は？

H(0)
CNOT(0→1)

初期状態：

|00⟩

---

Q26

同じ回路で初期状態：

|10⟩

結果は？

---

Q27

Bell 状態は entangled か？

---

# Section 7：Swap 等価変換

Q28

SWAP = ?

（CNOT を使って表現）

---

Q29

SWAP を 2回適用すると？

---

# Section 8：Phase Kickback

Q30

control qubit が |+⟩

target qubit が |1⟩

CZ 適用後

control に何が起きる？

---

# Section 9：測定結果の即答問題

Q31

H |0⟩ を Z basis 測定

結果は？

---

Q32

H |1⟩ を Z basis 測定

結果は？

---

Q33

X |0⟩ を測定

結果は？

---

Q34

Z |+⟩ は？

---

# Section 10：頻出等価変換まとめ問題

Q35

HZH = ?

---

Q36

HXH = ?

---

Q37

CNOT(control,target)

control に H を前後に挟むと？

---

Q38

Z = ?

（H と X を使って表現）

---

Q39

X = ?

（H と Z を使って表現）

---

Q40

HZH XH = ?

（段階的に簡約）

---

# 解答

Q1
I

Q2
Z

Q3
X

Q4
−Y

Q5
|+⟩

Q6
|−⟩

Q7
I

Q8
I

Q9
I

Q10
−ZX

Q11
−XZ

Q12
Z

Q13
S

Q14
I

Q15
S²

Q16
X

Q17
Z

Q18
50% / 50%

Q19
50% / 50%

Q20
変化なし

Q21
target が反転

Q22
I

Q23
control がコピーされる

Q24
control の値で反転

Q25
Bell 状態

(|00⟩ + |11⟩)/√2

Q26
(|10⟩ + |01⟩)/√2

Q27
Yes（最大エンタングル）

Q28
CNOT
CNOT(reverse)
CNOT

Q29
I

Q30
位相が反転（|−⟩ になる）

Q31
50% / 50%

Q32
50% / 50%

Q33
|1⟩

Q34
|−⟩

Q35
X

Q36
Z

Q37
control と target が入れ替わる構造になる

Q38
HXH

Q39
HZH

Q40
Z

---

このドリルを「反射的に解ける」レベルまで仕上げると、
Runtime / Primitive セクションと合わせて **合格確率はかなり高いゾーン**に入ります ✅
