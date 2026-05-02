
この章は：

* Zゲートとの関係
* 位相とは何か
* 測定では見えない情報
* 干渉で現れる差
* S / T / dagger の意味

まで理解する重要章です。

---

# 04_phase.md

# Part 4：位相ゲート（S / T）を完全に理解する

ここから量子計算の本質に入ります。

これまで：

* X = ビット反転
* Z = 符号反転

を学びました。

今回扱うのは：

```text
測定では見えないが計算を変える操作
```

＝位相ゲートです。

資格試験でも頻出です。

---

# 1. 位相とは何か

状態：

$$
|\psi\rangle=\frac{1}{\sqrt{2}}(|0\rangle+|1\rangle)
$$

と：

$$
|\psi\rangle=\frac{1}{\sqrt{2}}(|0\rangle-|1\rangle)
$$

は測定結果が同じ：

```text
50%
50%
```

しかし：

```text
計算結果は変わる
```

理由：

```text
位相が違う
```

---

# 2. 位相は複素数で表される

量子状態：

$$
|\psi\rangle=a|0\rangle+b|1\rangle
$$


ここで：

```text
a, b は複素数
```

例：

$$
|0\rangle+i|1\rangle
$$

確率：

```text
変わらない
```

理由：

```text
|i|^2 = 1
```

---

# 3. 位相ゲートとは何か

位相ゲートは：

```text
|1⟩ の振幅だけ回転させる
```

操作です。

つまり：

```text
確率を変えない
```

しかし：

```text
干渉を変える
```

---

# 4. Sゲート

Sゲートの作用：

$$
S|0\rangle=|0\rangle
$$

$$
S|1\rangle=i|1\rangle
$$


つまり：

```text
|1⟩ に i をかける
```

---

# 5. Sゲートの行列表現

行列：

$$
S=
\begin{pmatrix}
1 & 0 \
0 & i
\end{pmatrix}
$$

資格試験では：

```text
この行列の作用を読む問題
```

が出ます。

---

# 6. Qiskitで確認する

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(1)

qc.h(0)
qc.s(0)

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text
[0.707+0.j 0.+0.707j]
```

つまり：

```text
|1⟩ に i が付く
```

---

# 7. S†（Sダガー）

逆操作：

$$
S^\dagger
$$

作用：

$$
S^\dagger|1\rangle=-i|1\rangle
$$

関係：

$$
SS^{\dagger}=I
$$

---

# 8. Tゲート

Tゲートはさらに小さい位相回転です。

作用：

$$
T|1\rangle=e^{i\pi/4}|1\rangle
$$

つまり：

```text
45度回転
```

---

# 9. Tゲートの行列表現

$$
T=
\begin{pmatrix}
1 & 0 \
0 & e^{i\pi/4}
\end{pmatrix}
$$

特徴：

```text
Sより弱い回転
```

---

# 10. T†（Tダガー）

逆操作：

$$
T^\dagger
$$

作用：

$$
e^{-i\pi/4}
$$

関係：

$$
TT^\dagger=I
$$

---

# 11. 位相回転の関係まとめ

重要：

S=T^2

さらに：

Z=S^2

つまり：

```text
T → S → Z
```

と強くなる。

試験頻出です。

---

# 12. 位相は測定で見えない

例：

状態A：

$$
(|0\rangle+|1\rangle)/\sqrt{2}
$$

状態B：

$$
(|0\rangle+i|1\rangle)/\sqrt{2}
$$

測定結果：

```text
同じ
```

しかし：

```text
干渉結果が違う
```

---

# 13. Hと組み合わせると違いが見える

例：

```python
qc = QuantumCircuit(1)

qc.h(0)
qc.s(0)
qc.h(0)

state = Statevector.from_instruction(qc)

print(state)
```

ここで：

```text
結果が変わる
```

理由：

```text
位相が干渉に影響する
```

---

# 14. 位相キックバック（試験重要）

制御ゲートで：

```text
位相が別の量子ビットへ伝わる
```

これを：

```text
phase kickback
```

と呼びます。

Deutsch–JozsaやGroverで使われます。

---

# 15. よく出る試験問題

問題：

次の結果は？

```
S|1⟩
```

答え：

```
i|1⟩
```

---

問題：

次は？

```
T^2
```

答え：

```
S
```

---

問題：

次は？

```
S^2
```

答え：

```
Z
```

---

問題：

測定結果は変わるか？

```
(|0⟩+|1⟩)/√2
(|0⟩+i|1⟩)/√2
```

答え：

```
変わらない
```

---

# 16. この章のチェックリスト（合格基準）

次ができればOK：

✅ Sの作用を説明できる
✅ Tの作用を説明できる
✅ S = T² を理解している
✅ Z = S² を理解している
✅ 位相は測定で見えないと説明できる
✅ 位相が干渉に影響すると説明できる

---

次章：

**05_measurement.md**

では：

```text
なぜ測定すると状態が壊れるのか
shotsとは何か
countsの読み方
```

を扱います。

---



## コラム：ダガー（†）とは何か

量子ゲートに付く `†` は、基本的には「逆操作」を意味します。

Sゲートは `|1⟩` の位相を `i` だけ進めます。

```text
S|1⟩ = i|1⟩
````

S† はその逆で、位相を戻します。

```text
S†|1⟩ = -i|1⟩
```

そのため、SのあとにS†をかけると元に戻ります。

```text
SS† = I
```

ここで `I` は「何もしない操作」です。

Qiskitでは、S† は `sdg`、T† は `tdg` と書きます。

```python
qc.s(0)
qc.sdg(0)

qc.t(0)
qc.tdg(0)
```

つまり、ダガーは：

> このゲートを逆向きに戻すもの

と考えるとよいです。


数学的には「共役転置」ですが、最初は **undo記号** として理解するとかなり楽です。



