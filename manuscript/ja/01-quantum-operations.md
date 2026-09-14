# 1. 量子状態、行列、基本演算

[← 学び方](00-guide.md) | [次: 測定と可視化 →](02-visualization-measurement.md)

この章では、量子状態から測定の確率を求め、ゲートによる状態の変化を計算する方法を学びます。まず1量子ビットの振幅と行列を扱い、位相と各種ゲート、複数量子ビットへ進みます。最後に、測定値の平均である期待値へつなげます。

コード例はQiskit 2.5.2を基準とし、ローカルで実行します。実機やアカウントの準備は必要ありません。各コードは、それぞれ必要なimportと入力を含んでいます。

<a id="state-amplitude"></a>
## 状態と複素振幅

量子ビット（qubit）を測定すると、0または1という結果を得ます。しかし、測定前の状態を表すには、その結果の候補に対応する**複素振幅**が必要です。この節では、振幅の意味を確認し、状態の式から測定確率を計算できるようにします。

### 状態を表す記号を読む

$|0\rangle$と$|1\rangle$は、0と1に対応する基本の状態です。縦線と山括弧で囲む$|\ \rangle$をket（ケット）と呼び、状態を表す記号として使います。この2つを基準にした状態の表し方を、**計算基底**（**computational basis**）による表現と呼びます。

まず、1本の状態ベクトルで表せる**純粋状態**（**pure state**）を考えます。1量子ビットでは

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle,
\qquad \alpha,\beta\in\mathbb{C},
$$

と書きます。$\psi$は状態に付けた名前、$\mathbb{C}$は複素数の集合です。係数$\alpha$が$|0\rangle$の振幅、$\beta$が$|1\rangle$の振幅です。両方が0でない状態を、この基底に関する**重ね合わせ**と呼びます。

この式を「実際には0か1のどちらかだが、まだ分からない」とだけ読むと、後で扱う干渉を説明できません。振幅には、確率だけでは失われる符号や位相の情報も含まれるためです。

### 複素数から確率への変換

複素数は$a+bi$と書きます。$a,b$は実数で、$i$は$i^2=-1$を満たす虚数単位です。$i$の符号を反転した$a-bi$を**複素共役**と呼び、$(a+bi)^*$と表します。振幅から確率を求めるときは、通常の二乗ではなく、次の絶対値の二乗を使います。

$$
|a+bi|^2=(a+bi)^*(a+bi)=(a-bi)(a+bi)=a^2+b^2.
$$

したがって、計算基底で測定する確率は

$$
p(0)=|\alpha|^2,\qquad p(1)=|\beta|^2
$$

です。0か1のどちらかは必ず得られるので、状態は

$$
|\alpha|^2+|\beta|^2=1
$$

を満たす必要があります。この条件を**正規化**と呼びます。

例えば

$$
|\psi\rangle=\frac{\sqrt{3}}{2}|0\rangle+\frac{i}{2}|1\rangle
$$

ならば、

$$
p(0)=\left|\frac{\sqrt{3}}{2}\right|^2=\frac34,
\qquad
p(1)=\left|\frac{i}{2}\right|^2
=\left(-\frac{i}{2}\right)\left(\frac{i}{2}\right)=\frac14.
$$

$i^2/4=-1/4$を確率にしてはいけません。共役を掛けるので、確率は負になりません。また、この状態を1回測っても振幅そのものは読み出せません。同じ状態を毎回準備して測定を繰り返すと、0と1の頻度がそれぞれ$3/4$と$1/4$に近づきます。有限回の測定では、比率が正確に一致するとは限りません。

### 正規化とStatevector

係数が$1,i$のままでは、絶対値の二乗の和が$2$です。各係数を$\sqrt{2}$で割れば、和が1になります。一般に、0でない係数の組$(\alpha,\beta)$は、両方を$\sqrt{|\alpha|^2+|\beta|^2}$で割ると正規化できます。両方が0の組は量子状態にはできません。

Qiskitの`Statevector`には、計算基底の順に`[0の振幅, 1の振幅]`を渡します。Pythonでは虚数単位を`1j`と書きます。

```python
import numpy as np
from qiskit.quantum_info import Statevector

psi = Statevector([np.sqrt(3) / 2, 1j / 2])
raw = np.array([1, 1j], dtype=complex)
normalized = Statevector(raw / np.linalg.norm(raw))

print("psi is valid:", psi.is_valid())
print("psi probabilities:", psi.probabilities())
print("raw is valid:", Statevector(raw).is_valid())
print("normalized probabilities:", np.round(normalized.probabilities(), 6))
```

出力:

```text
psi is valid: True
psi probabilities: [0.75 0.25]
raw is valid: False
normalized probabilities: [0.5 0.5]
```

`probabilities()`の先頭が$p(0)$、次が$p(1)$です。`np.linalg.norm(raw)`は、係数の絶対値の二乗を足して平方根を取ります。`Statevector`の生成自体は、入力を自動的に正規化する操作ではありません。`is_valid()`で正規化条件を確認できます。

### 同じ確率でも、同じ状態とは限らない

よく使う次の4状態は、すべて計算基底では0と1が半々です。

$$
\begin{aligned}
|+\rangle &= \frac{|0\rangle+|1\rangle}{\sqrt{2}},\\
|-\rangle &= \frac{|0\rangle-|1\rangle}{\sqrt{2}},\\
|+i\rangle &= \frac{|0\rangle+i|1\rangle}{\sqrt{2}},\\
|-i\rangle &= \frac{|0\rangle-i|1\rangle}{\sqrt{2}}.
\end{aligned}
$$

振幅の違いは、測定前にゲートを適用すると確率の違いとして現れます。次節でその計算方法を学び、[位相の節](#phase)で符号や$i$の役割を確かめます。

### 確認問題

1. ある結果の振幅が$(1+i)/2$なら、その結果の確率はいくつですか。
2. 係数の組$(2,i)$を正規化すると、計算基底の確率はどうなりますか。
3. $|+\rangle$と$|-\rangle$は計算基底の確率が同じです。この事実だけで同じ状態と判断できますか。

**解答と理由**

1. $|(1+i)/2|^2=(1^2+1^2)/4=1/2$です。複素数をそのまま二乗するのではなく、実部と虚部の二乗を足します。
2. ノルムは$\sqrt{4+1}=\sqrt5$なので、振幅は$(2/\sqrt5,i/\sqrt5)$、確率は$(4/5,1/5)$です。
3. 判断できません。計算基底での確率には、振幅の相対的な符号が残らないためです。

振幅を読むときは、「どの基底の係数か」「正規化されているか」「絶対値の二乗はいくつか」を順に確認します。

参照: [Statevector API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector)

<a id="matrix-order"></a>
<a id="行列と演算順序"></a>
## ゲートの合成と基底変換

いくつかのゲートを順につなぐと、全体としてどのような演算になるでしょうか。また、状態を表す基準である「基底」を変えると、基本的な演算をどのように使い分けられるでしょうか。この節では、**ゲートの合成**を行列で読み、**基底変換と共役変換**を通して、演算や測定の向きを変える考え方を学びます。

まず状態と行列積の読み方を確認し、変換と逆変換で演算を挟む仕組みを導入します。その代表例として$HZH=X$を一段ずつ導き、ほかのゲートの変換、X・Y基底での測定へと広げます。目標は、個々の等式を同じ考え方で読み解き、回路での操作順まで説明できることです。

### 状態を列ベクトルで表す

1量子ビットの状態を表す$|0\rangle$と$|1\rangle$は、計算の基準になる二つの状態です。ket（ケット）と呼ぶ$|\ \rangle$の記号と、縦に数を並べる列ベクトルは、ここでは次のように対応します。

$$
|0\rangle=\begin{pmatrix}1\\0\end{pmatrix},\qquad
|1\rangle=\begin{pmatrix}0\\1\end{pmatrix},\qquad
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle
=\begin{pmatrix}\alpha\\\beta\end{pmatrix}.
$$

上の成分が$|0\rangle$の振幅、下の成分が$|1\rangle$の振幅です。振幅と測定確率の関係は[状態と複素振幅](#state-amplitude)を参照してください。まず測定を挟まず、ゲートによって振幅がどう変わるかを追います。

ゲートを行列で表すと、状態の変化は行列と列ベクトルの掛け算になります。行列の各行とベクトルの成分を掛けて足すのが計算規則です。

$$
\begin{pmatrix}a&b\\c&d\end{pmatrix}
\begin{pmatrix}\alpha\\\beta\end{pmatrix}
=\begin{pmatrix}a\alpha+b\beta\\c\alpha+d\beta\end{pmatrix}.
$$

今回使う三つのゲートは次の行列です。

$$
H=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$

Zは下の振幅の符号を反転し、Xは上下の振幅を交換します。Hについても、先ほどの掛け算の規則を使えば作用を求められます。

### 回路の時間順と、行列積の順序

状態にまず$U$、次に$V$を作用させると、途中の状態は$U|\psi\rangle$、最後の状態は$V(U|\psi\rangle)$です。したがって、まとめた行列は$VU$になります。

$$
|\psi\rangle\xrightarrow{U}U|\psi\rangle
\xrightarrow{V}VU|\psi\rangle.
$$

回路は左から右へ時間が進みますが、式では状態に最も近い右端の行列から作用します。H → Z → Hの場合は、$H(Z(H|\psi\rangle))$、すなわち$HZH|\psi\rangle$です。このゲート列は左右対称なので、順序の取り違えが見えにくい例でもあります。後でH → ZとZ → Hも比較します。

### 基底を変える操作と、その逆を組み合わせる

**基底**は、状態を重ね合わせとして表すための基準となる状態の組です。1量子ビットでは、$|0\rangle,|1\rangle$の組を**計算基底**、または**Z基底**と呼びます。別の基準として、$|+\rangle,|-\rangle$の組を使うこともでき、こちらを**X基底**と呼びます。

Hは、計算基底の二つの状態をX基底の二つの状態へ移すゲートです。

$$
H|0\rangle=|+\rangle,\qquad H|1\rangle=|-\rangle.
$$

逆に、Hをもう一度作用させると元へ戻ります。これらの関係は、この後の例題で行列を使って確かめます。

一般のゲート$U$でも、元に戻す**逆操作**を組み合わせて考えられます。測定を含まない量子ゲートを表す行列は**ユニタリ行列**で、その逆操作は$U^\dagger$です。$\dagger$は「行と列を入れ替え、各成分の複素共役を取る」ことを表します。複素共役では、例えば$a+bi$を$a-bi$にします。両方向に操作を打ち消せることを、

$$
U^\dagger U=UU^\dagger=I
$$

と書きます。$I$は状態を変えない恒等演算で、1量子ビットでは$\begin{pmatrix}1&0\\0&1\end{pmatrix}$です。

ここで、演算子$O$を変換$U$とその逆操作で挟み、

$$
O'=UOU^\dagger
$$

という演算子を作ります。これが$U$による**共役変換**です。回路で実現する順序は、右端から$U^\dagger$ → $O$ → $U$です。$U$で移した状態に$O'$を作用させると、

$$
O'(U|\psi\rangle)
=UO\underbrace{U^\dagger U}_{I}|\psi\rangle
=U(O|\psi\rangle)
$$

となります。つまり、**変換後の状態に対する$O'$の働きは、変換前の状態に$O$を作用させてから$U$で移す働きと対応します。** 基底を移す操作と、演算子の共役変換が結び付く理由です。

「同じ演算子を、新しい基底で表し直す」向きでは、逆に$U^\dagger O U$という行列になります。新しい基底での成分を並べた列ベクトルを$v$とすると、元の基底での状態ベクトルは$Uv$です。そこに演算を作用させ、新しい基底での成分へ戻すと$U^\dagger O(Uv)$となるためです。どちらも変換と逆変換で挟む形ですが、$U$をどちら向きの変換として使うかで位置が変わります。この節では$UOU^\dagger$で演算子を移す例から始め、測定の説明で操作の向きをもう一度確かめます。

Hは$H^\dagger=H$なので、共役変換は$HOH$という左右に同じHがある形になります。$HZH=X$は、ここで$O=Z$とした例です。以下では、この等式が二つの基底状態にも任意の重ね合わせにも成り立つことを詳しく導きます。

### 入力が0のとき、一段ずつ追う

最初のHを$|0\rangle$へ作用させます。

$$
H|0\rangle
=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}
\begin{pmatrix}1\\0\end{pmatrix}
=\frac{1}{\sqrt{2}}\begin{pmatrix}1\\1\end{pmatrix}
=\frac{|0\rangle+|1\rangle}{\sqrt{2}}
=|+\rangle.
$$

次のZは、$|1\rangle$の振幅だけにマイナスを付けます。

$$
Z|+\rangle
=\frac{|0\rangle-|1\rangle}{\sqrt{2}}
=|-\rangle.
$$

ここまでで二つの成分の符号が異なりました。最後のHで、その差がどう働くかを計算します。

$$
H|-\rangle
=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}
\frac{1}{\sqrt{2}}\begin{pmatrix}1\\-1\end{pmatrix}
=\frac{1}{2}\begin{pmatrix}1-1\\1+1\end{pmatrix}
=\begin{pmatrix}0\\1\end{pmatrix}
=|1\rangle.
$$

