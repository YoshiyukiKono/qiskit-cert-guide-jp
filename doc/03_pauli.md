ではシリーズ第3章として、**Pauliゲート（X / Y / Z）** を資格試験対策レベルで徹底解説します。
この章は：

* 単一量子ビット操作の理解
* 位相の意味
* Hゲートとの関係
* 回路変換問題

を解けるようになるための核心部分です。

---

# 03_pauli.md

# Part 3：Pauliゲート（X / Y / Z）を完全に理解する

Pauliゲートは量子回路の基本操作です。

資格試験では：

```text
回路の変換
状態の予測
ゲートの等価関係
```

として頻繁に出題されます。

この章では：

```text
X：ビット反転
Z：位相反転
Y：ビット＋位相反転
```

を統一的に理解します。

---

# 1. Pauli-Xゲート（量子NOT）

Pauli-Xは古典NOTに対応します。

変換：

X\lvert0\rangle=\lvert1\rangle

X\lvert1\rangle=\lvert0\rangle

つまり：

```text
0 ↔ 1 を交換する
```

---

# 2. Qiskitで確認する

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(1)
qc.x(0)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[0.+0.j 1.+0.j]
```

つまり：

```text
|1⟩
```

---

# 3. Pauli-Zゲート（位相反転）

Zゲートは状態を変えません。

変えるのは：

```text
符号（位相）
```

変換：

Z\lvert0\rangle=\lvert0\rangle

Z\lvert1\rangle=-\lvert1\rangle

つまり：

```text
|1⟩ に −1 をかける
```

---

# 4. なぜ位相は重要なのか

状態：

```text
(|0⟩ + |1⟩)/√2
```

と

```text
(|0⟩ − |1⟩)/√2
```

は測定確率が同じです：

```text
50%
50%
```

しかし：

```text
干渉結果が変わる
```

これが量子計算の核心です。

---

# 5. Qiskitで確認する

```python
qc = QuantumCircuit(1)

qc.h(0)
qc.z(0)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[ 0.707+0.j -0.707+0.j ]
```

つまり：

```text
符号が反転
```

---

# 6. Pauli-Yゲート

Yゲートは：

```text
X + Z を同時に実行
```

します。

変換：

Y\lvert0\rangle=i\lvert1\rangle

Y\lvert1\rangle=-i\lvert0\rangle

特徴：

```text
複素数 i が登場する
```

---

# 7. 行列表現（試験頻出）

Pauli行列：

X：

X=\begin{pmatrix}0&1\1&0\end{pmatrix}

Y：

Y=\begin{pmatrix}0&-i\i&0\end{pmatrix}

Z：

Z=\begin{pmatrix}1&0\0&-1\end{pmatrix}

試験では：

```text
この行列の作用を読む問題
```

が出ます。

---

# 8. Bloch球での意味

Pauliゲートは回転操作です：

| ゲート | 回転軸 |
| --- | --- |
| X   | x軸  |
| Y   | y軸  |
| Z   | z軸  |

つまり：

```text
回転として理解できる
```

---

# 9. XゲートとHadamardの関係

重要関係：

HXH=Z

意味：

```text
基底変換でゲートが変わる
```

---

# 10. ZゲートとHadamardの関係

同様に：

HZH=X

これは資格試験の頻出問題です。

---

# 11. X² = I

Pauliゲートは2回適用すると元に戻ります：

X^2=I

同様に：

Y^2=I

Z^2=I

---

# 12. XとZは可換ではない

順序が重要：

XZ=-ZX

つまり：

```text
順番で結果が変わる
```

量子回路の基本ルールです。

---

# 13. Qiskitで確認する

```python
from qiskit.quantum_info import Operator

qc = QuantumCircuit(1)
qc.x(0)
qc.z(0)

print(Operator(qc))
```

順序を変えると結果が変わります。

---

# 14. よく出る試験問題

問題：

次の結果は？

```text
X|0⟩
```

答え：

```text
|1⟩
```

---

問題：

次の結果は？

```text
Z|1⟩
```

答え：

```text
-|1⟩
```

---

問題：

次の結果は？

```text
HXH
```

答え：

```text
Z
```

---

問題：

次は？

```text
HZH
```

答え：

```text
X
```

---

# 15. 状態変換まとめ（暗記推奨）

| 入力 | X  | Z |    |   |    |
| -- | -- | - | -- | - | -- |
|    | 0⟩ |   | 1⟩ |   | 0⟩ |
|    | 1⟩ |   | 0⟩ | − | 1⟩ |

---

# 16. この章のチェックリスト（合格基準）

次ができればOK：

✅ Xの作用を説明できる
✅ Zの作用を説明できる
✅ Yの作用を説明できる
✅ HXH=Z を理解している
✅ HZH=X を理解している
✅ XZ ≠ ZX を理解している

---

次章：

**04_phase.md**

では：

```text
Sゲート
Tゲート
位相ゲートの意味
```

を扱います。

ここから：

```text
確率に現れない情報
```

という量子計算の核心に入ります。
