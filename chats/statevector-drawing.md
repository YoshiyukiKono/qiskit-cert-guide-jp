Qiskitの`Statevector`は、**数値配列・ケット記法の数式・ベクトルの数式・各種グラフ**として表示できます。中心となるのは **`sv.draw("表示形式")`** です。([IBM Quantum][1])

まず、共通の例として次の状態を使います。

```python
import numpy as np
from qiskit.quantum_info import Statevector
from IPython.display import display

sv = Statevector(np.array([1, 0, 0, 1j]) / np.sqrt(2))
```

これは次の2量子ビット状態です。

$$
|\psi\rangle
=
\frac{1}{\sqrt{2}}|00\rangle
+
\frac{i}{\sqrt{2}}|11\rangle.
$$

## 1. まず、表示方法の一覧

`draw()`には次の表示形式があります。引数を省略した`sv.draw()`は、設定を変更していなければ`"repr"`になります。([IBM Quantum][1])

| 書き方                                     | 表示内容                              |
| --------------------------------------- | --------------------------------- |
| `sv.draw("repr")`                       | `Statevector(...)`というオブジェクトの文字列表現 |
| `sv.draw("text")`                       | 振幅を数値で並べたテキスト                     |
| `sv.draw("latex")`                      | ケット記法による数式                        |
| `sv.draw("latex", convention="vector")` | 振幅を横に並べたベクトルの数式                   |
| `sv.draw("latex_source")`               | 数式を描画する前のLaTeXソース文字列              |
| `sv.draw("bloch")`                      | 各量子ビットのBloch球                     |
| `sv.draw("qsphere")`                    | 基底成分の確率と位相を表すQ-sphere             |
| `sv.draw("city")`                       | 密度行列の実部・虚部を表す立体棒グラフ               |
| `sv.draw("hinton")`                     | 密度行列の成分を正方形で表す図                   |
| `sv.draw("paulivec")`                   | Pauli演算子の期待値を表す棒グラフ               |

`convention="vector"`は`"latex"`の表示方法を切り替える追加引数です。また、**グラフの種類によって、状態のどの情報を見せているかが異なります**。

## 2. 数式で表示する

### ケット記法で表示する

Notebookのセルの最後に、次のように書きます。

```python
sv.draw("latex")
```

表示される内容は、次の数式です。係数は$\sqrt{2}/2$のような同値な表記になることもあります。

$$
\frac{1}{\sqrt{2}}|00\rangle
+
\frac{i}{\sqrt{2}}|11\rangle
$$

名前を付けて表示することもできます。

```python
sv.draw("latex", prefix=r"|\psi\rangle = ")
```

また、表示する小数点以下の桁数や、項数の上限を指定できます。これらは**表示上の設定**であり、`sv`に保存されている振幅を変更する操作ではありません。

```python
sv.draw(
    "latex",
    decimals=4,      # 表示に使う丸めの桁数
    max_size=16,     # 表示する非ゼロ項の上限
)
```

### 振幅を横に並べた数式で表示する

```python
sv.draw("latex", convention="vector")
```

次のように、ケットのラベルを付けずに振幅を並べます。

$$
\begin{bmatrix}
\frac{1}{\sqrt{2}} & 0 & 0 & \frac{i}{\sqrt{2}}
\end{bmatrix}
$$

**これは、ブラ$\langle\psi|$に変換したという意味ではありません。** 複素共役は取っておらず、同じ振幅を横に並べた表示です。実装では、状態の配列をそのまま`array_to_latex()`へ渡しています。

### 列ベクトルで表示する

数学でよく使う**縦の列ベクトル**にしたい場合は、こちらが分かりやすいです。

```python
from qiskit.visualization import array_to_latex

array_to_latex(
    sv.data.reshape(-1, 1),
    prefix=r"|\psi\rangle = ",
)
```

$$
|\psi\rangle
=
\begin{bmatrix}
\frac{1}{\sqrt{2}}\\
0\\
0\\
\frac{i}{\sqrt{2}}
\end{bmatrix}
$$

