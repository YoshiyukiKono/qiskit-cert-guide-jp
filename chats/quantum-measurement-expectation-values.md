# 量子測定と期待値

https://chatgpt.com/share/6aa84d0f-414c-83e9-8250-854101a91d03

## You said:

量子計算において、期待値の説明として、雑な理解として、Zの測定値・期待値が+1,-1になる。という説明がされると理解しています。そして、これは単なる測定とは違う特徴として語られ、固有値の特徴としても言われます。
これはZだから？期待値・Obserbableは、Zに結び付いているわけではない理解ですが。

---

## ChatGPT said:

はい。ここは **「測定結果」「期待値」「Observable（観測量）」「固有値」** が少し混ざりやすいところです。

結論からいうと、

> **±1 になるのは「期待値だから」ではなく、Observable として $Z$ を選んだから**

です。さらに厳密には、**1回の測定結果が $+1$ または $-1$** であり、**期待値は一般にはその間の値**になります。

### まず $Z$ の場合

Pauli $Z$ は

$$
Z=
\begin{pmatrix}
1&0\\
0&-1
\end{pmatrix}
$$

で、

$$
Z|0\rangle=+1|0\rangle
$$

$$
Z|1\rangle=-1|1\rangle
$$

です。

つまり、

- $|0\rangle$ は $Z$ の固有状態、固有値 $+1$

- $|1\rangle$ は $Z$ の固有状態、固有値 $-1$

です。

量子力学では、**Observable を測定したときに得られる値は、その Observable の固有値**です。

したがって $Z$ を Observable として測定すると、1回ごとの測定結果は

$$
+1 \quad\text{または}\quad -1
$$

になります。

ここが「固有値」と直接つながっています。

---

### では「期待値」は何か

例えば

$$
|\psi\rangle
=
\sqrt{0.8}|0\rangle+\sqrt{0.2}|1\rangle
$$

なら、$Z$ 測定では

$$
+1 \quad\text{が確率 }0.8
$$

$$
-1 \quad\text{が確率 }0.2
$$

で得られます。

期待値はその平均なので、

$$
\langle Z\rangle
=
(+1)\times0.8+(-1)\times0.2
=
0.6
$$

です。

したがって大事なのは、

> **測定値**：$+1$ または $-1$\
>
> **期待値**：たとえば $0.6$

という違いです。

$\mathbb{E}[X] = \sum_x xP(X=x)$E[X]=2(0.25)+8(0.75)=6.5\mathbb{E}[X]=2(\text{0.25})+8(\text{0.75})=\text{6.5}E[X]=2(0.25)+8(0.75)=6.5結果8の確率、P(X=8)結果8の確率、P(X=8)結果8の確率スライダーを動かすと、結果の重みが変わり、期待値が再計算されます。

この場合、何回も測れば

$$
+1,+1,-1,+1,+1,\ldots
$$

のような列が得られ、その平均が多数回測定の極限で $0.6$ に近づく、というイメージです。

### $Z$ に限った話ではありません

ここがご質問の核心ですね。

Observable は一般に Hermitian operator $A$ で、

$$
A|a_i\rangle=a_i|a_i\rangle
$$

という固有値 $a_i$ を持っています。

この $A$ を測定すると、

$$
a_1,a_2,\ldots
$$

のどれかが測定結果になります。

そして期待値は

$$
\langle A\rangle
=
\langle\psi|A|\psi\rangle
$$

であり、測定確率を $p_i$ とすれば、

$$
\langle A\rangle
=
\sum_i a_i p_i
$$

です。

ですから、たとえば固有値が

$$
2,\quad 5
$$

の Observable があれば、測定値は $2$ または $5$、期待値はたとえば $3.2$ のようになります。

**±1 は期待値一般の特徴ではありません。**

### なぜ量子計算ではやたらと $Z$ と ±1 が出てくるのか

これは $Z$ が非常によく使われるからです。

通常の量子回路で computational basis measurement をすると、画面上では

$$
0,\quad1
$$

という classical bit が返ります。

しかし、それを **Pauli $Z$ という Observable の測定**として扱うと、

$$
0\longleftrightarrow +1
$$

$$
1\longleftrightarrow -1
$$

と対応させます。

したがって、

$$
\langle Z\rangle
=
P(0)-P(1)
$$

になります。

たとえば半々なら、

$$
P(0)=P(1)=\frac12
$$

なので

$$
\langle Z\rangle=0
$$

です。

---

なので、少し言い換えると、

> 「量子測定では ±1 が出る」

は一般論としては不正確です。

より正確には、

> **Observable を測定すると、その Observable の固有値のいずれかが得られる。Pauli $Z$ の固有値が $+1,-1$ なので、$Z$ 測定では ±1 が得られる。期待値はそれらの確率加重平均である。**

です。

そして実は同じことは **$X$ と $Y$** にも言えます。Pauli $X,Y,Z$ はすべて固有値が $\pm1$ なので、

$$
\langle X\rangle,\quad
\langle Y\rangle,\quad
\langle Z\rangle
$$

はいずれも $-1$ から $+1$ の範囲になります。