上の振幅では二つの寄与が打ち消し合い、下の振幅では足し合わされました。これがこの例での干渉です。全体の変化は次のようになります。

$$
|0\rangle\xrightarrow{H}|+\rangle
\xrightarrow{Z}|-\rangle\xrightarrow{H}|1\rangle.
$$

Xも$|0\rangle$を$|1\rangle$へ変えるので、この入力では作用が一致しました。

### 入力が1のときと、任意の重ね合わせ

演算子どうしが等しいと結論するには、$|1\rangle$に対する作用も必要です。まずHを作用させます。

$$
H|1\rangle
=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}
\begin{pmatrix}0\\1\end{pmatrix}
=\frac{1}{\sqrt{2}}\begin{pmatrix}1\\-1\end{pmatrix}
=|-\rangle.
$$

Zは下の振幅の符号をもう一度反転するため、$Z|-\rangle=|+\rangle$です。最後のHを計算すると、今度は下の振幅が打ち消し合います。

$$
H|+\rangle
=\frac{1}{2}\begin{pmatrix}1+1\\1-1\end{pmatrix}
=\begin{pmatrix}1\\0\end{pmatrix}
=|0\rangle.
$$

したがって、$|1\rangle\xrightarrow{H}|-\rangle\xrightarrow{Z}|+\rangle\xrightarrow{H}|0\rangle$となり、こちらもXと一致します。

行列による操作には、和を各項に分けて計算できる**線形性**があります。二つの基底状態に対する作用が分かれば、任意の重ね合わせも求められます。

$$
\begin{aligned}
HZH(\alpha|0\rangle+\beta|1\rangle)
&=\alpha HZH|0\rangle+\beta HZH|1\rangle\\
&=\alpha|1\rangle+\beta|0\rangle\\
&=X(\alpha|0\rangle+\beta|1\rangle).
\end{aligned}
$$

これで、すべての入力状態に対して$HZH=X$といえます。行列を直接掛けても、同じ結果を確かめられます。

$$
\begin{aligned}
HZH
&=\frac{1}{2}
\begin{pmatrix}1&1\\1&-1\end{pmatrix}
\begin{pmatrix}1&0\\0&-1\end{pmatrix}
\begin{pmatrix}1&1\\1&-1\end{pmatrix}\\
&=\frac{1}{2}
\begin{pmatrix}1&-1\\1&1\end{pmatrix}
\begin{pmatrix}1&1\\1&-1\end{pmatrix}\\
&=\begin{pmatrix}0&1\\1&0\end{pmatrix}=X.
\end{aligned}
$$

