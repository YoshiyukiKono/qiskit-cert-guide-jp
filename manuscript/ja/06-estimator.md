# 6. Estimator V2

[← Sampler V2](05-sampler.md) | [次: jobと結果分析 →](07-results-analysis.md)

<a id="estimator-purpose"></a>
## 期待値を評価する

Estimatorはcircuitが用意する状態とobservableから期待値$\langle\psi|O|\psi\rangle$を評価します。bitstring sampleを主出力にするSamplerとは目的が違います。

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(1)
qc.h(0)
obs = SparsePauliOp("Z")
result = StatevectorEstimator().run([(qc, obs)]).result()
assert abs(float(result[0].data.evs)) < 1e-12
```

$|+\rangle$を$Z$で測るeigenvalueは$+1$と$-1$が等確率なので$\langle Z\rangle=0$。$\langle X\rangle=1$との取り違えに注意します。QPU用classは`qiskit_ibm_runtime.EstimatorV2`です。

<a id="estimator-pub"></a>
## Estimator PUB

一般形は`(circuit, observables, optional parameter_values, optional precision)`です。observableは`str`、`Pauli`、`SparsePauliOp`等で表せます。同じcircuitのcommuting observablesを同じ測定groupとして扱いたい場合は同じPUB内にまとめます。QPU用ではcircuit layoutをobservableにも適用します。

<a id="estimator-broadcasting"></a>
## broadcastingをshapeで読む

observables arrayとparameter binding arrayはNumPy-styleで右端から比較し、dimensionが同じか一方が1ならcompatibleです。parameter valuesの最終軸はcircuit parameter数であり、binding shapeから除外されます。

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

theta = Parameter("θ")
pqc = QuantumCircuit(1)
pqc.ry(theta, 0)
observables = np.array([["Z"], ["X"]], dtype=object)  # shape (2, 1)
values = np.array([[0.0], [1.0], [2.0]])              # binding shape (3,)
pub = (pqc, observables, values)                       # result shape (2, 3)
```

判断手順: (1) circuit parameters数を数える、(2) valuesの最後の軸をparameter軸として外す、(3) observable shapeと右からbroadcastする。

<a id="estimator-options"></a>
## precision、shots、resilience

Estimatorはtarget precisionをPUBまたは`run(..., precision=...)`で指定できます。Runtime implementationには`default_precision`や`default_shots`もありますが、precisionとshotsは同義ではありません。

2026-09-12確認時、Runtime Estimatorの`resilience_level`は0, 1, 2です。概略は0=no mitigation、1=readout errorへの低cost mitigation、2=level 1にZNE等を加えるpresetです。ただしserver defaultや手法は変化し得ます。

```python
from qiskit_ibm_runtime import EstimatorV2

estimator = EstimatorV2(mode=backend)
estimator.options.resilience_level = 0
estimator.options.resilience.zne_mitigation = True
```

個別optionはpresetを上書き/追加できます。この例ではlevel 0だけ見て「ZNEは無効」と断定できません。mitigationはbias低減を狙いますが、計算costが増え、真値を保証しません。DDは主にsuppression、ZNE/TREX等はmitigationという役割の違いも押さえます。

<a id="estimator-result"></a>
## Estimator result

`PrimitiveResult`の各`PubResult.data.evs`に期待値arrayが入ります。実装・optionsにより`data.stds`や`ensemble_standard_error`等のuncertainty情報が加わります。`stds`をsampled bitstringsと解釈しません。

## 章末チェック

1. `values.shape==(5,2)`でcircuit parametersが2個ならbinding shapeは？
2. `resilience_level=0`なら個別ZNE指定を無視してよいですか。

答え: 1. `(5,)`。2. いいえ。最終的な個別optionsを確認します。

公式参照: [Estimator input/output](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output)、[Estimator options](https://quantum.cloud.ibm.com/docs/en/guides/estimator-options)、[noise management](https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management)

[← Sampler V2](05-sampler.md) | [次: jobと結果分析 →](07-results-analysis.md)
