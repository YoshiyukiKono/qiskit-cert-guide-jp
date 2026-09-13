# 7. Job、PrimitiveResult、結果分析

[← Estimator V2](06-estimator.md) | [次: OpenQASM 3 →](08-openqasm3.md)

<a id="job-lifecycle"></a>
## jobを取得・監視する

Runtime primitiveの`run()`はjob objectを返します。既知IDの過去jobは`service.job(job_id)`、複数jobの検索・filterは`service.jobs(...)`、状態確認は`job.status()`、結果取得は`job.result()`です。

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
past = service.job(job_id)
status = past.status()
recent = service.jobs(limit=10)
result = past.result()
```

status pollingと結果の統計分析は別Objectiveです。失敗・cancel・queue中に`result()`が常に成功するとは限りません。

<a id="result-hierarchy"></a>
## result階層

構造は次の順です。

```text
PrimitiveResult
├─ metadata（job/result全体、実装依存）
└─ PubResult[i]（入力PUBごとに1つ）
   ├─ metadata（shots, target_precision等、実装依存）
   └─ data: DataBin
      ├─ Sampler: <classical-register-name>: BitArray
      └─ Estimator: evs, stds, ...
```

`result[0]`は最初のPUB結果です。Samplerのfield名は回路のclassical register名に由来し、`measure_all()`の既定が`meas`であるだけです。metadataのkeyは実装・options依存で、常に空でも固定schemaでもありません。

<a id="bitarray-counts"></a>
## BitArrayからcountsを得る

```python
pub_result = result[0]
bit_array = pub_result.data.meas  # register名がmeasの場合
counts = bit_array.get_counts()
```

`get_counts()`は全shotsを数えたdictを返します。`expectation_values(observables)`も対角observableに対する別APIとして存在しますが、counts辞書を返すものではなくobservable引数が必要です。

<a id="empirical-analysis"></a>
## 経験確率と不確かさ

outcome $x$の経験確率は、出現回数$n_x$と総shots数$N$から求めます。

$$
\hat{p}(x)=\frac{n_x}{N}.
$$

1000 shots中240なら0.24です。二項標本の標準誤差の目安は次のとおりです。

$$
\widehat{\mathrm{SE}}=\sqrt{\frac{\hat{p}(1-\hat{p})}{N}}.
$$

$N=1000$、$\hat{p}=0.24$なら約0.0135。有限shotsのcountsをexact probabilityと呼ばないでください。

Estimatorでは`evs`と同shapeの`stds`または別error estimateが返り得ます。値の意味はprimitive implementationとresilience settingの公式説明を確認します。

<a id="metadata"></a>
## metadataを読む

metadataにはshots、target precision、circuit metadata、resilience/execution情報、version等が含まれ得ます。結果の再現性・監査に重要ですが、metadata自体がquantum stateではなく、読むだけでjobが再実行されることもありません。

## 章末チェック

1. 20 PUBsを送ると通常何個のPubResultがありますか。
2. `data.readout`があり`data.meas`がない理由として最初に何を確認しますか。

答え: 1. 20。2. circuitのclassical register名。

公式参照: [Primitive input/output](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output)、[QiskitRuntimeService API](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service)、[BitArray API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray)

[← Estimator V2](06-estimator.md) | [次: OpenQASM 3 →](08-openqasm3.md)