ここから **「Bloch球の座標がなぜ $\langle X\rangle,\langle Y\rangle,\langle Z\rangle$ なのか」** へつなげると、かなりきれいに一つの話になります。

---

## You said:

期待値  自体は純粋に数学的・確率的な話だとして、Observableはイコール±1 の性質を持つもの（を選ぶ）ということでしょうか？そうではなくでもObservableになりえる？\

---

## ChatGPT said:

そうです。**Observable が ±1 でなければならないわけではありません。**

むしろ一般には、

> Observable = 測定したい物理量を表す Hermitian operator

です。

そして、その Observable の**固有値が、測定で取りうる値**になります。

たとえば

$$
A=
\begin{pmatrix}
2&0\\
0&5
\end{pmatrix}
$$

なら、これは Hermitian なので Observable として扱えます。固有値は

$$
2,\ 5
$$

ですから、測定結果は $2$ または $5$ です。

状態が

$$
|\psi\rangle=\sqrt{0.7}|0\rangle+\sqrt{0.3}|1\rangle
$$

なら期待値は

$$
\langle A\rangle
=
2\times0.7+5\times0.3
=
2.9
$$

です。

つまり、

- **Observable の条件**：基本的には Hermitian であること

- **測定結果**：その Observable の固有値

- **期待値**：固有値を確率で平均したもの

という関係です。

ではなぜ量子計算で $\pm1$ が多いのかというと、**Pauli observables を非常によく使うから**です。

$$
X,\ Y,\ Z
$$

はいずれも固有値が

$$
+1,\ -1
$$

です。そのため量子計算、特に VQE や expectation value の説明では、

$$
\langle Z\rangle,\quad \langle X\rangle
$$

のようなものが頻出し、「Observable の値は ±1」という印象を持ちやすいです。

さらに少し一般化すると、

$$
Z\otimes Z
$$

のような Pauli string も固有値はやはり $\pm1$ です。だから量子アルゴリズムでは、複雑な Observable を

$$
H
=
c_1 Z
+c_2 X
+c_3 Z\otimes Z+\cdots
$$

のように **Pauli observable の線形結合として分解する**ことがよくあります。

ここでは最終的な $H$ 自体の固有値は、必ずしも $\pm1$ ではありません。

なので、かなり重要な整理としては、

> **「Observable = ±1」ではない。**
>
> **「Pauli Observable は固有値 ±1 を持つ」**
>
> そして量子計算では Pauli Observable を多用するため、±1 が目立つ。

という理解が一番すっきりしています。

そして「期待値自体は純粋に数学・確率の概念」という捉え方もかなりよいです。量子力学側の特徴は、**何を確率変数の値として許すかが Observable の固有値によって決まる**ところにあります。

---

## You said:

上記の疑問は、下記のような文章を読んで受けた印象から来ています。あらためて読むと納得できる気もしましたが、ミスリーディングなところもあるでしょうか？
### 調べたい量から測定基底を選ぶ
一般の正規直交基底$|u_0\rangle,|u_1\rangle$で測るとは、どちらの基底状態に対応する結果を得るかを調べることです。「正規直交」は、各状態の長さが1で、異なる状態の内積が0であることを意味します。
$$
P_b=|u_b\rangle\langle u_b|,
\qquad p_b=|\langle u_b|\psi\rangle|^2.
$$
結果$b$を得た状態は、global phaseを除いて$|u_b\rangle$です。Z・X・Y測定では、それぞれの演算子の固有状態をこの基底に選びます。0を$+1$、1を$-1$と読み替えて平均すると、対応する演算子の[期待値]になります。Show moreShow less

---

## ChatGPT said:

はい、かなり筋のよい文章です。大筋では正しいです。ただし、あなたが今回抱いた疑問を考えると、**少しだけミスリーディングになりうる箇所**があります。

特に最後の一文です。

> 0を$+1$、1を$-1$と読み替えて平均すると、対応する演算子の期待値になります。

これは **Z・X・Y のような固有値が $\pm1$ の Observable に限れば正しい**です。ただ、直前まで「一般の正規直交基底」で話しているので、そのまま読むと

> 任意の測定基底について、0/1 を $\pm1$ に読み替えれば期待値になる

ように見える余地があります。

実際には、一般の Observable $A$ が

$$
A=\sum_b a_b |u_b\rangle\langle u_b|
$$

とスペクトル分解できるなら、基底 $|u_b\rangle$ で測定した結果 $b$ に対して、本当に対応づけるべき値は **その固有値 $a_b$** です。

期待値は

$$
\langle A\rangle
=
\sum_b a_b\,p_b
$$

です。

つまり本質は、

> 「0を$+1$、1を$-1$に読む」

ことではなく、

> **測定結果ラベル $b$ を、その Observable の固有値 $a_b$ に読み替えて平均する**

ことです。

Z・X・Y ではたまたま固有値が

$$
+1,\,-1
$$

なので、

$$
0\mapsto +1,\qquad 1\mapsto -1
$$

という非常に簡単な読み替えになります。

なので、この文章を少し直すなら、たとえばこうするとかなり明確です。

