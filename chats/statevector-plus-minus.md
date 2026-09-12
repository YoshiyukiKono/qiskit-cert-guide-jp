できます。ポイントは、Qiskit の `Statevector` は最終的には **計算基底 $|0\rangle,|1\rangle$ における係数ベクトル**を受け取るので、$|+\rangle,|-\rangle$ をベクトルに直して渡す、ということです。

1量子ビットなら、

$$
|+\rangle=\frac{1}{\sqrt2}(|0\rangle+|1\rangle)
=
\frac{1}{\sqrt2}
\begin{pmatrix}
1\\
1
\end{pmatrix}
$$

なので、

```python
from qiskit.quantum_info import Statevector
import numpy as np

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
```

同様に、

$$
|-\rangle=\frac{1}{\sqrt2}(|0\rangle-|1\rangle)
=
\frac{1}{\sqrt2}
\begin{pmatrix}
1\\
-1
\end{pmatrix}
$$

なので、

```python
minus = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])
```

と書けます。

さらに簡単には、Qiskit はラベル指定もできます。

```python
plus = Statevector.from_label('+')
minus = Statevector.from_label('-')
```

これはかなり便利です。

2量子ビットなら、たとえば

$$
|++\rangle=|+\rangle\otimes|+\rangle
$$

なので、

```python
pp = Statevector.from_label('++')
```

とできます。

これは計算基底に展開すると、

$$
|++\rangle
=
\frac12
\left(
|00\rangle
+|01\rangle
+|10\rangle
+|11\rangle
\right)
$$

したがって Statevector としては、

```python
[0.5, 0.5, 0.5, 0.5]
```

になります。

同様に、

```python
pm = Statevector.from_label('+-')
mp = Statevector.from_label('-+')
mm = Statevector.from_label('--')
```

も可能です。

ここで大事なのは、

> `Statevector.from_label('+')` は「$+$ 基底専用の別形式」で保存しているわけではない

という点です。

内部的には結局、

$$
|+\rangle
=
\frac{1}{\sqrt2}|0\rangle
+
\frac{1}{\sqrt2}|1\rangle
$$

として、計算基底で

```text
[1/√2, 1/√2]
```

と保持されています。

なので、前の話につなげると、

```python
Statevector.from_label('++')
```

は

```python
Statevector([1/2, 1/2, 1/2, 1/2])
```

と同じ状態です。

この「$|+\rangle$ を $|0\rangle,|1\rangle$ の係数へ展開する」という感覚を持つと、X基底での状態もかなり読みやすくなります。

# X規定表示

Qiskit の `Statevector` は、基本的には **Z基底（計算基底）で表示**します。なので、X基底 $|+\rangle,|-\rangle$ で見たい場合は、**Hadamard $H$ で基底変換してから表示**するのが分かりやすいです。

1量子ビットなら、たとえば

```python
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import HGate

sv = Statevector.from_label('+')
print(sv)
```

これは Z 基底表示なので、

```text
Statevector([0.70710678+0.j, 0.70710678+0.j],
            dims=(2,))
```

のようになります。

X基底での係数を見たいなら、

```python
sv_x = sv.evolve(HGate())
print(sv_x)
```

すると、

```text
Statevector([1.+0.j, 0.+0.j],
            dims=(2,))
```

になります。

これは X 基底では

$$
|+\rangle
=
1|+\rangle + 0|-\rangle
$$

という意味です。

逆に、

```python
sv = Statevector.from_label('-')
sv_x = sv.evolve(HGate())
print(sv_x)
```

なら、

```text
[0, 1]
```

となって、

$$
|-\rangle
=
0|+\rangle+1|-\rangle
$$

と読めます。

つまり対応はこうです。

| 物理状態 | Z基底でのベクトル | X基底でのベクトル              |         |
| ---- | --------- | ---------------------- | ------- |
| $    | +\rangle$ | $\frac1{\sqrt2}[1,1]$  | $[1,0]$ |
| $    | -\rangle$ | $\frac1{\sqrt2}[1,-1]$ | $[0,1]$ |

大事なのは、

> 同じ状態でも、どの基底で座標を書くかによってベクトル表示が変わる

ということです。

2量子ビットなら、各量子ビットに $H$ をかけます。

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

sv = Statevector.from_label('+-')

qc = QuantumCircuit(2)
qc.h([0, 1])

