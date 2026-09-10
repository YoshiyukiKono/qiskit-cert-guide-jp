# Exam Objectives Map

2026-09 時点で IBM が公開している Qiskit v2.X Developer Associate の8主要領域に、本問題集を対応付けたものです。

> 注意: これは公開情報を整理した学習用マップであり、IBM が非公開としている問題配分や採点ロジックを推測したものではありません。

| # | 公開主要領域 | Topic test | 主な練習内容 |
|---|---|---|---|
| 1 | Performing quantum operations | `01-quantum-operations.md` | X/Y/Z/H/S/T, rotation, controlled gates, global/relative phase, inverse |
| 2 | Visualizing quantum circuits, measurements, and states | `02-visualization-measurement-states.md` | `draw`, measurement, Statevector, probabilities, Bloch intuition, bit ordering |
| 3 | Creating quantum circuits | `03-circuit-construction.md` | registers, append/compose, parameters, inverse, control, classical bits |
| 4 | Running quantum circuits | `04-running-circuits.md` | transpilation, target/basis, simulators, backend-oriented execution concepts |
| 5 | Using the sampler primitive | `05-sampler.md` | V2 Sampler, PUB, shots, parameter values, sampled classical outputs |
| 6 | Using the estimator primitive | `06-estimator.md` | V2 Estimator, observables, expectation values, SparsePauliOp, precision |
| 7 | Retrieving and analyzing results | `07-results-analysis.md` | counts/bitstrings, expectation values, probability interpretation, metadata |
| 8 | Operating with OpenQASM 3 | `08-openqasm3.md` | syntax, `OPENQASM 3.0`, `bit`/`qubit`, measurement assignment, dump/dumps/load/loads |

## 学習上の横断テーマ

試験領域は独立ではありません。特に以下は複数領域にまたがります。

### Endianness / bit ordering

Qiskit の表示では、量子ビット番号と文字列の左右関係を取り違えやすいため、回路追跡・測定結果解析の双方で反復します。

### Phase

グローバル位相は単独の測定確率を変えませんが、相対位相はその後の干渉で観測可能になります。Z/S/T と H を組み合わせた問題を多めに配置しています。

### Parameters

parameterized circuit は circuit construction だけでなく Sampler / Estimator の PUB 入力理解にも関係します。

### Transpilation

「回路の数学的意味」と「ターゲットハードウェアで実行可能な命令列への変換」を区別することが重要です。

### Primitive V2

本問題集では V1 より V2 の考え方を優先します。概念として、Sampler は**古典出力のサンプル**、Estimator は**observable の期待値**を得るための primitive と整理します。

## 模擬試験での配分

`mock-01.md` は全8領域を含みます。ただし、問題数配分は学習上のバランスを取るための独自設計であり、IBM 本試験の正確な weighting を表しません。

## 公式情報で必ず再確認する項目

- 試験名・試験コード
- 問題数・試験時間
- 現在の受験ポリシー
- Qiskit の最新 API
- Runtime / IBM Quantum Compute Service の名称や API の更新
- OpenQASM 3 import/export のサポート状況