> Z・X・Y測定では、それぞれの演算子の固有状態を測定基底に選びます。測定結果のラベルを、その固有状態に対応する固有値へ読み替えて平均すると、その演算子の期待値が得られます。Pauli $X,Y,Z$ の固有値は $+1,-1$ なので、通常は 0 を $+1$、1 を $-1$ と対応づけます。

この形なら、「なぜ ±1 なのか」が **Observable 一般の性質ではなく、Pauli Observable の固有値だから**と自然に読めます。

もう一点だけ細かく言うと、

> 結果$b$を得た状態は、global phaseを除いて$|u_b\rangle$です。

も、射影測定を前提とした1量子ビットの説明としては問題ありません。ただ「一般の測定」という広い意味では POVM などもあるので、厳密には「この射影測定では」と限定するとより安全です。

なので評価すると、

- 前半：かなりよい

- 中盤：正しい

- 最後：**Pauli 測定に限定した話だと明示した方がよい**

という感じです。

そして今回あなたが引っかかったのは、まさにその「一般の基底の話」から「Pauli の ±1」へ、少し説明を省略して飛んでいるところだと思います。

---

## You said:

「測定結果のラベルを、その固有状態に対応する固有値へ読み替え」ることは、単なる操作上のルール、＋１とー１が扱いやすいから、と思えばよいでしょうか？

---

## ChatGPT said:

半分は「操作上のルール」ですが、**「±1が扱いやすいから適当に付けている」わけではありません。**

重要なのは、

> **固有値は、その Observable を測ったときに得られる値そのもの**

という点です。

たとえば $Z$ なら

$$
Z|0\rangle=+1|0\rangle,\qquad
Z|1\rangle=-1|1\rangle
$$

なので、$|0\rangle$ と $|1\rangle$ は単に「0番目、1番目の状態」なのではなく、

- $|0\rangle$：$Z$ という Observable の値が $+1$

- $|1\rangle$：$Z$ という Observable の値が $-1$

を持つ固有状態です。

ですから、回路上で測定結果が bit の

$$
0,\ 1
$$

として出てきたとき、

$$
0\to +1,\qquad 1\to -1
$$

とするのは、**古典ビットのラベルを、もともとの Observable の値へ戻している**、と考えるのが一番近いです。

もし Observable が

$$
A=
2|u_0\rangle\langle u_0|
+
5|u_1\rangle\langle u_1|
$$

なら、

$$
A|u_0\rangle=2|u_0\rangle,\qquad
A|u_1\rangle=5|u_1\rangle
$$

です。

この基底で測定装置が結果を単に

$$
0,\ 1
$$

と記録するなら、期待値を計算するときには

$$
0\to2,\qquad1\to5
$$

と読み替えます。

つまり一般則は

$$
\text{測定ラベル }b
\quad\longrightarrow\quad
\text{対応する固有値 }a_b
$$

です。

---

では「なぜ Pauli $Z$ はそもそも固有値 $\pm1$ なのか」というところでは、多少「都合のよい規格化」という面があります。

たとえば

$$
A=3Z
$$

も立派な Hermitian Observable で、固有値は

$$
+3,\ -3
$$

です。

同じ固有状態を測っていますが、観測量のスケールを3倍にしただけです。

したがって、

> **$+1,-1$ でなければならない物理的必然性がある**

というより、

> Pauli 演算子は「二値 Observable」を標準的に $\pm1$ に規格化した、とても便利な表現

という側面があります。

しかもこの規格化には数学的な利点がかなりあります。

たとえば

$$
Z^2=I
$$

なので固有値 $\lambda$ は

$$
\lambda^2=1
$$

を満たし、

$$
\lambda=\pm1
$$

です。

同じことが

$$
X^2=Y^2=Z^2=I
$$

について成立します。

なので $\pm1$ は単に「計算しやすい数字を人間が選んだ」というより、

> **Pauli 演算子の数学的構造に自然に組み込まれている規格化**

です。

今回の疑問を一言で整理すると、

> **0/1 は測定装置が返すラベル。**
>
> **±1 は $Z$ という Observable の固有値。**
>
> **0→+1、1→−1 は、ラベルから物理量の値へ戻す対応。**

と見ると、かなりすっきりします。

そしてこの区別は Qiskit の `counts` と `expectation value` の関係を理解するときにも、そのまま効いてきます。

---

## You said:

＋－１に限らず、ラベル自体ではなく、固有値を使う理由はなんでしょうか？測定には使わず、期待値にそれを使う、というのが恣意的に感じています。

---

## ChatGPT said:

その違和感はかなり大事です。結論からいうと、

> **固有値を期待値に使うのは、後から恣意的に決めたルールではありません。**
>
> **Observable そのものが「どの状態に、どんな測定値を割り当てるか」を定義しているからです。**

ここで、少し切り分けると分かりやすいです。

測定装置が返す「0」「1」は、かなり人工的な**ラベル**です。これは「どちらの射影先だったか」を区別するための記号にすぎません。

一方で Observable $A$ は、たとえば

$$
A = 2|u_0\rangle\langle u_0|+5|u_1\rangle\langle u_1|
$$

のように書けます。

この式は単に基底を指定しているだけではなく、

$$
|u_0\rangle \mapsto 2,
\qquad
|u_1\rangle \mapsto 5
$$

