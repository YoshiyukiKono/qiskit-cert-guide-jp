では第21章として、**Qiskit Runtime Primitives（Sampler / Estimator / Runtime execution）**を資格試験対策レベルで体系的に解説します。

ここは **最新のIBM Qiskit資格試験で最重要領域の一つ**です。理由：

```text id="r4m9qs"
旧 execute() API は現在の主流ではない
```

ため、

```text id="k7v2dn"
Sampler / Estimator を理解しているか
```

が評価されます。

---

# 21_runtime_primitives.md

# Part 21：Runtime Primitives（Sampler / Estimator）を完全に理解する

まず結論：

```text id="a8t3pm"
Primitive = 量子計算の標準インターフェース
```

です。

---

# 1. なぜPrimitiveが必要なのか

従来：

```python id="xv3mpo"
backend.run(circuit)
```

でした。

現在：

```text id="k9y2fr"
Sampler
Estimator
```

が推奨されています。

理由：

```text id="f3n6zc"
抽象化された計算モデル
```

だからです。

---

# 2. Primitiveとは何か

Primitive：

```text id="t6m1pa"
量子計算の基本操作単位
```

です。

2種類あります：

| Primitive | 用途     |
| --------- | ------ |
| Sampler   | 測定結果取得 |
| Estimator | 期待値計算  |

---

# 3. Samplerとは何か

Sampler：

```text id="x8q4zs"
測定確率分布を返す
```

Primitiveです。

つまり：

```text id="g2r7kn"
counts を取得する
```

役割です。

---

# 4. Samplerの基本構文

例：

```python id="6zvx6x"
from qiskit.primitives import Sampler

sampler = Sampler()

job = sampler.run(circuit)

result = job.result()
```

---

# 5. Samplerの出力

出力：

```text id="v7t4pm"
quasi-probability distribution
```

です。

例：

```text id="y3c6ks"
{00:0.5, 11:0.5}
```

---

# 6. quasi-probabilityとは何か

特徴：

```text id="q9k2fd"
負値を持つ可能性がある
```

理由：

```text id="c7m5rn"
誤差補正処理を含む
```

ためです。

---

# 7. Estimatorとは何か

Estimator：

```text id="j5w3mx"
期待値を計算する
```

Primitiveです。

例：

[
\langle Z \rangle
]

などを計算します。

---

# 8. Estimatorの基本構文

例：

```python id="0p7ktl"
from qiskit.primitives import Estimator

estimator = Estimator()

job = estimator.run(circuit, observable)

result = job.result()
```

---

# 9. observableとは何か

observable：

```text id="v2q9nb"
測定対象演算子
```

です。

例：

```text id="u6t3ks"
Z
X
ZZ
XX
```

など。

---

# 10. なぜEstimatorが重要なのか

理由：

以下で必須：

```text id="f4x2rm"
VQE
QAOA
量子機械学習
```

---

# 11. SamplerとEstimatorの違い

比較：

|     | Sampler | Estimator |
| --- | ------- | --------- |
| 出力  | 確率分布    | 期待値       |
| 用途  | 測定結果    | 演算子評価     |
| 使用例 | Grover  | VQE       |

試験頻出です 📌

---

# 12. Runtimeとは何か

Runtime：

```text id="s3n6kw"
クラウド側で量子計算を実行する仕組み
```

です。

つまり：

```text id="p7x5zs"
量子計算をサーバー側に移動
```

します。

---

# 13. なぜRuntimeが必要なのか

理由：

```text id="n4k2dp"
通信遅延削減
```

です。

従来：

```text id="r9m3jq"
送信
↓
実行
↓
取得
↓
再送信
```

Runtime：

```text id="k1t8vx"
まとめて実行
```

できます。

---

# 14. Qiskit Runtimeの構造

構造：

```text id="d6y7mz"
local client
↓
IBM cloud runtime
↓
quantum hardware
```

---

# 15. Runtime Sessionとは何か

Session：

```text id="z5r3nc"
連続ジョブをまとめて実行
```

します。

例：

```python id="x8y7pt"
with Session(service=service, backend=backend):
```

---

# 16. なぜSessionが重要なのか

理由：

```text id="h6w9qs"
queue待ち削減
```

です。

つまり：

```text id="k4v2mt"
高速実行可能
```

になります。

---

# 17. Primitive + Runtimeの統合モデル

現在の標準構造：

```text id="p3x7dn"
Sampler
Estimator
+
Runtime Session
```

です。

---

# 18. 実機実行例（Sampler）

例：

```python id="r6t9ks"
from qiskit_ibm_runtime import Sampler

sampler = Sampler(backend)

sampler.run(circuit)
```

---

# 19. 実機実行例（Estimator）

例：

```python id="q4m2wr"
from qiskit_ibm_runtime import Estimator

estimator = Estimator(backend)

estimator.run(circuit, observable)
```

---

# 20. Runtimeのメリットまとめ

特徴：

| 特徴 | 内容            |
| -- | ------------- |
| 高速 | queue削減       |
| 効率 | 通信削減          |
| 柔軟 | iterative計算対応 |

---

# 21. 試験によく出る問題

問題：

Samplerの役割は？

答え：

```text id="c8v4zt"
測定確率分布取得
```

---

問題：

Estimatorの役割は？

答え：

```text id="j2w6yr"
期待値計算
```

---

問題：

observableとは？

答え：

```text id="t7k3ns"
測定対象演算子
```

---

問題：

Sessionの目的は？

答え：

```text id="r1p6mx"
連続ジョブ高速化
```

---

# 22. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ Samplerを説明できる
✅ Estimatorを説明できる
✅ observableを説明できる
✅ Runtimeの役割を説明できる
✅ Sessionの役割を説明できる
✅ Primitive APIの目的を説明できる

---

次章（最終章）：

**22_exam_strategy.md**

では：

```text id="p4z7nm"
試験頻出テーマ整理
出題パターン分類
最短合格ルート
演習問題セット
```

を扱います。

ここで：

```text id="x2c6qp"
資格試験対策シリーズ完成
```

になります。
