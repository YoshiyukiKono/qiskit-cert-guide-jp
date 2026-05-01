では第15章として、**Controlled Phase ゲート（CU / CRZ / CP）と位相制御回路**を資格試験対策レベルで体系的に解説します。

この章は：

```text
QFT
Phase Estimation
Shor
Grover拡張版
```

などのアルゴリズム理解の入口になります。

特に重要なのは：

```text
制御された位相は「確率ではなく干渉」を操作する
```

という点です。

---

# 15_controlled_phase.md

# Part 15：Controlled Phase（CU / CRZ / CP）を完全に理解する

ここまでで：

* Z
* S
* T
* CZ
* phase kickback

を理解しました。

ここからは：

```text
制御付き位相回転
```

を扱います。

---

# 1. Controlled Phaseとは何か

Controlled Phase：

```text
control=1 のときだけ位相回転
```

です。

一般形：

CP(\theta)|11\rangle=e^{i\theta}|11\rangle

それ以外：

```text
変化なし
```

---

# 2. CZは特殊ケース

CZは：

CP(\pi)=CZ

つまり：

```text
θ = π
```

のケースです。

---

# 3. CRZゲートとは何か

CRZ：

```text
control=1 のときだけ
```

targetに：

```text
RZ(θ)
```

を適用します。

数式：

CRZ(\theta)|11\rangle=e^{i\theta}|11\rangle

---

# 4. CPとCRZの違い

重要：

| ゲート | 位相対象   |
| --- | ------ |
| CP  | 全体     |
| CRZ | target |

試験で区別が問われます。

---

# 5. QiskitでのCPゲート

例：

```python
qc.cp(theta, control, target)
```

例：

```python
qc.cp(3.1415/2, 0, 1)
```

意味：

```text
90度回転
```

---

# 6. CRZの書き方

例：

```python
qc.crz(theta, 0, 1)
```

---

# 7. Controlled-Uゲートとは何か

一般形：

CU|1\rangle|\psi\rangle=|1\rangle U|\psi\rangle

つまり：

```text
control=1 のときだけ
任意ユニタリ適用
```

---

# 8. なぜControlled-Uが重要なのか

理由：

```text
量子アルゴリズムの基本構造
```

だからです。

例：

* Phase estimation
* QFT
* Shor

すべて：

```text
controlled-U
```

で構成されます。

---

# 9. phase kickbackとの関係

Controlled Phaseは：

```text
phase kickback を発生させる装置
```

です。

例：

回路：

```
|+⟩ ──■──
       │
|1⟩ ──RZ─
```

結果：

```text
control に位相が戻る
```

---

# 10. 位相情報をcontrol側へ書き込む

重要：

```text
targetではなく
controlに情報が移動する
```

これが：

```text
phase estimation の基礎
```

です。

---

# 11. CPゲートの行列表現（試験対応）

行列：

[
CP(\theta)=
\begin{pmatrix}
1&0&0&0
\
0&1&0&0
\
0&0&1&0
\
0&0&0&e^{i\theta}
\end{pmatrix}
]

つまり：

```text
|11⟩だけ回転
```

---

# 12. Controlled-S / Controlled-T

特殊例：

| ゲート | 角度  |
| --- | --- |
| CS  | π/2 |
| CT  | π/4 |

つまり：

```text
CP(π/2)=CS
```

```text
CP(π/4)=CT
```

---

# 13. 多段Controlled Phase

例：

```python
qc.cp(pi/2, q0, q1)
qc.cp(pi/4, q0, q2)
qc.cp(pi/8, q0, q3)
```

これは：

```text
QFTの基本構造
```

です。

---

# 14. 位相を角度として扱う理由

量子計算では：

```text
数値 = 位相
```

として保存します。

例：

```
2進数
↓
位相回転
↓
干渉
↓
測定
```

---

# 15. QFTとの関係

QFTでは：

```text
H + Controlled Phase
```

だけで構成されます。

つまり：

```text
Controlled Phase = QFTの核心
```

です。

---

# 16. Controlled Phaseの直感理解

CNOT：

```text
bit flip
```

Controlled Phase：

```text
phase flip
```

です。

つまり：

| ゲート | 操作 |
| --- | -- |
| CX  | 振幅 |
| CP  | 位相 |

---

# 17. 干渉制御の例

回路：

```
H
↓
CP(π)
↓
H
```

結果：

```text
出力が変化する
```

理由：

```text
relative phase が変わる
```

ためです。

---

# 18. Qiskit実例

例：

```python
from qiskit import QuantumCircuit
from numpy import pi

qc = QuantumCircuit(2)

qc.h(0)
qc.cp(pi/2, 0, 1)
qc.h(0)

qc.draw("text")
```

---

# 19. 試験によく出る問題

問題：

CP(θ)が変化させる状態は？

答え：

```text
|11⟩
```

---

問題：

CZはCPの何？

答え：

```text
θ=π
```

---

問題：

Controlled-Uとは？

答え：

```text
control=1のときだけU適用
```

---

問題：

phase kickbackの役割は？

答え：

```text
位相情報をcontrol側へ移動
```

---

# 20. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ CPゲートの意味を説明できる
✅ CRZゲートの意味を説明できる
✅ CUゲートを説明できる
✅ CZ=CP(π) を理解している
✅ phase kickbackとの関係を説明できる
✅ QFTとの関係を説明できる

---

次章：

**16_qft_intro.md**

では：

```text
量子フーリエ変換とは何か
なぜ高速なのか
回路構造
Controlled Phaseの並び方
bit reversal
```

を扱います。

ここから：

```text
Shorアルゴリズム理解の入口
```

に入ります。