sv_x = sv.evolve(qc)
print(sv_x)
```

すると X 基底の順序

$$
|++\rangle,\ |+-\rangle,\ |-+\rangle,\ |--\rangle
$$

に対応する係数として読むことができます。

なので、かなり直感的には

```text
Z基底で表示したい → そのまま Statevector
X基底で表示したい → H をかけてから Statevector
```

と覚えておくとよいです。

`Statevector.draw("latex")` 自体には、**表示基底を X 基底に切り替えて $|+\rangle,|-\rangle$ と書かせるオプションは基本的にありません**。`draw("latex")` の ket 表示は計算基底、つまり $|0\rangle,|1\rangle$ で展開されます。IBM の現行ドキュメントでもその形になっています。([IBM Quantum][1])

たとえば、

```python
plus = Statevector.from_label("+")
display(plus.draw("latex"))
```

としても、表示は

$$
\frac{1}{\sqrt2}|0\rangle+\frac{1}{\sqrt2}|1\rangle
$$

になります。`from_label("+")` は $|+\rangle$ を生成できますが、`draw("latex")` はそれを Z 基底で展開して表示します。IBM の教材でも、`from_label("+")` で作った状態を `draw("latex")` すると計算基底へ展開される例があります。([IBM Quantum][2])

なので、

```python
Statevector.from_label("+")
```

に対して、そのまま

$$
|+\rangle
$$

と表示したいだけなら、Qiskit の drawer に任せるのではなく、Jupyter 側で LaTeX を表示するのが素直です。

```python
from IPython.display import display, Math

plus = Statevector.from_label("+")
display(Math(r"|+\rangle"))
```

2量子ビットなら、

```python
sv = Statevector.from_label("+-")
display(Math(r"|+-\rangle"))
```

で

$$
|+-\rangle
$$

とできます。

ただ、ここには面白い区別があります。

```python
Statevector.from_label("+-")
```

は実際に **$|+-\rangle$ という状態を作る命令**ですが、

```python
sv.draw("latex")
```

は

> 「この Statevector を計算基底で展開すると何か」

を表示するものです。

つまり、

$$
|+-\rangle
$$

を Qiskit が展開すると、

$$
|+-\rangle
=
\frac12
\left(
|00\rangle-|01\rangle+|10\rangle-|11\rangle
\right)
$$

というような表示になります。

前の質問とのつながりでいうと、**「X基底での座標として $|+\rangle,|-\rangle$ を使って自動表示したい」**なら、`draw("latex")` の機能ではなく、自分で基底変換後の係数を求めて

$$
a|+\rangle+b|-\rangle
$$

の形に整形する小さな関数を作るのがよいです。

必要なら次に、たとえば

```python
draw_xbasis(sv)
```

とすると

$$
\frac{1}{\sqrt2}|+\rangle+
\frac{1}{\sqrt2}|-\rangle
$$

のように表示してくれる関数を、1量子ビット・複数量子ビット両対応で作れます。

[1]: https://quantum.cloud.ibm.com/docs/en/guides/plot-quantum-states?utm_source=chatgpt.com "Plot quantum states | IBM Quantum Documentation"
[2]: https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/multiple-systems/qiskit-implementation?utm_source=chatgpt.com "Qiskit implementation | IBM Quantum Learning"

できます。Jupyter Notebook で使いやすいように、`Statevector` を **X基底の ket 記法で LaTeX 表示する関数**にしておくのが便利です。

```python
import numpy as np
from IPython.display import display, Math
from qiskit.quantum_info import Statevector

def draw_xbasis(sv, atol=1e-10):
    """
    Statevector を X 基底 {|+>, |->} で展開して LaTeX 表示する。
    複数量子ビットにも対応。
    """

    if not isinstance(sv, Statevector):
        sv = Statevector(sv)

    n = sv.num_qubits

    # H^{⊗n} をかけると、X基底での係数が
    # 計算基底上の係数として得られる
    x_amplitudes = sv.data.copy()

    # 1-qubit Hadamard
    H = np.array([
        [1,  1],
        [1, -1]
    ]) / np.sqrt(2)

    # H^{⊗n}
    Hn = H
    for _ in range(n - 1):
        Hn = np.kron(Hn, H)

    x_amplitudes = Hn @ x_amplitudes

    terms = []

    for i, amp in enumerate(x_amplitudes):
        if abs(amp) < atol:
            continue

        bits = format(i, f"0{n}b")
        label = "".join("+" if b == "0" else "-" for b in bits)

        # 係数を表示用文字列に
        if np.isclose(amp.imag, 0, atol=atol):
            a = amp.real

            if np.isclose(a, 1, atol=atol):
                coeff = ""
            elif np.isclose(a, -1, atol=atol):
                coeff = "-"
            else:
                coeff = f"{a:.4g}"
        else:
            coeff = f"({amp:.4g})"

        terms.append(f"{coeff}|{label}\\rangle")

    latex = " + ".join(terms)
    latex = latex.replace("+ -", "- ")

    display(Math(latex))
