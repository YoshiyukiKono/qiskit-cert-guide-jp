# 5. Sampler V2

[← transpile・実行](04-transpile-execution.md) | [次: Estimator V2 →](06-estimator.md)

<a id="sampler-purpose"></a>
## 何を計算するか

Samplerはcircuitのclassical output registerをshotsごとにsampleします。出力はexact spectrumやstatevectorではなく、有限標本のbit dataです。測定を含むcircuitが必要です。

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0); qc.cx(0, 1); qc.measure_all()
sampler = StatevectorSampler(seed=7)
result = sampler.run([qc], shots=256).result()
counts = result[0].data.meas.get_counts()
```

local `StatevectorSampler`は理想statevectorに基づく参照実装です。QPU用は`from qiskit_ibm_runtime import SamplerV2`で、ISA circuitとbackend/modeを使います。

<a id="sampler-pub"></a>
## Sampler PUBとshots優先順位

一般形は`(circuit, optional parameter_values, optional shots)`。shotsだけPUB指定するなら`(qc, None, 128)`で、`(qc, 128)`と前詰めしません。

Runtime Samplerでは概念上、PUB-specific shotsが最優先、次に`run(..., shots=...)`、その次に`options.default_shots`です。run-level shotsはそのrunだけ、PUB値がないPUBへ適用されます。

```python
sampler.options.default_shots = 500
job = sampler.run([isa_circuit], shots=128)
```

<a id="sampler-result-registers"></a>
## result fieldはregister名から来る

`measure_all()`の既定register名は`meas`なので`result[0].data.meas`になります。しかし、自分で`ClassicalRegister(2, "readout")`を作ればfieldは`data.readout`です。`meas`を全Sampler結果の固定field名と暗記しないでください。複数registerならDataBinに複数fieldがあり得ます。

<a id="sampler-options"></a>
## Runtime optionsとdynamical decoupling

```python
from qiskit_ibm_runtime import SamplerV2

runtime_sampler = SamplerV2(mode=backend)
runtime_sampler.options.dynamical_decoupling.enable = True
runtime_sampler.options.dynamical_decoupling.sequence_type = "XY4"
```

DDはidle periodへpulse sequenceを挿入し、decoherence等の影響を抑えるerror suppressionです。coupling mapを変えたり、countsを期待値へ変換したりしません。追加gate、duration、hardware supportとのtrade-offがあります。

<a id="sampler-compatibility"></a>
## feature compatibilityは都度確認する

2026-09-12に確認したIBM Sampler optionsガイドのcompatibility表では、dynamic circuitsとdynamical decouplingは同一jobでincompatibleとされています。一方、別項目の「fractional gatesはruntime 0.42.0以降dynamic circuitsとcompatible」をDDの説明と読み違えないでください。これはversion-sensitiveで、backend capabilityと最新表を実行直前に確認します。

## 典型的な誤答

- `StatevectorSampler`をQPU service classと考える。
- Sampler PUBへobservableを入れる（Estimatorとの混同）。
- `precision`をSampler `run()`のshots指定に使う。
- `data.meas`をregister名と無関係な固定schemaと考える。

## 章末チェック

1. `(qc, 128)`は「shots=128」のPUBですか。
2. `data.meas`が無いとSampler失敗と断定できますか。

答え: 1. いいえ。第2要素はparameter valuesです。2. できません。classical register名を確認します。

公式参照: [Sampler input/output](https://quantum.cloud.ibm.com/docs/en/guides/sampler-input-output)、[Sampler optionsとcompatibility表](https://quantum.cloud.ibm.com/docs/en/guides/sampler-options)

[← transpile・実行](04-transpile-execution.md) | [次: Estimator V2 →](06-estimator.md)
