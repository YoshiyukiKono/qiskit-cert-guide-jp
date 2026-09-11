# 1. 量子状態、行列、基本演算

[← 学び方](00-guide.md) | [次: 測定と可視化 →](02-visualization-measurement.md)

<a id="state-amplitude"></a>
## 状態と複素振幅

1 qubit pure stateは

`|ψ> = α|0> + β|1>`, `α,β ∈ C`, `|α|²+|β|²=1`

です。`α, β`は確率ではなく複素振幅で、computational basis測定の確率が`|α|², |β|²`です。よく使う状態は`|+>=(|0>+|1>)/√2`、`|->=(|0>-|1>)/√2`、`|+i>=(|0>+i|1>)/√2`です。

<a id="matrix-order"></a>
## 行列と演算順序

column vectorへ右から作用するので、`U`の後に`V`なら状態は`VU|ψ>`です。回路図を左から読む時間順と、行列積の右から左への作用を取り違えないでください。

```python
from qiskit.quantum_info import Operator
from qiskit.circuit.library import HGate, XGate, ZGate

assert Operator(HGate()) @ Operator(ZGate()) @ Operator(HGate()) == Operator(XGate())
```

`H=1/√2 [[1,1],[1,-1]]`なので`HZH=X`です。典型的誤答は回路順と積の順を反転することです。

<a id="phase"></a>
## global phaseとrelative phase

`|ψ>`と`e^{iφ}|ψ>`はすべての振幅へ共通因子を掛けたもので、同じphysical state（ray）です。しかしstatevectorや行列の**厳密な等式**では同じとは限りません。relative phaseは成分間の位相差で、干渉結果を変えます。

`Rz(θ)=exp(-iθZ/2)=diag(e^{-iθ/2},e^{iθ/2})`より`Rz(π)=-iZ`。物理作用はZ相当でも厳密な行列は`Z`ではありません。Qiskitの`QuantumCircuit.global_phase`はglobal phaseを表現・保持できます。

判断手順: (1) 「厳密」とあるか、(2) 全成分に同じ因子か、(3) 確率だけか干渉も問うか。

<a id="basic-gates"></a>
## Pauli、Hadamard、位相、回転

`X=[[0,1],[1,0]]`、`Y=[[0,-i],[i,0]]`、`Z=diag(1,-1)`です。したがって`Y|0>=i|1>`、`XZ=-ZX`。`H|0>=|+>`、`H|1>=|->`、逆に`H|+>=|0>`、`H|->=|1>`です。`S=diag(1,i)`、`S†=diag(1,-i)`、`T=diag(1,e^{iπ/4})`。`S†|+i>=|+>`です。

回転は`Rx(θ)=exp(-iθX/2)`、`Ry(θ)=exp(-iθY/2)`、`Rz(θ)=exp(-iθZ/2)`。角度の半分と`-i`を落とす誤答が頻出です。

```python
from math import pi
from qiskit import QuantumCircuit

qc = QuantumCircuit(1)
qc.h(0); qc.sdg(0); qc.rx(pi / 3, 0); qc.t(0)
```

<a id="multi-entanglement"></a>
## 複数量子ビット、CX、もつれ

2 qubit state空間はtensor productで、basisは`|00>,|01>,|10>,|11>`です。Qiskit statevectorのindexでは`|q1 q0>`と読みます。CXはcontrolが1のときだけtargetをXで反転します。`H(q0)`の後に`CX(q0,q1)`を置くとBell state `(|00>+|11>)/√2`を作れます。各qubit単独では50/50でも、同一basisで測る結果は完全相関します。これは単なる独立な乱数ではありません。

<a id="bit-pauli-order"></a>
## bit/qubit orderingとPauli label

Qiskitでは通常、bit 0は整数のleast-significant bitで、bitstringの**右端**に表示されます。Pauli labelも右端がq0です。したがって`"XZ"`はq1へX、q0へZ。回路図は通常q0が上です。これらは同じ「上下/左右規則」ではありません。

```python
from qiskit.quantum_info import SparsePauliOp
op = SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])
```

これは`0.5(Z on q1 ⊗ I on q0) - (X on q1 ⊗ X on q0)`というobservableです。

<a id="expectation"></a>
## observableと期待値

Hermitian operator `A`の期待値は`<A>=<ψ|A|ψ>`。eigenstateならeigenvalueがそのまま期待値です。`|++>`は`XX`の+1 eigenstateなので`<XX>=1`。一般には測定結果のeigenvalueを確率で重み付けした平均です。

## 章末チェック

1. `Z|+>`を厳密なketで書いてください。
2. Pauli label `IY`のYはどのqubitですか。
3. control q0=1, target q1=0へCXを作用させた後の`|q1 q0>`表記は？

答え: 1. `|->`。2. q0。3. `|11>`。

公式参照: [Qiskit bit-ordering guide](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)、[SparsePauliOp API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp)

[← 学び方](00-guide.md) | [次: 測定と可視化 →](02-visualization-measurement.md)