```

たとえば、

```python
sv = Statevector.from_label("+")
draw_xbasis(sv)
```

なら、

$$
|+\rangle
$$

と表示されます。

`|-\rangle` も同様です。

```python
sv = Statevector.from_label("-")
draw_xbasis(sv)
```

$$
|-\rangle
$$

---

たとえば Z 基底の

```python
sv = Statevector.from_label("0")
draw_xbasis(sv)
```

なら、

$$
\frac{1}{\sqrt2}|+\rangle
+
\frac{1}{\sqrt2}|-\rangle
$$

に相当します。

ただし上の簡易版では数値表示なので、

$$
0.7071|+\rangle+0.7071|-\rangle
$$

のようになります。

学習用途なら、むしろ **`0.7071` を `\frac{1}{\sqrt2}` に自動変換する版**にした方がかなり見やすいです。

たとえば理想的には、

```python
draw_xbasis(Statevector.from_label("0"))
```

を

$$
\frac{1}{\sqrt2}|+\rangle
+
\frac{1}{\sqrt2}|-\rangle
$$

と表示し、

```python
draw_xbasis(Statevector.from_label("00"))
```

なら

$$
\frac12
\left(
|++\rangle
+
|+-\rangle
+
|-+\rangle
+
|--\rangle
\right)
$$

と出す形です。

この **「よく出る係数を $\frac1{\sqrt2},\frac12$ などに整形する版」**の方をおすすめします。

はい。学習用途なら、係数をなるべく

* $1$
* $-1$
* $\frac{1}{\sqrt2}$
* $-\frac{1}{\sqrt2}$
* $\frac12$
* $-\frac12$
* $\frac{i}{\sqrt2}$

のような見慣れた形に戻して表示する版が使いやすいです。

```python
import numpy as np
from IPython.display import display, Math
from qiskit.quantum_info import Statevector


def _latex_amplitude(z, atol=1e-10):
    """
    複素振幅を、量子情報でよく出る形の LaTeX に変換する。
    """

    # ほぼ 0
    if abs(z) < atol:
        return "0"

    r = z.real
    i = z.imag

    common = [
        (1.0, "1"),
        (-1.0, "-1"),

        (1 / np.sqrt(2), r"\frac{1}{\sqrt{2}}"),
        (-1 / np.sqrt(2), r"-\frac{1}{\sqrt{2}}"),

        (0.5, r"\frac{1}{2}"),
        (-0.5, r"-\frac{1}{2}"),

        (1 / np.sqrt(8), r"\frac{1}{2\sqrt{2}}"),
        (-1 / np.sqrt(8), r"-\frac{1}{2\sqrt{2}}"),
    ]

    # 実数だけの場合
    if abs(i) < atol:
        for value, latex in common:
            if np.isclose(r, value, atol=atol):
                return latex

        return f"{r:.4g}"

    # 純虚数の場合
    if abs(r) < atol:
        for value, latex in common:
            if np.isclose(i, value, atol=atol):

                if latex == "1":
                    return "i"
                elif latex == "-1":
                    return "-i"

                if latex.startswith("-"):
                    return "-" + latex[1:] + "i"
                else:
                    return latex + "i"

        return f"{i:.4g}i"

    # 一般の複素数
    sign = "+" if i >= 0 else "-"
    imag = abs(i)

    return f"\\left({r:.4g}{sign}{imag:.4g}i\\right)"


