# Topic Test 08 — OpenQASM 3

全10問。各問1つ選択してください。

## Questions

### Q1
OpenQASM 3 プログラムの先頭宣言として正しいものはどれか。

A. `OPENQASM 3.0;`  
B. `QASM VERSION 3;`  
C. `OPENQASM = 3.0`  
D. `import qasm3`

### Q2
OpenQASM 3 で2量子ビットを宣言する代表的な構文はどれか。

A. `qubit[2] q;`  
B. `qbit q = 2;`  
C. `quantum[2] q;`  
D. `qubits q(2);`

### Q3
2古典ビットを宣言する代表的な構文はどれか。

A. `bit[2] c;`  
B. `classical[2] c;`  
C. `cbit c(2);`  
D. `measure[2] c;`

### Q4
`qiskit.qasm3.dumps(qc)` の役割はどれか。

A. `QuantumCircuit` を OpenQASM 3 の文字列へexportする  
B. OpenQASM 3文字列を必ず実機で実行する  
C. countsをJSONへ変換する  
D. circuitをPNGにする

### Q5
`qiskit.qasm3.dump(qc, stream)` と `dumps(qc)` の主な違いはどれか。

A. `dump` はstreamへ書き、`dumps` は文字列を返す  
B. `dump` はQASM2、`dumps` はQASM3  
C. `dump` はEstimator専用  
D. 違いはない

### Q6
OpenQASM 3 を Qiskit に import する `loads()` / `load()` について正しいものはどれか。

A. 現在は追加の `qiskit_qasm3_import` package が必要な場合がある  
B. QiskitではOpenQASM 3 importは原理的に禁止  
C. `loads()` はPNGしか読めない  
D. `load()` はSamplerの別名

### Q7
次のOpenQASM 3の意味はどれか。

```qasm
bit c;
qubit q;
h q;
c = measure q;
```

A. Hで重ね合わせを作り、qを測定して結果をcへ格納する  
B. cを量子ビットへ変換する  
C. Hを測定する  
D. qを削除する

### Q8
`include "stdgates.inc";` の役割として最も適切なのはどれか。

A. 標準的なゲート定義を利用可能にする  
B. Python standard libraryを読む  
C. backend calibrationをdownloadする  
D. shot数を指定する

### Q9
OpenQASM 3 が OpenQASM 2 と比べて重視する拡張方向の一つはどれか。

A. richer classical control / dynamic circuit表現  
B. 量子ビットを完全廃止する  
C. Pythonコードそのものに置換する  
D. measurementを禁止する

### Q10
Qiskit の OpenQASM 3 support について適切な姿勢はどれか。

A. import/export機能は発展中なので最新版ドキュメントを確認する  
B. APIは永久に固定されている  
C. QASM3はQiskit v2.xでは使用できない  
D. `dumps()` は常にbinaryを返す

---

# Answers & Explanations

### A1 — A
OpenQASM 3 のversion宣言は `OPENQASM 3.0;`。

### A2 — A
OpenQASM 3 は `qubit[2] q;` のように量子ビット配列を宣言できる。

### A3 — A
classical bit は `bit` 型で宣言する。`bit[2] c;` は2bit配列。

### A4 — A
`qiskit.qasm3.dumps` は circuit をOpenQASM 3 textへserializeし、Python stringとして返す。

### A5 — A
Pythonの一般的な `dump` / `dumps` 命名と同様、前者はstream、後者はstringを主に扱う。

### A6 — A
2026-09時点の公式docsでは、OpenQASM 3 import に `qiskit_qasm3_import` (`qiskit-qasm3-import`) が必要と案内されている。将来統合される可能性があるため最新版確認が重要。

### A7 — A
H後のqは `|+>`。measurement結果0/1をclassical bit cへ代入する。

### A8 — A
`stdgates.inc` は標準ゲート群を定義・利用するためのinclude。

### A9 — A
OpenQASM 3 は古典制御やdynamic circuitの表現力を拡張する方向を持つ。

### A10 — A
IBM/Qiskit自身がOpenQASM 3 interoperabilityを発展中の領域として説明している。資格対策でも古いサンプルの丸暗記より最新版を優先する。
