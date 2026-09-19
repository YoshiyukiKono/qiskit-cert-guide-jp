この式は、**入力の重ね合わせをいったん二つに分け、それぞれに $U_f$ を作用させる**と理解できます。「左の項」が左辺を指す場合も、右辺の最初の項を指す場合も分かるように、途中式を補います。

まず左辺の
$$
U_f\bigl(|-\rangle_1\otimes|+\rangle_0\bigr)
$$
は、「$q_1$ を $|-\rangle$、$q_0$ を $|+\rangle$ に準備した2量子ビット全体に、$U_f$ を適用する」という意味です。ここで $\otimes$ は、二つの量子ビットの状態を組み合わせる記号です。

$|+\rangle_0=(|0\rangle_0+|1\rangle_0)/\sqrt2$ を代入すると、

$$
\begin{aligned}
&U_f\bigl(|-\rangle_1\otimes|+\rangle_0\bigr)\\
&=\frac{1}{\sqrt2}\,
U_f\Bigl(
|-\rangle_1\otimes|0\rangle_0
+
|-\rangle_1\otimes|1\rangle_0
\Bigr)\\
&=\frac{1}{\sqrt2}\Bigl[
U_f\bigl(|-\rangle_1\otimes|0\rangle_0\bigr)
+
U_f\bigl(|-\rangle_1\otimes|1\rangle_0\bigr)
\Bigr].
\end{aligned}
$$

最後の変形が「線形性」です。つまり、**和に作用させた結果は、それぞれに作用させた結果の和になる**という性質です。

ここで、直前に示された
$$
U_f\bigl(|-\rangle_1\otimes|x\rangle_0\bigr)
=(-1)^{f(x)}|-\rangle_1\otimes|x\rangle_0
$$
を、$x=0$ と $x=1$ にそれぞれ使います。

$$
=\frac{
(-1)^{f(0)}|-\rangle_1\otimes|0\rangle_0
+
(-1)^{f(1)}|-\rangle_1\otimes|1\rangle_0
}{\sqrt2}.
$$

両方の項に共通する $|-\rangle_1$ をくくり出すと、本文の式になります。

$$
=|-\rangle_1\otimes
\frac{(-1)^{f(0)}|0\rangle_0+(-1)^{f(1)}|1\rangle_0}{\sqrt2}.
$$

右辺の最初の項 **$(-1)^{f(0)}|0\rangle_0$** は、入力が $|0\rangle_0$ の成分に由来します。

- $f(0)=0$ なら、作業ビットを反転しないので符号は $+1$。
- $f(0)=1$ なら、作業ビットに $X$ が作用し、$X|-\rangle=-|-\rangle$ なので符号は $-1$。

**入力が0だから必ずプラスになるのではなく、関数値 $f(0)$ によって符号が決まる**、という点がポイントです。