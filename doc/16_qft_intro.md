では第16章として、**量子フーリエ変換（QFT: Quantum Fourier Transform）入門**を資格試験対策レベルで体系的に解説します。

この章はシリーズの中でも特に重要です。理由：

```text
Shor
Phase Estimation
量子周期検出
量子信号処理
```

すべての核心に **QFT** があるからです 🚀

また IBM Qiskit資格試験でも：

* QFT回路構造
* CPゲートの並び
* bit reversal
* classical FFTとの違い

が頻出です。

---

# 16_qft_intro.md

# Part 16：量子フーリエ変換（QFT）を完全に理解する

まず最初に：

```text
QFT = 量子版フーリエ変換
```

ですが、本質は：

```text
確率を変換するのではなく
位相を変換する
```

操作です。

---

# 1. フーリエ変換とは何か（直感）

古典フーリエ変換：

```text
時間 → 周波数
```

への変換でした。

例：

| 入力 | 出力   |
| -- | ---- |
| 波形 | 周期構造 |

---

# 2. QFTとは何か

QFTは：

```text
振幅ではなく
位相構造を変換する
```

操作です。

数学的には：

QFT|x\rangle=\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1} e^{2\pi i xk/N}|k\rangle

意味：

```text
入力状態 |x⟩ を
位相重ね合わせ状態へ変換する
```

---

# 3. なぜQFTが重要なのか ⭐

理由：

量子アルゴリズムでは：

```text
周期を見つける
```

ことが鍵になるからです。

例：

| アルゴリズム           | 目的    |
| ---------------- | ----- |
| Shor             | 周期検出  |
| Phase estimation | 固有値抽出 |
| QPE              | 位相推定  |

---

# 4. classical FFTとの違い

比較：

|      | FFT        | QFT         |
| ---- | ---------- | ----------- |
| 計算対象 | 数列         | 量子状態        |
| 計算量  | O(N log N) | O((log N)²) |
| 操作対象 | 値          | 位相          |

つまり：

```text
指数的高速化が可能
```

になります。

---

# 5. QFT回路の基本構造

QFTは：

```text
Hadamard
+
Controlled Phase
```

だけで構成されます。

つまり：

```text
H + CP の繰り返し
```

です。

---

# 6. 2量子ビットQFT回路

構造：

```text
q0 ──H────CP(π/2)────
                     │
q1 ─────────H────────
```

最後に：

```text
SWAP
```

が入ります。

---

# 7. なぜSWAPが必要なのか

理由：

QFTの出力は：

```text
bit順序が逆転する
```

からです。

つまり：

```text
bit reversal
```

が起きます。

---

# 8. bit reversalとは何か

例：

入力：

```text
|q0 q1 q2⟩
```

出力：

```text
|q2 q1 q0⟩
```

になります。

そのため：

```text
SWAPで順序を戻す
```

必要があります。

---

# 9. 3量子ビットQFT回路構造

構造：

```text
q0 ──H──CP(π/2)──CP(π/4)────
            │         │
q1 ─────H──CP(π/2)──────
                  │
q2 ─────────────H──────
```

最後：

```text
SWAP(q0,q2)
```

---

# 10. 位相角の規則性

重要パターン：

| 距離 | 位相  |
| -- | --- |
| 1  | π/2 |
| 2  | π/4 |
| 3  | π/8 |

つまり：

```text
距離が倍になると角度は半分
```

です。

試験頻出です 📌

---

# 11. 一般n量子ビットQFT

一般構造：

```text
for each qubit:
    H
    CP(π/2)
    CP(π/4)
    CP(π/8)
    ...
```

つまり：

```text
指数減衰位相回転列
```

になります。

---

# 12. QiskitでQFTを書く

例：

```python
from qiskit.circuit.library import QFT

qc = QFT(3)

qc.draw("text")
```

簡単ですが非常に重要です。

---

# 13. 手動実装QFT

例：

```python
from numpy import pi
from qiskit import QuantumCircuit

qc = QuantumCircuit(3)

qc.h(0)
qc.cp(pi/2, 0, 1)
qc.cp(pi/4, 0, 2)

qc.h(1)
qc.cp(pi/2, 1, 2)

qc.h(2)
```

最後：

```python
qc.swap(0,2)
```

を追加します。

---

# 14. なぜHadamardから始まるのか

理由：

Hadamardは：

```text
基底変換
```

だからです。

つまり：

```text
計算基底 → フーリエ基底
```

への変換を行います。

---

# 15. Controlled Phaseの役割

CPは：

```text
位相差を埋め込む
```

役割があります。

つまり：

```text
入力値の情報を位相として保存
```

します。

---

# 16. QFTの直感理解

処理の流れ：

```text
入力値
↓
位相へ変換
↓
干渉発生
↓
周期抽出可能
```

これが：

```text
量子高速化の核心
```

です。

---

# 17. inverse QFTとは何か

inverse QFT：

```text
QFTの逆変換
```

です。

書き方：

```python
QFT(3).inverse()
```

用途：

```text
Phase estimation
```

で必須です。

---

# 18. QFTの計算量

古典：

```text
O(N log N)
```

量子：

```text
O((log N)^2)
```

つまり：

```text
指数高速化
```

が可能です。

---

# 19. 試験によく出る問題

問題：

QFTの構成要素は？

答え：

```text
Hadamard + Controlled Phase
```

---

問題：

CP角度の並びは？

答え：

```text
π/2 → π/4 → π/8
```

---

問題：

QFT最後に必要な操作は？

答え：

```text
SWAP
```

---

問題：

SWAPの理由は？

答え：

```text
bit reversal補正
```

---

# 20. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ QFTの目的を説明できる
✅ H + CP構造を説明できる
✅ 位相角の規則を説明できる
✅ bit reversalを説明できる
✅ inverse QFTを説明できる
✅ QFTの計算量を説明できる

---

次章：

**17_qpe.md**

では：

```text
Quantum Phase Estimation
固有値抽出
phase kickback応用
Shorアルゴリズムの核心
```

を扱います。

ここからいよいよ：

```text
実用量子アルゴリズム領域
```

に入ります 🔬
