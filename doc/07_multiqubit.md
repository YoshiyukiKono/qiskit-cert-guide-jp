**多量子ビット（multi-qubit）系**を資格試験対策レベルで体系的に解説します。
ここは合格ラインを超えるための**最重要分岐点**です。

理由：

* tensor product が理解できる
* 状態ベクトルの並び順が読める
* 2量子ビット状態を解釈できる
* Bell状態の準備理解につながる

からです。

---

# 07_multiqubit.md

# Part 7：多量子ビット状態（tensor product）を完全に理解する

単一量子ビット：

$$
|\psi\rangle=a|0\rangle+b|1\rangle
$$

でした。

2量子ビットになると：

```text
状態空間が4次元になる
```

ここが最初の重要な変化です。

---

# 1. 状態数は指数的に増える

量子ビット数と状態数：

| qubit数 | 状態数 |
| ------ | --- |
| 1      | 2   |
| 2      | 4   |
| 3      | 8   |
| n      | 2ⁿ  |

つまり：

```text
量子状態は指数的に増える
```

これが量子計算の基本原理の1つです。

---

# 2. 2量子ビットの基底状態

基底状態は4つあります：

$$
|00\rangle, |01\rangle, |10\rangle, |11\rangle
$$

これは：

```text
2ビットの組み合わせ
```

と同じです。

---

# 3. tensor productとは何か

2量子ビット状態は：

$$
|a\rangle \otimes |b\rangle
$$

で表されます。

例：

$$
|0\rangle \otimes |1\rangle = |01\rangle
$$

つまり：

```text
2つの量子ビットの結合
```

です。

---

# 4. ベクトルとしての表現

単一量子ビット：

$$
|0\rangle=
\begin{pmatrix}
1\
0
\end{pmatrix}
$$

2量子ビット：

$$
|00\rangle=
\begin{pmatrix}
1\
0\
0\
0
\end{pmatrix}
$$

同様に：

| 状態 | ベクトル |           |
| -- | ---- | --------- |
|    | 00⟩  | [1,0,0,0] |
|    | 01⟩  | [0,1,0,0] |
|    | 10⟩  | [0,0,1,0] |
|    | 11⟩  | [0,0,0,1] |

---

# 5. 一般の2量子ビット状態

一般状態：

$$
|\psi\rangle = a|00\rangle + b|01\rangle + c|10\rangle + d|11\rangle
$$

正規化条件：

```text
|a|² + |b|² + |c|² + |d|² = 1
```

試験でよく出ます。

---

# 6. Qiskitで2量子ビット状態を見る

例：

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[1,0,0,0]
```

つまり：

```text
|00⟩
```

---

# 7. 1つ目の量子ビットだけ操作する

例：

```python
qc = QuantumCircuit(2)

qc.x(0)
```

結果：

```text
|10⟩
```

ここ重要：

```text
左がqubit0
```

です。

---

# 8. Qiskitの並び順（頻出）

Qiskitでは：

```text
|q1 q0⟩
```

の順序で表示されます。

例：

```text
qc.x(0)
```

結果：

```text
|01⟩
```

ではありません。

正しくは：

```text
|10⟩
```

ここは試験で非常に重要です。

---

# 9. Hadamardを1つの量子ビットに適用

例：

```python
qc = QuantumCircuit(2)

qc.h(0)
```

状態：

$$
\frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)
$$

つまり：

```text
qubit0だけ重ね合わせ
```

です。

---

# 10. 両方にHadamardを適用

例：

```python
qc = QuantumCircuit(2)

qc.h([0,1])
```

状態：

$$
\frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)
$$

つまり：

```text
4状態同時生成
```

です。

---

# 11. tensor productの計算例

例：

$$
(|0\rangle + |1\rangle)/\sqrt{2}
$$

と

$$
|0\rangle
$$

のtensor product：

$$
\frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)
$$

---

# 12. separable状態とは何か

次の状態：

$$
\frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)
$$

は：

```text
分離可能
```

つまり：

```text
独立した2量子ビット
```

です。

---

# 13. entangled状態とは何か

例：

$$
\frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)
$$

これは：

```text
分離できない
```

状態です。

これを：

```text
エンタングルメント
```

と呼びます。

---

# 14. なぜ重要なのか

この状態では：

```text
片方を見るともう片方が決まる
```

つまり：

```text
古典では表現できない相関
```

です。

---

# 15. Statevectorの読み方（2量子ビット）

例：

```text
[0.707, 0, 0, 0.707]
```

意味：

$$
\frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)
$$

順序：

```text
|00⟩
|01⟩
|10⟩
|11⟩
```

です。

---

# 16. よく出る試験問題

問題：

次の状態の確率：

$$
(|00\rangle + |11\rangle)/\sqrt{2}
$$

答え：

| 状態 | 確率  |
| -- | --- |
| 00 | 50% |
| 11 | 50% |

---

問題：

次は分離可能か？

$$
(|00\rangle + |10\rangle)/\sqrt{2}
$$

答え：

```text
YES
```

---

問題：

次は分離可能か？

$$
(|00\rangle + |11\rangle)/\sqrt{2}
$$

答え：

```text
NO
```

---

# 17. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ tensor product を説明できる
✅ 2量子ビット基底を書ける
✅ Statevector順序を理解している
✅ separable状態を判定できる
✅ entangled状態を判定できる
✅ Qiskitのビット順序を理解している

---

次章：

**08_cnot.md**

では：

```text
エンタングルメントを生成するCXゲート
Bell状態の作り方
制御ビットとターゲットビット
```

を扱います。ここが量子アルゴリズム理解の入口になります。
