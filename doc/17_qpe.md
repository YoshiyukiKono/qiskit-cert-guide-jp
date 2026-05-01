では第17章として、**Quantum Phase Estimation（QPE：量子位相推定）**を資格試験対策レベルで体系的に解説します。

この章はシリーズ全体の中でも最重要クラスです。理由：

```text id="e5lm94"
Shor
VQE
HHL
量子シミュレーション
```

など多くのアルゴリズムの基盤が **QPE** だからです。

また IBM Qiskit資格試験でも：

* phase kickback の理解
* inverse QFT の役割
* 固有値問題の構造
* 制御付きユニタリ

が頻出です。

---

# 17_qpe.md

# Part 17：Quantum Phase Estimation（QPE）を完全に理解する

まず最初に：

```text id="wm8q8t"
QPE = 位相を測定するアルゴリズム
```

です。

もう少し正確に言うと：

```text id="b5k7m8"
ユニタリ演算の固有値を求めるアルゴリズム
```

です。

---

# 1. QPEが解く問題

QPEは次を解きます：

U|\psi\rangle=e^{2\pi i\phi}|\psi\rangle

ここで：

| 記号 | 意味     |
| -- | ------ |
| U  | ユニタリ演算 |
| ψ  | 固有ベクトル |
| φ  | 固有位相   |

QPEの目的：

```text id="b0hzp5"
φ を求める
```

です。

---

# 2. なぜ位相を求めたいのか

理由：

多くの問題は：

```text id="rxu36o"
固有値問題
```

に帰着できるからです。

例：

| 問題       | 固有値     |
| -------- | ------- |
| Shor     | 周期      |
| HHL      | 線形方程式   |
| VQE      | エネルギー   |
| シミュレーション | ハミルトニアン |

---

# 3. QPEの回路構造

基本構造：

```text id="c8p0i5"
Hadamard
↓
Controlled-U
↓
inverse QFT
↓
measurement
```

です。

---

# 4. なぜHadamardを使うのか

Hadamard：

```text id="5y3i0r"
superposition を作る
```

つまり：

```text id="v6e3ql"
複数の位相を同時に取得
```

できます。

---

# 5. Controlled-Uの役割

Controlled-U：

```text id="qz2y68"
位相を書き込む
```

装置です。

つまり：

```text id="rv5qf1"
phase kickback を発生させる
```

---

# 6. 位相がcontrol側に戻る仕組み

状態：

```text id="l3m3nl"
|+⟩|ψ⟩
```

に：

```text id="8rs8dp"
CU
```

を適用すると：

```text id="4f6tmu"
controlに位相が現れる
```

これが：

```text id="r1pnyc"
phase kickback
```

です。

---

# 7. なぜinverse QFTが必要なのか

phase kickback後：

```text id="snv6hn"
位相は重ね合わせ状態
```

として存在します。

inverse QFT：

```text id="mb6c4l"
位相 → bit列
```

に変換します。

---

# 8. QPEの処理フローまとめ

流れ：

```text id="hbd9oy"
Hadamard
↓
phase kickback
↓
inverse QFT
↓
measurement
```

---

# 9. 2ビットQPEの例

例：

```text id="h3c2jv"
φ = 0.25
```

なら：

```text id="j63ncs"
0.01（二進数）
```

として出力されます。

つまり：

```text id="5c4r4p"
位相をbit列として取得
```

できます。

---

# 10. 精度はどう決まるか

重要：

```text id="zkn9xa"
使用するqubit数
```

で決まります。

例：

| qubit数 | 精度   |
| ------ | ---- |
| 2      | 1/4  |
| 3      | 1/8  |
| 4      | 1/16 |

つまり：

```text id="bdrmzw"
指数精度向上
```

します。

---

# 11. Controlled-U² の意味

QPEでは：

```text id="63c7sq"
CU
CU²
CU⁴
CU⁸
```

を使います。

理由：

```text id="6h0fhi"
2進展開で位相を抽出
```

するためです。

---

# 12. なぜ指数的に増やすのか

例：

位相：

```text id="f06lsv"
0.101
```

を取得するには：

```text id="5q9i6o"
2⁰
2¹
2²
```

の情報が必要です。

---

# 13. QPE回路（概念図）

構造：

```text id="j35yb6"
q0 ──H──■──────────────
         │
q1 ──H──■────■─────────
         │    │
q2 ──H──■────■────■────
              │    │
ψ ────────────U────U²──U⁴
```

最後：

```text id="36jk09"
inverse QFT
```

---

# 14. QiskitでのQPE（簡易版）

例：

```python id="z8p2jr"
from qiskit.circuit.library import PhaseEstimation
```

使用：

```python id="0v1gn0"
PhaseEstimation(num_evaluation_qubits, unitary)
```

---

# 15. 手動実装の基本構造

構造：

```python id="9qfrmb"
qc.h(q0)
qc.h(q1)

qc.cu(U)
qc.cu(U**2)

inverse_qft()

measure()
```

---

# 16. QPEの直感理解

処理：

```text id="csgn9j"
固有値
↓
位相
↓
phase kickback
↓
inverse QFT
↓
bit列
```

---

# 17. なぜShorで重要なのか

Shorでは：

```text id="n7r0h4"
周期検出
```

を行います。

周期検出は：

```text id="2n36m7"
位相検出
```

と等価です。

つまり：

```text id="l8flk5"
Shor = QPE応用
```

です。

---

# 18. inverse QFTが出てくる理由（試験頻出）

QPE：

```text id="w0c2hy"
位相を重ね合わせとして保存
```

inverse QFT：

```text id="g9m3qa"
それをbit列へ変換
```

---

# 19. よく出る試験問題

問題：

QPEの目的は？

答え：

```text id="y2yfb1"
固有位相を求める
```

---

問題：

phase kickbackの役割は？

答え：

```text id="dxh5tz"
位相情報をcontrol側へ移動
```

---

問題：

inverse QFTの役割は？

答え：

```text id="8k44ra"
位相をbit列に変換
```

---

問題：

精度を上げる方法は？

答え：

```text id="4s2xdt"
qubit数を増やす
```

---

# 20. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ QPEの目的を説明できる
✅ 固有値問題との関係を説明できる
✅ phase kickbackの役割を説明できる
✅ inverse QFTの役割を説明できる
✅ CU²構造を説明できる
✅ Shorとの関係を説明できる

---

次章：

**18_grover.md**

では：

```text id="4l9gdy"
Groverアルゴリズム
振幅増幅
oracle
diffusion operator
```

を扱います。

ここから：

```text id="3nvl45"
探索問題の量子高速化
```

に入ります。
