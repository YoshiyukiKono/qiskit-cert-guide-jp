では第18章として、**Groverアルゴリズム（振幅増幅：Amplitude Amplification）**を資格試験対策レベルで体系的に解説します。

この章は：

```text id="u3t8y7"
探索問題の量子高速化
```

の核心です。

IBM Qiskit資格試験でも：

* oracle の意味
* diffusion operator の役割
* √N高速化の理由
* 反復回数の決まり方

が頻出です。

---

# 18_grover.md

# Part 18：Groverアルゴリズムを完全に理解する

Groverアルゴリズムとは：

```text id="o2b7kx"
未整列探索を高速化する量子アルゴリズム
```

です。

古典計算：

```text id="r5z3qp"
O(N)
```

量子計算：

```text id="q0g6mj"
O(√N)
```

になります 🚀

---

# 1. どんな問題を解くのか

例：

```text id="q6f4ym"
N個の候補から正解を1つ見つける
```

古典：

```text id="h4q2df"
平均 N/2 回試行
```

Grover：

```text id="z6n3as"
√N 回
```

で見つかります。

---

# 2. なぜ高速化できるのか

理由：

```text id="d8v5lw"
正解状態の振幅だけ増幅する
```

からです。

つまり：

```text id="m1x7he"
確率ではなく振幅を操作する
```

のがポイントです。

---

# 3. Groverの基本構造

構造：

```text id="q4y2vc"
superposition
↓
oracle
↓
diffusion
↓
repeat
↓
measurement
```

です。

---

# 4. 初期状態の準備

最初に：

```text id="r7n5pk"
全状態の重ね合わせ
```

を作ります。

例：

2量子ビット：

[
|s\rangle=\frac{1}{2}(|00\rangle+|01\rangle+|10\rangle+|11\rangle)
]

これは：

```text id="w0k3bf"
均等確率分布
```

です。

---

# 5. oracleとは何か ⭐

oracleは：

```text id="g9l8jt"
正解だけ位相反転する装置
```

です。

例：

正解が |10⟩ の場合：

[
|10\rangle \rightarrow -|10\rangle
]

他は：

```text id="n4t6qs"
変化なし
```

---

# 6. oracleの役割

oracleは：

```text id="c8d2vr"
答えを教えない
```

が：

```text id="v5k3ha"
答えに印をつける
```

装置です。

重要な概念です ⭐

---

# 7. diffusion operatorとは何か

diffusion operator：

```text id="k2r8mw"
平均値に対する反転
```

です。

別名：

```text id="m9w1zc"
inversion about the mean
```

---

# 8. diffusion operatorの数式

Grover演算子：

G=(2|s\rangle\langle s|-I)O

ここで：

| 記号 | 意味     |    |           |
| -- | ------ | -- | --------- |
| O  | oracle |    |           |
| 2  | s⟩⟨s   | −I | diffusion |

---

# 9. diffusionの直感理解

処理：

```text id="f7k9dw"
平均より小さい振幅 → 増加
平均より大きい振幅 → 減少
```

結果：

```text id="j2v6pr"
正解振幅が増える
```

---

# 10. Grover反復とは何か

Grover iteration：

```text id="x4h9ne"
oracle
+
diffusion
```

のセットです。

つまり：

```text id="s3k8yb"
G = DO
```

---

# 11. 振幅はどう変化するのか

各反復で：

```text id="t8z6qm"
正解振幅が回転する
```

と考えます。

つまり：

```text id="y1d3fs"
確率空間で回転運動
```

が起きています。

---

# 12. 反復回数の決まり方

重要公式：

k\approx \frac{\pi}{4}\sqrt{N}

ここで：

| 記号 | 意味      |
| -- | ------- |
| k  | 反復回数    |
| N  | 探索空間サイズ |

試験頻出です 📌

---

# 13. なぜ繰り返しすぎるとダメなのか

理由：

```text id="b6t4qe"
振幅は回転しているだけ
```

だからです。

つまり：

```text id="m3w2hk"
最大値を超えると減少する
```

---

# 14. Groverの回路構造

構造：

```text id="g8z1dc"
H
↓
oracle
↓
H
↓
X
↓
multi-controlled Z
↓
X
↓
H
```

これが diffusion operator です。

---

# 15. diffusion operatorの分解

実際の形：

```text id="p2n6wy"
H⊗n
↓
X⊗n
↓
CZ
↓
X⊗n
↓
H⊗n
```

です。

試験でもよく問われます。

---

# 16. 2量子ビットGrover例

例：

探索空間：

```text id="r5c9ta"
|00⟩ |01⟩ |10⟩ |11⟩
```

正解：

```text id="w2f8mv"
|11⟩
```

手順：

```text id="k9x1gh"
H
↓
oracle
↓
diffusion
```

結果：

```text id="q4m7zu"
|11⟩ の確率最大
```

---

# 17. QiskitでGroverを書く

例：

```python
from qiskit.algorithms import Grover
from qiskit.circuit.library import PhaseOracle
```

使用：

```python
oracle = PhaseOracle("a & b")

grover = Grover(oracle)

result = grover.run()
```

---

# 18. oracleはどう作るのか

方法：

```text id="d7p3wf"
論理式
```

から生成できます。

例：

```text id="v6n9qy"
a & b
```

意味：

```text id="f1x8ts"
|11⟩ が正解
```

---

# 19. Groverの直感まとめ

処理：

```text id="h3q7vk"
均等状態
↓
正解に位相印
↓
平均反転
↓
振幅増幅
↓
測定
```

---

# 20. よく出る試験問題

問題：

oracleの役割は？

答え：

```text id="k5t2xz"
正解状態の位相反転
```

---

問題：

diffusion operatorの役割は？

答え：

```text id="n8c4vj"
平均に対する反転
```

---

問題：

Groverの計算量は？

答え：

```text id="q6r1mf"
√N
```

---

問題：

Grover iterationとは？

答え：

```text id="y4v8sp"
oracle + diffusion
```

---

# 21. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ oracleの役割を説明できる
✅ diffusion operatorを説明できる
✅ √N高速化を説明できる
✅ 反復回数の意味を説明できる
✅ 振幅増幅の仕組みを説明できる
✅ Grover iterationを説明できる

---

次章：

**19_vqe.md**

では：

```text id="c7y2rm"
VQE（Variational Quantum Eigensolver）
ハイブリッド量子アルゴリズム
NISQ時代の実用量子計算
```

を扱います。

ここから：

```text id="z1m8ke"
実務レベル量子アルゴリズム領域
```

に入ります 🧠⚛️
