# Topic Test 03 — Circuit Construction

全10問。basic / parameterized / dynamic circuitsとtranspilationを横断します。

## Questions

### Q1
2量子ビット・2古典ビットの回路を作る最も直接的なコードはどれか。

A. `QuantumCircuit(4)`  
B. `QuantumCircuit(2, 2)`  
C. `QuantumCircuit("2,2")`  
D. `QuantumCircuit(2).measure_all(2)`

### Q2
q0の測定結果をc1へ格納する呼び出しはどれか。

A. `qc.measure(1, 0)`  
B. `qc.measure_all(0, 1)`  
C. `qc.measure(0, 1)`  
D. `qc.read(0, 1)`

### Q3
`new_qc = qc.compose(other)` について正しい説明はどれか。

A. defaultでは合成した新しい回路を返し、`qc`自体をin-place変更しない  
B. defaultで`qc`を必ずin-place変更し、戻り値はない  
C. `compose`はmeasurement resultだけを結合する  
D. `compose`はQiskit v2.xでは削除されている

### Q4
parameterized rotationを作る代表的な組み合わせはどれか。

A. `theta = Target("theta"); qc.ry(theta, 0)`  
B. `theta = Parameter("theta"); qc.ry(theta, 0)`  
C. `theta = SamplerV2("theta"); qc.ry(theta, 0)`  
D. `theta = ClassicalRegister("theta"); qc.ry(theta, 0)`

### Q5
parameterized circuitを事前に数値へ束縛する代表的なAPIはどれか。

A. `draw_parameters`  
B. `measure_parameters`  
C. `bind_runtime`  
D. `assign_parameters`

### Q6
X gateからcontrolled-X相当のgateを構成する考え方として適切なのはどれか。

A. gateの`control()`を使う  
B. gateの`measure()`を使う  
C. classical registerへcastする  
D. `reverse_bits()`を使う

### Q7
次のコードの中心的な意味はどれか。

```python
qc.h(q0)
qc.measure(q0, c0)
with qc.if_test((c0, 1)):
    qc.x(q1)
```

A. q1を常にXするstatic circuit  
B. q0を測定した後、q0の量子状態そのものをif文で直接比較する  
C. q0の測定結果が1のときだけq1へXを適用するclassical feedforward  
D. q0とq1をSWAPする

### Q8
Qiskit SDKのdynamic-circuit/control-flow supportについて正しいものはどれか。

A. SDKは`if_test`しか表現できない  
B. SDKは`if_test`, `switch`, `for_loop`, `while_loop`等を表現できるが、実QPUで利用可能な機能はbackend/service側のsupportも確認する  
C. dynamic circuitではmid-circuit measurementを使えない  
D. dynamic circuitはSampler/Estimatorと無関係なので実行できない

### Q9
backend向けの標準的なstaged transpilation pipelineを作る代表的な方法はどれか。

A. `Statevector.from_instruction(backend)`  
B. `qc.draw(backend)`  
C. `SamplerV2(optimization_level=3)`  
D. `generate_preset_pass_manager(optimization_level=..., backend=backend)`

### Q10
IBM QPUへRuntime primitiveで送る回路について最も適切なのはどれか。

A. backendのISAへtranspileした回路を用意する  
B. abstract circuitならbackendに関係なく必ずそのまま受理される  
C. coupling mapを無視するためtranspilationを禁止する  
D. circuitをOpenQASM 2へ変換しなければならない

---

# Answers & Explanations

### A1 — B
- A: `QuantumCircuit(4)`は4 quantum bits、classical bitsなし。
- B: 正解。2 qubits + 2 clbits。
- C: constructorの有効な指定ではない。
- D: `measure_all`の呼び方・意味が異なる。

### A2 — C
`measure(qubit, clbit)`の順。
- A: q1→c0になる。
- B: `measure_all()`は個別mapping指定用ではない。
- C: 正解。
- D: `read`という対応APIではない。

### A3 — A
- A: 正解。default `inplace=False`では新しい回路を返す。
- B: in-place更新したい場合は`inplace=True`。
- C: circuit operations全般を合成する。
- D: 現行APIで利用できる。

### A4 — B
- A/C/D: symbolic circuit parameterを作るクラスではない。
- B: 正解。`qiskit.circuit.Parameter`をgate parameterへ使える。

### A5 — D
- A/B/C: 該当する標準APIではない。
- D: 正解。`assign_parameters`で数値や別Parameterへ置換できる。V2 Primitiveへ未束縛回路とparameter valuesを渡す方法も別途ある。

### A6 — A
- A: 正解。Gate/Instructionのcontrolled versionを構成できる。
- B/C/D: controlled gate生成の方法ではない。

### A7 — C
- A: Xは条件付き。
- B: 条件はmeasurementで得たclassical bit `c0`。
- C: 正解。mid-circuit measurement + classical feedforwardの例。
- D: SWAPではない。

### A8 — B
- A: SDKには複数のcontrol-flow constructがある。
- B: 正解。SDK representationとhardware execution supportは区別する。
- C: mid-circuit measurementはdynamic circuitsの中心的要素。
- D: IBM Quantum Computeでdynamic-circuit execution supportがあるがfeature compatibilityを確認する。

### A9 — D
- A/B/C: transpilation pass manager生成ではない。
- D: 正解。preset staged pass managerを作り`run(circuit)`するのが推奨workflow。

### A10 — A
- A: 正解。IBM Quantum primitives workflowではtarget backendのISA/layoutへ合わせる。
- B: local reference primitiveとRuntime/QPU workflowを混同している。
- C: connectivityとinstruction supportを満たすためtranspilationが必要。
- D: OpenQASM 2への変換は要件ではない。

## Official references

- Construct circuits: https://quantum.cloud.ibm.com/docs/en/guides/construct-circuits
- Dynamic circuits: https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
- Transpile with pass managers: https://quantum.cloud.ibm.com/docs/en/guides/transpile-with-pass-managers
- IBM Quantum ISA boundary: https://quantum.cloud.ibm.com/docs/en/guides/simulate-with-qiskit-sdk-primitives
