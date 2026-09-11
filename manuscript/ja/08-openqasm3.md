# 8. OpenQASM 3と相互運用

[← jobと結果分析](07-results-analysis.md) | [次: coverage →](coverage.md)

<a id="qasm-types"></a>
## version、量子型、古典型

OpenQASM 3 programはversion宣言から始めます。量子registerは`qubit[2] q;`、classical bit registerは`bit[2] c;`です。`bool`、`int[32]`、`uint[8]`、`float[64]`、`angle[32]`、`complex[float[64]]`等の型があります。width、cast、未初期化値の規則は仕様で確認します。OpenQASM 2の`qreg`/`creg`構文と混ぜません。

```qasm
OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
h q[0];
cx q[0], q[1];
c = measure q;
```

<a id="qasm-semantics"></a>
## programを意味で追う

上例はstandard gateを読み込み、Bell stateを用意し、2 qubitsを測って結果をcへ代入します。`measure`はstatevectorをclassical変数へコピーする操作ではありません。`reset q[0];`はq0を`|0>`へ戻すnon-unitary operationです。

OpenQASM 3にはclassical expressionとcontrol flowがあります。次は測定結果が1ならXを適用します。

```qasm
bit flag;
qubit q;
h q;
flag = measure q;
if (flag == 1) {
  x q;
}
```

<a id="qasm-qiskit-interop"></a>
## Qiskitとのimport/export

```python
from qiskit import QuantumCircuit, qasm3

qc = QuantumCircuit(1)
qc.h(0)
program = qasm3.dumps(qc)  # circuit -> string
round_trip = qasm3.loads(program)  # string -> circuit
```

`dump`/`load`はfile-likeまたはfilename側、`dumps`/`loads`はstring側です。Qiskit 2.5.2でOpenQASM 3 importにはoptional `qiskit-qasm3-import` package（`qiskit[qasm3-import]`）が必要です。import supportはexport可能featureと完全対称とは限らず、annotationやcontrol-flow featureのround tripを検証します。OpenQASM 2は`qiskit.qasm2`という別moduleです。

<a id="qasm-support-boundary"></a>
## 仕様、SDK、QPU、RESTの境界

OpenQASM 3仕様にfeatureがあること、Qiskitがparse/representできること、特定IBM backendが実行できることは別です。IBMのQASM feature tableとbackend targetを確認します。SDKでround tripできてもQPU supportの証明にはなりません。

IBM Quantum Compute REST APIでもEstimator/Sampler primitive workloadをJob / Session / Batchで扱えます。RESTを使うとprimitive概念が消える、Job modeしかない、という理解は誤りです。認証やendpoint payloadはservice API versionに依存するため、hard-code前に現行REST referenceを確認します。

<a id="qasm-version-differences"></a>
## OpenQASM 2と3を見分ける

| 観点 | OpenQASM 2 | OpenQASM 3 |
|---|---|---|
| 宣言 | `OPENQASM 2.0;` | `OPENQASM 3.0;` |
| register | `qreg q[2]; creg c[2];` | `qubit[2] q; bit[2] c;` |
| 測定 | `measure q -> c;` | `c = measure q;`も使用 |
| 古典処理 | 限定的 | 型、式、control flowを拡張 |

## 章末チェック

1. `dumps`と`loads`の方向は？
2. OpenQASM 3仕様にあるloopは全QPUで必ず実行できますか。

答え: 1. circuit→string、string→circuit。2. いいえ。SDKとbackend/service supportを別確認します。

公式参照: [OpenQASM 3仕様](https://openqasm.com/versions/3.0/)、[Qiskitとの相互運用](https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3)、[QASM feature table](https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table)、[REST execution modes](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api)

[← jobと結果分析](07-results-analysis.md) | [次: coverage →](coverage.md)
