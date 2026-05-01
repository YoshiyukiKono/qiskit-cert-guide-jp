では第20章として、**QAOA（Quantum Approximate Optimization Algorithm）**を資格試験対策レベルで体系的に解説します。

この章は：

```text id="oqk4yb"
VQEの応用版
```

とも言えるアルゴリズムで、

```text id="txj5mn"
組合せ最適化問題
```

を量子回路で解く代表例です。

IBM Qiskit資格試験でも：

* cost Hamiltonian
* mixer Hamiltonian
* パラメータ層構造
* MaxCut問題
* variational algorithm の理解

が重要です。

---

# 20_qaoa.md

# Part 20：QAOA（Quantum Approximate Optimization Algorithm）を完全に理解する

まず結論：

```text id="sd7w21"
QAOA = 最適化問題を解く変分量子アルゴリズム
```

です。

---

# 1. どんな問題を解くのか

例：

```text id="r5u1jb"
MaxCut問題
```

です。

グラフ：

```
A ---- B
 \    /
  \  /
   C
```

目的：

```text id="p4c6ye"
できるだけ多くの辺を分断する
```

ようにノードを2グループへ分けます。

---

# 2. なぜ量子で解くのか

古典：

```text id="h7t9mf"
NP-hard
```

問題です。

QAOA：

```text id="v1g3re"
近似解を高速に見つける
```

ことができます。

---

# 3. QAOAの基本構造

構造：

```text id="x8c2df"
initial state
↓
cost Hamiltonian
↓
mixer Hamiltonian
↓
repeat
↓
measurement
```

---

# 4. cost Hamiltonianとは何か

cost Hamiltonian：

```text id="k3n5wd"
問題を量子形式に変換したもの
```

です。

例：

MaxCut：

[
H_C=\sum_{(i,j)\in E} \frac{1-Z_iZ_j}{2}
]

意味：

```text id="f6d9pm"
異なるグループならスコア加算
```

---

# 5. mixer Hamiltonianとは何か

mixer：

```text id="w2q8ls"
探索空間を移動する操作
```

です。

代表例：

[
H_M=\sum_i X_i
]

つまり：

```text id="n8j4yr"
bit flip 操作
```

です。

---

# 6. QAOA回路構造

1層：

```text id="j5t7gh"
exp(-iγHc)
↓
exp(-iβHm)
```

を実行します。

---

# 7. なぜ指数演算子が出てくるのか

量子時間発展：

genui{"math_block_widget_always_prefetch_v2": {"content": "U=e^{-iHt}"}}

と同じ構造だからです。

つまり：

```text id="r9k3yb"
Hamiltonian evolution
```

です。

---

# 8. γとβとは何か

パラメータ：

| 記号 | 意味       |
| -- | -------- |
| γ  | cost回転角  |
| β  | mixer回転角 |

これを：

```text id="d4h7mz"
classical optimizer
```

で調整します。

---

# 9. p層QAOAとは何か

p層：

```text id="n5k3zs"
(cost → mixer) × p回
```

です。

例：

```text id="z2w9mf"
p=3
```

なら：

```text id="a7k5yd"
6回回転
```

になります。

---

# 10. pが増えるとどうなるか

特徴：

| p   | 精度 |
| --- | -- |
| 小さい | 速い |
| 大きい | 正確 |

つまり：

```text id="f4g9yc"
精度と計算量のトレードオフ
```

です。

---

# 11. QAOAの直感理解

処理：

```text id="k7t3px"
候補状態生成
↓
良い解を強調
↓
探索
↓
繰り返し
```

---

# 12. VQEとの違い

比較：

|             | VQE   | QAOA  |
| ----------- | ----- | ----- |
| 対象          | 固有値問題 | 最適化問題 |
| Ansatz      | 任意    | 構造付き  |
| Hamiltonian | 物理系   | コスト関数 |

---

# 13. MaxCutの回路例

2ノード：

[
H_C=\frac{1-Z_0Z_1}{2}
]

回路：

```text id="w3q6fr"
CZ回転
+
RX回転
```

で実装されます。

---

# 14. QiskitでQAOAを書く

例：

```python id="3g0cjh"
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.algorithms.optimizers import COBYLA
```

構成：

```python id="7f92zk"
qaoa = QAOA(optimizer=COBYLA(), reps=2)
```

---

# 15. repsとは何か

reps：

```text id="z5n7pv"
p層数
```

です。

つまり：

```text id="f1k8hz"
回路深さ
```

を意味します。

---

# 16. なぜQAOAが重要なのか

理由：

```text id="d6t3kx"
NISQで動く最適化アルゴリズム
```

だからです。

応用：

| 分野   | 問題      |
| ---- | ------- |
| 物流   | 配送      |
| 金融   | ポートフォリオ |
| 回路設計 | 配線最適化   |
| AI   | 組合せ探索   |

---

# 17. cost Hamiltonianの役割

役割：

```text id="v9p6rm"
良い解に位相を与える
```

です。

つまり：

```text id="r2c4jf"
phase encoding
```

です。

---

# 18. mixer Hamiltonianの役割

役割：

```text id="n7t1ks"
探索空間を移動
```

です。

つまり：

```text id="p3q8xb"
状態遷移
```

です。

---

# 19. 試験によく出る問題

問題：

QAOAは何の問題を解く？

答え：

```text id="y5w7ln"
組合せ最適化問題
```

---

問題：

γの役割は？

答え：

```text id="h6r3zx"
cost回転角
```

---

問題：

βの役割は？

答え：

```text id="t9m2df"
mixer回転角
```

---

問題：

repsとは？

答え：

```text id="x4p8ks"
層数
```

---

# 20. QAOAの流れまとめ

処理：

```text id="m7n2wd"
初期状態
↓
cost evolution
↓
mixer evolution
↓
測定
↓
optimizer更新
```

---

# 21. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ QAOAの目的を説明できる
✅ cost Hamiltonianを説明できる
✅ mixer Hamiltonianを説明できる
✅ γとβを説明できる
✅ repsの意味を説明できる
✅ VQEとの違いを説明できる

---

次章：

**21_runtime_primitives.md**

では：

```text id="c6y4mk"
Sampler primitive
Estimator primitive
Runtime execution
クラウド量子実行モデル
```

を扱います。

ここで：

```text id="v8q2tg"
最新Qiskit API体系
```

が完成します。
