ではシリーズ第2章として、**資格試験で最も重要な単一ゲート**である Hadamard を徹底的に扱います。
この章を理解すると：

* 重ね合わせの生成
* 干渉の準備
* H×H=I
* 基底変換
* 位相との関係

まで一気に整理できます。

---

# 02_hadamard.md

# Part 2：Hadamardゲートを完全に理解する

Hadamardゲート（H）は、量子コンピューティングで最も重要なゲートです。

理由：

```text
重ね合わせを作る
干渉を可能にする
アルゴリズムの入口になる
```

資格試験でも**最頻出ゲート**です。

---

# 1. Hadamardゲートとは何か

Hadamardは：

```text
基底状態を重ね合わせ状態へ変換する
```

ゲートです。

変換：

H\lvert0\rangle=\frac{1}{\sqrt{2}}(\lvert0\rangle+\lvert1\rangle)

そして：

H\lvert1\rangle=\frac{1}{\sqrt{2}}(\lvert0\rangle-\lvert1\rangle)

ここで重要なのは：

```text
符号が違う
```

という点です。

---

# 2. なぜ符号が重要なのか

違い：

| 入力 | 出力 |   |
| -- | -- | - |
|    | 0⟩ | + |
|    | 1⟩ | − |

つまり：

```text
位相が変わる
```

この違いが干渉を生みます。

---

# 3. QiskitでHadamardを使う

例：

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(1)

qc.h(0)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[0.707+0.j 0.707+0.j]
```

意味：

```text
50% |0⟩
50% |1⟩
```

---

# 4. |1⟩にHadamardをかける

```python
qc = QuantumCircuit(1)

qc.x(0)
qc.h(0)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[0.707+0.j -0.707+0.j]
```

ここで：

```text
マイナスがつく
```

---

# 5. 測定結果は同じになる理由

状態：

```text
(|0⟩ − |1⟩)/√2
```

確率：

```text
50%
50%
```

なぜなら：

```text
符号は確率に影響しない
```

影響するのは：

```text
干渉
```

です。

---

# 6. Hadamardを2回かける

資格試験の典型問題：

```text
H → H = ?
```

答え：

H^2=I

つまり：

```text
元に戻る
```

---

# 7. Qiskitで確認する

```python
qc = QuantumCircuit(1)

qc.h(0)
qc.h(0)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[1.+0.j 0.+0.j]
```

つまり：

```text
|0⟩
```

---

# 8. なぜ元に戻るのか

理由：

Hadamardは：

```text
基底変換
```

だからです。

変換：

```text
Z基底 ↔ X基底
```

つまり：

```text
座標変換を2回やると元に戻る
```

---

# 9. 行列表現（試験重要）

Hadamardは次の行列：

H=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\1&-1\end{pmatrix}

試験では：

```text
この行列を読む問題
```

が出ます。

---

# 10. 行列として理解する

例：

入力：

```text
|0⟩ = [1,0]
```

計算：

```text
H|0⟩ = [1/√2, 1/√2]
```

入力：

```text
|1⟩ = [0,1]
```

計算：

```text
H|1⟩ = [1/√2, -1/√2]
```

---

# 11. H → X → H

資格試験の定番問題です。

回路：

```text
H → X → H
```

結果：

```text
Z
```

つまり：

```text
HZH = X
HXH = Z
```

は必須暗記です。

---

# 12. Qiskitで確認する

```python
from qiskit.quantum_info import Operator

qc = QuantumCircuit(1)

qc.h(0)
qc.x(0)
qc.h(0)

print(Operator(qc))
```

出力：

```text
Z行列
```

---

# 13. 重ね合わせ生成の本質

Hadamardは：

```text
確率を分割している
```

のではなく：

```text
振幅を分割している
```

ここが重要です。

つまり：

```text
干渉が可能になる
```

---

# 14. 多量子ビットHadamard

例：

```python
qc = QuantumCircuit(2)

qc.h([0,1])
```

結果：

```text
|00⟩
|01⟩
|10⟩
|11⟩
```

すべて同時に生成されます。

---

# 15. なぜ量子並列性が生まれるのか

Hadamardをn回適用すると：

```text
2^n状態
```

が同時に生成されます。

例：

| qubit数 | 状態数 |
| ------ | --- |
| 1      | 2   |
| 2      | 4   |
| 3      | 8   |
| n      | 2^n |

これが：

```text
量子並列性
```

です。

---

# 16. 試験頻出問題

問題：

次の結果は？

```text
H|0⟩
```

答え：

```text
(|0⟩ + |1⟩)/√2
```

---

問題：

次の結果は？

```text
H|1⟩
```

答え：

```text
(|0⟩ − |1⟩)/√2
```

---

問題：

次は？

```text
H → H → |1⟩
```

答え：

```text
|1⟩
```

---

# 17. この章のチェックリスト（合格基準）

できればOK：

✅ H|0⟩を書ける
✅ H|1⟩を書ける
✅ H²=Iを説明できる
✅ HZH=Xを理解している
✅ HXH=Zを理解している
✅ 基底変換として説明できる

---

次章：

**03_pauli.md**

では：

```text
X / Y / Z の意味と関係
```

を扱います。