`reshape(-1, 1)`は、表示に渡す配列を「1列」に整えています。`array_to_latex()`は1次元・2次元の数値配列を数式表示する関数です。こちらの桁数指定は、`decimals`ではなく **`precision`** です。([IBM Quantum][2])

```python
array_to_latex(
    sv.data.reshape(-1, 1),
    precision=4,
    max_size=16,
)
```

## 3. 数値や基底ラベルを確認する

### オブジェクト全体と、配列だけの違い

```python
print(sv)
```

```text
Statevector([0.70710678+0.j        , 0.        +0.j        ,
             0.        +0.j        , 0.        +0.70710678j],
            dims=(2, 2))
```

一方、`data`を取り出すと、振幅を格納したNumPy配列だけになります。

```python
print(sv.data)
```

```text
[0.70710678+0.j         0.        +0.j
 0.        +0.j         0.        +0.70710678j]
```

`print(sv)`は状態の次元情報も含めて確認したい場合、`sv.data`は振幅を数値として扱いたい場合に使えます。([GitHub][3])

### 基底ラベルと振幅を対応させる

```python
sv.to_dict(decimals=4)
```

この例では、非ゼロの成分について、次の対応を得られます。

| 基底ラベル  |         振幅 |
| ------ | ---------: |
| `"00"` |  約$0.7071$ |
| `"11"` | 約$0.7071i$ |

**ここに出る値は確率ではなく、複素数の振幅です。** `to_dict()`は、計算基底のラベルをキーとする辞書に変換します。([IBM Quantum][1])

なお、Qiskitの2量子ビットの振幅の並びは、

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle
$$

に対応し、ケット内のビットは$|q_1q_0\rangle$の順です。**右端が量子ビット0**です。([IBM Quantum][4])

## 4. グラフで表示する

### Bloch球：各量子ビットの状態を見る

```python
sv.draw("bloch")
```

量子ビットごとにBloch球が表示されます。各球の$(x,y,z)$は、その量子ビットに対するPauli $X,Y,Z$の期待値です。([IBM Quantum][5])

今回のようなもつれ状態では、各量子ビットだけを見るとBlochベクトルはゼロになります。これは、上の状態から各局所Pauli期待値を計算すると、すべてゼロになるためです。

したがって、**複数量子ビットのBloch球を並べても、量子ビット間の相関を含む全体の状態は分かりません。**

最初にBloch球を試すなら、1量子ビットの例のほうが見やすいです。

```python
sv1 = Statevector(np.array([1, 1j]) / np.sqrt(2))

sv1.draw("bloch")
```

これは、

$$
|{+i}\rangle
=
\frac{1}{\sqrt{2}}|0\rangle
+
\frac{i}{\sqrt{2}}|1\rangle
$$

なので、Blochベクトルは$+Y$方向になります。

### Q-sphere：全体の基底成分と位相を見る

```python
sv.draw("qsphere")
```

Q-sphereでは、**点の大きさが各基底成分の確率、色が位相**を表します。位相の数値も表示できます。([IBM Quantum][6])

```python
sv.draw(
    "qsphere",
    show_state_phases=True,
    use_degrees=True,
)
```

今回の例では、$|00\rangle$と$|11\rangle$の確率はどちらも$1/2$で、相対位相は$90^\circ$です。

**Bloch球とQ-sphereは、どちらも球状の図ですが、同じ表示方法ではありません。**

### City・Hinton・Pauli-vector

次のコードでは、3種類を同じセルから順に表示できます。

```python
display(sv.draw("city"))
display(sv.draw("hinton"))
display(sv.draw("paulivec"))
```

それぞれの見方は次の通りです。([IBM Quantum][7])

| 表示           | 何を見ているか                     |
| ------------ | --------------------------- |
| `"city"`     | 密度行列$\rho$の実部・虚部を、棒の高さで表示   |
| `"hinton"`   | 密度行列の実部・虚部を、正方形の大きさと色で表示    |
| `"paulivec"` | $I,X,Y,Z$や、それらのテンソル積の期待値を表示 |

