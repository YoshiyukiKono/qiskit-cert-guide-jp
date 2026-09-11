# 4. Transpile、ISA、IBM Quantum実行方式

[← 回路の構築](03-circuit-construction.md) | [次: Sampler V2 →](05-sampler.md)

<a id="transpile-preset"></a>
## preset pass manager

抽象回路をbackendのbasis gates、coupling、timing等へ適合させるのがtranspileです。標準的なstaged pipelineは次で作ります。

```python
from qiskit.transpiler import generate_preset_pass_manager

# backendを取得済みとする
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
```

`optimization_level`は0〜3。高いほど一般により積極的な探索・最適化を試みますが、特定の回路でdepthやgate countが必ず厳密に改善する保証ではありません。

<a id="isa-layout"></a>
## ISA circuitとlayout

QPU Runtimeへはtarget ISAに適合する回路が必要です。transpileによりvirtual qubitからphysical qubitへのlayoutが定まり、observableも同じ物理配置へ写す必要があります。

```python
from qiskit.quantum_info import SparsePauliOp

observable = SparsePauliOp("ZI")
isa_observable = observable.apply_layout(isa_circuit.layout)
```

Sampler回路にはclassical outputを得る測定が必要です。Estimatorでは通常、observableを別入力にするためterminal measurementを追加しません。「Runtimeならabstract circuitをそのまま受け取る」「常にQASM2へ変換する」は誤りです。

<a id="execution-modes"></a>
## Job / Session / Batch

現行IBM Quantum ComputeのPython execution mode名は三つです。

| mode | 適する仕事 | 注意 |
|---|---|---|
| Job | 単一primitive request | `SamplerV2(mode=backend)`のように指定 |
| Session | 前job結果で次入力を決める反復、専有windowが必要 | 最初のjobは通常queueを通る。plan制約あり |
| Batch | 相互依存のない複数jobs | 同時投入しclassical preprocessingを効率化。専有ではない |

公開Objective中の`dedicated` / `priority`という語を、独立した第4・第5のPython mode名と解釈しません。Sessionのactive windowの専有・優先特性やREST resource上のmode値と、公開APIのJob/Session/Batch分類を区別します。

<a id="backend-selection"></a>
## serviceとbackend選択

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
```

これは条件を満たす比較的空いたbackendを選ぶ代表例です。認証、instance、必要qubit数、feature support、costも実務では条件に加えます。

<a id="runtime-local"></a>
## local primitivesとRuntime primitives

```python
from qiskit.primitives import StatevectorSampler, StatevectorEstimator
from qiskit_ibm_runtime import SamplerV2, EstimatorV2
```

前者はlocal statevector-based V2 reference implementationで、hardware queueやexecution modeを必要としません。後者はIBM Quantum Computeへworkloadを送るclientです。同じV2 PUB/result概念を共有しても、noise、options、job型、metadata、ISA要求は同一ではありません。

<a id="pub-job"></a>
## PUB、run、job

PUB（Primitive Unified Bloc）は1 circuitを核にしたvectorizedな実行単位です。`primitive.run([pub1, pub2])`は通常submitted job objectを返し、完了後`job.result()`で`PrimitiveResult`を得ます。scalar値が`run()`から直接返るわけではありません。

Estimator PUB一般形は`(circuit, observables, parameter_values, precision)`。未parameter化回路でprecisionだけ指定するなら`(qc, observable, None, 0.01)`で、`None`を詰めません。Sampler PUBは次章です。

<a id="broadcasting-preview"></a>
## Estimator broadcasting予告

observable arrayとparameter binding arrayはNumPy-style broadcastingを使います。parameter valuesの最後の軸はcircuit parametersの軸で、broadcast shapeには含めません。たとえば1 parameterでvalues shape `(3,1)`ならbinding shapeは`(3,)`。observables shape `(2,1)`とbroadcastすると結果shapeは`(2,3)`です。

## 章末チェック

1. Sessionは独立jobsを最初から全投入する唯一の選択ですか。
2. circuitをtranspileした後、Estimator observableは常にそのままでよいですか。

答え: 1. いいえ。独立jobsにはBatchが自然です。2. いいえ。layout適用が必要です。

公式参照: [Transpile to ISA circuits](https://quantum.cloud.ibm.com/docs/en/guides/transpile)、[Execution modes](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes)、[Primitive input/output](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output)

[← 回路の構築](03-circuit-construction.md) | [次: Sampler V2 →](05-sampler.md)