def draw_xbasis(sv, atol=1e-10):
    """
    Statevector を X 基底
        {|+>, |->}
    で展開し、Jupyter 上で LaTeX 表示する。

    複数量子ビット対応。
    """

    if not isinstance(sv, Statevector):
        sv = Statevector(sv)

    n = sv.num_qubits

    # Hadamard
    H = np.array([
        [1,  1],
        [1, -1]
    ], dtype=complex) / np.sqrt(2)

    # H^{⊗n}
    Hn = np.array([[1]], dtype=complex)

    for _ in range(n):
        Hn = np.kron(Hn, H)

    # X基底での係数
    amplitudes = Hn @ sv.data

    terms = []

    for i, amp in enumerate(amplitudes):

        if abs(amp) < atol:
            continue

        bits = format(i, f"0{n}b")

        # X基底では
        # 0 -> +
        # 1 -> -
        label = "".join(
            "+" if bit == "0" else "-"
            for bit in bits
        )

        coeff = _latex_amplitude(amp, atol)

        if coeff == "1":
            term = f"|{label}\\rangle"

        elif coeff == "-1":
            term = f"-|{label}\\rangle"

        else:
            term = f"{coeff}|{label}\\rangle"

        terms.append(term)

    if not terms:
        latex = "0"

    else:
        latex = terms[0]

        for term in terms[1:]:

            if term.startswith("-"):
                latex += " - " + term[1:]
            else:
                latex += " + " + term

    display(Math(latex))
```

たとえば、

```python
draw_xbasis(Statevector.from_label("+"))
```

なら、

$$
|+\rangle
$$

です。

```python
draw_xbasis(Statevector.from_label("-"))
```

なら、

$$
|-\rangle
$$

です。

そして、

```python
draw_xbasis(Statevector.from_label("0"))
```

なら、

$$
\frac{1}{\sqrt2}|+\rangle
+
\frac{1}{\sqrt2}|-\rangle
$$

となります。

2量子ビットなら、

```python
draw_xbasis(Statevector.from_label("00"))
```

で、

$$
\frac12|++\rangle
+
\frac12|+-\rangle
+
\frac12|-+\rangle
+
\frac12|--\rangle
$$

と表示されます。

さらに、たとえば

```python
draw_xbasis(Statevector.from_label("++"))
```

なら単純に

$$
|++\rangle
$$

です。

---

この関数の中で一番重要なのは、実はここです。

```python
amplitudes = Hn @ sv.data
```

これは単なる「表示上の細工」ではありません。

元の Statevector が Z 基底で

$$
|\psi\rangle
=
a|0\rangle+b|1\rangle
$$

と記述されているところに Hadamard を使って、

$$
H|\psi\rangle
$$

を計算することで、

$$
|+\rangle,\ |-\rangle
$$

を基底としたときの**座標**を求めています。

つまり、

```python
sv.draw("latex")
```

が

> Z基底で見た座標

なら、

```python
draw_xbasis(sv)
```

は

> X基底で見た同じ状態の座標

です。

これは今ちょうど整理されている「Statevector の配列は何を意味するのか」を理解する上でも、かなり良い実験道具になると思います。

# 派生クラス

可能です。`Statevector` を継承して、たとえば `draw_xbasis()` を持つ派生クラスにするのは自然です。

```python
import numpy as np
from IPython.display import display, Math
from qiskit.quantum_info import Statevector


class XStatevector(Statevector):

    def draw_xbasis(self, atol=1e-10):
        n = self.num_qubits

        H = np.array([
            [1,  1],
            [1, -1]
        ], dtype=complex) / np.sqrt(2)

        Hn = np.array([[1]], dtype=complex)

        for _ in range(n):
            Hn = np.kron(Hn, H)

        amplitudes = Hn @ self.data

        terms = []

        for i, amp in enumerate(amplitudes):
            if abs(amp) < atol:
                continue

            bits = format(i, f"0{n}b")
            label = "".join(
                "+" if bit == "0" else "-"
                for bit in bits
            )

            coeff = self._latex_amplitude(amp, atol)

            if coeff == "1":
                term = f"|{label}\\rangle"
            elif coeff == "-1":
                term = f"-|{label}\\rangle"
            else:
                term = f"{coeff}|{label}\\rangle"

            terms.append(term)

        if not terms:
            latex = "0"
        else:
            latex = terms[0]

            for term in terms[1:]:
                if term.startswith("-"):
                    latex += " - " + term[1:]
                else:
                    latex += " + " + term

        display(Math(latex))

    @staticmethod
    def _latex_amplitude(z, atol=1e-10):

        if abs(z) < atol:
            return "0"

        common = [
            (1.0, "1"),
            (-1.0, "-1"),
            (1 / np.sqrt(2), r"\frac{1}{\sqrt{2}}"),
            (-1 / np.sqrt(2), r"-\frac{1}{\sqrt{2}}"),
            (0.5, r"\frac{1}{2}"),
            (-0.5, r"-\frac{1}{2}"),
            (1 / np.sqrt(8), r"\frac{1}{2\sqrt{2}}"),
            (-1 / np.sqrt(8), r"-\frac{1}{2\sqrt{2}}"),
        ]

        r = z.real
        i = z.imag

        if abs(i) < atol:
            for value, latex in common:
                if np.isclose(r, value, atol=atol):
                    return latex

            return f"{r:.4g}"

        if abs(r) < atol:
            for value, latex in common:
                if np.isclose(i, value, atol=atol):
                    if latex == "1":
                        return "i"
                    if latex == "-1":
                        return "-i"

                    if latex.startswith("-"):
                        return "-" + latex[1:] + "i"

                    return latex + "i"

            return f"{i:.4g}i"

        sign = "+" if i >= 0 else "-"
        return f"\\left({r:.4g}{sign}{abs(i):.4g}i\\right)"
