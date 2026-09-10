# Topic Test 08 — OpenQASM 3

全10問。syntaxだけでなくclassical types、control flow、Qiskit interoperability、IBM Quantum Compute REST executionまで扱います。

## Questions

### Q1
OpenQASM 3で3量子ビットと3古典ビットを宣言する組み合わせとして正しいものはどれか。

A. `qbit[3] q; cbit[3] c;`  
B. `qubit[3] q; bit[3] c;`  
C. `quantum[3] q; classical[3] c;`  
D. `qubits q(3); bits c(3);`

### Q2
OpenQASM 3のclassical typeとして実際に存在する組み合わせはどれか。

A. `string`, `object`, `complex`だけ  
B. `qubit`だけがclassical typeでもある  
C. `bit`, `int`, `uint`, `float`, `angle`など  
D. Pythonの`list`, `dict`, `tuple`をそのまま使う

### Q3
次の完全なOpenQASM 3 programの意味として最も適切なのはどれか。

```qasm
OPENQASM 3.0;
include "stdgates.inc";
bit c;
qubit q;
reset q;
h q;
c = measure q;
```

A. `c`を量子状態へ変換してからHを作用させる  
B. qをゼロ初期化してからHで`|+>`を準備し、その後の測定結果をclassical bit cへ格納する  
C. qを測定せずstatevectorをcへ代入する  
D. H gateの定義をcへ保存する

### Q4
OpenQASM 3の`if`文について最も適切な説明はどれか。

A. measurement等で得たclassical dataに応じたcontrol flowを表現できる  
B. quantum statevectorそのものをPython objectとして比較する構文である  
C. OpenQASM 3ではclassical controlは廃止された  
D. `if`はQiskitの描画専用annotationである

### Q5
`include "stdgates.inc";` の役割として最も適切なのはどれか。

A. IBM account credentialsを読む  
B. Python standard libraryをimportする  
C. standard gate definitionsを利用可能にする  
D. shotsの既定値を指定する

### Q6
Qiskit circuitをOpenQASM 3 textへexportするAPIについて正しいものはどれか。

A. `loads(qc)`がstringを返し、`load(qc)`がstreamへ書く  
B. `dump(qc, stream)`はstreamへ書き、`dumps(qc)`はstringを返す  
C. `QuantumCircuit.qasm()`だけがOpenQASM 3 exporterである  
D. OpenQASM 3 exportには`qiskit-qasm3-import`が必須である

### Q7
OpenQASM 3 programをQiskitへimportする`load()` / `loads()`について正しいものはどれか。

A. `load()`はstringだけを受け、`loads()`はbackendを受ける  
B. importはQiskit 2.xでは完全に削除された  
C. import機能は成熟済みでAPI変更の可能性はない  
D. current docsでは`qiskit-qasm3-import` optional packageが必要で、機能はexploratoryとされている

### Q8
QiskitのOpenQASM 2とOpenQASM 3 APIについて正しいものはどれか。

A. `qiskit.qasm2`と`qiskit.qasm3`は別moduleであり、version-specific syntax/supportを区別する  
B. QASM2 sourceは文字列の先頭だけ3.0へ書き換えれば常にQASM3として等価  
C. `qiskit.qasm3.dumps`はOpenQASM 2 textを生成する  
D. QASM2とQASM3にはclassical-control機能上の差がない

### Q9
OpenQASM 3 feature supportについて最も安全な理解はどれか。

A. OpenQASM 3 specificationにある全featureはIBM QPUで必ずそのまま実行できる  
B. Qiskitでparse/represent/exportできる範囲とIBM Quantum Computeで実行可能な範囲は同一とは限らない  
C. QiskitでparseできなければOpenQASM 3 specificationにも存在しない  
D. hardware supportはOpenQASM versionと無関係なので確認不要

### Q10
IBM Quantum Compute ServiceのREST APIとOpenQASM/primitive executionについて正しいものはどれか。

A. REST APIではjob modeしか存在しない  
B. REST APIはOpenQASM 2 sourceしか受け付けない  
C. REST API経由でもprimitive workloadをjob / session / batchのexecution modesで扱える  
D. REST APIを使う場合Sampler/Estimatorというprimitive conceptはなくなる

---

# Answers & Explanations

### A1 — B
- A/C/D: OpenQASM 3のtype/declaration syntaxではない。
- B: 正解。`qubit[n]`はquantum bits、`bit[n]`はclassical bits。

### A2 — C
- A: `complex`自体はOpenQASM 3に存在する。ただし`string`や`object`をこのような標準型として列挙し、これら「だけ」とする説明は誤り。
- B: `qubit`はquantum typeでclassical typeではない。
- C: 正解。OpenQASM 3には`bit`, `int`, `uint`, `float`, `angle`等のclassical typesがある。
- D: Pythonのcontainer typeをそのままOpenQASMの型として使うことはできない。

### A3 — B
- A: `c`はclassical bitでquantum stateへ変換しない。
- B: 正解。`reset q`で`|0>`を準備し、`stdgates.inc`のHで測定直前の状態を`|+>`にする。その後、測定結果をcへ代入する。
- C: measurementを実行している。
- D: gate definitionをclassical bitへ保存するコードではない。

OpenQASM 3.0仕様ではqubitの初期状態は未定義であり、`qubit q;`だけではゼロ初期化を保証しない。この例の`reset`はその前提を明示するための操作である。測定後も`|+>`のままと述べているわけではない。

### A4 — A
- A: 正解。OpenQASM 3はclassical control/dynamic-circuit semanticsを表現できる。
- B: statevector objectを直接比較するPython構文ではない。
- C/D: OpenQASM 3のcontrol-flowの位置付けと異なる。

### A5 — C
- A/B/D: include fileの目的ではない。
- C: 正解。standard gatesを定義するlibrary include。

### A6 — B
- A: import/export方向が逆。
- B: 正解。`dump`はfile-like stream、`dumps`はPython string。
- C: current OpenQASM 3 high-level exporterは`qiskit.qasm3.dump/dumps`。
- D: optional import packageはOpenQASM 3からQiskitへimportする側で必要。

### A7 — D
- A: `load(filename)`と`loads(program_string)`。
- B: current Qiskit 2.xで利用できる。
- C: IBM docsはexploratoryで変更があり得ると明記している。
- D: 正解。

### A8 — A
- A: 正解。version-specific moduleとsemanticsを区別する。
- B: version declarationだけを換えて意味を保証できない。
- C: `qiskit.qasm3.dumps`はOpenQASM 3を出力する。
- D: OpenQASM 3はより豊かなclassical computation/controlを持つ。

### A9 — B
- A: specification supportとQPU executable supportは同一ではない。
- B: 正解。IBMはfeature tableでparse/representation/export/hardware supportを分けて示している。
- C: Qiskit importerの実装範囲はlanguage specificationそのものではない。
- D: hardware supportは必ずcurrent documentationを確認する。

### A10 — C
- A: REST APIにもjob/session/batchがある。
- B: current REST primitive workflowではOpenQASM 3を含むprimitive payload例がある。
- C: 正解。
- D: REST APIでもEstimator/Sampler primitive workloadとして送信する。

## Official references

- OpenQASM 3 + Qiskit: https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3
- QASM feature table: https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table
- REST execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api
- OpenQASM types and initial state: https://openqasm.com/versions/3.0/language/types.html
- OpenQASM reset: https://openqasm.com/versions/3.0/language/insts.html
