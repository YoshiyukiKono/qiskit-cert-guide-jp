では第12章として、**Statevector（状態ベクトル）の読み方・確率計算・位相の意味**を資格試験対策レベルで体系的に解説します。

この章は特に重要です。理由：

```text
回路の最終状態を「計算できる」ようになる
```

＝試験の**回路出力予測問題**が解けるようになります。

---

# 12_statevector.md

# Part 12：Statevector（状態ベクトル）を完全に理解する

量子回路の出力は：

```text
bit列ではない
```

まず：

```text
Statevector（状態ベクトル）
```

として表現されます。

---

# 1. Statevectorとは何か

Statevectorとは：

```text
量子状態を表すベクトル
```

です。

例：

|\psi\rangle=a|0\rangle+b|1\rangle

ここで：

| 記号 | 意味 |         |
| -- | -- | ------- |
| a  |    | 0⟩になる振幅 |
| b  |    | 1⟩になる振幅 |

---

# 2. 振幅から確率を求める

確率は：

P(0)=|a|^2,\quad P(1)=|b|^2

つまり：

```text
係数の2乗＝確率
```

です。

---

# 3. 正規化条件

Statevectorは必ず：

|a|^2+|b|^2=1

を満たします。

これを：

```text
normalization condition
```

と呼びます。

試験頻出です。

---

# 4. QiskitでStatevectorを見る

例：

```python
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

qc = QuantumCircuit(1)
qc.h(0)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[0.70710678+0.j, 0.70710678+0.j]
```

意味：

```text
(|0⟩ + |1⟩)/√2
```

---

# 5. 配列の順序に注意（重要）

Statevector：

```text
[a, b]
```

は：

```text
a|0⟩ + b|1⟩
```

を意味します。

順序：

```text
|0⟩ → |1⟩
```

です。

---

# 6. 2量子ビットの場合

状態：

|\psi\rangle=a|00\rangle+b|01\rangle+c|10\rangle+d|11\rangle

配列：

```text
[a, b, c, d]
```

順序：

| index | state |
| ----- | ----- |
| 0     | 00    |
| 1     | 01    |
| 2     | 10    |
| 3     | 11    |

---

# 7. Bell状態をStatevectorで見る

例：

```python
qc = QuantumCircuit(2)

qc.h(0)
qc.cx(0,1)

Statevector.from_instruction(qc)
```

出力：

```text
[0.707, 0, 0, 0.707]
```

意味：

```text
(|00⟩ + |11⟩)/√2
```

---

# 8. なぜ中間2つが0になるのか

理由：

```text
|01⟩ と |10⟩ が存在しない
```

からです。

つまり：

```text
非ゼロ成分だけが状態を構成する
```

---

# 9. 位相（phase）とは何か

例：

```text
[0.707, 0.707]
```

と

```text
[0.707, -0.707]
```

は違います。

後者：

\frac{1}{\sqrt{2}}(|0\rangle-|1\rangle)

これは：

```text
relative phase が違う
```

状態です。

---

# 10. なぜ位相が重要なのか

理由：

```text
干渉を決める
```

からです。

例：

Grover
QFT
phase kickback

すべて位相が核心です。

---

# 11. グローバル位相と相対位相

例：

次の2つ：

[
|0\rangle+|1\rangle
]

と

[

* (|0\rangle+|1\rangle)
  ]

は：

```text
同じ状態
```

です。

理由：

```text
global phase は観測できない
```

---

# 12. 相対位相は観測できる

例：

[
|0\rangle+|1\rangle
]

と

[
|0\rangle-|1\rangle
]

は：

```text
別状態
```

です。

試験頻出ポイントです。

---

# 13. 複素数が出てくる理由

例：

```text
[0.707+0j, 0.707j]
```

意味：

```text
虚数位相を持つ
```

状態です。

つまり：

```text
回転方向の違い
```

を表しています。

---

# 14. 確率計算の例

例：

```text
[0.6, 0.8]
```

確率：

| state | probability |
| ----- | ----------- |
| 0     | 0.36        |
| 1     | 0.64        |

---

# 15. 2量子ビット確率例

例：

```text
[0.5, 0.5, 0.5, 0.5]
```

確率：

| state | probability |
| ----- | ----------- |
| 00    | 0.25        |
| 01    | 0.25        |
| 10    | 0.25        |
| 11    | 0.25        |

---

# 16. Statevectorから測定結果を予測する方法

手順：

Step1：

```text
振幅を見る
```

Step2：

```text
2乗する
```

Step3：

```text
確率を得る
```

---

# 17. 試験によく出る問題

問題：

```
[1,0]
```

意味：

```text
|0⟩
```

---

問題：

```
[0,1]
```

意味：

```text
|1⟩
```

---

問題：

```
[1/√2, 1/√2]
```

意味：

```text
(|0⟩+|1⟩)/√2
```

---

問題：

```
[1/√2, -1/√2]
```

意味：

```text
(|0⟩-|1⟩)/√2
```

---

# 18. 2量子ビット問題（重要）

問題：

```
[0,0,1,0]
```

意味：

```text
|10⟩
```

---

問題：

```
[0,1,0,0]
```

意味：

```text
|01⟩
```

---

# 19. Bell状態判定問題

問題：

```
[0.707,0,0,0.707]
```

答え：

```text
(|00⟩+|11⟩)/√2
```

＝ entangled

---

問題：

```
[0.707,0.707,0,0]
```

答え：

```text
(|00⟩+|01⟩)/√2
```

＝ separable

---

# 20. separableかどうかの見分け方（試験頻出）

次の形なら：

[
(a|0\rangle+b|1\rangle)\otimes(c|0\rangle+d|1\rangle)
]

```text
separable
```

それ以外：

```text
entangled
```

---

# 21. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ Statevectorを読める
✅ 振幅から確率を計算できる
✅ global phase を説明できる
✅ relative phase を説明できる
✅ 2量子ビット配列順序を理解している
✅ Bell状態を判定できる

---

次章：

**13_measurement.md**

では：

```text
測定の数理
collapseとは何か
部分測定
古典レジスタとの関係
```

を扱います。

ここは **measurement問題の正答率を決める核心領域**です。