特に、**`"city"`と`"hinton"`は、状態ベクトルの成分を直接描いているわけではありません。**

入力が`Statevector`でも、

$$
\rho=|\psi\rangle\langle\psi|
$$

という密度行列に対応する図になります。([GitHub][8])

## 5. 測定確率を表示する

計算基底で測定したときの確率を取り出すには、次を使います。

```python
sv.probabilities()
```

```text
array([0.5, 0. , 0. , 0.5])
```

基底ラベル付きなら、こちらです。

```python
sv.probabilities_dict()
```

内容は、`"00"`と`"11"`がそれぞれ確率$1/2$という辞書になります。どちらも、**計算基底での測定確率**を返します。([IBM Quantum][1])

棒グラフにするには、`plot_distribution()`へ渡します。

```python
from qiskit.visualization import plot_distribution

plot_distribution(sv.probabilities_dict())
```

`plot_distribution()`は、辞書で与えた分布を描画できます。([IBM Quantum][9])

ここで重要なのは、**確率のグラフには位相情報が出ない**ことです。例えば、

$$
\frac{|00\rangle+|11\rangle}{\sqrt{2}}
\qquad\text{と}\qquad
\frac{|00\rangle+i|11\rangle}{\sqrt{2}}
$$

は異なる状態ですが、振幅の絶対値の2乗が同じなので、この確率グラフは同じになります。

## 6. Jupyterでの`print()`と`display()`の使い分け

数式や図を表示するときは、**セルの最後に置くか、`display()`を使います**。`display()`は、LaTeXなどの表示形式に応じてNotebookへ出力します。([IPython Documentation][10])

```python
# セルの最後に置く
sv.draw("latex")
```

複数の形式を1つのセルで表示する場合は、次のようにします。

```python
display(sv.draw("latex"))

display(
    array_to_latex(
        sv.data.reshape(-1, 1),
        prefix=r"|\psi\rangle = ",
    )
)

display(plot_distribution(sv.probabilities_dict()))
```

一方、**LaTeXのソース文字列そのもの**が欲しい場合には、`print()`が適しています。([IBM Quantum][1])

```python
print(sv.draw("latex_source"))
```

### 描画用ライブラリが不足している場合

`MissingOptionalLibraryError`などが出る場合は、描画用の追加依存関係を導入します。Qiskit公式の指定は`qiskit[visualization]`です。([IBM Quantum][7])

```python
%pip install "qiskit[visualization]"
```

---

今の学習では、まず **ケット記法の`sv.draw("latex")`、列ベクトルの`array_to_latex(sv.data.reshape(-1, 1))`、測定確率のグラフ**を見比べる使い方がよいと思います。**「基底状態の線形結合」「振幅の列」「振幅から求めた確率」**を、同じ状態で対応づけられます。

[1]: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector "Statevector (latest version) | IBM Quantum Documentation"
[2]: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.array_to_latex "array_to_latex (latest version) | IBM Quantum Documentation"
[3]: https://github.com/Qiskit/qiskit/tree/stable/2.5/qiskit/quantum_info/states/statevector.py "qiskit/qiskit/quantum_info/states/statevector.py at stable/2.5 · Qiskit/qiskit · GitHub"
[4]: https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering "Bit-ordering in the Qiskit SDK | IBM Quantum Documentation"
[5]: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_bloch_multivector "plot_bloch_multivector (latest version) | IBM Quantum Documentation"
[6]: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_state_qsphere "plot_state_qsphere (latest version) | IBM Quantum Documentation"
[7]: https://quantum.cloud.ibm.com/docs/en/api/qiskit/visualization "visualization (latest version) | IBM Quantum Documentation"
[8]: https://raw.githubusercontent.com/Qiskit/qiskit/stable/2.5/qiskit/visualization/state_visualization.py "raw.githubusercontent.com"
[9]: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_distribution "plot_distribution (latest version) | IBM Quantum Documentation"
[10]: https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html "Module: display — IPython 9.17.1 documentation"
