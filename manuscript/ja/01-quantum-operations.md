# 1. 量子状態、行列、基本演算

[← 学び方](00-guide.md) | [次: 測定と可視化 →](02-visualization-measurement.md)

<a id="state-amplitude"></a>
## 状態と複素振幅

1 qubit pure stateは

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle,
\qquad \alpha,\beta\in\mathbb{C},
\qquad |\alpha|^2+|\beta|^2=1
$$

です。$\alpha,\beta$は確率ではなく複素振幅で、computational basis測定の確率が$|\alpha|^2,|\beta|^2$です。よく使う状態は次のとおりです。

$$
\begin{aligned}
|+\rangle &= \frac{|0\rangle+|1\rangle}{\sqrt{2}},\\
|-\rangle &= \frac{|0\rangle-|1\rangle}{\sqrt{2}},\\
|+i\rangle &= \frac{|0\rangle+i|1\rangle}{\sqrt{2}}.
\end{aligned}
$$

<a id="matrix-order"></a>
## 行列と演算順序

column vectorへ右から作用するので、$U$の後に$V$なら状態は$VU|\psi\rangle$です。回路図を左から読む時間順と、行列積の右から左への作用を取り違えないでください。

```python
from qiskit.quantum_info import Operator
from qiskit.circuit.library import HGate, XGate, ZGate

assert Operator(HGate()) @ Operator(ZGate()) @ Operator(HGate()) == Operator(XGate())
```

Hadamard行列と、上のコードで確認した等式は次のとおりです。

$$
H=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad HZH=X.
$$

典型的誤答は回路順と積の順を反転することです。

<a id="phase"></a>
## global phaseとrelative phase

$|\psi\rangle$と$e^{i\varphi}|\psi\rangle$はすべての振幅へ共通因子を掛けたもので、同じphysical state（ray）です。しかしstatevectorや行列の**厳密な等式**では同じとは限りません。relative phaseは成分間の位相差で、干渉結果を変えます。

$$
R_z(\theta)=\exp\!\left(-\frac{i\theta Z}{2}\right)
=\begin{pmatrix}e^{-i\theta/2}&0\\0&e^{i\theta/2}\end{pmatrix},
\qquad R_z(\pi)=-iZ.
$$

物理作用は$Z$相当でも厳密な行列は$Z$ではありません。Qiskitの`QuantumCircuit.global_phase`はglobal phaseを表現・保持できます。

判断手順: (1) 「厳密」とあるか、(2) 全成分に同じ因子か、(3) 確率だけか干渉も問うか。

<a id="basic-gates"></a>
## Pauli、Hadamard、位相、回転

Pauli行列は次のとおりです。

$$
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\qquad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
$$

したがって$Y|0\rangle=i|1\rangle$、$XZ=-ZX$。$H|0\rangle=|+\rangle$、$H|1\rangle=|-\rangle$、逆に$H|+\rangle=|0\rangle$、$H|-\rangle=|1\rangle$です。位相gateは次の行列です。

$$
S=\begin{pmatrix}1&0\\0&i\end{pmatrix},\qquad
S^\dagger=\begin{pmatrix}1&0\\0&-i\end{pmatrix},\qquad
T=\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}.
$$

$S^\dagger|+i\rangle=|+\rangle$です。

回転は次のように定義します。

$$
\begin{aligned}
R_x(\theta)&=\exp\!\left(-\frac{i\theta X}{2}\right),\\
R_y(\theta)&=\exp\!\left(-\frac{i\theta Y}{2}\right),\\
R_z(\theta)&=\exp\!\left(-\frac{i\theta Z}{2}\right).
\end{aligned}
$$

角度の半分と$-i$を落とす誤答が頻出です。

```python
from math import pi
from qiskit import QuantumCircuit

qc = QuantumCircuit(1)
qc.h(0); qc.sdg(0); qc.rx(pi / 3, 0); qc.t(0)
```

<a id="multi-entanglement"></a>
## 複数量子ビット、CX、もつれ

2 qubit state空間はtensor productで、basisは$|00\rangle,|01\rangle,|10\rangle,|11\rangle$です。Qiskit statevectorのindexでは$|q_1q_0\rangle$と読みます。CXはcontrolが1のときだけtargetを$X$で反転します。q0へ$H$を適用した後にcontrol q0、target q1のCXを置くと、次のBell stateを作れます。

$$
\frac{|00\rangle+|11\rangle}{\sqrt{2}}.
$$

各qubit単独では50/50でも、同一basisで測る結果は完全相関します。これは単なる独立な乱数ではありません。

<a id="bit-pauli-order"></a>
## bit/qubit orderingとPauli label

Qiskitでは通常、bit 0は整数のleast-significant bitで、bitstringの**右端**に表示されます。Pauli labelも右端がq0です。したがって`"XZ"`はq1へX、q0へZ。回路図は通常q0が上です。これらは同じ「上下/左右規則」ではありません。

```python
from qiskit.quantum_info import SparsePauliOp
op = SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])
```

これは次のobservableです。各tensor productの左の演算子がq1、右がq0に作用します。

$$
\frac{1}{2}(Z\otimes I)-(X\otimes X).
$$

<a id="expectation"></a>
## observableと期待値

Hermitian operator $A$の期待値は次のとおりです。

$$
\langle A\rangle=\langle\psi|A|\psi\rangle.
$$

eigenstateならeigenvalueがそのまま期待値です。$|++\rangle$は$X\otimes X$の$+1$ eigenstateなので$\langle X\otimes X\rangle=1$。一般には測定結果のeigenvalueを確率で重み付けした平均です。

## 章末チェック

1. $Z|+\rangle$を厳密なketで書いてください。
2. Pauli label `IY`のYはどのqubitですか。
3. control q0=1, target q1=0へCXを作用させた後の$|q_1q_0\rangle$表記は？

答え: 1. $|-\rangle$。2. q0。3. $|11\rangle$。

公式参照: [Qiskit bit-ordering guide](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)、[SparsePauliOp API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp)

[← 学び方](00-guide.md) | [次: 測定と可視化 →](02-visualization-measurement.md)