```

すると普通の `Statevector` とほぼ同じ感覚で、

```python
sv = XStatevector([1, 0])

sv.draw("latex")
```

では通常どおり

$$
|0\rangle
$$

を表示し、

```python
sv.draw_xbasis()
```

では

$$
\frac{1}{\sqrt2}|+\rangle
+
\frac{1}{\sqrt2}|-\rangle
$$

と表示できます。

### `from_label()` も使いたい場合

ここは少し注意があります。

```python
sv = XStatevector.from_label("+")
```

としたとき、Qiskit側の実装によっては返り値が通常の `Statevector` になる可能性があります。なので確実に派生クラスにしたいなら、

```python
sv = XStatevector(Statevector.from_label("+").data)
```

とできます。

より使いやすくするなら、自分のクラス側に、

```python
@classmethod
def from_label(cls, label):
    sv = Statevector.from_label(label)
    return cls(sv.data)
```

を追加します。

すると、

```python
sv = XStatevector.from_label("+-")

sv.draw("latex")
sv.draw_xbasis()
```

という形で使えます。

### さらに `draw("latex", basis="x")` のようにもできる

技術的には `draw()` 自体をオーバーライドして、

```python
sv.draw("latex", basis="x")
```

のようなAPIにすることもできます。

ただ、私は最初は

```python
sv.draw("latex")
sv.draw_xbasis()
```

のように**別メソッドにしておく方をおすすめします**。

理由は、Qiskit本来の

```python
Statevector.draw()
```

の意味を変更しないからです。

つまり、

```text
Statevector
    └─ XStatevector
          ├─ draw()         ← Qiskit本来の表示
          └─ draw_xbasis()  ← 自作のX基底表示