という**値の割り当てまで含めて**定義しています。

つまり $A$ は、

- どの状態を区別するか

- それぞれに何という値を持たせるか

の両方を一体として持っています。

だから、実際に測定して $|u_0\rangle$ 側が出たなら、その Observable の測定値は $2$ です。$|u_1\rangle$ 側なら $5$ です。

0/1 はあくまで「どっちだったか」という記録ラベルです。

---

ここで期待値を考えると、

$$
\langle A\rangle
=
2\,P(u_0)+5\,P(u_1)
$$

になります。

なぜならこれは、普通の確率論でいう

$$
\text{期待値}
=
\sum (\text{値})\times(\text{確率})
$$

そのものだからです。

ここで使うべき「値」は、ラベル 0/1 ではなく、**その確率変数が本来取る値**です。

たとえば普通のサイコロでも、「出目1のイベント」「出目2のイベント」などを内部的に event A, B, C... とラベルしても、サイコロの期待値を計算するときは

$$
1,2,3,4,5,6
$$

を使いますよね。

イベントの識別名を使って平均するわけではありません。

量子でも同じです。

$$
\text{結果ラベル } b
$$

は event ID に近く、

$$
\text{固有値 } a_b
$$

が、その Observable における「数値としての測定結果」です。

---

そしてさらに重要なのは、**測定にもちゃんと固有値を使っている**、という点です。

「測定には固有値を使わず、期待値だけで使う」という理解ではありません。

理論上は、

$$
A\text{ を測定して }a_b\text{ を得る}
$$

と言います。

ただ量子コンピュータの実装では、ハードウェアがしばしば

$$
0,\;1
$$

のような classical bit を返すだけなので、あとでそれを固有値に対応づけています。

つまり、

> 理論：測定値は固有値\
>
> 実装：まずラベルを取得し、そのラベルを固有値へ対応づける

です。

ここはかなり重要な違いです。

---

さらに、「同じ測定基底なのに Observable は違えるのか？」というと、違えます。

たとえば

$$
A=2|0\rangle\langle0|+5|1\rangle\langle1|
$$

と

$$
B=100|0\rangle\langle0|-7|1\rangle\langle1|
$$

は、**同じ $Z$ 基底で測定できます**。

どちらも「0か1か」を調べればよい。

でも Observable としては違います。

$0$ が出たとき、

- $A$ の測定値なら $2$

- $B$ の測定値なら $100$

です。

つまり、

$$
\text{測定基底}
$$

だけでは Observable は決まりません。

Observable には、

$$
\text{固有状態}+\text{固有値}
$$

の両方が必要です。

ここがたぶん、今回の違和感を解く一番大きなポイントです。

---

なので、かなり短く言うと、

> **固有状態は「どの結果か」を決める。**
>
> **固有値は「その結果の値はいくつか」を決める。**
>
> **期待値は、その値を確率で平均したもの。**

です。

そして 0/1 は、多くの場合その間に挟まっているだけの**古典的な記録用ラベル**です。

ここまで来ると、Observable を

$$
A=\sum_i a_i P_i
$$

と書く意味がかなり見えやすくなります。\

この式そのものが、「どの projector $P_i$ に落ちたか」と「そのとき返す値 $a_i$」をセットで表しているからです。

---

## You said:

量子コンピュータが内部で固有値を持っているわけではないので、ラベルを一次情報として感じていた、ということだろうか？実用上では、固有値が重要であるにもかかわらず。
Qiskitでいえば、Estimatorなどは、量子コンピュータの外側で固有値を対応させている？

---

## ChatGPT said:

はい、その捉え方でかなり合っています。

