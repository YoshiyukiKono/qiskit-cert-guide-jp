では第19章として、**VQE（Variational Quantum Eigensolver）**を資格試験対策レベルで体系的に解説します。

この章はこれまで扱った：

* QFT
* QPE
* Grover

とは違い、

```text id="t2k4mf"
NISQ時代に実際に使われるアルゴリズム
```

です。

IBM Qiskit資格試験でも：

* ハイブリッド量子アルゴリズム
* パラメータ付き回路
* 期待値最小化
* classical optimizer の役割

が重要論点として出題されます。

---

# 19_vqe.md

# Part 19：VQE（Variational Quantum Eigensolver）を完全に理解する

まず結論から：

```text id="3h8kqp"
VQE = 固有値を近似的に求めるアルゴリズム
```

です。

特に：

```text id="9jw2ls"
ハミルトニアンの最小固有値
```

を求めます。

---

# 1. どんな問題を解くのか

VQEは次を解きます：

H|\psi\rangle=E|\psi\rangle

ここで：

| 記号 | 意味         |
| -- | ---------- |
| H  | ハミルトニアン    |
| ψ  | 固有状態       |
| E  | 固有値（エネルギー） |

目的：

```text id="oz7g4m"
最小固有値 Emin を求める
```

です。

---

# 2. なぜ重要なのか

理由：

多くの現実問題は：

```text id="ph8w6y"
最低エネルギー状態を求める問題
```

に帰着するからです。

例：

| 分野   | 問題       |
| ---- | -------- |
| 化学   | 分子基底状態   |
| 材料科学 | 安定構造     |
| 量子物理 | 基底エネルギー  |
| 最適化  | コスト関数最小化 |

---

# 3. なぜQPEではなくVQEを使うのか

QPE：

```text id="u5r3mk"
高精度
```

しかし：

```text id="9nt6sb"
深い回路が必要
```

VQE：

```text id="hx9m7d"
浅い回路で動く
```

つまり：

```text id="rq2k6p"
NISQ向け
```

です。

---

# 4. VQEの基本構造

処理フロー：

```text id="b3p7tf"
parameterized circuit
↓
measurement
↓
期待値計算
↓
classical optimizer
↓
パラメータ更新
↓
repeat
```

---

# 5. ハイブリッドアルゴリズムとは何か

VQEは：

```text id="m4s2ya"
量子 + 古典
```

で動作します。

役割分担：

| 処理   | 担当 |
| ---- | -- |
| 状態生成 | 量子 |
| 測定   | 量子 |
| 最適化  | 古典 |

---

# 6. パラメータ付き回路とは何か

例：

```python
qc.ry(theta, 0)
```

ここで：

```text id="v2x6lb"
θ を調整する
```

ことで：

```text id="p5r8hk"
状態を変化させる
```

ことができます。

---

# 7. variational principle（変分原理）

VQEの理論基盤：

E(\theta)=\langle \psi(\theta)|H|\psi(\theta)\rangle

重要：

```text id="a7m9dj"
この値は必ず真の基底エネルギー以上
```

になります。

つまり：

```text id="c2f5wr"
最小化すれば基底状態に近づく
```

---

# 8. VQEの直感理解

処理：

```text id="w9p3mz"
回路を仮定
↓
測定
↓
エネルギー計算
↓
パラメータ調整
↓
繰り返し
```

---

# 9. classical optimizerの役割

optimizerは：

```text id="r1h8xy"
θ を更新する
```

装置です。

例：

| optimizer        | 特徴    |
| ---------------- | ----- |
| COBYLA           | 微分不要  |
| SPSA             | ノイズ耐性 |
| Gradient descent | 高速収束  |

---

# 10. なぜgradient不要optimizerが重要か

理由：

量子測定は：

```text id="t4j6sv"
ノイズを含む
```

ため：

```text id="x3k7pu"
微分が難しい
```

からです。

---

# 11. Ansatzとは何か

Ansatz：

```text id="k8q1vz"
状態の仮定モデル
```

です。

例：

```python
RealAmplitudes(2)
```

意味：

```text id="n6w4fj"
探索する状態空間を制限
```

します。

---

# 12. 良いAnsatzの条件

条件：

```text id="d3m9rb"
表現力が高い
```

かつ

```text id="p2j5ts"
回路が浅い
```

---

# 13. ハミルトニアン分解とは何か

ハミルトニアン：

例：

```text id="y7z4kg"
H = Z₀ + Z₁ + X₀X₁
```

のように：

```text id="m5c8lw"
Pauli演算子の和
```

として書けます。

---

# 14. なぜ分解が必要なのか

理由：

量子コンピュータは：

```text id="q8h2tr"
Pauli演算子しか直接測定できない
```

からです。

---

# 15. 期待値計算の流れ

例：

```text id="j6k3dp"
⟨Z₀⟩
⟨Z₁⟩
⟨X₀X₁⟩
```

を測定し：

```text id="z9v4yn"
加算
```

します。

---

# 16. QiskitでVQEを書く

例：

```python
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.circuit.library import RealAmplitudes
from qiskit.algorithms.optimizers import COBYLA
```

構成：

```python
ansatz = RealAmplitudes(2)

optimizer = COBYLA()

vqe = VQE(ansatz, optimizer)
```

---

# 17. Primitive APIとの関係

新しいQiskitでは：

```text id="r7d6jq"
Estimator primitive
```

を使います。

理由：

```text id="x5c9pf"
期待値計算を抽象化
```

するためです。

---

# 18. VQEのメリット

特徴：

| 特徴    | 内容     |
| ----- | ------ |
| 浅い回路  | NISQ対応 |
| ノイズ耐性 | 高い     |
| 柔軟性   | 高い     |

---

# 19. VQEのデメリット

課題：

| 課題          | 内容    |
| ----------- | ----- |
| 局所最適解       | 落ちやすい |
| Ansatz依存    | 強い    |
| optimizer依存 | 強い    |

---

# 20. 試験によく出る問題

問題：

VQEは何を求める？

答え：

```text id="b6n3tw"
最小固有値
```

---

問題：

VQEはどんなアルゴリズム？

答え：

```text id="p4x8ks"
ハイブリッド量子古典アルゴリズム
```

---

問題：

Ansatzとは？

答え：

```text id="w2c5fy"
状態の仮定回路
```

---

問題：

optimizerの役割は？

答え：

```text id="g9m1zr"
パラメータ更新
```

---

# 21. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ VQEの目的を説明できる
✅ ハイブリッド構造を説明できる
✅ Ansatzの意味を説明できる
✅ optimizerの役割を説明できる
✅ Pauli分解の意味を説明できる
✅ Estimator primitiveとの関係を説明できる

---

次章：

**20_qaoa.md**

では：

```text id="x7t3qa"
QAOA
組合せ最適化
MaxCut問題
cost Hamiltonian
mixer Hamiltonian
```

を扱います。

ここで：

```text id="k4v9hn"
量子最適化アルゴリズム
```

の体系が完成します。