```

という設計です。

さらに発展させるなら、`XStatevector` ではなく、

```python
BasisStatevector
```

のようにして、

```python
sv.draw_basis("x")
sv.draw_basis("y")
sv.draw_basis("z")
```

まで一般化するのがかなり面白いと思います。今作っているものは、本質的にはすでに「X基底専用 Statevector」というより**任意基底で Statevector の座標を見る仕組み**に近いです。


## Y基底対応

あります。むしろ、**Z・X・Yの3つまで揃うと、1量子ビットの状態の見方としてかなり完成度が高くなります。**

Y基底は

$$
|+i\rangle=\frac{1}{\sqrt2}\left(|0\rangle+i|1\rangle\right)
$$

$$
|-i\rangle=\frac{1}{\sqrt2}\left(|0\rangle-i|1\rangle\right)
$$

です。

これは Pauli-$Y$ の固有状態で、

$$
Y|+i\rangle=+|+i\rangle
$$

$$
Y|-i\rangle=-|-i\rangle
$$

を満たします。

なので、整理すると、

| 基底  | 基底状態 | 対応する Pauli |            |     |
| --- | ---- | ---------- | ---------- | --- |
| Z基底 | $    | 0\rangle,  | 1\rangle$  | $Z$ |
| X基底 | $    | +\rangle,  | -\rangle$  | $X$ |
| Y基底 | $    | +i\rangle, | -i\rangle$ | $Y$ |

となります。

これは Bloch 球ともきれいに対応しています。

* $|0\rangle, |1\rangle$：$\pm Z$ 方向
* $|+\rangle, |-\rangle$：$\pm X$ 方向
* $|+i\rangle, |-i\rangle$：$\pm Y$ 方向

つまり、**Bloch球の3本の直交軸を全部見る**ことになります。

特にY基底を対応させる意味が大きいのは、「虚数の位相」が見えるからです。

たとえば、

$$
|+i\rangle
=
\frac{1}{\sqrt2}
\begin{pmatrix}
1\\
i
\end{pmatrix}
$$

は、Z基底で見ると少し複雑ですが、Y基底で見れば単に

$$
|+i\rangle
=
\begin{pmatrix}
1\\
0
\end{pmatrix}_Y
$$

です。

つまり以前のX基底とまったく同じ構造で、

$$
|+\rangle
\leftrightarrow
\begin{pmatrix}
1\\
0
\end{pmatrix}_X
$$

に対応して、

$$
|+i\rangle
\leftrightarrow
\begin{pmatrix}
1\\
0
\end{pmatrix}_Y
$$

となります。

ここがかなり重要です。

たとえば

$$
|\psi\rangle
=
\frac{1}{\sqrt2}
\left(
|0\rangle+i|1\rangle
\right)
$$

をZ基底で見ると、

```text
[1/√2, i/√2]
```

ですが、

Y基底では

```text
[1, 0]
```

です。

なので、今作ろうとしているクラスを

```python
sv.draw_basis("z")
sv.draw_basis("x")
sv.draw_basis("y")
```

のようにする意味は十分あります。

むしろ私は、**X専用クラスにするより、XYZ基底を扱う一般化クラスにした方が学習用としてよい**と思います。

たとえばAPIとしては、

```python
sv.draw_basis("z")
```

$$
a|0\rangle+b|1\rangle
$$

```python
sv.draw_basis("x")
```

$$
c|+\rangle+d|-\rangle
$$

```python
sv.draw_basis("y")
```

$$
e|+i\rangle+f|-i\rangle
$$

のようになります。

そして、この3つは単なる表示方法の違いではなく、

> 同じ量子状態を、Bloch球のZ・X・Y方向から見た座標

と理解できます。

これはかなり教育的価値があります。

さらに一歩進めると、1量子ビット状態

$$
|\psi\rangle
$$

に対して、

$$
\langle X\rangle,\quad
\langle Y\rangle,\quad
\langle Z\rangle
$$

を求めれば、その3つがそのままBlochベクトルの座標になります。

なので、

```python
sv.draw_basis("x")
sv.draw_basis("y")
sv.draw_basis("z")
```

と

```python
sv.bloch_vector()
```

を同じクラスに持たせる設計は、かなり相性がいいです。

今の流れなら、次は `BasisStatevector` として **Z/X/Y基底に対応した完成版**にするのが一番きれいです。

# リファクタリング

はい、その設計の方が分かりやすいと思います。

特に学習用途では、

```python
sv.draw_zbasis()
sv.draw_xbasis()
sv.draw_ybasis()
```

の方が、`draw_basis("x")` よりも「何を表示しているか」がコード上で即座に分かります。

内部では共通処理を1か所にまとめて、公開メソッドだけ3つに分けるのがきれいです。たとえばこうです。

```python
import numpy as np
from IPython.display import display, Math
from qiskit.quantum_info import Statevector


