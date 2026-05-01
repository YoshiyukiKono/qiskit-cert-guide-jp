では第8章として、**CX（CNOT）ゲートとエンタングルメント生成**を資格試験対策レベルで体系的に解説します。
この章はシリーズの中でも特に重要です。理由は：

* Bell状態の生成
* 制御ビット／ターゲットビット理解
* entanglement の実装
* 多量子ビット回路の基本

がすべてここに集約されているためです。

---

# 08_cnot.md

# Part 8：CNOT（CX）ゲートとエンタングルメントを完全に理解する

ここから：

```text
古典計算では表現できない状態
```

を実際に作ります。

それを可能にするのが：

```text
CNOT（CX）ゲート
```

です。

---

# 1. CNOTとは何か

CNOTは：

```text
control qubit が 1 のときだけ
target qubit を反転する
```

ゲートです。

---

# 2. 動作ルール

変換：

CX|00\rangle=|00\rangle

CX|01\rangle=|01\rangle

CX|10\rangle=|11\rangle

CX|11\rangle=|10\rangle

つまり：

```text
control = 1 のときだけ反転
```

です。

---

# 3. Qiskitでの書き方

構文：

```python
qc.cx(control, target)
```

例：

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)

qc.cx(0,1)
```

意味：

```text
qubit0 が control
qubit1 が target
```

---

# 4. 実際の状態変化を見る

例：

```python
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)

qc.x(0)
qc.cx(0,1)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[0,0,0,1]
```

つまり：

```text
|11⟩
```

---

# 5. control と target を間違えやすい理由（試験頻出）

例：

```python
qc.cx(1,0)
```

意味：

```text
qubit1 が control
qubit0 が target
```

順序が重要です。

---

# 6. Hadamard + CNOT = Bell状態

これが最重要ポイントです ⭐

回路：

```python
qc = QuantumCircuit(2)

qc.h(0)
qc.cx(0,1)
```

状態：

\frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)

これを：

```text
Bell状態
```

と呼びます。

---

# 7. なぜエンタングルメントになるのか

理由：

この状態は：

```text
2つの独立した状態に分解できない
```

からです。

つまり：

```text
separable ではない
```

状態です。

---

# 8. 測定すると何が起きるか

Bell状態：

[
(|00\rangle + |11\rangle)/\sqrt{2}
]

測定すると：

| 結果 | 確率  |
| -- | --- |
| 00 | 50% |
| 11 | 50% |

重要：

```text
01 と 10 は出ない
```

---

# 9. 相関が生まれる理由

もし：

```text
qubit0 = 0
```

なら：

```text
qubit1 = 0
```

もし：

```text
qubit0 = 1
```

なら：

```text
qubit1 = 1
```

つまり：

```text
完全相関
```

が生まれます。

---

# 10. Bell状態の作り方まとめ

手順：

Step1：

```text
Hadamard
```

Step2：

```text
CNOT
```

つまり：

```text
H → CX
```

で生成できます。

---

# 11. 別のBell状態

例：

```python
qc.x(0)
qc.h(0)
qc.cx(0,1)
```

状態：

\frac{1}{\sqrt{2}}(|01\rangle + |10\rangle)

Bell状態は全部で4種類あります：

| 名前 | 状態 |      |         |
| -- | -- | ---- | ------- |
| Φ+ | (  | 00⟩+ | 11⟩)/√2 |
| Φ− | (  | 00⟩− | 11⟩)/√2 |
| Ψ+ | (  | 01⟩+ | 10⟩)/√2 |
| Ψ− | (  | 01⟩− | 10⟩)/√2 |

---

# 12. 行列表現（資格試験対応）

CNOT行列：

[
CX =
\begin{pmatrix}
1&0&0&0
\
0&1&0&0
\
0&0&0&1
\
0&0&1&0
\end{pmatrix}
]

試験では：

```text
行列作用を読む問題
```

が出ます。

---

# 13. CNOTは可逆操作

重要：

[
CX^2 = I
]

つまり：

```text
2回適用すると元に戻る
```

---

# 14. CNOTはエンタングルメント生成器

単独では：

```text
entanglement は作れない
```

例：

```text
|10⟩ → |11⟩
```

だけ。

しかし：

```text
superposition + CNOT
```

で：

```text
entanglement が生成される
```

---

# 15. QiskitでBell状態を測定する

例：

```python
from qiskit_aer import AerSimulator
from qiskit import transpile

qc = QuantumCircuit(2,2)

qc.h(0)
qc.cx(0,1)

qc.measure([0,1],[0,1])

sim = AerSimulator()

result = sim.run(transpile(qc, sim)).result()

print(result.get_counts())
```

出力：

```text
{'00': 512, '11': 512}
```

---

# 16. よく出る試験問題

問題：

次の結果は？

```text
H(0)
CX(0,1)
```

答え：

```text
(|00⟩+|11⟩)/√2
```

---

問題：

control=0 target=1 の意味は？

答え：

```text
qubit0 が 1 のとき qubit1 を反転
```

---

問題：

次の状態はエンタングル状態か？

```text
(|00⟩+|11⟩)/√2
```

答え：

```text
YES
```

---

問題：

次は？

```text
(|00⟩+|10⟩)/√2
```

答え：

```text
NO
```

---

# 17. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ CXの動作を説明できる
✅ control / target を区別できる
✅ Bell状態を作れる
✅ Bell状態を判定できる
✅ separable と entangled を区別できる
✅ H→CX の意味を説明できる

---

次章：

**09_circuit.md**

では：

```text
SWAPゲート
Toffoliゲート
barrier
compose
回路の読み方
```

を扱います。ここから回路理解力が完成します。