この等式では、符号や複素位相も含めて行列が一致します。測定確率だけが同じ、という結論より強い主張です。位相の違いは[次の節](#phase)で扱います。

### Qiskitで回路と行列を対応させる

次の例はQiskit 2.5.2とNumPyを使い、ローカルで実行できます。コードの記述順は、回路での時間順と同じです。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, XGate, ZGate
from qiskit.quantum_info import Operator, Statevector

qc = QuantumCircuit(1)
qc.h(0)
qc.z(0)
qc.h(0)

h = Operator(HGate()).data
z = Operator(ZGate()).data
x = Operator(XGate()).data
matrix = Operator(qc).data

print("circuit = HZH:", np.allclose(matrix, h @ z @ h, rtol=0, atol=1e-12))
print("circuit = X:", np.allclose(matrix, x, rtol=0, atol=1e-12))

for label in ("0", "1"):
    state = Statevector.from_label(label).evolve(qc)
    # 表示だけ小数点以下6桁に丸める。成分の順は [0の振幅, 1の振幅]。
    print(f"input {label}:", np.round(state.data, 6))
```

出力:

```text
circuit = HZH: True
circuit = X: True
input 0: [0.+0.j 1.+0.j]
input 1: [1.+0.j 0.+0.j]
```

`Operator(qc).data`は回路全体の行列、NumPy配列の`@`は行列積です。最初の二行は、回路の行列が手計算の積とXにそれぞれ一致することを確認しています。後半の配列は測定回数ではなく複素振幅で、`0.j`は虚部が0であることを表します。

計算機では$1/\sqrt{2}$などに丸め誤差が入るので、`np.allclose`で各成分の差がここでは`1e-12`以下かを確認しています。これは数値的な確認です。数学的に厳密な等式であることは、上の導出で示しています。

### ほかの演算子にも同じ考え方を使う

同じHによる共役変換をXやYにも適用すると、次の一組の関係が得られます。Yは三つ目のPauli演算子で、行列は$Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}$です。

$$
HXH=Z,\qquad HZH=X,\qquad HYH=-Y.
$$

Hによる変換はXとZを交換し、Yの符号を反転させます。例えばXは$|+\rangle$を変えず、$|-\rangle$にはマイナスを付けます。最初のHで$|0\rangle,|1\rangle$をこの二状態へ移し、Xを作用させ、最後のHで戻せば、$|0\rangle$はそのまま、$|1\rangle$にはマイナスが付きます。これが$HXH=Z$です。

変換に使うゲートもHに限りません。**Sゲート**は、$|1\rangle$の振幅に$i$を掛ける位相ゲートです。Sとその逆操作は、

$$
S=\begin{pmatrix}1&0\\0&i\end{pmatrix},\qquad
S^\dagger=\begin{pmatrix}1&0\\0&-i\end{pmatrix}
$$

となります。Sによる共役変換の一例を、行列で計算します。

$$
\begin{aligned}
SXS^\dagger
&=\begin{pmatrix}1&0\\0&i\end{pmatrix}
\begin{pmatrix}0&1\\1&0\end{pmatrix}
\begin{pmatrix}1&0\\0&-i\end{pmatrix}\\
&=\begin{pmatrix}0&-i\\i&0\end{pmatrix}=Y.
\end{aligned}
$$

YとZについても同様に求められます。変換をまとめると、次の表になります。

| 変換する演算子$O$ | Hによる$HOH^\dagger$ | Sによる$SOS^\dagger$ |
|---|---|---|
| X | Z | Y |
| Y | $-Y$ | $-X$ |
| Z | X | Z |

例えば表のSの列の一行目は、回路では$S^\dagger$ → X → Sの順です。Hと違い、$S^\dagger\ne S$なので、両側に同じSを置いた$SXS$とは区別します。また、表のマイナスも等式の一部です。$-Y$をYと厳密に等しいと扱うことはできません。位相の違いの扱いは[次の節](#phase)へつながります。

この表は、HとSがPauli演算子にどう作用するかをまとめたものです。任意のゲートで共役変換した結果が、必ず単独のX・Y・Zのいずれかになるとは限りません。基本ゲートの行列を確認したい場合は[Pauli、Hadamard、位相、回転](#basic-gates)を参照してください。

### 基底を戻してから測る

基底変換は、測定の向きを変えるためにも使えます。計算基底での測定は$|0\rangle$と$|1\rangle$に対応するビット0・1を読み出します。X基底で測るとは、代わりに$|+\rangle$と$|-\rangle$に対応する結果を読み出すことです。

Hは$|+\rangle$を$|0\rangle$へ、$|-\rangle$を$|1\rangle$へ戻します。したがって、**Hを適用してから計算基底で測ると、元の状態をX基底で測った結果の確率が得られます。** 回路に置くのはH一つと測定です。$HZH$という三つのゲートを置いてから測る手順ではありません。

例えば任意の状態をX基底で$|\psi\rangle=c_+|+\rangle+c_-|-\rangle$と表すと、測定前のHによって、

$$
H|\psi\rangle=c_+|0\rangle+c_-|1\rangle
$$

となります。Z測定で0・1を得る確率は、それぞれ$|c_+|^2,|c_-|^2$です。これは元の状態のX基底での確率です。ビット0に測定値$+1$、ビット1に$-1$を対応させれば、Xの期待値も求められます。

演算子でも同じ関係を表せます。測定前に適用するゲート列を$M$とすると、その後のZ測定は、元の状態に対する$M^\dagger ZM$という観測量の測定に対応します。観測量は「何を測るか」を表す演算子です。期待値の記法を使うと、

$$
\langle M\psi|Z|M\psi\rangle
=\langle\psi|M^\dagger ZM|\psi\rangle.
$$

$|M\psi\rangle$は$M|\psi\rangle$、$\langle M\psi|$はその複素共役転置である行ベクトルです。上の式は、左の行ベクトルを$\langle\psi|M^\dagger$と書き直したものです。期待値をこの形で計算する意味は[observableと期待値](#expectation)で詳しく扱います。

X測定では$M=H$なので、$M^\dagger ZM=HZH=X$です。ここに現れるZは最後に測る観測量であり、追加するZゲートではありません。前半の$UOU^\dagger$と左右の位置が異なるのは、ここでは「測定前に$M$を適用した結果を、元の状態の観測量で表す」という向きに読んでいるためです。

Y基底の二つの状態は、$|+i\rangle=(|0\rangle+i|1\rangle)/\sqrt{2}$と$|-i\rangle=(|0\rangle-i|1\rangle)/\sqrt{2}$です。SはX基底をこのY基底へ移します。測定するときは逆操作で戻すので、まず$S^\dagger$、次にHを適用します。

$$
|\mathord{\pm}i\rangle\xrightarrow{S^\dagger}|\mathord{\pm}\rangle
\xrightarrow{H}
\begin{cases}|0\rangle & (+)\\|1\rangle & (-).\end{cases}
$$

このゲート列は$M=HS^\dagger$です。積の逆操作では順序も逆になるので$M^\dagger=SH$となり、

$$
M^\dagger ZM=SHZHS^\dagger=SXS^\dagger=Y
$$

が成り立ちます。

| 測りたい基底 | 計算基底からその基底を作る$U$ | 測定前に戻す操作$M=U^\dagger$（時間順） | 最後の測定 |
|---|---|---|---|
| Z | $I$ | なし | Z測定 |
| X | $H$ | H | Z測定 |
| Y | $SH$（H → S） | $HS^\dagger$（$S^\dagger$ → H） | Z測定 |

以下では、同じ状態をX基底とY基底で測る確率をローカルで確かめます。前のコードとは独立して実行できます。状態を$\sqrt{3}|0\rangle/2+i|1\rangle/2$に選ぶと、測定の向きによる違いが見えます。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

psi = Statevector([np.sqrt(3) / 2, 1j / 2])
x_readout = QuantumCircuit(1)
x_readout.h(0)
y_readout = QuantumCircuit(1)
y_readout.sdg(0)
y_readout.h(0)

x_probabilities = psi.evolve(x_readout).probabilities()
y_probabilities = psi.evolve(y_readout).probabilities()

print("X basis [+, -]:", np.round(x_probabilities, 6))
print("Y basis [+i, -i]:", np.round(y_probabilities, 6))
```

出力:

```text
X basis [+, -]: [0.5 0.5]
Y basis [+i, -i]: [0.933013 0.066987]
```

`sdg`はSの逆操作$S^\dagger$です。ここでは測定前の変換までを回路に書き、`probabilities()`で、その後の計算基底測定の理論確率を求めています。有限回の測定から得た出現回数ではありません。配列は変換後のビット0・1の順で、元の状態のX基底では$+, -$、Y基底では$+i, -i$に対応します。

手計算でも、X測定前のHの後では振幅が$(\sqrt{3}+i)/(2\sqrt{2})$と$(\sqrt{3}-i)/(2\sqrt{2})$になるので、確率はどちらも$1/2$です。Y測定前では、まず$S^\dagger$で虚数の振幅$i/2$が$1/2$へ変わります。続くHの後の振幅は$(\sqrt{3}+1)/(2\sqrt{2})$と$(\sqrt{3}-1)/(2\sqrt{2})$なので、

$$
p_Y(+i)=\frac{(\sqrt{3}+1)^2}{8}=\frac{2+\sqrt{3}}{4},\qquad
p_Y(-i)=\frac{(\sqrt{3}-1)^2}{8}=\frac{2-\sqrt{3}}{4}
$$

となり、出力と一致します。測定後の状態や実際の測定回路は、第2章の[測定と基底](02-visualization-measurement.md#measurement-basis)で扱います。

### 間違えやすい考え方と確認問題

「Hを二回使うから消えてZだけが残る」と考えたくなりますが、間にあるZの作用を飛ばすことはできません。Hが連続する$HH=I$と、$HZH$は区別します。また、一つの入力に対する出力や測定確率だけでは、演算子の等式を確かめたことにはなりません。

次の問題を、ゲートを適用する順序と途中の状態を書いて解いてください。

1. 入力$|0\rangle$へH → Zの順に作用させた場合と、Z → Hの順に作用させた場合の最終状態は何ですか。
2. 真ん中のZをXに変えたH → X → Hは、どの演算子と等しくなりますか。$|0\rangle$と$|1\rangle$の両方で確かめてください。
3. $SXS^\dagger=Y$を回路として実行するゲートの時間順は何ですか。S → X → Sとしてよいですか。
4. $|+i\rangle$をY基底で測るため、$S^\dagger$ → H → Z測定を行うと、どのビットが出ますか。操作をH → $S^\dagger$の順へ変えても同じですか。

**解答と理由**

1. H → Zは$ZH|0\rangle=Z|+\rangle=|-\rangle$です。Z → Hは、最初のZが$|0\rangle$を変えないので$HZ|0\rangle=H|0\rangle=|+\rangle$です。同じ二つのゲートでも順序によって状態が変わります。この二状態はZ基底の測定確率がともに50/50なので、確率だけでは違いが見えません。
2. Xは二つの振幅を交換するので、$X|+\rangle=|+\rangle$、$X|-\rangle=-|-\rangle$です。そのため、入力$|0\rangle$は$|+\rangle\to|+\rangle\to|0\rangle$、入力$|1\rangle$は$|-\rangle\to-|-\rangle\to-|1\rangle$と変わります。これはZの作用そのもので、線形性から$HXH=Z$です。
3. 右端から$S^\dagger$ → X → Sです。Sは逆操作と同じではないので、S → X → Sでは別の行列になります。例えば$SXS|0\rangle=i|1\rangle$はYと一致しても、$SXS|1\rangle=i|0\rangle$は$Y|1\rangle=-i|0\rangle$と異なります。一つの入力だけの一致では不十分です。
4. 0が確率1で出ます。$S^\dagger|+i\rangle=|+\rangle$、$H|+\rangle=|0\rangle$だからです。順序を逆にすると、Hを適用した後の計算基底の確率は半分ずつで、後から$S^\dagger$を掛けても各振幅の絶対値は変わりません。したがって0・1が半分ずつになり、同じ測定にはなりません。

**判断の要点**: 回路の時間順を読み、右端から作用する式へ直し、途中の状態を追います。変換で演算を移すときは$UOU^\dagger$、測定したい基底を作る変換が$U$なら測定前には逆操作$U^\dagger$を使います。演算子の等式は、基底状態すべてへの作用か行列全体で確かめます。

公式参照: [Pauli演算子の共役変換](https://learning.quantum.ibm.com/course/foundations-of-quantum-error-correction/the-stabilizer-formalism)、[Operator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator)、[Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector)

<a id="phase"></a>
## global phaseとrelative phase

振幅の符号や$i$は、どのような場合に測定結果へ影響するのでしょうか。この節では、状態全体に共通する位相と、成分間の位相差を区別します。そのうえで、2つの状態や行列について「同じ」と言える範囲を判断します。

### 位相を角度で表す

複素数は、絶対値$r$と角度$\varphi$を使って$re^{i\varphi}$と表せます。ここで

$$
e^{i\varphi}=\cos\varphi+i\sin\varphi,
\qquad |e^{i\varphi}|=1
$$

です。この角度を**位相**（**phase**）と呼びます。角度の単位はラジアンで、$\pi$が180度、$\pi/2$が90度に対応します。例えば$1,-1,i,-i$は、それぞれ角度$0,\pi,\pi/2,-\pi/2$の位相因子です。これらを振幅に掛けても絶対値は変わりません。

### 全体に共通するglobal phase

状態の**すべての振幅**に同じ$e^{i\varphi}$を掛ける変化を、global phase（大域位相）の変化と呼びます。例えば

$$
|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},
\qquad
-i|+\rangle=\frac{-i|0\rangle-i|1\rangle}{\sqrt2}
$$

はglobal phaseだけが異なります。計算基底の確率は共に半々です。さらに、どちらへも同じゲート$U$を適用すると

$$
U(e^{i\varphi}|\psi\rangle)=e^{i\varphi}U|\psi\rangle
$$

となり、変化後も違いは全体の位相だけです。したがって、測定の基底を変えても両者を区別できません。この意味で**同じ物理的状態**を表します。ただし、配列の各要素が等しいという意味ではありません。

### 成分間のrelative phaseと干渉

一方、$|+\rangle$と$|-\rangle$では、$|0\rangle$の係数をそのままにして、$|1\rangle$の係数だけが負になっています。全体に同じ因子を掛ける操作では移り合いません。このような成分間の位相差をrelative phase（相対位相）と呼びます。

計算基底で測るだけでは、両方とも半々です。しかし、先に$H$を適用すると、[前節の計算](#matrix-order)のとおり$H|+\rangle=|0\rangle$、$H|-\rangle=|1\rangle$となり、確実に区別できます。ゲートが振幅を足し合わせる際に、相対位相によって強め合いや打ち消し合いが起こります。これが**干渉**です。

符号の違いだけでなく、一般の角度でも確かめましょう。

$$
|\psi_\varphi\rangle=\frac{|0\rangle+e^{i\varphi}|1\rangle}{\sqrt2}
$$

に$H$を適用すると、

$$
\begin{aligned}
H|\psi_\varphi\rangle
&=\frac{1}{\sqrt2}\left(
\frac{|0\rangle+|1\rangle}{\sqrt2}
+e^{i\varphi}\frac{|0\rangle-|1\rangle}{\sqrt2}\right)\\
&=\frac{1+e^{i\varphi}}2|0\rangle
+\frac{1-e^{i\varphi}}2|1\rangle.
\end{aligned}
$$

例えば0の確率は、$(1+e^{-i\varphi})(1+e^{i\varphi})/4$です。$e^{i\varphi}+e^{-i\varphi}=2\cos\varphi$なので、

$$
p(0)=\frac{1+\cos\varphi}{2},\qquad
p(1)=\frac{1-\cos\varphi}{2}.
$$

$H$の前は常に半々だった確率が、後では相対位相に依存します。$\varphi=0$なら0が確率1、$\varphi=\pi$なら1が確率1、$\varphi=\pi/2$なら半々です。

### 配列の一致と物理的な同値をコードで分ける

`np.allclose`は要素ごとの一致を許容誤差付きで調べます。`Statevector.equiv`は、global phaseを除いて同値かどうかを調べます。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

plus = Statevector([1 / np.sqrt(2), 1 / np.sqrt(2)])
global_shift = Statevector(-1j * plus.data)
minus = Statevector([1 / np.sqrt(2), -1 / np.sqrt(2)])
h = QuantumCircuit(1)
h.h(0)

print("same entries:", np.allclose(plus.data, global_shift.data))
print("same up to global phase:", plus.equiv(global_shift))
print("plus equivalent to minus:", plus.equiv(minus))
for name, state in [("plus", plus), ("global", global_shift), ("minus", minus)]:
    print(name, "before H:", np.round(state.probabilities(), 6))
    print(name, "after H:", np.round(state.evolve(h).probabilities(), 6))
```

出力:

```text
same entries: False
same up to global phase: True
plus equivalent to minus: False
plus before H: [0.5 0.5]
plus after H: [1. 0.]
global before H: [0.5 0.5]
global after H: [1. 0.]
minus before H: [0.5 0.5]
minus after H: [0. 1.]
```

最初の2状態は$H$の後も同じ確率です。3つ目は$|1\rangle$側だけの符号を変えているため、干渉の結果が変わります。

### ゲートの行列にもglobal phaseの違いがある

Z軸回転ゲートの行列は次の形です。回転ゲート全体の定義は[次節](#basic-gates)で扱います。

$$
R_z(\theta)=\begin{pmatrix}e^{-i\theta/2}&0\\0&e^{i\theta/2}\end{pmatrix}.
$$

$\theta=\pi$を代入すると、$e^{-i\pi/2}=-i$、$e^{i\pi/2}=i$なので、

$$
R_z(\pi)=\begin{pmatrix}-i&0\\0&i\end{pmatrix}
=-i\begin{pmatrix}1&0\\0&-1\end{pmatrix}=-iZ.
$$

任意の入力状態について、出力は$Z$の場合に全体の$-i$を掛けたものです。したがって、この1量子ビットへの作用はglobal phaseを除いて$Z$と同値ですが、厳密な行列は$Z$ではありません。

`QuantumCircuit.global_phase`は、回路全体の位相角をラジアンで保持します。角度$\gamma$を加えると、回路の行列全体に$e^{i\gamma}$が掛かります。ここでは$\pi/2$を加えれば、$i(-iZ)=Z$になります。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

rz = QuantumCircuit(1)
rz.rz(np.pi, 0)
z = QuantumCircuit(1)
z.z(0)
corrected = rz.copy()
corrected.global_phase += np.pi / 2

print("Rz(pi) equals Z:", np.allclose(Operator(rz).data, Operator(z).data))
print("Rz(pi) equivalent to Z:", Operator(rz).equiv(Operator(z)))
print("Rz(pi) equals -iZ:", np.allclose(Operator(rz).data, -1j * Operator(z).data))
print("corrected equals Z:", np.allclose(Operator(corrected).data, Operator(z).data))
```

出力:

```text
Rz(pi) equals Z: False
Rz(pi) equivalent to Z: True
Rz(pi) equals -iZ: True
corrected equals Z: True
```

ここでの`True`は浮動小数点の許容誤差内の一致です。厳密な関係$R_z(\pi)=-iZ$は、上の行列計算で示しています。

また、「1量子ビットの演算としてglobal phaseだけが違う」ことと、「その演算を条件付きで実行する大きな回路でも同値である」ことは別です。制御ゲートに組み込む場合は、位相が状態全体に掛かるかを改めて確認します。[複数量子ビットの節](#multi-entanglement)で例を扱います。

### 確認問題

1. $i|-\rangle$は$|-\rangle$と$|+\rangle$のどちらとglobal phaseを除いて同値ですか。
2. $(|0\rangle+i|1\rangle)/\sqrt2$に$H$を適用した後、計算基底で0が出る確率はいくつですか。
3. $R_z(\pi)$の回路にどのglobal phaseを加えれば、行列として$Z$に一致しますか。

**解答と理由**

1. $|-\rangle$です。$i$は両方の振幅へ共通に掛かり、成分間の負符号は残ります。
2. $\varphi=\pi/2$なので、$(1+\cos(\pi/2))/2=1/2$です。この測定だけでは$|+i\rangle$と$|-i\rangle$を区別できず、同値かどうかを判定するには不十分です。
3. $\pi/2$です。$e^{i\pi/2}(-iZ)=i(-iZ)=Z$となります。$2\pi$の整数倍を足した角度でも同じです。

判断するときは、すべての振幅に共通する因子かをまず調べます。そのうえで、要素の一致、global phaseを除いた同値、特定の測定での確率の一致のどれを確かめたいのかを分けます。

参照: [Statevector.equiv](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector#equiv)、[Operator.equiv](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator#equiv)、[RZGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RZGate)

<a id="basic-gates"></a>
## Pauli、Hadamard、位相、回転

基本ゲートの行列は、状態への作用と結び付けると読みやすくなります。この節では、振幅の入替え、位相の変更、角度を指定した回転を整理します。行列を暗記するだけでなく、入力状態と操作順から出力を求めることを目標にします。

### PauliとHadamardの作用

Pauli（パウリ）ゲートの行列は次のとおりです。

$$
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\qquad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
$$

行列の第1列は$|0\rangle$への作用、第2列は$|1\rangle$への作用です。例えば$Y$の第1列は$(0,i)^{\mathsf T}$なので、$Y|0\rangle=i|1\rangle$です。$\mathsf T$は、ここでは横に並べた成分を縦にする転置を表します。

| ゲート | $\lvert0\rangle$への作用 | $\lvert1\rangle$への作用 | $\alpha\lvert0\rangle+\beta\lvert1\rangle$への作用 |
|---|---|---|---|
| $X$ | $\lvert1\rangle$ | $\lvert0\rangle$ | $\beta\lvert0\rangle+\alpha\lvert1\rangle$ |
| $Y$ | $i\lvert1\rangle$ | $-i\lvert0\rangle$ | $-i\beta\lvert0\rangle+i\alpha\lvert1\rangle$ |
| $Z$ | $\lvert0\rangle$ | $-\lvert1\rangle$ | $\alpha\lvert0\rangle-\beta\lvert1\rangle$ |

$X$は振幅を交換し、$Z$は$|1\rangle$側の符号を反転します。$Y$では交換と位相の変更が同時に起こります。$Y|0\rangle$と$X|0\rangle$がglobal phaseを除いて同じでも、$Y$と$X$が任意の入力に同じ作用をするわけではありません。例えば$Y|+\rangle=-i|-\rangle$ですが、$X|+\rangle=|+\rangle$です。

Hadamard（アダマール）ゲートは

$$
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad
H(\alpha|0\rangle+\beta|1\rangle)
=\frac{\alpha+\beta}{\sqrt2}|0\rangle
+\frac{\alpha-\beta}{\sqrt2}|1\rangle
$$

です。$H|0\rangle=|+\rangle$、$H|1\rangle=|-\rangle$となり、もう一度適用すると$H|+\rangle=|0\rangle$、$H|-\rangle=|1\rangle$に戻ります。したがって「$H$を使うと必ず0と1が半々になる」とは言えません。入力の振幅の和と差によって、出力が決まります。

$X,Y,Z,H$はいずれも2回続けると恒等演算$I$になります。$Y$についても、例えば$Y(Y|0\rangle)=Y(i|1\rangle)=i(-i)|0\rangle=|0\rangle$です。途中の$i$を落とさずに計算すると、元に戻ることが分かります。

### 異なるゲートの順番を入れ替えられるか

[ゲートの合成](#matrix-order)で扱ったように、先に適用するゲートを右に書きます。$X$と$Z$について実際に掛けると、

$$
XZ=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
ZX=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
XZ=-ZX.
$$

つまり順番を入れ替えると符号が変わります。一般に、演算子$A,B$が次の関係を満たすとき、「**$A$と$B$は反交換する**（**anticommute**）」と言います。

$$
AB=-BA
$$

$XZ=-ZX$は、$X$と$Z$の反交換関係（**anticommutation relation**）を表しています。

上の$XZ=-ZX$という等式は、行列として厳密に成り立つ等式です。したがって、$XZ$と$ZX$は符号が逆の異なる行列であり、$XZ=ZX$とは書けません。一方で、それぞれを同じ入力状態に適用した出力はglobal phaseだけが異なるため、同じ測定確率を与えます。

Pauli行列$X,Y,Z$は、異なる二つを選ぶと反交換します。すなわち、$XY=-YX$、$YZ=-ZY$、$ZX=-XZ$です。

反交換はPauli行列に固有の性質ではありません。例えば、本章のHadamardゲート$H$と$Y$も$HY=-YH$を満たします。

交換/可換・反交換・非可換の関係は以下のように整理できます。

| 性質 | 条件 | 積の順番を入れ替えると |
|---|---|---|
| 交換する・可換である | $AB=BA$ | 同じになる |
| 反交換する | $AB=-BA$ | 符号が反転する |
| 非可換である | $AB\ne BA$ | 同じにはならない |

特に重要な点として、「非可換なら反交換する」とは限りません。 順番によって異なる行列になっても、その違いが符号の反転だけとは限らないためです。

ここでは1量子ビットの行列を掛けています。別々の量子ビットへゲートを適用する場合は、回路全体の演算子をテンソル積で表してから比較します。詳しくは[異なる量子ビットへの作用とゲートの順番](#different-qubit-order)で扱います。

#### Pauliゲートの合成とのつながり

計算した$XZ$を、先に示した$Y$の行列と比較すると、$iXZ=Y$であることが分かります。したがって$XZ=-iY$です。これは、先に$Z$、次に$X$を適用する回路が、$Y$を1回適用する回路とglobal phaseを除いて同値であることを示します。

### 位相ゲートを一つの式で捉える

位相ゲート$P(\varphi)$は、$|0\rangle$の振幅を変えず、$|1\rangle$の振幅にだけ$e^{i\varphi}$を掛けます。

$$
P(\varphi)=\begin{pmatrix}1&0\\0&e^{i\varphi}\end{pmatrix},
\qquad
P(\varphi)(\alpha|0\rangle+\beta|1\rangle)
=\alpha|0\rangle+e^{i\varphi}\beta|1\rangle.
$$

この角度を固定したものが$S$と$T$です。

$$
S=\begin{pmatrix}1&0\\0&i\end{pmatrix},\qquad
S^\dagger=\begin{pmatrix}1&0\\0&-i\end{pmatrix},\qquad
T=\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}.
$$

$S=P(\pi/2)$、$T=P(\pi/4)$です。$\dagger$は複素共役を取って転置する記号で、ユニタリゲートでは逆演算を表します。$S^\dagger=P(-\pi/2)$、$T^\dagger=P(-\pi/4)$なので、反対向きの位相を与えると元に戻せます。Qiskitではそれぞれ`.s()`、`.t()`、`.sdg()`、`.tdg()`を使います。

例えば$S^\dagger|+i\rangle$は

$$
S^\dagger\frac{|0\rangle+i|1\rangle}{\sqrt2}
=\frac{|0\rangle+(-i)i|1\rangle}{\sqrt2}
=\frac{|0\rangle+|1\rangle}{\sqrt2}=|+\rangle
$$

となります。また、位相因子は掛けると角度が足されるので、

$$
P(\varphi)P(\lambda)=P(\varphi+\lambda),
\qquad S^2=Z,\qquad T^2=S,\qquad T^4=Z.
$$

これらはglobal phaseを除く必要のない、行列としての等式です。

### 回転ゲートの指数と半角の意味

1量子ビットの純粋状態は、global phaseの違いを同一視すると、球面上の点として表せます。この表現が**Bloch球**です。$|0\rangle$と$|1\rangle$をZ軸の正・負の端、$|+\rangle$と$|-\rangle$をX軸の正・負の端、$|+i\rangle$と$|-i\rangle$をY軸の正・負の端に置きます。「回転」は、この状態を表す点を指定した軸の周りに動かすことを指します。図による見方は[第2章](02-visualization-measurement.md)で扱い、ここでは振幅を行列で計算します。

X・Y・Z軸に関する回転ゲートは、次のように定義します。角度$\theta$はラジアンです。

$$
\begin{aligned}
R_x(\theta)&=\exp\!\left(-\frac{i\theta X}{2}\right),\\
R_y(\theta)&=\exp\!\left(-\frac{i\theta Y}{2}\right),\\
R_z(\theta)&=\exp\!\left(-\frac{i\theta Z}{2}\right).
\end{aligned}
$$

ここでの$\exp$は**行列の指数関数**です。各要素へ個別に指数関数を適用するという意味ではありません。行列$A$について、

$$
\exp(A)=I+A+\frac{A^2}{2!}+\frac{A^3}{3!}+\cdots
$$

と定義します。$n!$は$1$から$n$までの整数の積です。Pauli行列を$\sigma$と書くと、$\sigma^2=I$なので、偶数乗は$I$、奇数乗は$\sigma$になります。指数関数の偶数次と奇数次をまとめると、

$$
\begin{aligned}
\exp\!\left(-\frac{i\theta\sigma}{2}\right)
&=\left(1-\frac{(\theta/2)^2}{2!}+\cdots\right)I
-i\left(\frac\theta2-\frac{(\theta/2)^3}{3!}+\cdots\right)\sigma\\
&=\cos\frac\theta2\,I-i\sin\frac\theta2\,\sigma.
\end{aligned}
$$

括弧内は、それぞれ余弦と正弦の級数です。この式に$X,Y,Z$を代入すると、具体的な行列が得られます。

$$
\begin{aligned}
R_x(\theta)&=\begin{pmatrix}
\cos(\theta/2)&-i\sin(\theta/2)\\
-i\sin(\theta/2)&\cos(\theta/2)
\end{pmatrix},\\
R_y(\theta)&=\begin{pmatrix}
\cos(\theta/2)&-\sin(\theta/2)\\
\sin(\theta/2)&\cos(\theta/2)
\end{pmatrix},\\
R_z(\theta)&=\begin{pmatrix}
e^{-i\theta/2}&0\\0&e^{i\theta/2}
\end{pmatrix}.
\end{aligned}
$$

回転角$\theta$に対して、振幅には**半角$\theta/2$**が現れます。例えば$R_y(\theta)|0\rangle$の振幅は$(\cos(\theta/2),\sin(\theta/2))$なので、計算基底の確率は$(\cos^2(\theta/2),\sin^2(\theta/2))$です。確率の差は$\cos\theta$となり、[期待値](#expectation)で扱うZ方向の測定値の平均に対応します。

### 回転した状態を計算する

$\theta=\pi/3$なら半角は$\pi/6$で、$\cos(\pi/6)=\sqrt3/2$、$\sin(\pi/6)=1/2$です。したがって、

$$
\begin{aligned}
R_x(\pi/3)|0\rangle&=\frac{\sqrt3}{2}|0\rangle-\frac{i}{2}|1\rangle,\\
R_y(\pi/3)|0\rangle&=\frac{\sqrt3}{2}|0\rangle+\frac{1}{2}|1\rangle.
\end{aligned}
$$

どちらも計算基底の確率は$(3/4,1/4)$です。ただし、2つ目の振幅の相対位相が異なるため、同じ物理的状態ではありません。

```python
import numpy as np
from qiskit.circuit.library import RXGate, RYGate, SGate, TGate, XGate
from qiskit.quantum_info import Operator, Statevector

zero = Statevector.from_label("0")
rx_state = zero.evolve(RXGate(np.pi / 3))
ry_state = zero.evolve(RYGate(np.pi / 3))
t = Operator(TGate()).data
s = Operator(SGate()).data
x = Operator(XGate()).data

print("Rx amplitudes:", np.round(rx_state.data, 6))
print("Ry amplitudes:", np.round(ry_state.data, 6))
print("Rx probabilities:", np.round(rx_state.probabilities(), 6))
print("Ry probabilities:", np.round(ry_state.probabilities(), 6))
print("same up to global phase:", rx_state.equiv(ry_state))
print("T squared equals S:", np.allclose(t @ t, s))
print("Rx(pi) equals -iX:", np.allclose(Operator(RXGate(np.pi)).data, -1j * x))
```

出力:

```text
Rx amplitudes: [0.866025+0.j  0.      -0.5j]
Ry amplitudes: [0.866025+0.j 0.5     +0.j]
Rx probabilities: [0.75 0.25]
Ry probabilities: [0.75 0.25]
same up to global phase: False
T squared equals S: True
Rx(pi) equals -iX: True
```

`data`は振幅、`probabilities()`はその絶対値の二乗を返します。`np.round(..., 6)`は、表示のために小数点以下6桁へ丸めています。最後の行は、半角が$\pi/2$なら余弦が0、正弦が1となることに対応します。同様に$R_y(\pi)=-iY$、$R_z(\pi)=-iZ$です。

### 逆回転と位相ゲートとの関係

同じ軸については、回転角を足せます。例えば

$$
R_y(\theta)R_y(\lambda)=R_y(\theta+\lambda),
\qquad R_y(-\theta)R_y(\theta)=I.
$$

X軸・Z軸でも同様です。異なる軸の回転では、単に角度を足して一方の軸の回転にまとめることはできません。

また、$R_z(\theta)$の行列から共通因子$e^{-i\theta/2}$を取り出すと、

$$
R_z(\theta)=e^{-i\theta/2}
\begin{pmatrix}1&0\\0&e^{i\theta}\end{pmatrix}
=e^{-i\theta/2}P(\theta).
$$

つまり$P(\theta)$と$R_z(\theta)$は、同じ相対位相の変化を与えますが、global phaseが異なります。特に$P(\pi)=Z$は厳密な等式で、$R_z(\pi)=-iZ$とは区別します。

### 確認問題

1. $Y|1\rangle$を求め、続けてもう一度$Y$を適用してください。
2. $T$を4回適用すると、どのゲートに一致しますか。
3. $R_y(\pi)|0\rangle$は何ですか。また、$R_y(\pi)$の行列は$Y$と厳密に等しいですか。
4. $R_x(\pi/3)$を取り消すには、同じ軸でどの回転を加えますか。

**解答と理由**

1. $Y|1\rangle=-i|0\rangle$で、$Y(-i|0\rangle)=(-i)i|1\rangle=|1\rangle$です。
2. $Z$です。$|1\rangle$側の位相が$4\times\pi/4=\pi$となり、$e^{i\pi}=-1$になるためです。
3. $|1\rangle$です。半角の式へ代入すると$(0,1)$になります。一方、行列は$-iY$であり、$Y$そのものではありません。
4. $R_x(-\pi/3)$です。同じ軸の角度が足されて0となり、恒等演算に戻ります。

ゲートを計算するときは、まず振幅への作用を確認し、合成では順番を保ちます。回転は半角を代入し、最後にglobal phaseも含めて行列が一致するかを確認します。

参照: [RXGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RXGate)、[RYGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RYGate)、[RZGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RZGate)

<a id="multi-entanglement"></a>
## 複数量子ビット、CX、もつれ

量子ビットを2つに増やすと、個々の状態を並べるだけでは表せない状態が現れます。この節では、テンソル積で2量子ビットを表し、CXの作用を追います。そのうえで、もつれと測定結果の相関の関係を調べます。

### 2量子ビットの状態を表す

2量子ビットの計算基底には、$|00\rangle,|01\rangle,|10\rangle,|11\rangle$の4つがあります。本章ではQiskitに合わせて**$|q_1q_0\rangle$の順**で書きます。例えば$|01\rangle$は、$q_1$が0、$q_0$が1です。量子ビット番号と左右の関係は[次節](#bit-pauli-order)で整理します。

2量子ビット全体の純粋状態は

$$
|\psi\rangle=A|00\rangle+B|01\rangle+C|10\rangle+D|11\rangle
\quad\longleftrightarrow\quad
\begin{pmatrix}A\\B\\C\\D\end{pmatrix}
$$

と表します。$A,B,C,D$は複素振幅で、$|A|^2+|B|^2+|C|^2+|D|^2=1$です。両方を計算基底で測定すると、例えば01が出る確率は$|B|^2$です。

まず、それぞれの量子ビットに状態を割り当てられる場合を考えます。2つの状態を組み合わせる演算を**テンソル積**（**tensor product**）と呼び、$\otimes$で表します。

$$
\begin{aligned}
&\left(a|0\rangle+b|1\rangle\right)
\otimes\left(c|0\rangle+d|1\rangle\right)\\
&\qquad=ac|00\rangle+ad|01\rangle+bc|10\rangle+bd|11\rangle.
\end{aligned}
$$

左が$q_1$、右が$q_0$です。それぞれの項を掛け合わせ、$|0\rangle\otimes|1\rangle$を$|01\rangle$とまとめています。ベクトルでは、

$$
\begin{pmatrix}a\\b\end{pmatrix}\otimes
\begin{pmatrix}c\\d\end{pmatrix}
=\begin{pmatrix}ac\\ad\\bc\\bd\end{pmatrix}.
$$

このように個々の状態のテンソル積で書ける状態を**積状態**（**product state**）と呼びます。例えば$q_1$が$|0\rangle$、$q_0$が$|+\rangle$なら、

$$
|0\rangle\otimes|+\rangle
=\frac{|00\rangle+|01\rangle}{\sqrt2}
\quad\longleftrightarrow\quad
\frac1{\sqrt2}\begin{pmatrix}1\\1\\0\\0\end{pmatrix}.
$$

後で使う$|0+\rangle$という書き方も、このテンソル積の略記です。

### CXのcontrolとtarget

CX（controlled-X、CNOTとも呼ぶ）は、**制御側**（**control**）**が1の成分で、標的側**（**target**）**へ$X$を適用する**ゲートです。Qiskitの`.cx(control, target)`では、第1引数が制御側です。

`qc.cx(0, 1)`なら、右側の$q_0$を見て、左側の$q_1$を反転します。

| 入力 $\lvert q_1q_0\rangle$ | 制御側$q_0$ | 標的側$q_1$の操作 | 出力 |
|---|---|---|---|
| $\lvert00\rangle$ | 0 | そのまま | $\lvert00\rangle$ |
| $\lvert01\rangle$ | 1 | 0から1へ | $\lvert11\rangle$ |
| $\lvert10\rangle$ | 0 | そのまま | $\lvert10\rangle$ |
| $\lvert11\rangle$ | 1 | 1から0へ | $\lvert01\rangle$ |

各出力のベクトルを列に並べれば、同じ基底順の行列が得られます。

$$
\mathrm{CX}_{0\to1}=
\begin{pmatrix}
1&0&0&0\\
0&0&0&1\\
0&0&1&0\\
0&1&0&0
\end{pmatrix}.
$$

重ね合わせに対しても、各成分へこの表の操作を行い、振幅付きで足します。制御側を途中で測定する操作ではありません。

### Bell状態を一段ずつ作る

初期状態$|00\rangle$から、$q_0$へ$H$を適用します。$q_1$はそのままなので、

$$
|00\rangle\ \xrightarrow{H\text{ on }q_0}\
|0\rangle\otimes|+\rangle
=\frac{|00\rangle+|01\rangle}{\sqrt2}.
$$

次にCXを適用します。表から$|00\rangle$はそのまま、$|01\rangle$は$|11\rangle$に移るので、

$$
\frac{|00\rangle+|01\rangle}{\sqrt2}
\ \xrightarrow{\mathrm{CX}_{0\to1}}\
\frac{|00\rangle+|11\rangle}{\sqrt2}
=|\Phi^+\rangle.
$$

この$|\Phi^+\rangle$は、代表的な**Bell状態**です。次のコードで振幅と確率を確かめます。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)
qc.h(0)
after_h = Statevector.from_instruction(qc)
qc.cx(0, 1)
bell = Statevector.from_instruction(qc)

# この例の振幅はすべて実数なので、実部だけを表示する。
print("after H amplitudes:", np.round(after_h.data.real, 6))
print("Bell amplitudes:", np.round(bell.data.real, 6))
print("Bell probabilities:", np.round(bell.probabilities(), 6))
```

出力:

```text
after H amplitudes: [0.707107 0.707107 0.       0.      ]
Bell amplitudes: [0.707107 0.       0.       0.707107]
Bell probabilities: [0.5 0.  0.  0.5]
```

`Statevector.from_instruction(qc)`は、全量子ビットが0の状態から回路を適用した状態を計算します。配列の順は00、01、10、11です。最後の行は、同時に測ると00と11が各$1/2$で、01と10は出ないことを示します。

### なぜ個々の状態へ分解できないのか

Bell状態を$(a|0\rangle+b|1\rangle)\otimes(c|0\rangle+d|1\rangle)$と書けると仮定すると、振幅を比較して

$$
ac=\frac1{\sqrt2},\quad ad=0,\quad bc=0,\quad bd=\frac1{\sqrt2}
$$

が必要です。$ac$と$bd$が0でないためには、$a,b,c,d$がすべて0でない必要があります。しかし、それでは$ad=bc=0$にできません。したがって、この状態は個々の純粋状態の積に分解できません。このような純粋状態を**もつれた状態**（**entangled state**）と呼びます。

各量子ビットだけに注目すると、0と1は半々です。ただし、それぞれが独立な$|+\rangle$であるわけではありません。$|+\rangle\otimes|+\rangle$なら4つの振幅がすべて$1/2$であり、01や10も各$1/4$の確率で現れます。

### 測定結果の相関だけでもつれが分かるか

Bell状態では、両方をZ基底、つまり計算基底で測ると、結果は必ず一致します。しかし、古典的なコインで「今回は$|00\rangle$を準備する」「今回は$|11\rangle$を準備する」を半々に選んでも、同じ確率分布になります。このように、状態を確率的に選ぶ準備を**混合**（**mixture**）と呼びます。

混合の測定確率は、各状態の測定確率を重み付きで足して求めます。Bell状態のように、まず振幅を足してから絶対値の二乗を取る操作とは異なります。そのため、Z基底で結果が一致することだけでは、もつれの根拠として不十分です。

違いを見るため、両方をX基底で測ります。[測定基底の変換](#matrix-order)のとおり、各量子ビットへ$H$を適用してから計算基底で測ればよいので、Bell状態は

$$
\begin{aligned}
(H\otimes H)|\Phi^+\rangle
&=\frac{|++\rangle+|--\rangle}{\sqrt2}\\
&=\frac{1}{2\sqrt2}\bigl[
(|00\rangle+|01\rangle+|10\rangle+|11\rangle)\\
&\qquad\qquad\quad+(|00\rangle-|01\rangle-|10\rangle+|11\rangle)\bigr]\\
&=\frac{|00\rangle+|11\rangle}{\sqrt2}
\end{aligned}
$$

となります。01と10の振幅が打ち消し合い、結果は再び一致します。一方、混合では$|00\rangle$は$|++\rangle$へ、$|11\rangle$は$|--\rangle$へ移ります。それぞれの計算基底の確率は4通りとも$1/4$なので、混合でも4通りが均等です。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

prepare = QuantumCircuit(2)
prepare.h(0)
prepare.cx(0, 1)
bell = Statevector.from_instruction(prepare)
x_readout = QuantumCircuit(2)
x_readout.h(0)
x_readout.h(1)

bell_x = bell.evolve(x_readout).probabilities()
mixed_x = (
    0.5 * Statevector.from_label("00").evolve(x_readout).probabilities()
    + 0.5 * Statevector.from_label("11").evolve(x_readout).probabilities()
)
print("Bell, X readout:", np.round(bell_x, 6))
print("mixture, X readout:", np.round(mixed_x, 6))
```

出力:

```text
Bell, X readout: [0.5 0.  0.  0.5]
mixture, X readout: [0.25 0.25 0.25 0.25]
```

このX基底でのビット0は$|+\rangle$側、1は$|-\rangle$側の結果です。上の比較は、Bell状態とこの混合が異なることを示しています。任意の状態について、1種類の相関だけからもつれを判定できると一般化しないでください。また、ここで示したのはZ基底とX基底での相関であり、どの同一基底でも結果が一致するという主張ではありません。

### 制御ゲートについての2つの注意

CXを適用すれば、常にもつれができるわけではありません。例えば入力が$|++\rangle$なら、標的側の$|+\rangle$は$X$で変わらないため、CXの後も$|++\rangle$のままです。出力が積状態に分解できるかを確認する必要があります。

また、[global phase](#phase)は「全体に共通」という条件が重要です。制御側を$q_0$として、1の成分だけで標的側へ$-I$を適用すると、

$$
\frac{|00\rangle+|01\rangle}{\sqrt2}
\ \longmapsto\
\frac{|00\rangle-|01\rangle}{\sqrt2}.
$$

標的側だけなら$I$と$-I$はglobal phaseを除いて同値ですが、制御付きでは$|01\rangle$側だけに負符号が付きます。2量子ビット全体ではrelative phaseの変化です。このため、制御ゲートを作る前の行列のglobal phaseを不用意に捨ててはいけません。

### 確認問題

1. $q_1$が$|+\rangle$、$q_0$が$|0\rangle$の積状態を、計算基底で展開してください。
2. 入力$|01\rangle$へ`cx(1, 0)`を適用すると、どうなりますか。
3. $|\Phi^+\rangle$へもう一度`cx(0, 1)`を適用すると、もつれは残りますか。
4. 計算基底で00と11が半々に出たことだけで、Bell状態だと判断できますか。

**解答と理由**

1. $|+\rangle\otimes|0\rangle=(|00\rangle+|10\rangle)/\sqrt2$です。変わるのは左側の$q_1$です。
2. $|01\rangle$のままです。制御側は左側の$q_1$であり、その値が0なので標的側は反転しません。
3. 残りません。$|11\rangle$が$|01\rangle$へ戻り、$(|00\rangle+|01\rangle)/\sqrt2=|0\rangle\otimes|+\rangle$という積状態になります。
4. 判断できません。$|00\rangle$と$|11\rangle$を古典的に半々で準備した混合でも、同じ結果になるためです。

複数量子ビットでは、まずketの順番を固定し、各基底状態へゲートを適用します。もつれを考えるときは、全体の振幅と、測定後の確率分布を分けて読みます。

参照: [CXGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.CXGate)、[Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector)

<a id="bit-pauli-order"></a>
## bit/qubit orderingとPauli label

「回路図の上の線」「文字列の左端」「配列の先頭」は、それぞれ何を表すのでしょうか。この節では、回路、状態ベクトル、測定結果、Pauli文字列の対応を整理します。量子ビット番号を正しく割り当て、2量子ビット以上の出力を読めるようにします。

### 回路図、ket、配列を対応させる

Qiskitの回路図では、既定で$q_0$を一番上に描きます。一方、2量子ビットのketは$|q_1q_0\rangle$の順です。$q_0$の値を整数の$2^0$の桁、$q_1$の値を$2^1$の桁に対応させるためです。この$2^0$の桁を**最下位ビット**（**least-significant bit、LSB**）と呼びます。

状態ベクトルの添字は、ketのビット列を2進数として読んだ整数です。

| 配列の添字 | ket | $q_1$ | $q_0$ | 整数としての値 |
|---|---|---|---|---|
| 0 | $\lvert00\rangle$ | 0 | 0 | $2\times0+0=0$ |
| 1 | $\lvert01\rangle$ | 0 | 1 | $2\times0+1=1$ |
| 2 | $\lvert10\rangle$ | 1 | 0 | $2\times1+0=2$ |
| 3 | $\lvert11\rangle$ | 1 | 1 | $2\times1+1=3$ |

例えば$|00\rangle$の$q_0$だけを$X$で反転すると$|01\rangle$になり、状態ベクトルでは添字1の振幅が1です。$q_1$だけを反転すれば$|10\rangle$なので、添字2が1になります。

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

flip_q0 = QuantumCircuit(2)
flip_q0.x(0)
flip_q1 = QuantumCircuit(2)
flip_q1.x(1)

print("X on q0 probabilities:", Statevector.from_instruction(flip_q0).probabilities())
print("X on q1 probabilities:", Statevector.from_instruction(flip_q1).probabilities())
```

出力:

```text
X on q0 probabilities: [0. 1. 0. 0.]
X on q1 probabilities: [0. 0. 1. 0.]
```

ここでの0や1は測定確率です。`[0., 1., 0., 0.]`を4つの量子ビットの値と読むのではなく、「2量子ビットの4通りの結果のうち、01だけが確率1」と読みます。一般に$n$量子ビットの状態ベクトルには$2^n$個の振幅があります。

回路図を`draw(reverse_bits=True)`で描くと上下の表示順を反転できますが、ゲートの作用や状態ベクトルの並び順は変わりません。

### 測定結果の文字列は古典ビットの並び

測定では、量子ビットの結果を**古典ビット**（**classical bit**）へ保存します。`qc.measure(量子ビット, 古典ビット)`の第2引数が保存先です。

2ビットの古典レジスタ`c`なら、結果の文字列は`c1 c0`の順です。`q0`を`c0`へ、`q1`を`c1`へ測定した場合は、量子ビットの並びとそのまま対応します。保存先を入れ替えた場合は、この対応も変わります。

次の例では、量子状態$|q_1q_0\rangle=|01\rangle$を準備し、$q_0$を$c_1$、$q_1$を$c_0$へ保存します。したがって、古典ビットの結果は`10`です。

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2, 2)
qc.x(0)
qc.measure(0, 1)
qc.measure(1, 0)

sampler = StatevectorSampler(seed=7)
result = sampler.run([qc], shots=8).result()
print(result[0].data.c.get_counts())
```

出力:

```text
{'10': 8}
```

`StatevectorSampler`は、ローカルで状態を計算して測定結果をサンプリングします。`shots=8`は8回分の測定を指定し、`get_counts()`は結果ごとの回数を返します。この例では確率1の結果を測るため、8回とも同じです。一般の重ね合わせでは回数は変動します。`c`は`QuantumCircuit(2, 2)`で作られる古典レジスタの名前です。結果オブジェクトの詳しい読み方は[第5章](05-sampler.md)で扱います。

測定結果を読む際には、文字列の順番に加えて、`measure`の保存先も確認します。複数の古典レジスタがある場合は、どのレジスタの結果を読んでいるかも区別します。

### Pauli labelの右端が$q_0$

Pauli labelは、各量子ビットへ作用する$I,X,Y,Z$を並べた文字列です。状態のketと同じく、右端が$q_0$です。$I$は、その量子ビットを変えない恒等演算です。

| label | $q_1$への作用 | $q_0$への作用 | 演算子の表現 |
|---|---|---|---|
| `"XI"` | $X$ | $I$ | $X\otimes I$ |
| `"IX"` | $I$ | $X$ | $I\otimes X$ |
| `"XZ"` | $X$ | $Z$ | $X\otimes Z$ |
| `"IY"` | $I$ | $Y$ | $I\otimes Y$ |

演算子にもテンソル積を使います。$A\otimes B$は、左の量子ビットへ$A$、右へ$B$を適用する演算です。積状態への作用は

$$
(A\otimes B)(|u\rangle\otimes|v\rangle)
=(A|u\rangle)\otimes(B|v\rangle)
$$

となります。重ね合わせには、各項へこの作用を適用して足します。例えば`"XZ"`を$|01\rangle$へ適用すると、

$$
(X\otimes Z)|01\rangle
=(X|0\rangle)\otimes(Z|1\rangle)
=|1\rangle\otimes(-|1\rangle)=-|11\rangle.
$$

ここでの文字列`"XZ"`は、**別々の量子ビットへのテンソル積**です。[基本ゲートの節](#basic-gates)で扱った、同じ量子ビットへ先に$Z$、次に$X$を適用する行列積$XZ$とは異なります。前者は2量子ビットの$4\times4$行列、後者は1量子ビットの$2\times2$行列です。

<a id="different-qubit-order"></a>
### 異なる量子ビットへの作用とゲートの順番

$q_1$へ$X$、$q_0$へ$Z$を適用するとき、この2つの操作は順番を入れ替えられるでしょうか。先に扱った$XZ=-ZX$だけでは判断できません。今回は作用する量子ビットが異なるので、まず各操作を**2量子ビット全体の演算子**として表します。

$$
U_X=X\otimes I,\qquad U_Z=I\otimes Z.
$$

$U_X$は$q_1$へ$X$を適用し、$q_0$には何もしません。$U_Z$は$q_1$には何もせず、$q_0$へ$Z$を適用します。どちらも$4\times4$行列で、$X,Z$そのものとは区別します。

#### テンソル積の演算子を順に適用する

1量子ビットの演算子を$A,B,C,D$とし、先に$C\otimes D$、次に$A\otimes B$を適用します。積状態$|u\rangle\otimes|v\rangle$への作用を一段ずつ書くと、

$$
\begin{aligned}
&(A\otimes B)(C\otimes D)(|u\rangle\otimes|v\rangle)\\
&\quad=(A\otimes B)\bigl((C|u\rangle)\otimes(D|v\rangle)\bigr)\\
&\quad=(AC|u\rangle)\otimes(BD|v\rangle).
\end{aligned}
$$

左の量子ビットでは$C$の後に$A$、右では$D$の後に$B$が作用するので、それぞれの合成は$AC$と$BD$です。これは$(AC)\otimes(BD)$を適用した結果と同じです。

4つの計算基底状態はすべて積状態なので、上で比較した二つの演算子は、どの計算基底状態に対しても同じ結果を与えます。また、任意の2量子ビットの状態ベクトルは、この4つの基底状態の重ね合わせで表せます。さらに、行列による演算は線形なので、重ね合わせに演算子を適用するときは、各基底状態に演算子を適用し、それぞれの結果に重ね合わせの係数を掛けて足し合わせることができます。したがって、二つの演算子は任意の状態ベクトルに対して同じ結果を与え、行列として等しいことが分かります。

結果として、次の行列の等式が成り立ちます。この例では、両辺は同じ$4\times4$行列です。

$$
(A\otimes B)(C\otimes D)=(AC)\otimes(BD)
$$

この式でまとめているのは**各量子ビットへの演算の合成**であり、$AC$を$CA$へ入れ替えているわけではありません。

#### 異なる量子ビットに作用するゲートは交換する

$q_1$への$X$と$q_0$への$Z$について、適用する順番を入れ替えても、合成演算の行列が同じになることを確かめます。
上で導いたテンソル積の合成規則に従い、左の量子ビットへの行列同士、右の量子ビットへの行列同士を、それぞれ順序を保って掛けます。具体的には、上の式に$A=X,\ B=I,\ C=I,\ D=Z$を代入すると、$(X\otimes I)(I\otimes Z)=(XI)\otimes(IZ)$となります。ここで、$XI$は$q_1$への合成演算、$IZ$は$q_0$への合成演算を表しています。

$$
\begin{aligned}
U_XU_Z&=(X\otimes I)(I\otimes Z)
       =(XI)\otimes(IZ)=X\otimes Z,\\
U_ZU_X&=(I\otimes Z)(X\otimes I)
       =(IX)\otimes(ZI)=X\otimes Z.
\end{aligned}
$$

1行目は先に$q_0$へ$Z$、次に$q_1$へ$X$を適用する順序です。2行目はその逆です。結果が同じ行列になるため、**$U_X$と$U_Z$は交換します**。ここではglobal phaseを除く必要もありません。

これは演算子全体の等式なので、入力を積状態に限定していません。Bell状態など、もつれた状態に適用しても二つの順序は同じ出力を与えます。また、$X,Z$を任意の1量子ビットゲート$U,V$に置き換えても、同じ計算で両方の積が$U\otimes V$になります。したがって、**別々の量子ビットに作用する1量子ビットゲートは交換します**。

一方、両方を$q_0$へ適用するなら、比較する演算子は$I\otimes X$と$I\otimes Z$です。

$$
\begin{aligned}
(I\otimes X)(I\otimes Z)&=I\otimes(XZ),\\
(I\otimes Z)(I\otimes X)&=I\otimes(ZX)
                         =-I\otimes(XZ).
\end{aligned}
$$

この場合は反交換します。$XZ=-ZX$というPauli行列の性質はそのままで、**どの量子ビットへ作用するかによって、回路全体として比較する行列が変わる**のです。

#### Qiskitで回路と行列を対応させる

次の例では、$q_1$への$X$と$q_0$への$Z$を、逆の順番で追加した2つの回路を作ります。`Operator(回路).data`は回路全体の行列です。`Pauli("XZ").to_matrix()`は、先ほど導いた$X\otimes Z$を表します。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Pauli

x_then_z = QuantumCircuit(2)
x_then_z.x(1)
x_then_z.z(0)

z_then_x = QuantumCircuit(2)
z_then_x.z(0)
z_then_x.x(1)

u_x_then_z = Operator(x_then_z).data
u_z_then_x = Operator(z_then_x).data
tensor_xz = Pauli("XZ").to_matrix()
print("Different qubits, equal matrices:", np.allclose(u_x_then_z, u_z_then_x))
print("Matches X tensor Z:", np.allclose(u_x_then_z, tensor_xz))

x = Pauli("X").to_matrix()
z = Pauli("Z").to_matrix()
print("Same qubit, XZ = ZX:", np.allclose(x @ z, z @ x))
print("Same qubit, XZ = -ZX:", np.allclose(x @ z, -(z @ x)))
```

出力:

```text
Different qubits, equal matrices: True
Matches X tensor Z: True
Same qubit, XZ = ZX: False
Same qubit, XZ = -ZX: True
```

最初の2行は、異なる量子ビットへの操作が、どちらの順序でも$X\otimes Z$になることに対応します。後半の2行は、同じ量子ビットへの行列積では負符号が必要であることを確かめています。Pythonの`@`は行列積で、`np.allclose`は配列の成分を数値誤差の許容範囲内で比較します。global phaseを取り除く比較ではないので、$XZ$と$ZX$には`False`を返します。数学的な等式は上の導出で示し、コードではその具体例を照合しています。

ゲートの順番を検討するときは、まず作用する量子ビットを確認し、回路全体の演算子を書きます。別々の量子ビットへの1量子ビットゲートなら交換します。同じ量子ビットの場合は、ゲートの組合せごとに行列積を比較します。

### SparsePauliOpの係数と和を読む

複数のPauli文字列を、係数付きの和として表すのが`SparsePauliOp`です。例えば

$$
O=\frac12(Z\otimes I)-(X\otimes X)
$$

なら、`("ZI", 0.5)`と`("XX", -1.0)`をリストに入れます。`from_list`の各組は`(label, 係数)`です。この和は、2つのゲートを順に実行するという意味ではありません。状態へ作用させる場合は、それぞれの演算結果を係数付きで足します。測定量として使う意味は[次節](#expectation)で学びます。

$Z\otimes I$の対角要素は、左側が0なら$+1$、1なら$-1$なので、$(1,1,-1,-1)$です。$X\otimes X$は00と11、01と10を交換します。したがって、行列は

$$
O=\begin{pmatrix}
1/2&0&0&-1\\
0&1/2&-1&0\\
0&-1&-1/2&0\\
-1&0&0&-1/2
\end{pmatrix}
$$

になります。コードでは次のように確認できます。

```python
from qiskit.quantum_info import Pauli, SparsePauliOp, Statevector

initial = Statevector.from_label("01")
print("XZ on |01>:", initial.evolve(Pauli("XZ")).data.real)
op = SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])
print("0.5 ZI - XX:")
print(op.to_matrix().real)
```

出力:

```text
XZ on |01>: [ 0.  0.  0. -1.]
0.5 ZI - XX:
[[ 0.5  0.   0.  -1. ]
 [ 0.   0.5 -1.   0. ]
 [ 0.  -1.  -0.5  0. ]
 [-1.   0.   0.  -0.5]]
```

最初の行は、添字3、つまり$|11\rangle$の振幅が$-1$になったことを示します。この例では振幅も行列も実数なので`.real`で表示しています。$Y$を含む演算などでは虚部が必要になるため、一般の状態や行列で虚部を捨ててよいわけではありません。

### 確認問題

1. 3量子ビットのPauli label`"ZIX"`は、各量子ビットへ何を適用しますか。
2. $|q_1q_0\rangle=|10\rangle$に対応する状態ベクトルの添字はいくつですか。
3. $|10\rangle$を準備し、$q_0\to c_1$、$q_1\to c_0$へ測定すると、2ビットレジスタ`c`の文字列は何ですか。
4. `"XZ"`を$|10\rangle$へ適用すると、何になりますか。
5. $q_1$への$H$と$q_0$への$Y$は、順番を入れ替えられますか。両方を$q_0$へ適用する場合と比較してください。

**解答と理由**

1. $q_2$へ$Z$、$q_1$へ$I$、$q_0$へ$X$です。右端から番号0、1、2を対応させます。
2. $2$です。$2\times q_1+q_0=2\times1+0=2$となります。
3. `01`です。$c_1$には$q_0$の0、$c_0$には$q_1$の1が入ります。
4. $|00\rangle$です。左側は$X|1\rangle=|0\rangle$、右側は$Z|0\rangle=|0\rangle$で、この入力には負符号が付きません。
5. 別々の量子ビットなら交換します。$(H\otimes I)(I\otimes Y)$も$(I\otimes Y)(H\otimes I)$も$H\otimes Y$です。両方を$q_0$へ適用する場合は、$HY=-YH$より$I\otimes H$と$I\otimes Y$は反交換します。後者の二つの順序はglobal phaseを除いて同値ですが、行列としては等しくありません。

文字列を読む際は右端から量子ビット番号を対応させます。測定結果なら古典ビットへの保存先を確認し、演算子ならテンソル積・行列積・係数付きの和を区別します。

参照: [Bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)、[Operator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator)、[SparsePauliOp](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp)

<a id="expectation"></a>
## observableと期待値

量子回路が用意した状態について、「ある量を測ると、平均としてどの値が得られるか」を調べるのが期待値の計算です。この節では、測定結果の平均から出発し、固有値・固有状態の意味と行列による計算を結び付けます。最後に、複数量子ビットの期待値を求めます。

### 何の値を平均するのか

**観測量**（**observable**）は、状態について測定で調べる量です。例えばPauliのZを観測量にすると、計算基底での測定結果を次の数値に対応させます。

| 記録されるbit | Zの測定値 | その結果が出る確率 |
|---|---|---|
| `0` | $+1$ | $p_0$ |
| `1` | $-1$ | $p_1$ |

$p_0$と$p_1$はそれぞれ0と1を得る確率で、$p_0+p_1=1$です。Zの**期待値**は、Zの測定値をこれらの確率で重み付けして足したものです。山括弧を使って$\langle Z\rangle$と書きます。

$$
\langle Z\rangle=(+1)p_0+(-1)p_1=p_0-p_1.
$$

例えば0の確率が$3/4$、1の確率が$1/4$なら、次のようになります。

$$
\langle Z\rangle=(+1)\frac{3}{4}+(-1)\frac{1}{4}
=\frac{1}{2}.
$$

同じ状態を毎回用意してZを測定し、得られた$+1$と$-1$を多数回平均すると、この値へ近づきます。1回の測定で$1/2$が出るわけではありません。ここで平均するのは、記録されたbitの0と1ではなく、表で対応付けたZの測定値です。

### 固有値と固有状態は、確定する測定値を表す

Zの測定値として$+1$と$-1$を使う理由を、行列から確かめます。

$$
\begin{aligned}
Z|0\rangle
&=\begin{pmatrix}1&0\\0&-1\end{pmatrix}
\begin{pmatrix}1\\0\end{pmatrix}
=\begin{pmatrix}1\\0\end{pmatrix}
=(+1)|0\rangle,\\
Z|1\rangle
&=\begin{pmatrix}1&0\\0&-1\end{pmatrix}
\begin{pmatrix}0\\1\end{pmatrix}
=\begin{pmatrix}0\\-1\end{pmatrix}
=(-1)|1\rangle.
\end{aligned}
$$

どちらも、行列を作用させた結果が元の状態の定数倍になっています。一般に、正規化された状態$|a\rangle$と行列$A$について

$$
A|a\rangle=\lambda|a\rangle
$$

が成り立つとき、$|a\rangle$を$A$の**固有状態**（**eigenstate**）、掛かっている数$\lambda$を**固有値**（**eigenvalue**）と呼びます。観測量$A$をその固有状態で測定すると、測定値は対応する固有値に確定します。したがって、Zの固有状態$|0\rangle$では$+1$、$|1\rangle$では$-1$が確定し、それぞれの期待値も$+1$、$-1$です。

観測量を表す行列には、**エルミート行列**（**Hermitian matrix**）を使います。行と列を入れ替え、各成分の複素共役を取った行列を$A^\dagger$と書き、$A^\dagger=A$となるのがその条件です。この性質により、固有値が実数になります。ZやXはその例です。

上の式は、観測量の固有状態と測定値の対応を調べる計算です。Zをゲートとして回路に追加する操作と、Zを観測量として測定する操作は別です。また、$-|1\rangle$と$|1\rangle$が同じ物理状態を表しても、固有値$-1$という測定値の符号は省略できません。

### 状態から期待値を直接計算する

一般の観測量でも、可能な測定値を$\lambda_k$、それを得る確率を$p_k$とすると、期待値は同じ重み付き平均です。$k$は可能な測定値を区別する番号です。

$$
\langle A\rangle=\sum_k\lambda_k p_k.
$$

正規化された状態ベクトル$|\psi\rangle$が分かっていれば、この平均を行列から直接求められます。

$$
\langle A\rangle=\langle\psi|A|\psi\rangle.
$$

$\langle\psi|$はbra（ブラ）と呼ぶ行ベクトルです。ketの列を横に並べ直し、各成分の複素共役を取って作ります。複素共役は$i$の符号を反転する操作で、$\alpha^*$のように星印でも表します。

$$
|\psi\rangle=\begin{pmatrix}\alpha\\\beta\end{pmatrix},\qquad
\langle\psi|=\begin{pmatrix}\alpha^*&\beta^*\end{pmatrix},\qquad
\langle\psi|\psi\rangle=|\alpha|^2+|\beta|^2=1.
$$

まず右側の$A|\psi\rangle$を計算し、その結果に左から$\langle\psi|$を掛けます。Zの場合を実際に計算すると、先ほどの確率による式が現れます。

$$
\begin{aligned}
\langle Z\rangle
&=\begin{pmatrix}\alpha^*&\beta^*\end{pmatrix}
\begin{pmatrix}1&0\\0&-1\end{pmatrix}
\begin{pmatrix}\alpha\\\beta\end{pmatrix}\\
&=\begin{pmatrix}\alpha^*&\beta^*\end{pmatrix}
\begin{pmatrix}\alpha\\-\beta\end{pmatrix}\\
&=|\alpha|^2-|\beta|^2=p_0-p_1.
\end{aligned}
$$

例えば$|\psi\rangle=(\sqrt{3}/2)|0\rangle+(1/2)|1\rangle$なら、振幅の絶対値二乗は$3/4$と$1/4$です。行列の式でも$\langle Z\rangle=1/2$を得ます。振幅そのものを平均するのではなく、確率で測定値を重み付けしていることを確認してください。

### 同じ状態でも、観測量によって期待値が変わる

状態$|+\rangle=(|0\rangle+|1\rangle)/\sqrt{2}$では、Z測定の確率が各$1/2$なので

$$
\langle Z\rangle=(+1)\frac{1}{2}+(-1)\frac{1}{2}=0.
$$

この0は、$+1$と$-1$が平均で打ち消し合うことを表します。Zの測定で0という値が出る、という意味ではありません。

次に、同じ状態に対するXの期待値を考えます。Xは$|0\rangle$と$|1\rangle$を交換するので、次の固有値の関係が成り立ちます。

$$
X|+\rangle
=\frac{|1\rangle+|0\rangle}{\sqrt{2}}
=|+\rangle.
$$

つまり$|+\rangle$はXの固有値$+1$の固有状態です。Xを測れば$+1$が確定するため、$\langle X\rangle=1$です。行列による期待値の式でも確認できます。

$$
\langle+|X|+\rangle=\langle+|+\rangle=1.
$$

状態が同じでも、ZとXでは調べる量が違うので、期待値も異なります。Xの測定を回路で実装する方法は[測定と基底](02-visualization-measurement.md#measurement-basis)で扱います。

### Qiskitで1量子ビットの計算を確かめる

次の例はQiskit 2.5.2とNumPyでローカル実行できます。`Statevector`に状態、`Pauli`に観測量を指定し、`expectation_value`で期待値を計算します。

```python
import numpy as np
from qiskit.quantum_info import Pauli, Statevector

psi = Statevector([np.sqrt(3) / 2, 1 / 2])
plus = Statevector.from_label("+")

z_value = psi.expectation_value(Pauli("Z"))
plus_z = plus.expectation_value(Pauli("Z"))
plus_x = plus.expectation_value(Pauli("X"))

print(f"psi, Z: {z_value.real:.6f}")
print(f"+, Z: {plus_z.real:.6f}")
print(f"+, X: {plus_x.real:.6f}")
```

出力:

```text
psi, Z: 0.500000
+, Z: 0.000000
+, X: 1.000000
```

最初の行が確率$3/4$と$1/4$の例、後の二行が同じ$|+\rangle$に対するZとXの比較です。`from_label("+")`は$|+\rangle$を作る指定です。期待値はこの観測量では理論上実数なので、出力には`.real`で実部を取り出し、小数点以下6桁で表示しています。

このコードは状態ベクトルから理論上の期待値を数値計算しており、測定を繰り返して標本平均を取っているわけではありません。

### 複数量子ビットでは、積の測定値を考える

2量子ビットの観測量$X\otimes X$は、それぞれの量子ビットでXを測り、二つの測定値の積を読む量です。各測定値が$+1$または$-1$なので、積も$+1$または$-1$です。その積を確率で重み付けして平均すると、$\langle X\otimes X\rangle$になります。

両方の量子ビットが$|+\rangle$なら、全体は積状態$|++\rangle$です。記号$\otimes$は、二つの量子ビットの状態や演算子を組み合わせるテンソル積を表します。

$$
|++\rangle=|+\rangle\otimes|+\rangle
=\frac{|00\rangle+|01\rangle+|10\rangle+|11\rangle}{2}.
$$

積の演算子を積状態に作用させると、それぞれの因子に分けて計算できます。

$$
\begin{aligned}
(X\otimes X)(|+\rangle\otimes|+\rangle)
&=(X|+\rangle)\otimes(X|+\rangle)\\
&=(+1)|+\rangle\otimes(+1)|+\rangle\\
&=(+1)(+1)|++\rangle=|++\rangle.
\end{aligned}
$$

これで$|++\rangle$が$X\otimes X$の固有値$+1$の固有状態だと分かり、$\langle X\otimes X\rangle=1$を得ます。測定値で考えても、各量子ビットのXの測定値が$+1$に確定するので、その積も$+1$です。

同じ$|++\rangle$でも、Zをそれぞれ測ると、独立に$+1$と$-1$を各$1/2$の確率で得ます。

| 二つのZの測定値 | 積 | 確率 |
|---|---|---|
| $(+1,+1)$ | $+1$ | $1/4$ |
| $(+1,-1)$ | $-1$ | $1/4$ |
| $(-1,+1)$ | $-1$ | $1/4$ |
| $(-1,-1)$ | $+1$ | $1/4$ |

したがって、$\langle Z\otimes Z\rangle=(1-1-1+1)/4=0$です。**二つの測定値の積を平均する**という意味を保って考えます。積状態では各量子ビットの期待値の積にも分けられますが、もつれた状態で同じ分解ができるとは限りません。

### 観測量が和で書かれている場合

`SparsePauliOp`では、Pauli演算子の和を観測量として表せます。例えば、前の節にあった観測量を$A$とすると

$$
A=\frac{1}{2}(Z\otimes I)-(X\otimes X)
$$

です。$I$は状態をそのままにする恒等演算子で、その測定値は$+1$です。期待値の式は演算子の和にも分配できるので、各項の期待値を係数付きで足します。

$$
\begin{aligned}
\langle A\rangle
&=\langle\psi|\left[\frac{1}{2}(Z\otimes I)-(X\otimes X)\right]|\psi\rangle\\
&=\frac{1}{2}\langle Z\otimes I\rangle-\langle X\otimes X\rangle.
\end{aligned}
$$

状態が$|++\rangle$なら、$Z\otimes I$の期待値はZの期待値0とIの測定値$+1$の積で0です。先ほど求めた$\langle X\otimes X\rangle=1$と合わせると、$\langle A\rangle=(1/2)\times0-1=-1$となります。

この線形性による期待値の計算は、各項が同じ測定方法で同時に測れることを意味するものではありません。

### Qiskitで複数量子ビットと和の計算を確かめる

この例も、必要なimportと状態の定義を含むので単独で実行できます。

```python
from qiskit.quantum_info import Pauli, SparsePauliOp, Statevector

pair = Statevector.from_label("++")
xx_value = pair.expectation_value(Pauli("XX"))
zz_value = pair.expectation_value(Pauli("ZZ"))
observable = SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])
sum_value = pair.expectation_value(observable)

print(f"++, XX: {xx_value.real:.6f}")
print(f"++, ZZ: {zz_value.real:.6f}")
print(f"++, A: {sum_value.real:.6f}")
```

出力:

```text
++, XX: 1.000000
++, ZZ: 0.000000
++, A: -1.000000
```

文字列`"XX"`は$X\otimes X$を、`"ZI"`は$Z\otimes I$を表します。Qiskitでは右端がq0なので、`"ZI"`のZはq1に対応します。`from_list`の各組は「Pauli文字列とその係数」で、`expectation_value(observable)`が係数を含めた全体の期待値を返します。

### 有限回の測定から推定するとき

実際の測定回数を使う場合、期待値は標本から推定します。Z測定で0を得た回数を$n_0$、1を得た回数を$n_1$、合計を$N=n_0+n_1$とすると、推定値は次のとおりです。帽子付きの記号$\widehat{\langle Z\rangle}$で、理論値と区別します。

$$
\widehat{\langle Z\rangle}
=\frac{(+1)n_0+(-1)n_1}{N}
=\frac{n_0-n_1}{N}.
$$

例えば1000回中0が740回、1が260回なら、推定値は0.48です。理論値が0.5でも、有限回の測定では一致しない場合があります。これは先ほどの`Statevector.expectation_value`による計算とは取得方法が異なります。測定回数から確率を求める方法は[経験確率と不確かさ](07-results-analysis.md#empirical-analysis)で扱います。

### 確認問題

1. 状態$|1\rangle$のZの期待値はいくつですか。bitとしての記録値と区別して答えてください。
2. 状態$(\sqrt{3}/2)|0\rangle+(i/2)|1\rangle$のZの期待値はいくつですか。虚数を含む振幅をどのように扱いますか。
3. 状態$|--\rangle=|-\rangle\otimes|-\rangle$の$X\otimes X$の期待値はいくつですか。
4. Z測定の記録が0を300回、1を700回だった場合、期待値の推定値はいくつですか。

**解答と理由**

1. $-1$です。$Z|1\rangle=-|1\rangle$なのでZの測定値は$-1$に確定します。記録するbitは1ですが、Zの平均に使う値は$-1$です。
2. $3/4-1/4=1/2$です。確率は振幅の絶対値二乗なので、$|i/2|^2=(-i/2)(i/2)=1/4$です。$(i/2)^2=-1/4$を確率に使うことはできません。
3. $+1$です。$X|-\rangle=(|1\rangle-|0\rangle)/\sqrt{2}=-|-\rangle$より、各因子の固有値は$-1$です。二つの測定値の積は$(-1)(-1)=+1$に確定します。
4. $(300-700)/1000=-0.4$です。観測された回数による推定値で、理論上の期待値が厳密に$-0.4$であるとまではいえません。

**判断の要点**: 状態と観測量を指定し、何を測定値として平均するかを確認します。固有状態なら固有値、一般の状態なら確率による重み付き平均か$\langle\psi|A|\psi\rangle$で求めます。複数量子ビットでは積の測定値、観測量が和なら各項の係数も含めて計算します。

API参照: [Statevector.expectation_value](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector#expectation_value)、[Statevector.from_label](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector#from_label)、[SparsePauliOp](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp)

## 章末チェック

次の問題では、答えとともに、振幅・位相・量子ビットの順番のどれに注目したかを説明してください。

1. 状態$(|0\rangle+2i|1\rangle)/\sqrt5$の計算基底の確率と、Zの期待値を求めてください。
2. $Z|+\rangle$を厳密なketで書いてください。その後に$H$を適用すると、測定結果はどうなりますか。
3. $|0\rangle$へ、先に$S$、次に$H$を適用しました。全体の行列積と出力状態を答えてください。
4. $R_y(\pi/2)|0\rangle$を求めてください。また、$R_y(2\pi)$は行列として$I$に等しいですか。
5. $R_z(\pi)$と$Z$の違いは、どのglobal phaseで表せますか。その違いを制御ゲートに組み込む場合にも無条件に捨ててよいですか。
6. Pauli label `"IY"`の$Y$はどの量子ビットに作用しますか。入力$|00\rangle$への作用も答えてください。
7. 制御側$q_0=1$、標的側$q_1=0$へ`cx(0, 1)`を作用させた後、ketと状態ベクトルの添字は何になりますか。
8. $|\Phi^+\rangle$と$|++\rangle$について、計算基底で01が出る確率をそれぞれ求めてください。
9. 状態$|+\rangle\otimes|-\rangle$の$X\otimes X$の期待値を求めてください。Z基底の確率だけを使って同じ値を求めてよいですか。

**解答と理由**

1. 確率は$(1/5,4/5)$です。Zの測定値は0に対して$+1$、1に対して$-1$なので、期待値は$1/5-4/5=-3/5$です。振幅の$2i$をそのまま測定値にしません。
2. $Z|+\rangle=(|0\rangle-|1\rangle)/\sqrt2=|-\rangle$です。その後は$H|-\rangle=|1\rangle$なので、計算基底で1が確率1です。位相の変化が干渉を通じて確率の違いになります。
3. 行列積は$HS$です。$S|0\rangle=|0\rangle$なので、出力は$H|0\rangle=|+\rangle$です。回路の時間順と行列を左から読む順は逆です。
4. 半角は$\pi/4$なので、$R_y(\pi/2)|0\rangle=(|0\rangle+|1\rangle)/\sqrt2=|+\rangle$です。一方、$R_y(2\pi)=\cos\pi\,I-i\sin\pi\,Y=-I$であり、厳密な行列は$I$ではありません。
5. $R_z(\pi)=-iZ$です。制御側が1の成分だけにこの位相が付くと、全体では相対位相になるため、無条件には捨てられません。
6. 右端の$q_0$です。$(I\otimes Y)|00\rangle=|0\rangle\otimes i|1\rangle=i|01\rangle$となります。
7. $|01\rangle$から$|11\rangle$へ移り、添字は3です。右側の制御ビットが1なので、左側の標的ビットが反転します。
8. $|\Phi^+\rangle$では01の振幅が0なので確率0です。$|++\rangle$では振幅が$1/2$なので確率$1/4$です。各量子ビット単独の0・1が半々でも、同時に測った分布は異なります。
9. $X|+\rangle=|+\rangle$、$X|-\rangle=-|-\rangle$なので、積の測定値は$-1$です。Z基底の0・1をそのまま使うと別の観測量を計算することになります。X基底へ測定を変換するか、$\langle\psi|X\otimes X|\psi\rangle$を計算します。

公式参照: [Qiskit bit-ordering guide](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)、[SparsePauliOp API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp)

[← 学び方](00-guide.md) | [次: 測定と可視化 →](02-visualization-measurement.md)