class BasisStatevector(Statevector):

    def draw_zbasis(self, atol=1e-10):
        return self._draw_basis("z", atol)

    def draw_xbasis(self, atol=1e-10):
        return self._draw_basis("x", atol)

    def draw_ybasis(self, atol=1e-10):
        return self._draw_basis("y", atol)

    def _draw_basis(self, basis, atol=1e-10):
        if basis == "z":
            transform = np.eye(2, dtype=complex)
            labels = ("0", "1")

        elif basis == "x":
            transform = np.array([
                [1,  1],
                [1, -1]
            ], dtype=complex) / np.sqrt(2)

            labels = ("+", "-")

        elif basis == "y":
            transform = np.array([
                [1, -1j],
                [1,  1j]
            ], dtype=complex) / np.sqrt(2)

            labels = ("+i", "-i")

        else:
            raise ValueError(f"Unsupported basis: {basis}")

        n = self.num_qubits

        # U^{⊗n}
        transform_n = np.array([[1]], dtype=complex)

        for _ in range(n):
            transform_n = np.kron(transform_n, transform)

        amplitudes = transform_n @ self.data

        terms = []

        for i, amp in enumerate(amplitudes):
            if abs(amp) < atol:
                continue

            bits = format(i, f"0{n}b")

            label = "".join(
                labels[int(bit)]
                for bit in bits
            )

            coeff = self._latex_amplitude(amp, atol)

            if coeff == "1":
                term = f"|{label}\\rangle"
            elif coeff == "-1":
                term = f"-|{label}\\rangle"
            else:
                term = f"{coeff}|{label}\\rangle"

            terms.append(term)

        latex = self._join_terms(terms)

        display(Math(latex))

    @staticmethod
    def _join_terms(terms):
        if not terms:
            return "0"

        latex = terms[0]

        for term in terms[1:]:
            if term.startswith("-"):
                latex += " - " + term[1:]
            else:
                latex += " + " + term

        return latex

    @staticmethod
    def _latex_amplitude(z, atol=1e-10):
        if abs(z) < atol:
            return "0"

        common = [
            (1.0, "1"),
            (-1.0, "-1"),
            (1 / np.sqrt(2), r"\frac{1}{\sqrt{2}}"),
            (-1 / np.sqrt(2), r"-\frac{1}{\sqrt{2}}"),
            (0.5, r"\frac{1}{2}"),
            (-0.5, r"-\frac{1}{2}"),
            (1 / np.sqrt(8), r"\frac{1}{2\sqrt{2}}"),
            (-1 / np.sqrt(8), r"-\frac{1}{2\sqrt{2}}"),
        ]

        r = z.real
        i = z.imag

        if abs(i) < atol:
            for value, latex in common:
                if np.isclose(r, value, atol=atol):
                    return latex

            return f"{r:.4g}"

        if abs(r) < atol:
            for value, latex in common:
                if np.isclose(i, value, atol=atol):
                    if latex == "1":
                        return "i"
                    elif latex == "-1":
                        return "-i"
                    elif latex.startswith("-"):
                        return "-" + latex[1:] + "i"
                    else:
                        return latex + "i"

            return f"{i:.4g}i"

        sign = "+" if i >= 0 else "-"
        return f"\\left({r:.4g}{sign}{abs(i):.4g}i\\right)"

    @classmethod
    def from_label(cls, label):
        sv = Statevector.from_label(label)
        return cls(sv.data)
```

使い方は、

```python
sv = BasisStatevector.from_label("0")

sv.draw_zbasis()
sv.draw_xbasis()
sv.draw_ybasis()
```

です。

それぞれ、

$$
|0\rangle
$$

$$
\frac{1}{\sqrt2}|+\rangle
+
\frac{1}{\sqrt2}|-\rangle
$$

$$
\frac{1}{\sqrt2}|+i\rangle
+
\frac{1}{\sqrt2}|-i\rangle
$$

になります。

この設計の良いところは、公開APIが非常に素直なことです。

```text
draw_zbasis()   ← Z基底で見る
draw_xbasis()   ← X基底で見る
draw_ybasis()   ← Y基底で見る
```

内部だけ、

```python
_draw_basis(...)
```

で共通化しています。

しかも、ユーザー側が

```python
sv.draw_basis("foo")
```

のような「存在しない基底名」を渡す余地もありません。

なので今回の目的なら、**3つの明示的メソッド + 1つのprivate共通実装**という形が一番きれいだと思います。

作成しました。ローカルでインストールして、Jupyter Notebook から普通に `import` して使える構成です。

[ZIPをダウンロード](sandbox:/mnt/data/basis-statevector-0.1.0.zip)

中身は主に以下です。

```text
basis-statevector/
├── pyproject.toml
├── README.md
├── src/
│   └── basis_statevector/
│       ├── __init__.py
│       └── statevector.py
├── examples/
│   └── quickstart.ipynb
└── tests/
    └── test_statevector.py
```

展開後、そのディレクトリで

```bash
pip install -e .
```

とすれば、

```python
from basis_statevector import BasisStatevector
```

で利用できます。

たとえば Notebook では、

```python
from basis_statevector import BasisStatevector

sv = BasisStatevector.from_label("0")

sv.draw_zbasis()
sv.draw_xbasis()
sv.draw_ybasis()
```

のように使えます。

`draw("latex")` も継承元の `Statevector` のものをそのまま利用できます。

```python
sv.draw("latex")
```

一方、自作メソッドでは、

```python
sv.draw_zbasis()
sv.draw_xbasis()
sv.draw_ybasis()
```

と、表示する基底を明示できます。

Y基底についても、

```python
import numpy as np

sv = BasisStatevector(
    [1 / np.sqrt(2), 1j / np.sqrt(2)]
)

