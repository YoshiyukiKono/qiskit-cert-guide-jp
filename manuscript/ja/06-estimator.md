# 6. Estimator V2

[← Sampler V2](05-sampler.md) | [次: jobと結果分析 →](07-results-analysis.md)

<a id="estimator-purpose"></a>
## 期待値を評価する

量子回路を実行した後に知りたいことは、測定で得られるビット列とは限りません。「この状態をZで測ったときの平均はいくつか」「角度を変えると、その平均はどう変わるか」を直接調べたいこともあります。そのための道具が**Estimator**です。

この章では、期待値を求める入力を作り、複数の条件をまとめ、精度や誤差への対処を指定して、結果を読むまでを説明します。まず、入力と出力の意味を一つの量子ビットで確認します。

### 回路が状態を、観測量が調べる内容を決める

**観測量**（**observable**）は、状態に対して何を測るかを表す演算子です。**期待値**は、その測定で得られる値を確率で重み付けした平均です。状態を$|\psi\rangle$、観測量を$O$とすると、期待値を$\langle\psi|O|\psi\rangle$と書きます。記号や行列計算から確認したい場合は、第1章の[observableと期待値](01-quantum-operations.md#expectation)を参照してください。

例えば、$|0\rangle$にHを適用すると$|+\rangle=(|0\rangle+|1\rangle)/\sqrt{2}$になります。この状態をZで測ると、ビット0に対応する測定値$+1$と、ビット1に対応する測定値$-1$が半分ずつ現れます。したがって、

$$
\langle Z\rangle=(+1)\times\frac12+(-1)\times\frac12=0.
$$

**平均が0でも、一回のZ測定で値0が出るわけではありません。** 同じ状態をXで測ると常に測定値$+1$となり、$\langle X\rangle=1$です。回路が同じでも、観測量を変えると答える問いが変わります。

| 知りたいこと | 主に使うprimitive | 結果の例 |
|---|---|---|
| 測定でどのビット列が何回出たか | Sampler | 0と1の測定データ、そこから数えた出現回数 |
| 指定した観測量の平均はいくつか | Estimator | Zの期待値0、Xの期待値1 |

### 一つの期待値を計算する

次の例はQiskit 2.5.2でローカル実行できます。`StatevectorEstimator`は、ここで使う測定を含まない回路では状態ベクトルから期待値を計算します。`precision=0.0`を指定し、標本の揺らぎを加えずに値を確かめます。

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(1)
qc.h(0)
obs = SparsePauliOp("Z")
estimator = StatevectorEstimator()
job = estimator.run([(qc, obs)], precision=0.0)
result = job.result()

print("Z expectation:", f"{float(result[0].data.evs):.6f}")
```

出力:

```text
Z expectation: 0.000000
```

`SparsePauliOp("Z")`はZという観測量を作ります。`(qc, obs)`は回路と観測量を一組にした入力で、次節で説明するPUBです。`run()`は実行を表すjobを返し、`job.result()`で結果を取得します。最初のPUBの期待値が`result[0].data.evs`に入っています。`float(...)`は、この例のように値が一つだけの配列をPythonの数値に変換しています。

この回路には`measure_all()`を付けていません。Estimatorでは観測量を別に渡し、実装がその評価に必要な処理を担当するからです。例えばXの評価にはZと異なる測定の向きが必要ですが、利用者が観測量ごとに測定回路を組み直す必要はありません。

### ローカル計算とQPU実行を区別する

**QPU**（Quantum Processing Unit）は量子計算を行う実機です。IBMのQPUへ送る場合は、`qiskit_ibm_runtime.EstimatorV2`を使います。二つの実装はPUBや結果の基本形を共有しますが、計算方法や設定項目は同じではありません。

| 実装 | この章での役割 | 実行の前提 |
|---|---|---|
| `qiskit.primitives.StatevectorEstimator` | 理想的な期待値や配列の対応を手元で確かめる | Qiskitを入れたローカル環境 |
| `qiskit_ibm_runtime.EstimatorV2` | QPU上で測定し、期待値を推定する | Runtimeの認証、実行先、実行先に適合した回路と観測量 |

以降は、まずローカルで入力の意味を確かめ、[precision、shots、resilience](#estimator-options)で実機の測定回数や誤差への対処を説明します。**同じ入力の形式を使えても、ローカルの理想値と実機の推定値が必ず一致するわけではありません。**

<a id="estimator-pub"></a>
## Estimator PUB

期待値の計算には、「どの回路で状態を用意するか」と「何を測るか」が必要です。さらに、回路の角度が未定ならその値を、個別の精度を希望するならその指定を加えます。これらをまとめた入力単位が**PUB**（**Primitive Unified Bloc**）です。この節では、要素の順序と、一つのPUBにまとめられる範囲を確認します。

### タプルの位置には決まった意味がある

Estimator PUBの一般形は`(circuit, observables, parameter_values, precision)`です。

| 位置 | 要素 | 役割と省略条件 |
|---|---|---|
| 1 | `circuit` | 状態を用意する一つの`QuantumCircuit`。必須 |
| 2 | `observables` | 期待値を求める観測量一つ、またはその配列。必須 |
| 3 | `parameter_values` | 回路中の未定のパラメータに割り当てる値。未定の値がなければ省略または`None` |
| 4 | `precision` | このPUBに求める統計的な精度の目標。省略できる。詳しくは[後の節](#estimator-options)で説明 |

パラメータのない回路なら`(qc, observable)`で足ります。precisionだけを指定したい場合は、`(qc, observable, None, 0.02)`と書きます。3番目の`None`は「割り当てるパラメータ値がない」という位置を保つためのものです。`(qc, observable, 0.02)`と詰めると、`0.02`はprecisionではなくパラメータ値として読まれます。

観測量は`"Z"`などの文字列、`Pauli`、`SparsePauliOp`などで表せます。**複数の観測量を並べることと、観測量の和を作ることは違います。** 例えば`["Z", "X"]`なら、ZとXの二つの期待値を得ます。一方、`SparsePauliOp.from_list([("Z", 0.5), ("X", -1.0)])`は、$O=0.5Z-X$という一つの観測量です。得る値は$\langle O\rangle=0.5\langle Z\rangle-\langle X\rangle$の一つで、$|+\rangle$に対しては$-1$になります。

### 一つの回路で複数条件を評価する

次の例では、Hで$|+\rangle$を用意する回路と、角度を変えられる$R_y(\theta)$の回路を、二つのPUBとして渡します。`Parameter`は回路中の「後で具体的な値を入れる場所」を表します。`[[0.0], [np.pi]]`は、角度一つを必要とする回路に対する、2通りの値の割当てです。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator

plus_circuit = QuantumCircuit(1)
plus_circuit.h(0)

theta = Parameter("theta")
rotation_circuit = QuantumCircuit(1)
rotation_circuit.ry(theta, 0)

pub1 = (plus_circuit, ["Z", "X"])
pub2 = (rotation_circuit, "Z", [[0.0], [np.pi]])
result = StatevectorEstimator().run([pub1, pub2], precision=0.0).result()

print("PUB results:", len(result))
print("plus, Z and X:", np.round(result[0].data.evs, 6))
print("rotation, Z at 0 and pi:", np.round(result[1].data.evs, 6))
```

出力:

```text
PUB results: 2
plus, Z and X: [0. 1.]
rotation, Z at 0 and pi: [ 1. -1.]
```

`result[0]`と`result[1]`はPUBの順序に対応します。最初のPUBは一つの状態について観測量を二つ、二つ目は一つの観測量について状態を二通り評価しています。$R_y(0)|0\rangle=|0\rangle$、$R_y(\pi)|0\rangle=|1\rangle$なので、二つ目のZの期待値は$+1,-1$です。角度と観測量の両方を複数にする指定は、次節のbroadcastingで扱います。

一つのPUBに入る回路は一つですが、得られる期待値は一つとは限りません。回路の構造自体が異なるならPUBを分けます。また、**PUBを一つにまとめても、実機で一回だけ測定するという意味ではありません。** 上のZとXは測定の向きが異なり、それぞれの評価が必要です。

同じ測定データを共有できる観測量もあります。例えば2量子ビットの`"ZI"`と`"IZ"`は、両量子ビットをZで測ったデータから評価できます。このような、演算の順序を交換しても変わらない関係を**可換**（commuting）といいます。Runtimeが対応する観測量を測定グループにまとめられるよう、同じ回路に対するものは同じPUBに入れます。別々のPUBへ分けた観測量は、このグループ化の対象になりません。グループ化の具体的な条件は実装に依存します。

### QPU向けに回路を変換したら、観測量も対応させる

実機で使えるゲートや量子ビットの接続には制約があります。回路をその制約に適合させる変換が**transpile**で、実行先の命令セット（Instruction Set Architecture、**ISA**）に適合した回路をISA circuitと呼びます。その際、回路で書いた量子ビットが、実機のどの量子ビットを使うかという**layout**も決まります。

例えば、元の2量子ビット回路の$q_0$を物理量子ビット2へ移したなら、「元の$q_0$をZで調べる」という観測量も物理量子ビット2へ移さなければなりません。回路だけを移すと、別の量子ビットを調べることになったり、量子ビット数が合わずエラーになったりします。

次の例は、3量子ビットの仮の実行先`GenericBackendV2`をローカルで作り、対応関係を確かめます。実機への送信はありません。`initial_layout=[2, 0]`で、元の$q_0$を物理2へ、$q_1$を物理0へ割り当てます。

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager

qc = QuantumCircuit(2)
qc.x(0)
observable = SparsePauliOp("IZ")  # 右端の文字が元のq0

backend = GenericBackendV2(3, seed=123)
pm = generate_preset_pass_manager(
    backend=backend, optimization_level=0, initial_layout=[2, 0]
)
isa_circuit = pm.run(qc)
isa_observable = observable.apply_layout(isa_circuit.layout)

result = StatevectorEstimator().run(
    [(qc, observable), (isa_circuit, isa_observable)], precision=0.0
).result()

print("mapped observable:", isa_observable.paulis.to_labels())
print("before:", f"{float(result[0].data.evs):.6f}")
print("after:", f"{float(result[1].data.evs):.6f}")
```

出力:

```text
mapped observable: ['ZII']
before: -1.000000
after: -1.000000
```

Pauli文字列は右端が量子ビット0なので、変換後の`"ZII"`は物理量子ビット2のZです。変換前後で「元の$q_0$を調べる」という意味を保ち、期待値も$-1$で一致しています。`apply_layout`は量子ビットの並べ替えに加え、回路の幅に合わせた拡張も扱います。QPUへ渡すPUBは、この例の`(isa_circuit, isa_observable)`の組です。実機の取得方法は[serviceとbackend選択](04-transpile-execution.md#backend-selection)を参照してください。

**判断の要点**: PUBの要素は位置で読み、一つの回路に対する観測量と値の割当てをまとめます。QPU向けに変換するときは、回路と観測量を必ず同じlayoutにそろえます。

公式参照: [Estimator input/output](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output)、[PUBの構成](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output#estimator-pub)、[SparsePauliOp.apply_layout](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp#apply_layout)

<a id="estimator-broadcasting"></a>
## broadcastingをshapeで読む

同じ回路で角度を何通りか試し、それぞれについて複数の期待値を求めたいとします。Estimator V2では、観測量とパラメータ値を配列にまとめられます。そのとき「どの観測量と、どの値を組み合わせるか」を決めるのが**broadcasting**（**ブロードキャスト**）です。

この節の目標は、配列の`shape`から結果の形を求め、その一つ一つの要素が何の期待値かを説明できることです。NumPyのbroadcastingは、この節で基礎から説明します。

### まず、何を何通り計算したいかを決める

例として、初期状態$|0\rangle$に$R_y(\theta)$を一回適用する1量子ビット回路を使います。$\theta$は回転角で、単位はラジアンです。回路中に値が未定の`Parameter`を置くと、回路の構造を保ったまま角度を変えられます。具体的な値の組をパラメータに当てはめることを、ここでは**binding**（**値の割当て**）と呼びます。

今回は$\theta=0,\pi/2,\pi$の3通りを試します。それぞれに対して、ZとXという2種類の**観測量**（**observable**）の期待値を求めます。観測量は「用意した状態の何を調べるか」を指定します。例えばZでは、測定値$+1$と$-1$をそれぞれの確率で重み付けして平均します。詳しい意味は[期待値を評価する](#estimator-purpose)を参照してください。

求めたい結果を、先に表にすると次のようになります。$\langle Z\rangle_{\theta=0}$は「**角度0で用意した状態に対するZの期待値**」という意味です。

| 観測量 / 角度 | $0$ | $\pi/2$ | $\pi$ |
|---|---|---|---|
| Z | $\langle Z\rangle_{\theta=0}$ | $\langle Z\rangle_{\theta=\pi/2}$ | $\langle Z\rangle_{\theta=\pi}$ |
| X | $\langle X\rangle_{\theta=0}$ | $\langle X\rangle_{\theta=\pi/2}$ | $\langle X\rangle_{\theta=\pi}$ |

行が観測量、列が角度で、全部で$2\times3=6$個の期待値を求めたいわけです。この対応を配列で指定します。一つのEstimator PUBは、一つの回路と観測量、その回路へ渡すパラメータ値などをまとめた入力です。今回は`(回路, 観測量の配列, パラメータ値の配列)`という形を使います。

### shapeと、それぞれの軸の意味

NumPy配列の`shape`は、各軸の長さを並べたものです。例えば`[["Z"], ["X"]]`は2行1列なので`(2, 1)`、`["Z", "X"]`は長さ2の1次元配列なので`(2,)`です。括弧の末尾のカンマは、要素が一つのPythonのタプルを表します。

観測量は次の2行1列に並べます。

```text
[["Z"],
 ["X"]]     shape: (2, 1)
```

最初の軸の長さ2は、ZとXの2種類に対応します。最後の長さ1の軸は、各観測量を複数の角度と組み合わせるために用意した軸です。観測量が二つあるだけでは、全組合せを計算するかどうかは決まりません。この長さ1の軸が後で効いてきます。

パラメータ値は、1行に「一回の割当てに必要な値」を並べます。この回路のパラメータは$\theta$一つなので、各行も値一つです。

```text
[[0.0],
 [π/2],
 [π  ]]     shape: (3, 1)  ※ π は説明用の数学記号
```

こちらの最初の軸の長さ3は、角度を3通り試すことを表します。最後の軸の長さ1は、回路のパラメータが1個あることを表します。**観測量の配列にある長さ1の軸と、役割が違う**点に注意してください。

Estimatorが組み合わせる対象は、「観測量」と「回路への値の割当て」です。パラメータ値配列の最後の軸は、一つの割当てを構成する中身なので、組合せのshapeには数えません。この例では、パラメータ値のshape `(3, 1)`から最後の軸を除いた`(3,)`が**binding shape**です。

例えばパラメータが2個ある回路なら、`[[a0, b0], [a1, b1], [a2, b2]]`は3通りの割当てを表します。値のshapeは`(3, 2)`でも、binding shapeはやはり`(3,)`です。値を並べる順序は`circuit.parameters`で確認します。

最後の軸を除くのは、結果のshapeを考えるときの読み替えです。**PUBに渡す配列を実際に削ったり平坦にしたりする操作ではありません。** 今回は`(3, 1)`の配列をそのまま渡します。

### 右端から比較して、結果のshapeを求める

ここからNumPyと同じbroadcastingの規則を使います。

1. 二つのshapeを右端でそろえる。軸が足りない側は、左に長さ1の軸があると考える。
2. 各軸を比較し、長さが同じか、どちらかが1なら組み合わせられる。
3. 長さ1の側を相手の長さに合わせ、各軸の結果を並べる。長さが異なり、どちらも1でない軸があれば組み合わせられない。

今回の比較は次のようになります。

```text
observables shape: (2, 1)
binding shape:        (3,)
左に1を補って比較: (1, 3)
--------------------------------
result shape:      (2, 3)
```

右の軸は1と3なので3へ、左の軸は2と1なので2へ広がります。これは、Zを3通りの角度に、Xも同じ3通りの角度に対応させる指定です。結果は最初に作った表と同じ、2行3列になります。

### 実行して、六つの期待値を読む

次の例は必要な定義をすべて含み、Qiskit 2.5.2とNumPyがあればローカルで実行できます。`StatevectorEstimator`で、測定を含まないこの回路を`precision=0.0`で評価します。この条件では、状態ベクトルから期待値を計算するので、shotsによる標本の揺らぎは入りません。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator

theta = Parameter("theta")
pqc = QuantumCircuit(1)
pqc.ry(theta, 0)

observables = np.array([["Z"], ["X"]], dtype=object)
angles = np.array([0.0, np.pi / 2, np.pi])
values = angles.reshape(3, 1)  # 3通りの割当て × 各1個のパラメータ値

pub = (pqc, observables, values)
estimator = StatevectorEstimator()
job = estimator.run([pub], precision=0.0)
result = job.result()
evs = result[0].data.evs

print("observables:", observables.shape)
print("parameter values:", values.shape)
print("expectations:", evs.shape)
print(np.round(evs, 6))
```

出力:

```text
observables: (2, 1)
parameter values: (3, 1)
expectations: (2, 3)
[[ 1.  0. -1.]
 [ 0.  1.  0.]]
```

`reshape(3, 1)`は、3個の角度を3行1列に並べ直しています。観測量の`"Z"`と`"X"`はPauli演算子を表す文字列です。この例では、それぞれが配列の一要素です。

`run([pub])`はjobを返し、`job.result()`で結果を取得します。`result[0]`は、渡した一つのPUBに対応する結果です。その`data.evs`に六つの期待値が入ります。PUBが六つある、という意味ではありません。

`evs`の行と列は、最初の表にそのまま対応します。Pythonの添字は0から始まるので、`evs[0, 2]`は「Z、角度$\pi$」の期待値$-1$、`evs[1, 1]`は「X、角度$\pi/2$」の期待値$1$です。負の値が出ても異常ではありません。期待値は確率ではなく、測定値を重み付けした平均だからです。

この例はローカル計算です。QPUへ送る場合のISA circuitやobservableのlayoutは[ISA circuitとlayout](04-transpile-execution.md#isa-layout)を参照してください。

### 出力の値も、手計算で確かめる

shapeが正しくても、各要素の意味を取り違えていないかは別に確認します。この回路が用意する状態は次のとおりです。

$$
|\psi(\theta)\rangle=R_y(\theta)|0\rangle
=\cos\frac{\theta}{2}|0\rangle+\sin\frac{\theta}{2}|1\rangle.
$$

$c=\cos(\theta/2)$、$s=\sin(\theta/2)$と置くと、$R_y$の行列から上の状態を求める計算は次のとおりです。

$$
R_y(\theta)|0\rangle
=\begin{pmatrix}c&-s\\s&c\end{pmatrix}
\begin{pmatrix}1\\0\end{pmatrix}
=\begin{pmatrix}c\\s\end{pmatrix}.
$$

期待値を計算するときは、この列ベクトルの左に、その複素共役を横に並べた行ベクトルを置き、間に観測量の行列を挟みます。今回の$c,s$は実数なので、複素共役を取っても値は変わりません。

$$
\begin{aligned}
\langle Z\rangle
&=\begin{pmatrix}c&s\end{pmatrix}
\begin{pmatrix}1&0\\0&-1\end{pmatrix}
\begin{pmatrix}c\\s\end{pmatrix}
=c^2-s^2=\cos\theta,\\
\langle X\rangle
&=\begin{pmatrix}c&s\end{pmatrix}
\begin{pmatrix}0&1\\1&0\end{pmatrix}
\begin{pmatrix}c\\s\end{pmatrix}
=2cs=\sin\theta.
\end{aligned}
$$

最後の等号には三角関数の倍角公式を使いました。$\theta=0,\pi/2,\pi$を代入すると、Zの行は$1,0,-1$、Xの行は$0,1,0$となり、実行結果と一致します。コードは表示を小数点以下6桁に丸めています。丸め前には、理論値0が浮動小数点誤差によりごく小さい数として現れることがあります。

### 配列を平らにすると、何が変わるか

観測量を`["Z", "X"]`というshape `(2,)`にすると、今回のbinding shape `(3,)`とは組み合わせられません。右端の長さが2と3で、どちらも1ではないからです。Estimatorが自動的に全組合せへ直してくれるわけではありません。

さらに注意したいのは、長さが同じ場合です。次のコードは、上の実行例に続けて実行できます。

```python
pair_observables = np.array(["Z", "X"], dtype=object)  # shape (2,)
pair_values = np.array([[0.0], [np.pi / 2]])           # binding shape (2,)
pair_pub = (pqc, pair_observables, pair_values)
pair_evs = estimator.run([pair_pub], precision=0.0).result()[0].data.evs

print("paired expectations:", pair_evs.shape)
print(np.round(pair_evs, 6))
```

出力:

```text
paired expectations: (2,)
[1. 1.]
```

`(2,)`と`(2,)`は同じ位置どうしを対応させるので、「Z、角度0」と「X、角度$\pi/2$」の二つだけを評価します。「Z、角度$\pi/2$」と「X、角度0」も含めた四つの組合せがほしければ、観測量を`[["Z"], ["X"]]`のshape `(2, 1)`にします。結果は`(2, 2)`です。

### 確認問題

1. パラメータが2個の回路に、shape `(5, 2)`の値を渡します。binding shapeは何ですか。
2. その5通りの割当てに、shape `(3, 1)`の観測量を組み合わせると、結果のshapeと期待値の個数はいくつですか。
3. この節の最初の実行例で、観測量の行をX、Zの順に入れ替えると、`evs[0, 2]`は何の期待値になり、いくつになりますか。
4. 観測量のshapeとbinding shapeがともに`(3,)`なら、結果は`(3, 3)`になりますか。

**解答と理由**

1. `(5,)`です。最後の長さ2の軸は、一回の割当てに必要な二つのパラメータ値を表します。割当ては5通りです。
2. `(3, 5)`で15個です。`(3, 1)`と、左に1を補った`(1, 5)`を比べると、各軸が3と5へ広がります。各観測量について5通りの値を評価します。
3. Xの角度$\pi$での期待値となり、理論値は$\sin\pi=0$です。観測量の順を変えると結果の行の意味も変わります。実装上は0に近い浮動小数点数になる場合があります。
4. なりません。結果は`(3,)`で、同じ位置の観測量と割当てを対応させた3個です。9個の全組合せが目的なら、例えば観測量を`(3, 1)`にします。

**判断の要点**: まず欲しい組合せを表にし、観測量のshapeとbinding shapeを別々に求め、右端から比較します。結果のshapeだけでなく、各添字が指す観測量と値まで説明できれば、配列の書き方が変わった問題にも対応できます。

公式参照: [Primitive inputs and outputs — Broadcasting rules](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output#broadcasting-rules)、[StatevectorEstimator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorEstimator)、[NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)、[$R_y$の行列](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RYGate)

<a id="estimator-options"></a>
## precision、shots、resilience

実機では、同じ回路を繰り返して得た測定値から期待値を推定します。ここには、測定回数が有限であるための揺らぎと、装置の誤差による偏りが入り得ます。この節の目標は、この二つを区別し、precision、shots、誤差軽減の設定が何を変えるかを説明できることです。

### shotsは回数、precisionは平均の揺らぎに対する目標

**shot**は、状態を用意して測定する一回の試行です。**shots**はその回数を表します。例えばZの測定を100回行い、ビット0が60回、1が40回なら、期待値の推定値は次のようになります。

$$
\widehat{\langle Z\rangle}=\frac{60\times(+1)+40\times(-1)}{100}=0.2.
$$

帽子の記号$\widehat{\phantom{Z}}$は、測定データから得た推定値であることを示します。同じ条件で100回の実験をやり直しても、60回と40回という内訳が毎回再現されるとは限りません。このような平均の揺らぎの大きさを表すのが**標準誤差**（standard error）です。

関係を見やすくするため、測定値が$+1,-1$の一つのPauli観測量を、独立に$N$回測る場合を考えます。一回の測定値を$m$、その平均を$\mu$とすると、$m^2=1$です。一回の値のばらつきを表す分散は$\langle m^2\rangle-\mu^2=1-\mu^2$になります。独立な$N$回の平均では分散が$1/N$になるので、その平方根である標準誤差は、

$$
\mathrm{SE}=\sqrt{\frac{1-\mu^2}{N}}\leq\frac{1}{\sqrt{N}}
$$

です。例えば$\mu=0$なら、100 shotsで$\mathrm{SE}=0.1$、10,000 shotsで$0.01$です。**平均の揺らぎを半分にするには、shotsはおよそ4倍必要**になります。

Estimatorの**target precision**は、このような統計的な不確かさに対する目標です。値が小さいほど厳しい目標になります。例えば`precision=0.02`は、上の単純な条件で$1/\sqrt{N}$を目安にすると$N=1/0.02^2=2,500$に相当します。ただし、これは一つのPauli観測量を誤差軽減なしで測る場合の目安です。観測量の和、測定グループ、誤差軽減に必要な追加実験を含むjob全体のshots数を、常にこの式だけで決められるわけではありません。

また、precisionは「真の期待値との差が必ずこの値以内」という保証ではありません。実際に達成した統計的な不確かさは結果で確認し、装置の誤差による偏りは別に考えます。

### 回数を増やしても消えない偏りがある

本来は必ず0が出る状態を用意したのに、装置がその10%を1と読み間違える場合を考えます。Zの理想的な期待値は1ですが、読み間違いを含む平均は、

$$
(+1)\times0.9+(-1)\times0.1=0.8
$$

です。測定回数を増やすと、推定値は0.8の周りで安定していきます。1へ近づくとは限りません。このような理想値からの系統的なずれを**偏り**（bias）と呼びます。

対処には、実行中に誤差の影響を小さくする**誤差抑制**（error suppression）と、追加実験や測定後の計算を使って期待値の偏りを減らす**誤差軽減**（error mitigation）があります。以下では、それぞれの手法がどこに働きかけるかを見ていきます。

### ZNE: ノイズを増やした実験から、ノイズがない場合を推定する

**ZNE**は**Zero-Noise Extrapolation**の略で、日本語では「ゼロノイズ外挿」です。**外挿**とは、測った範囲の外へ傾向を延ばして、未測定の点の値を推定することです。ZNEでは、ノイズを段階的に増やした回路を実行し、期待値がどう変化するかを調べて、ノイズがゼロの点へ外挿します。

「誤差を減らしたいのに、なぜノイズを増やすのか」と感じるかもしれません。実機のノイズをゼロにして直接測ることはできなくても、追加の操作でノイズを増やした条件なら作れるためです。その変化から、ゼロの点を推定します。

仕組みだけを見るため、ある観測量について次の値が得られたと仮定します。**この表は説明用の仮想データで、実機の測定結果ではありません。** ノイズ倍率$\lambda=1$は元の回路の条件であり、ノイズがない状態ではありません。

| ノイズ倍率$\lambda$ | 期待値の推定値 | 役割 |
|---|---|---|
| 1 | 0.70 | 元のノイズ条件で測る点 |
| 3 | 0.50 | ノイズを増やして測る点 |
| 5 | 0.30 | さらに増やして測る点 |
| 0 | 未測定 | 外挿で推定したい点 |

この3点は直線上にあります。倍率が2増えると期待値が0.20減るので、直線の傾きは$-0.20/2=-0.10$です。直線を$f(\lambda)=a\lambda+b$と書くと、$f(1)=0.70$より、

$$
a=-0.10,\qquad b=0.70-(-0.10)\times1=0.80.
$$

したがって、ゼロノイズへの外挿値は$f(0)=0.80$になります。次のコードは、この**測定後の直線当てはめ**だけを再現します。

```python
import numpy as np

noise_factors = np.array([1.0, 3.0, 5.0])
measured_evs = np.array([0.70, 0.50, 0.30])  # 説明用の仮想データ
slope, intercept = np.polyfit(noise_factors, measured_evs, deg=1)

print("slope:", f"{slope:.2f}")
print("zero-noise estimate:", f"{intercept:.2f}")
```

出力:

```text
slope: -0.10
zero-noise estimate: 0.80
```

`np.polyfit(..., deg=1)`は、与えた点へ直線を当てはめ、その傾きと切片を返します。$\lambda=0$の値は切片です。0.80は仮定した直線から得た推定値であり、実機の真値が0.80だと証明されたわけではありません。実際のデータには揺らぎがあり、直線が適切とも限りません。曲線の選び方や測定誤差が外挿値に影響し、元の値より悪くなる場合もあります。

Runtimeでノイズを増やす代表的な方法に**gate folding**があります。あるゲート$U$を、理想的には同じ働きをする$UU^\dagger U$に置き換えます。$U^\dagger$は$U$を取り消す逆操作で、$U^\dagger U=I$なので、全体は$U$です。しかし実機では操作を増やした分の誤差が加わります。Runtimeのgate foldingは対象となる2量子ビットゲートを使って増幅します。先ほどの1量子ビットだけのbroadcasting例に、この方法を付ければ同じノイズ倍率の実験ができる、と考えないようにします。

`noise_factors=(1, 3, 5)`は、実験するノイズ倍率の指定です。ゼロノイズを直接測る指定ではないので、この並びに0を入れません。倍率は装置のすべての誤差が厳密にその倍数になる保証でもありません。ZNEでは複数の条件を測るため、追加のshotsや実行時間が必要です。

### TREXとtwirling: 読み出し誤差やノイズの性質に対処する

先ほどの「0を1と読む」ような誤差を**読み出し誤差**（readout error）といいます。これによる期待値の偏りを減らす手法が**TREX**（**Twirled Readout Error eXtinction**）です。測定の仕方をランダムに変えて読み出し誤差を扱いやすくし、別の校正実験で調べた補正係数を使います。校正とは、基準となる状態などを使って装置の誤差の性質を調べることです。

名前に含まれる**twirling**は、理想的な結果を保つように操作をランダムに変え、複数の実行結果を平均してノイズの性質を整える考え方です。測定のtwirlingでは、測定直前にXを入れるかをランダムに選び、入れた場合は得られたビットを古典計算で反転し直します。理想的には元の測定と同じ意味ですが、読み出し誤差の現れ方を変えられます。

補正の直感を得るため、0と1がどちらも確率$p$で読み間違えられる単純なモデルを考えます。正しく読めばZの符号はそのまま、読み間違えれば符号が逆になるので、

$$
\langle Z\rangle_{\mathrm{read}}=(1-p)\langle Z\rangle-p\langle Z\rangle
=(1-2p)\langle Z\rangle.
$$

仮に校正で$p=0.1$だと分かれば、読み取った平均0.8を$1-2p=0.8$で割って、補正値1を得ます。これは補正係数の役割を示す単純化した例です。実際のTREXは測定のtwirlingとノイズ学習を組み合わせます。校正自体にも測定回数が必要で、その不確かさや装置の変化が結果に影響します。また、読み出し誤差の補正だけで、状態を用意するゲートの誤差まで取り除けるわけではありません。

**ゲートのPauli twirling**は、測定のtwirlingとは対象が異なります。ゲートの前後に、理想的な演算を保つ組合せでランダムなPauli操作を挟みます。例えば同じ角度のずれが繰り返し積み重なるような誤差を、ランダムな誤りとして扱いやすくする狙いがあります。元の回路から作る複数のランダムな実行回路を**randomizations**と呼び、各回路を何shotsずつ測るかも指定できます。ZNEなどと併用されますが、twirlingだけで誤差がすべて消えるわけではありません。

### DD: 待機中の誤差を抑える

回路の途中で、ある量子ビットが他の量子ビットの操作を待つことがあります。その待機中にも、周囲との相互作用などで状態は変化し得ます。待機時間にパルス列を挿入し、その影響を打ち消すようにするのが**DD**（**Dynamical Decoupling**、動的デカップリング）です。

例えばXを二回行う列は、理想的には$XX=I$で状態を元に戻します。これを適切な間隔で挟むことで、待機中に蓄積する一部の誤差を抑えます。期待値を測定後に外挿するZNEとは、働きかける段階が異なります。待機時間がほとんどない回路では効果が小さく、追加パルス自身の誤差で結果が悪化する場合もあります。

Xの間隔によって位相のずれを打ち消す途中計算と、Runtime Samplerへの指定は[第5章のDD](05-sampler.md#sampler-dd)で扱います。ここでは、DDと期待値を求める他の設定が、何に働きかけるかを比べます。

| 方法 | 主に何をするか | 追加で必要になるもの |
|---|---|---|
| shotsを増やす | 有限回の測定に伴う平均の揺らぎを減らす | 測定回数 |
| ZNE | ノイズを増やした条件からゼロノイズへ外挿する | 複数のノイズ条件の実験と当てはめ |
| TREX | 読み出し誤差による期待値の偏りを補正する | 測定のtwirlingと校正実験 |
| ゲートのPauli twirling | 理想演算を保ったランダム化でノイズの性質を整える | 複数のランダムな実行回路 |
| DD | 待機中の一部の誤差を抑える | 待機時間に挿入するパルス列 |

公式参照: [誤差軽減・抑制手法の仕組み](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques)、[ZNEの設定](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-zne-options)

### resilience_levelは手法の組合せを選ぶ出発点

Runtime Estimatorの`resilience_level`は、誤差への対処をまとめて選ぶ**preset**、つまり設定のひな型です。本書のコードが基準とする`qiskit-ibm-runtime 0.49.0`では、levelに0・1・2を指定できます。

以下に、[Runtimeの公式ガイド](https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management#resilience-level)に基づく各levelの役割を示します。具体的な手法の割当てや既定値はRuntimeサービス側の仕様にも依存し、パッケージのバージョンを固定しても、同じ手法が適用され続けることは保証されません。

| level | 公式ガイドが示す主な設定 | 読み方 |
|---|---|---|
| 0 | 誤差軽減を適用しない | 理想的で誤差のない実行になる、という意味ではない |
| 1 | TREXによる読み出し誤差の軽減と測定のtwirling | 主に読み出し誤差に対処する |
| 2 | level 1にZNEとゲートのtwirlingを追加 | 追加実験を使って偏りの低減を狙う |

levelを上げると計算の負担も増えますが、特定の実験で必ず理想値に近づく保証はありません。また、DDを含めたすべての設定を、levelという数字一つから判断できるわけではありません。

**個別に指定したoptionは、presetの対応する設定を上書きします。** 次のコードで、その読み方を確かめます。`EstimatorOptions`に設定を作り、Runtimeの`EstimatorV2`へ渡します。ここでは仮のbackendを使って設定の保持だけを確認するので、認証や実機への送信はありません。

```python
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_ibm_runtime import EstimatorV2
from qiskit_ibm_runtime.options import EstimatorOptions

options = EstimatorOptions(resilience_level=0)
options.resilience.zne_mitigation = True
options.resilience.zne.noise_factors = (1, 3, 5)
options.resilience.zne.extrapolator = "linear"

backend = GenericBackendV2(3, seed=123)
estimator = EstimatorV2(mode=backend, options=options)

print("level:", estimator.options.resilience_level)
print("ZNE:", estimator.options.resilience.zne_mitigation)
print("noise factors:", estimator.options.resilience.zne.noise_factors)
print("extrapolator:", estimator.options.resilience.zne.extrapolator)
```

出力:

```text
level: 0
ZNE: True
noise factors: (1.0, 3.0, 5.0)
extrapolator: linear
```

この指定は「level 0を出発点にし、ZNEを個別に有効にする」と読みます。`resilience_level=0`だけを見てZNEが無効だと判断してはいけません。`extrapolator="linear"`は、直線による外挿の指定です。このコードが確認しているのはクライアント側の設定であり、ZNEを実行した結果ではありません。仮のbackendでのローカル実行は、Runtimeの誤差軽減処理の再現にはなりません。

実機で使う場合は、[第4章の手順](04-transpile-execution.md#backend-selection)で取得したbackendを`EstimatorV2(mode=backend, options=options)`へ渡し、そのbackend向けに変換した回路と観測量のPUBを`run()`へ渡します。使用する回路・ゲートが各手法に対応することも、公式資料の[機能の組合せ条件](https://quantum.cloud.ibm.com/docs/en/guides/estimator-options#feature-compatibility)で確認します。

作成後に変更する場合は、例えば`estimator.options.resilience.zne_mitigation = False`のようにEstimatorが持つ設定を変更します。更新する対象を明確にするため、作成時に渡した元の`options`を後から変更する書き方は避けます。未指定項目に現れる`Unset`は「無効」の意味ではなく、最終的な値をサーバー側の既定値などに委ねていることを示します。

### precisionやshotsを複数箇所で指定したとき

PUBに書いたprecisionは、そのPUB専用です。`run(..., precision=...)`に書いた値は、その呼出しのうちprecisionを個別指定していないPUBに使われます。次のローカル例では、どの目標値が各PUBへ渡ったかを結果の付随情報で確認します。

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator

qc = QuantumCircuit(1)
qc.h(0)
pub1 = (qc, "Z", None, 0.02)
pub2 = (qc, "X")

result = StatevectorEstimator(seed=123).run(
    [pub1, pub2], precision=0.03
).result()

print("PUB 1 target:", result[0].metadata["target_precision"])
print("PUB 2 target:", result[1].metadata["target_precision"])
```

出力:

```text
PUB 1 target: 0.02
PUB 2 target: 0.03
```

`metadata`は、結果に添えられた実行条件などの情報です。ここで表示しているのは目標precisionで、達成した誤差ではありません。また、`StatevectorEstimator`の正のprecisionは計算値に人工的なランダムな揺らぎを加える指定であり、実機のshotsやノイズを再現する設定ではありません。状態ベクトルの値を揺らぎなしで確認する前の例では0.0を使いましたが、RuntimeのQPU実行で要求するprecisionは正の値です。

なお、qiskit-ibm-runtime 0.49.0では、異なるprecisionを持つPUBを同じjobに含める指定は非推奨です。直前の例はローカルの`StatevectorEstimator`による優先順位の確認であり、Runtimeでは精度の指定ごとにjobを分けます。この変更は0.48.0の[公式リリースノート](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/release-notes)に記載されています。

Runtimeには、さらに`default_precision`、`default_shots`、twirlingに割り当てる測定回数があります。優先関係は、各PUBについて次の順に読みます。

1. PUB自身のprecision。
2. `run(..., precision=...)`のprecision。
3. twirlingが有効で回数を明示した場合の、`num_randomizations`と`shots_per_randomization`の積。
4. `default_shots`。
5. `default_precision`。

例えばランダム化した回路を32通り作り、それぞれ100 shots測るなら、積は3,200 shotsです。`"auto"`や未指定の項目は、ほかの設定を基にRuntimeが決定します。PUBや`run()`のprecisionを優先して指定しても、固定したtwirlingの回数との組合せによっては必要なshotsを割り当てられず、実行できない場合があります。すべてを同時に固定する場合は、この整合性も必要です。

`default_shots`はjob全体の総回数ではありません。一つのパラメータ割当てと、一つの物理的な測定の向きの組に対する回数です。例えばZとXを別々の向きで測るなら、その分の実験が必要になります。複数のノイズ倍率や校正実験を加える場合も、追加の実行を考慮します。

**判断の要点**: 平均の揺らぎを減らしたいのか、装置の誤差による偏りを減らしたいのかを分けます。その上で、目標precision、必要な実験、presetと個別optionsの順に確認します。

公式参照: [Estimator optionsとprecisionの優先関係](https://quantum.cloud.ibm.com/docs/en/guides/estimator-options#special-case-precision)、[resilience level](https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management)、[EstimatorOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-estimator-options)、[TwirlingOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-twirling-options)

<a id="estimator-result"></a>
## Estimator result

結果を読むときは、「何番目のPUBか」「そのPUBのどの観測量・パラメータ値か」「期待値か、不確かさか」を順にたどります。この節では、その階層と数値の意味を確認します。

### PUBを選んでから、配列の要素を選ぶ

`job.result()`が返す全体が`PrimitiveResult`です。その各要素が、一つのPUBの結果である`PubResult`です。さらに`data`に数値の配列、`metadata`に実行条件などの付随情報が入ります。

```text
result                         job.result()で得た全体
├─ result[0]                   1番目のPUBの結果
│  ├─ data.evs                 期待値の配列
│  ├─ data.stds                不確かさを表す配列
│  └─ metadata                 このPUBに関する付随情報
├─ result[1]                   2番目のPUBの結果（あれば）
└─ metadata                    結果全体の付随情報
```

`evs`はexpectation values、つまり期待値です。配列のshapeは[入力のbroadcasting](#estimator-broadcasting)で決まり、PUB数とは別に数えます。例えばPUBが一つで`evs.shape==(2, 3)`なら、`result[0]`の中に六つの期待値があります。`result[1]`を取っても二行目は得られません。二行目は`result[0].data.evs[1]`です。

次のコードは、それ自体で実行できるローカル例です。最初のPUBではZ一つ、二つ目ではZとXの二つを評価します。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator

qc = QuantumCircuit(1)
qc.h(0)
result = StatevectorEstimator().run(
    [(qc, "Z"), (qc, ["Z", "X"])], precision=0.0
).result()

print("PUB results:", len(result))
print("scalar shape:", result[0].data.evs.shape)
print("array shape:", result[1].data.evs.shape)
print("expectations:", np.round(result[1].data.evs, 6))
print("stds:", result[1].data.stds)
print("X expectation:", f"{float(result[1].data.evs[1]):.6f}")
print("data fields:", sorted(result[1].data.keys()))
print("target precision:", result[1].metadata["target_precision"])
```

出力:

```text
PUB results: 2
scalar shape: ()
array shape: (2,)
expectations: [0. 1.]
stds: [0. 0.]
X expectation: 1.000000
data fields: ['evs', 'stds']
target precision: 0.0
```

shape `()`は空の配列ではなく、軸を持たない一つの値、つまり**scalar**を表します。一方、shape `(2,)`には二つの値が入っています。`float(...)`で値を取り出すなら、後者では観測量の位置まで添字で選びます。

### stdsが0でも、一回の測定値が一定とは限らない

`stds`は、期待値の推定に伴う不確かさを表す欄です。測定で出たビット列やその出現回数ではありません。このローカル例は、測定を含まない回路を状態ベクトルからprecision 0.0で評価しているため、`stds`は0です。

それでも$|+\rangle$を実際にZで測れば、測定値は$+1,-1$に分かれます。**期待値を計算上正確に知っていることと、一回の測定が決まった値を返すことは別です。** この例のZの期待値0と`stds`の0は、異なる内容を表しています。

実機で、仮に期待値0.80、標準誤差0.03と報告されたなら、後者は平均の統計的な不確かさの尺度です。「真値は必ず0.77から0.83に入る」「装置の誤差による偏りも0.03以下」という意味ではありません。どの統計モデルや補正に基づく値かも確認します。

### Runtimeではデータ項目とmetadataも確認する

Runtimeでは、使用した誤差軽減や実装によって、`stds`に加えて`ensemble_standard_error`などの不確かさに関する項目が現れることがあります。ランダム化した回路どうしのばらつきまで含めるか、shots由来の揺らぎだけを考えるかなど、算出方法が同じとは限りません。名前だけから同じ意味の数値だと決めず、`pub_result.data.keys()`で実際の項目を確認し、対応する公式資料を読みます。

ZNEを有効にした結果では、最終的な期待値に加え、ノイズ倍率ごとの期待値`evs_noise_factors`や、外挿の結果`evs_extrapolated`などを確認できる場合があります。これらは「どの倍率で何を観測し、どの外挿で値を得たか」を調べるための情報です。ノイズ倍率などの軸が加わるため、通常の`evs`と同じshapeだとは限りません。詳細は[ZNEの結果配列](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-zne-options)を参照してください。

`metadata`には、実装に応じて目標precision、shots、誤差軽減の条件などが入ります。ローカル例に存在したキーが実機でもすべて同じ場所にあると仮定せず、結果全体の`result.metadata`と、各PUBの`result[i].metadata`をそれぞれ確認します。目標precisionの欄だけでは、実際の不確かさや偏りは分かりません。

二つの値の差と不確かさを一緒に読む方法は[第7章の比較例](07-results-analysis.md#compare-results)へ進みます。独立性などの前提を確認したうえで、Estimatorの結果へ応用します。比較の根拠として残す入力・測定記録・実行条件は、[第7章のmetadata](07-results-analysis.md#metadata)で整理します。

**判断の要点**: PUB番号を選び、`evs`のshapeと添字を入力に対応させてから、値と不確かさを読みます。どの条件で得られた値かはmetadataで確認します。

公式参照: [Estimatorの出力](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output)、[StatevectorEstimator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorEstimator)

期待値を繰り返し評価して状態を選ぶ応用は、[補章AのVQE](09-algorithm-worked-examples.md#algorithm-vqe)で扱います。ハミルトニアン、候補回路、Estimator、古典側の最適化が、それぞれ何を担当するかを小さなモデルで確かめます。

## 章末チェック

1. $|+\rangle$のZの期待値が0なら、一回のZ測定で値0が出ますか。観測量をXへ変えると期待値はいくつですか。
2. 未定のパラメータがない回路で、PUBにprecision 0.01だけを追加するにはどう書きますか。
3. 回路のパラメータが2個で、`values.shape==(5, 2)`ならbinding shapeは何ですか。観測量のshapeが`(3, 1)`なら、期待値のshapeは何ですか。
4. 元の$q_0$が物理量子ビット2へ移り、ISA circuitが3量子ビットになりました。元の$q_0$のZを調べるPauli文字列は何ですか。
5. 独立なPauli測定で、ほかの条件を変えず平均の標準誤差を半分にするには、shotsを何倍にしますか。それだけで読み出し誤差の偏りも消えますか。
6. ZNEで、ノイズ倍率1の期待値が0.6、倍率3の期待値が0.2でした。直線で外挿すると倍率0の値はいくつですか。その値は実測値ですか。
7. `resilience_level=0`と`resilience.zne_mitigation=True`を同時に指定した場合、ZNEは無効だと判断できますか。
8. PUBを一つだけ渡し、その`evs.shape`が`(2, 3)`でした。2番目の観測量と3番目のパラメータ割当ての期待値をどの添字で取り出しますか。ローカル計算で`stds`が0なら、実機の測定値も常に同じですか。

**解答と理由**

1. 出ません。Zの測定値は$+1,-1$が等確率で、平均が0です。Xでは$|+\rangle$に対して測定値$+1$が確定するので、期待値は1です。
2. `(qc, observable, None, 0.01)`です。3番目はパラメータ値の位置なので、`None`でその位置を保ちます。
3. binding shapeは`(5,)`です。最後の軸2は、一回の割当てに必要な値の個数だからです。`(3, 1)`と`(5,)`のbroadcastingは`(3, 5)`となり、15個の期待値を得ます。
4. `"ZII"`です。右端が物理量子ビット0なので、物理2のZは左端です。実際のコードでは`observable.apply_layout(isa_circuit.layout)`を使って回路との対応を保ちます。
5. 4倍です。標準誤差が$1/\sqrt{N}$に比例するためです。読み出し誤差がある場合、増やした測定は偏った平均の周りで安定するだけかもしれません。偏りには別の対処が必要です。
6. 傾きは$(0.2-0.6)/(3-1)=-0.2$なので、倍率0では$0.6-(-0.2)=0.8$です。これは直線を仮定した外挿値であり、倍率0で測定した値でも、正しいと保証された真値でもありません。
7. できません。個別のZNE指定がpresetの対応する設定を上書きします。levelだけでなく個別optionsを確認します。
8. `result[0].data.evs[1, 2]`です。最初の`[0]`はPUB番号、後ろの`[1, 2]`は期待値配列の行と列です。理想的な状態ベクトル計算で期待値の不確かさが0でも、一回の実機測定の値が一定になるとは限りません。

[← Sampler V2](05-sampler.md) | [次: jobと結果分析 →](07-results-analysis.md)
