# 3. QuantumCircuitの構築

[← 測定と可視化](02-visualization-measurement.md) | [次: transpile・実行 →](04-transpile-execution.md)

<a id="construct-registers"></a>
## qubitとclassical bitを作る

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

qc = QuantumCircuit(2, 2)  # 2 qubits, 2 clbits
q = QuantumRegister(2, "q")
c = ClassicalRegister(2, "readout")
named = QuantumCircuit(q, c)
```

qubit数とclbit数は別です。`QuantumCircuit(4)`は4 qubitsであり「2+2」ではありません。register名はSampler結果のfield名にも関係します。

<a id="measure-mapping"></a>
## 測定mapping

`measure(qubit, clbit)`の順です。q0の結果をc1へ格納するなら`qc.measure(0,1)`。`measure_all()`は全qubitを測る便利関数で、既定では`meas`というclassical registerを追加します。bitstringを読むときはこのmappingを確認します。

<a id="compose-control"></a>
## compose、append、inverse、control

`new_qc = qc.compose(other)`は既定で新しい回路を返し、`qc`を変更しません。変更したい場合は`inplace=True`。位置対応が必要なら`qubits=`/`clbits=`を明示します。`append(instruction, qargs, cargs)`は命令を特定wireへ追加し、unitaryなgate/circuitは`inverse()`で逆演算を作れます。

```python
from qiskit.circuit.library import XGate

cx_gate = XGate().control(1)
qc2 = QuantumCircuit(2)
qc2.append(cx_gate, [0, 1])
```

`Gate.control()`はcontrolled gateを作りますが、測定を含む任意の`Instruction`すべてに一般化できるわけではありません。

<a id="parameters"></a>
## parameterized circuit

```python
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

theta = Parameter("θ")
pqc = QuantumCircuit(1)
pqc.ry(theta, 0)
bound = pqc.assign_parameters({theta: 0.25})
assert len(pqc.parameters) == 1 and len(bound.parameters) == 0
```

parameterは回路構造を再利用し、値だけを変えるためのsymbolです。`assign_parameters`は数値または別Parameterへ置換します。sequenceで値を渡す場合の順序を思い込みで決めず、`circuit.parameters`または辞書bindingを使います。Primitiveへ未bound回路とparameter arrayを渡す方法は後章で扱います。

<a id="dynamic-circuits"></a>
## dynamic circuitとclassical feedforward

dynamic circuitはmid-circuit measurementと、その結果に基づく同一circuit内のcontrol flowを含み得ます。

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

q = QuantumRegister(2, "q")
c = ClassicalRegister(1, "flag")
dynamic = QuantumCircuit(q, c)
dynamic.h(q[0])
dynamic.measure(q[0], c[0])
with dynamic.if_test((c[0], 1)):
    dynamic.x(q[1])
```

Pythonの`if`が量子測定をsubmission前に評価するのではありません。`if_test`、`switch`、loopなどのcontrol-flow operationを回路へ記録します。parameter sweepやshots変更だけはdynamic circuitの定義になりません。

<a id="sdk-hardware-boundary"></a>
## SDK表現とhardware supportの境界

Qiskit SDKがcontrol flowを表現できても、全backend/serviceが全constructを実行できるとは限りません。backend target、dynamic-circuitガイド、feature compatibilityを確認します。transpileが意味を保って変換できるか、Runtime optionと互換かも別問題です。

## 章末チェック

1. `compose`の戻り値を捨てると、既定では元回路に合成されますか。
2. `with qc.if_test(...)`内の操作はいつ条件評価されますか。

答え: 1. されません。`inplace=True`または戻り値を使います。2. circuit execution中です。

公式参照: [Classical feedforward and control flow](https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow)、[QuantumCircuit API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit)

[← 測定と可視化](02-visualization-measurement.md) | [次: transpile・実行 →](04-transpile-execution.md)