あなたが「ラベルのほうが一次情報に見える」と感じたのは、**量子コンピュータの実装を入口に見ていたから**だと思います。QPU が直接返すのは典型的には bit string、つまり `0` / `1` や `0011` のような古典的結果です。ところが量子力学の理論では、Observable $A$ の測定結果として本質的なのは、その $A$ の固有値です。IBM の説明でも、Hermitian observable $A$ に対応する projective measurement の可能な outcome は $A$ の固有値だ、と明示されています。[![](https://www.google.com/s2/favicons?domain=https://qiskit.qotlabs.org&sz=128)IBM Quantum Documentation](https://qiskit.qotlabs.org/learning/courses/foundations-of-quantum-error-correction/stabilizer-formalism/pauli-operations-and-observables?utm_source=chatgpt.com)

Qiskit の Estimator は、まさにそのギャップを埋めています。

たとえば Observable として

$$
Z
$$

を渡すと、実機側では最終的に computational basis で測定できる形に変換され、ショットごとには `0` / `1` が得られます。$X$ や $Y$ なら、Qiskit が基底変換を入れてから $Z$ 基底測定に落とします。IBM の現行ドキュメントでも、Estimator を使う場合はこの基底変換が自動的に行われると説明されています。[![](https://www.google.com/s2/favicons?domain=https://qiskit.qotlabs.org&sz=128)IBM Quantum Documentation](https://qiskit.qotlabs.org/docs/guides/specify-observables-pauli?utm_source=chatgpt.com)

その後、概念的には

$$
0\mapsto +1,\qquad1\mapsto -1
$$

として Pauli observable の期待値を計算します。

なので、

$$
\text{QPU}
\longrightarrow
\text{bit outcomes}
\longrightarrow
\text{observable の値として解釈}
\longrightarrow
\text{expectation value}
$$

という階層だと思うとよいです。

特に `BackendEstimatorV2` の説明はかなり露骨です。Observable を

$$
O=\sum_i a_iP_i
$$

という Pauli の線形結合に分解し、それぞれの Pauli $P_i$ の期待値を求め、最後に

$$
\langle O\rangle
=
\sum_i a_i\langle P_i\rangle
$$

として組み立てる、と公式ドキュメントに書かれています。[![](https://www.google.com/s2/favicons?domain=https://qiskit.qotlabs.org&sz=128)IBM Quantum Documentation](https://qiskit.qotlabs.org/docs/api/qiskit/qiskit.primitives.BackendEstimatorV2?utm_source=chatgpt.com)

ここでかなり重要なのは、QPU が

> 「いま $O$ の固有値を測ったぞ」

という抽象的な操作をそのまま内部で行っているわけではない、ということです。

むしろ実用上は、

$$
O
=
0.7\,ZI
-1.2\,XX
+0.3\,YY
$$

のような Observable を与えると、それを測定可能な Pauli 項へ分解し、それぞれについてショット統計を集め、**外側のソフトウェア層で Observable として再構成する**、ということが起きます。EstimatorV2 自体も「circuits と observables から expectation values を estimate する」インターフェースとして定義されています。[![](https://www.google.com/s2/favicons?domain=https://quantum.cloud.ibm.com&sz=128)IBM Quantum+1](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/estimator-v2?utm_source=chatgpt.com)

ただし、一つだけ注意があります。

「Estimator が必ず QPU の `counts` を受け取って、Python 側で単純に `0→+1` としている」とまで具体化すると、実装依存なので言い過ぎです。Runtime 側でどこまで処理されるかはサービスの実装に依存します。

概念的には、

> **量子ハードウェアが測定統計を生成し、Estimator 層がそれを指定された Observable の期待値として解釈・集約する**

と理解するのが安全です。

そして `StatevectorEstimator` の場合はさらに分かりやすくて、実機の bit measurement すら必須ではありません。状態ベクトルに `SparsePauliOp` を作用させて、数学的に期待値を直接計算します。[![](https://www.google.com/s2/favicons?domain=https://qiskit.qotlabs.org&sz=128)IBM Quantum Documentation](https://qiskit.qotlabs.org/docs/api/qiskit/qiskit.primitives.StatevectorEstimator?utm_source=chatgpt.com)

つまり同じ

$$
\langle\psi|A|\psi\rangle
$$

でも、

$$
\begin{array}{c}
\text{StatevectorEstimator}\\
\downarrow\\
\text{状態ベクトルから直接計算}
\end{array}
$$

と

$$
\begin{array}{c}
\text{実機 Estimator}\\
\downarrow\\
\text{測定統計から推定}
\end{array}
$$

という二つの実現方法があります。

なので、今回の一連の疑問をまとめると、かなりきれいにこうなります。

> **量子コンピュータの生データを見れば、0/1 のラベルが一次情報に見える。**
>
> **量子力学の理論を見れば、Observable とその固有値のほうが一次概念で、0/1 は実装上の符号化に見える。**
>
> **Estimator は、その二つの層をつなぐ抽象化である。**

これはかなり本質的な見方です。特に IBM の `Sampler` と `Estimator` の違いも、この整理でほぼ説明できます。**Sampler は「ラベルの確率分布」に近く、Estimator は「その結果に Observable の数値的意味を与えて平均したもの」に近い**、という違いです。

---

## You said:

アルゴリズム的にいうと、量子アルゴリズムは全て、固有値を使う？それとも使うものと使わないもので分類できる？校舎の気がするが。

---

## ChatGPT said:

後者です。**量子アルゴリズムは「固有値を本質的に使うもの」と「そうでないもの」にかなり分けられます。**

ただしさらに正確には、

> **線形代数的には固有値・固有状態が背景に潜んでいることは非常に多いが、アルゴリズムの出力や中核処理として固有値を使うとは限らない**

です。

たとえば、固有値がど真ん中にある代表例は **Quantum Phase Estimation (QPE)** です。ユニタリ $U$ の固有状態 $|\psi\rangle$ に対して

$$
U|\psi\rangle=e^{2\pi i\theta}|\psi\rangle
$$

と書けるとき、その固有値の位相 $\theta$ を推定します。これは文字どおり「固有値を取り出すアルゴリズム」です。

Shor のアルゴリズムも、表面的には因数分解ですが、内部では周期発見を行い、その構造は位相推定・固有値問題として理解できます。HHL も行列 $A$ の固有値 $\lambda_i$ を利用して $1/\lambda_i$ に対応する操作を行うので、固有値依存が非常に強いです。

一方、**Grover 探索**は違います。もちろん Grover operator の固有値や固有ベクトルを解析すれば動作を美しく説明できますが、

> 「固有値を推定して、その値を答えとして使う」

アルゴリズムではありません。

中心にあるのは、oracle と amplitude amplification です。

同様に、単純な Bell state の生成、teleportation、superdense coding なども、アルゴリズムの目的として固有値を求めているわけではありません。

そして VQE のような変分アルゴリズムは、その中間にあります。

VQE の目標は Hamiltonian $H$ の最小固有値

$$
E_0
$$

を求めることです。

しかし QPU が直接固有値を返すわけではなく、

$$
\langle\psi(\theta)|H|\psi(\theta)\rangle
$$

という**期待値**を何度も評価し、それを古典 optimizer が最小化します。

Rayleigh–Ritz の原理によって、

$$
\min_{\psi}\langle\psi|H|\psi\rangle
=
\lambda_{\min}(H)
$$

なので、期待値を最小化すると最小固有値に到達する、という構造です。

ここは今回の話とかなり直接つながっています。

つまり VQE では、

$$
\text{測定}
\rightarrow
\text{Pauli expectation values}
\rightarrow
\langle H\rangle
\rightarrow
\text{最小化}
\rightarrow
\text{固有値}
$$

となっています。

なので、量子アルゴリズムをざっくり分類すると、

| タイプ | 固有値の位置づけ | 例 |
| --- | --- | --- |
| 固有値を直接推定 | 中核そのもの | QPE |
| 固有値問題を別形式で解く | 中核に近い | Shor, HHL |
| 期待値を通じて固有値を求める | 間接的だが本質的 | VQE |
| 固有値は解析には使えるが、アルゴリズムの目的ではない | 補助的 | Grover |
| 固有値をほぼ意識しない | 非本質的 | teleportation, Bell-state preparation |

です。

ただし少し面白い点があります。

量子計算では時間発展が

$$
U=e^{-iHt}
$$

で書かれます。

$H$ の固有状態

$$
H|E_k\rangle=E_k|E_k\rangle
$$

なら、

$$
U|E_k\rangle
=
e^{-iE_kt}|E_k\rangle
$$

となります。

つまり **Hamiltonian の固有値が phase になる**。

この構造が非常に強いため、

> 固有値 → phase → interference → 測定

という流れが、かなり多くの量子アルゴリズムの奥に潜んでいます。

だから「全部が固有値アルゴリズムではない」が、「量子アルゴリズムを深く理解していくと固有値が何度も出てくる」という感覚は正しいです。

今回の一連の話をつなげるなら、

$$
\boxed{
\text{Observableの固有値}
\quad\text{と}\quad
\text{Unitaryの固有値}
}
$$

は少し役割が違います。

前者は「**測定すると何という値が出るか**」、後者はしばしば「**どんな phase が蓄積するか**」に現れます。

この二つを分けて整理すると、QPE・VQE・Estimator の関係がかなり見通しよくなります。

---

## You said:

QiskitのEstimatorとの関係でいうと、あくまでObservableの固有値ですよね？Unitaryの、ではなく。
Unitaryの固有値は、Qiskitレベルでどう扱われますか？

---

## ChatGPT said:

はい、その理解で合っています。

**Estimator が扱うのは Observable の期待値であり、その背後にある固有値は Observable の固有値です。Unitary の固有値を求める仕組みではありません。** 現行の IBM Quantum の説明でも、Estimator は「回路が準備した状態に対する observable の expectation value」を計算する primitive とされています。[![](https://www.google.com/s2/favicons?domain=https://quantum.cloud.ibm.com&sz=128)IBM Quantum+1](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/estimator-v2?utm_source=chatgpt.com)

一方、**Unitary の固有値**は Qiskit では主に **Quantum Phase Estimation (QPE)** の文脈で扱われます。

QPE では、

$$
U|\psi\rangle=e^{2\pi i\phi}|\psi\rangle
$$

という関係を利用します。

ここで

$$
e^{2\pi i\phi}
$$

が unitary $U$ の固有値です。QPE はこの複素数そのものを直接表示するというより、**その位相 $\phi$** を量子回路によって推定します。IBM の現行 Qiskit ドキュメントも、この定義をそのまま採用しています。[![](https://www.google.com/s2/favicons?domain=https://quantum.cloud.ibm.com&sz=128)IBM Quantum+1](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.PhaseEstimation?utm_source=chatgpt.com)

つまり Qiskit レベルで見ると、かなり性格が違います。

|  | Estimator | QPE |
| --- | --- | --- |
| 対象 | Hermitian Observable $A$ | Unitary $U$ |
| 固有値 | 実数 $a_i$ | 複素位相 $e^{2\pi i\phi_i}$ |
| 欲しいもの | $\langle A\rangle$ | 位相 $\phi_i$ |
| 典型的入力 | circuit + observable | eigenstate + controlled-$U$ |
| QPUで得る情報 | 測定統計 | 位相をbinary encodingした測定結果 |

ここはかなり大きな区別です。

### Unitary の固有値はなぜ「phase」として扱えるのか

Unitary $U$ の固有値を $\lambda$ とすると、

$$
U|\psi\rangle=\lambda|\psi\rangle
$$

です。

Unitary であるため、

$$
|\lambda|=1
$$

でなければなりません。

したがって必ず

$$
\lambda=e^{i\theta}
$$

と書けます。

QPE では慣例的に

$$
\lambda=e^{2\pi i\phi}
$$

と書き、

$$
0\leq\phi<1
$$

の $\phi$ を推定します。

つまり、

$$
\boxed{\text{Unitaryの固有値を求める}
\;\approx\;
\text{そのphaseを求める}}
$$

となります。

### Qiskitでは「固有値を classical に計算する」こともできます

もう一つ区別しておくと、Qiskit の `quantum_info.Operator` などで行列を作ってしまえば、NumPy 等を使って普通の線形代数として

```
np.linalg.eig(...)
```

で固有値を求めることもできます。

これは当然、QPE とは全然違います。

例えば1量子ビットの $S$ gate

$$
S=
\begin{pmatrix}
1&0\\
0&i
\end{pmatrix}
$$

なら古典計算で、

$$
\lambda_0=1,\qquad
\lambda_1=i
$$

とすぐ求められます。

これは

$$
1=e^{2\pi i\cdot0},
\qquad
i=e^{2\pi i\cdot1/4}
$$

なので、QPE にかければ対応する phase は

$$
0,\qquad\frac14
$$

です。

したがって Qiskit では、

**小さな行列なら**

$$
U\rightarrow\text{matrix}\rightarrow\text{classical eigensolver}
$$

**量子アルゴリズムとして扱うなら**

$$
U,\ |\psi\rangle
\rightarrow\text{QPE}
\rightarrow\phi
\rightarrow e^{2\pi i\phi}
$$

という二通りがあります。

### Estimatorとの違いを、今回の話につなげると

ここは特に整理しておく価値があります。

Estimator では、

$$
A|a_i\rangle=a_i|a_i\rangle
$$

という **Hermitian observable の実数固有値** $a_i$ が測定値の意味になります。

そして、

$$
\langle A\rangle
=
\sum_i p_i a_i
$$

を求めます。

一方 QPE では、

$$
U|u_i\rangle
=
e^{2\pi i\phi_i}|u_i\rangle
$$

という **unitary の複素固有値**を、その phase として量子状態に刻み込み、

$$
\phi_i
$$

を読み出します。

つまり、

$$
\boxed{
\begin{array}{rcl}
\text{Estimator} &:&
\text{Observableの固有値を重み付き平均する}\\[2mm]
\text{QPE} &:&
\text{Unitaryの固有値のphaseを推定する}
\end{array}}
$$

です。

そして面白いのは、両者が **Hamiltonian** のところで再びつながることです。

Hamiltonian $H$ は Hermitian なので、

$$
H|E_i\rangle=E_i|E_i\rangle
$$

と実数固有値 $E_i$ を持ちます。

これから

$$
U=e^{-iHt}
$$

という unitary を作ると、

$$
U|E_i\rangle
=
e^{-iE_i t}|E_i\rangle
$$

になります。

つまり

$$
\boxed{
H\text{ の固有値 }E_i
\quad\longrightarrow\quad
U\text{ の固有値の phase }-E_it
}
$$

です。

ここが **VQE と QPE がどちらも energy eigenvalue を求められるのに、やり方が全然違う理由**です。

- VQE → Estimator で $\langle H\rangle$ を最小化

- QPE → $e^{-iHt}$ の eigenphase を直接推定

この比較まで押さえると、Estimator と unitary eigenvalue の位置関係はかなりきれいに整理できます。

---

## You said:

Qiskitプログラミング・APIのレベルでは、Unitaryの固有値は、どのレベルで現れますか？直接現れない？

---

## ChatGPT said:

はい。**Qiskit の通常のプログラミング/APIレベルでは、Unitary の固有値はかなり「直接は現れない」ものです。**

たとえば `QuantumCircuit` や `UnitaryGate` を使って

```
qc.h(0)
qc.rz(theta, 0)
```

あるいは

```
UnitaryGate(U)
```

と書いても、API上で「このゲートの固有値はこれです」という情報を通常扱うわけではありません。`UnitaryGate` は基本的に「ユニタリ行列としてのゲート」を表すクラスです。[![](https://www.google.com/s2/favicons?domain=https://quantum.cloud.ibm.com&sz=128)IBM Quantum](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.UnitaryGate?utm_source=chatgpt.com)

つまり普段のQiskitでは、

$$
U|\psi\rangle
$$

という**作用**を扱っていて、

$$
U|u_i\rangle=\lambda_i|u_i\rangle
$$

という固有値分解を明示的に意識する必要はありません。

### 直接現れるのは QPE のような場面

Quantum Phase Estimation まで来ると、Unitary の固有値がアルゴリズムの仕様そのものに現れます。

QPE は

$$
U|\psi\rangle=e^{2\pi i\phi}|\psi\rangle
$$

を前提にして、

$$
e^{2\pi i\phi}
$$

という固有値そのものではなく、その **eigenphase $\phi$** を推定します。Qiskit の `PhaseEstimation` のAPI説明もまさにこの定義です。[![](https://www.google.com/s2/favicons?domain=https://quantum.cloud.ibm.com&sz=128)IBM Quantum](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.PhaseEstimation?utm_source=chatgpt.com)

ただし、ここでもAPIとして

```
eigenvalue = ...
```

という値を `UnitaryGate` から取り出すわけではありません。

むしろ、

```
unitary U
    ↓
controlled-U
controlled-U²
controlled-U⁴
...
    ↓
inverse QFT
    ↓
bitstring
    ↓
phase φ の推定
```

です。

つまり **Unitary の固有値は回路の動作の中に埋め込まれていて、測定結果から phase として復元される**わけです。IBMの現行QPEチュートリアルでも、測定 bitstring が $\phi$ の二進小数近似になる形で説明されています。[![](https://www.google.com/s2/favicons?domain=https://quantum.cloud.ibm.com&sz=128)IBM Quantum](https://quantum.cloud.ibm.com/docs/en/tutorials/quantum-phase-estimation-qctrl?utm_source=chatgpt.com)

### 普通の線形代数としてなら直接取り出せる

もちろん行列が手元にあるなら、

```
U = Operator(qc).data
eigenvalues, eigenvectors = np.linalg.eig(U)
```

のように NumPy で求められます。

これは、

$$
\text{Qiskit circuit}
\rightarrow
\text{matrix}
\rightarrow
\text{NumPy eigensolver}
$$

という**古典計算**です。

Qiskit の量子回路APIが特別に「unitary eigenvalue」というオブジェクトを管理しているわけではありません。

### Estimatorとの違いがここでかなりはっきりします

Estimator の場合、

```
QuantumCircuit
+
Observable
↓
expectation value
```

なので、Observable がAPI上で明示的な入力です。

一方 QPE は、

```
eigenstate
+
Unitary circuit
↓
phase
```

です。

ここでは固有値は**入力データとして渡しません**。むしろ、それを知りたいのがアルゴリズムです。

なのでAPI感覚としては、

| Qiskitで扱うもの | API上での見え方 |
| --- | --- |
| Observable | `SparsePauliOp` などとして明示的に渡す |
| Observable expectation value | Estimator の明示的な出力 |
| Unitary | `QuantumCircuit` / `Gate` / `Operator` として明示的 |
| Unitary eigenvalue | 普通は明示的オブジェクトとして現れない |
| eigenphase | QPE の測定結果から推定する |

となります。

なので、今回の問いへのかなり端的な答えは、

> **通常のQiskitプログラミングでは Unitary の固有値はほとんど表面に出ない。**
>
> **QPEのように固有値がアルゴリズム上の対象になったとき、初めて eigenphase として明示的に意識する。**

です。

この意味で、Qiskitを普通に学んでいると **Observable の固有値のほうが先に「実用的な概念」として目につきやすい**のはかなり自然です。EstimatorやPauli expectation valueを先に触ると、なおさらそう見えます。

---

## You said:

eigenphase  は、eigen value やeigen stateと比べてあまり聞かない印象ですが、数学的な一般概念ですか？

---

## ChatGPT said:

はい。**eigenphase は数学的に一般に使える概念ではありますが、eigenvalue / eigenvector ほど基礎数学の標準用語として前面には出ません。** 特に、unitary operator の固有値を扱う文脈で自然に使われる言葉です。

理由は単純で、unitary $U$ の固有値 $\lambda$ は必ず絶対値1なので、

$$
|\lambda|=1
$$

したがって

$$
\lambda=e^{i\theta}
$$

と書けます。このとき、その角度 $\theta$ を **eigenphase** と呼びます。

つまり、

$$
U|u\rangle=\lambda|u\rangle
$$

に対して、

$$
\lambda=e^{i\theta}
$$

なら、

$$
\theta
$$

が eigenphase です。

QPE ではしばしば

$$
\lambda=e^{2\pi i\phi}
$$

と書いて、$\phi$ を推定します。この $\phi$ も eigenphase を $2\pi$ で規格化したもの、と見てよいです。

重要なのは、

> **eigenphase は固有値とは別の新しい数学的対象ではない**

ということです。

固有値が単位円上にある特殊な場合に、その固有値を角度で表現しているだけです。

なので関係は、

$$
\text{eigenvalue}
\quad\lambda=e^{i\theta}
\quad\longleftrightarrow\quad
\text{eigenphase }\theta
$$

です。

このため、普通の線形代数ではまず

- eigenvalue

- eigenvector / eigenstate

を学び、**unitary / orthogonal operator や量子力学に入ってから eigenphase という言い方が目立つ**、という順序になります。

たとえば一般の Hermitian 行列なら固有値は

$$
-3,\quad 0.7,\quad 12
$$

のような実数なので、「phase」として表す意味はありません。

一方 unitary なら

$$
1,\quad i,\quad -1,\quad e^{i0.37}
$$

のようにすべて単位円上なので、

$$
0,\quad \frac{\pi}{2},\quad \pi,\quad 0.37
$$

という角度で見るのが非常に自然です。

なので感覚としては、

> eigenvalue = 一般概念\
>
> eigenphase = unitary の固有値を角度表示したときの便利な呼び方

くらいでよいです。

量子計算ではこの「便利な呼び方」がかなり重要になります。なぜなら unitary の固有値そのものより、**phase が interference や QPE に直接現れる**からです。