sv.draw_ybasis()
```

で

$$
|+i\rangle
$$

と表示される設計です。

`README.md` にインストール方法、Jupyterでの利用方法、複数量子ビットの例、設計方針も記載し、`examples/quickstart.ipynb` も入れています。

なお、こちらの実行環境には Qiskit が入っておらず外部インストールもできなかったため、実Qiskit上でのテスト実行まではできていません。Pythonの構文チェックとNotebook構造の検証までは通しています。ご自身のQiskit環境で `pytest` を実行できるよう、テストも同梱してあります。

# 結果検証

はい、ここはかなり興味深い違いです。結論からいうと、**同じ状態を表しているが、係数の“簡約の仕方”が違う**だけです。

Qiskit標準の

```python
svplus.draw("latex")
```

では、$|+\rangle$ が

$$
\frac{\sqrt2}{2}|0\rangle+\frac{\sqrt2}{2}|1\rangle
$$

と表示されています。

一方、こちらの `BasisStatevector` の `draw_zbasis()` では

$$
\frac{1}{\sqrt2}|0\rangle+\frac{1}{\sqrt2}|1\rangle
$$

です。

この2つは完全に同じです。

$$
\frac{\sqrt2}{2}
=
\frac{1}{\sqrt2}
$$

だからです。

違うのは、単に

* Qiskit側：$\sqrt2/2$
* 今回の自作側：$1/\sqrt2$

という**記号表現の選択**です。

今回の `BasisStatevector` では `_latex_amplitude()` の中で、

```python
1 / np.sqrt(2)
```

に近い数値を見つけたら、

```latex
\frac{1}{\sqrt{2}}
```

と表示するよう、こちらが明示的に決めています。

つまり、

```python
(1 / np.sqrt(2), r"\frac{1}{\sqrt{2}}")
```

というルールを自作しているため、そう見えています。

Qiskitの `draw("latex")` は、Qiskit側の数値→記号式変換ロジックに従って、同じ値を

$$
\frac{\sqrt2}{2}
$$

と整形しています。

どちらが自然かは文脈次第ですが、**量子情報の学習用途では、私は $\frac1{\sqrt2}$ の方がかなり読みやすいと思います。**

たとえば

$$
|+\rangle
=
\frac1{\sqrt2}
\left(
|0\rangle+|1\rangle
\right)
$$

という定義とそのまま対応するからです。

Qiskit標準の

$$
\frac{\sqrt2}{2}|0\rangle
+
\frac{\sqrt2}{2}|1\rangle
$$

も数学的には正しいのですが、

$$
|+\rangle
=
\frac1{\sqrt2}(|0\rangle+|1\rangle)
$$

を頭に入れている学習者から見ると、少し余計な変換が入っています。

今回のスクリーンショットを見ると、さらにこの違いがはっきりしています。

```python
display(svplus.draw("latex"))
```

は

$$
\frac{\sqrt2}{2}|0\rangle
+
\frac{\sqrt2}{2}|1\rangle
$$

ですが、

```python
display(svplus.draw_zbasis())
```

は

$$
\frac1{\sqrt2}|0\rangle
+
\frac1{\sqrt2}|1\rangle
$$

です。

状態は同一です。

それから、Y基底で

$$
(0.5-0.5i)|+i\rangle
+
(0.5+0.5i)|-i\rangle
$$

と出ているのも、今の自作フォーマッタが**一般複素数についてはまだ小数表示にフォールバックしている**ためです。

これも本当は、

$$
\frac{1-i}{2}|+i\rangle
+
\frac{1+i}{2}|-i\rangle
$$

と表示した方が学習用途ではずっときれいです。

つまり今の差は、

> Qiskitと自作クラスで「状態の数学」が違うのではなく、「数値をどの記号表現に戻すか」という表示ポリシーが違う

ということです。

この観点からいうと、次の改善はかなり明確です。`BasisStatevector` の表示規約を、

* $0.7071 \rightarrow \frac1{\sqrt2}$
* $0.5 \rightarrow \frac12$
* $0.5+0.5i \rightarrow \frac{1+i}{2}$
* $0.5-0.5i \rightarrow \frac{1-i}{2}$
* $\frac{1}{2\sqrt2}$ などもできるだけ記号化

という方向に揃えると、**Qiskit標準よりも量子情報学習向けに読みやすい表示器**としてかなり意味のあるものになります。

個人的には、このパッケージは「Qiskitの表示を真似る」より、**量子情報の教科書でよく見る形を優先する**方針にした方が良さそうです。
