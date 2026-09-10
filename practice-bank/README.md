# Qiskit v2.X Practice Bank

IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate (C1000-179) 向けの、公開Exam Objectives準拠を目標とするオリジナル演習セットです。

既存の `exams/` は変更せず、`practice-bank/` だけで完結します。

## この問題集の基準

2026-09-10時点の以下を優先して作成・検証します。

1. IBMの現行certification / Study Guideで公開されているExam Objectives
2. IBM Quantum Documentationの現行Qiskit SDK / IBM Quantum Compute (Qiskit Runtime) API
3. OpenQASM 3の現行仕様とIBM Quantumのinterop documentation
4. 本リポジトリの解説

本問題集と公式情報が食い違う場合は公式情報を優先してください。

## 試験形式

IBM公開情報ではC1000-179は次の形式です。

- 68 questions
- 90 minutes
- 47 correct answers to pass
- English exam

本問題集は実試験問題、dump、受験者から得た非公開問題の再現ではありません。

## 公開領域とweight

| Domain | Weight | Mock 01 |
|---|---:|---:|
| Performing quantum operations | 16% | 11 |
| Visualizing quantum circuits, measurements, and states | 11% | 8 |
| Creating quantum circuits | 18% | 12 |
| Running quantum circuits | 15% | 10 |
| Using the sampler primitive | 12% | 8 |
| Using the estimator primitive | 12% | 8 |
| Retrieving and analyzing results | 10% | 7 |
| Operating with OpenQASM | 6% | 4 |

合計68問です。整数化のため公開weightとの完全一致ではありませんが、各領域の比率を近似しています。

## Local primitives と IBM Quantum Compute primitives

V2 Primitivesには、用途の異なる実装があります。本問題集では混同しません。

- `qiskit.primitives.StatevectorSampler` / `StatevectorEstimator`: ローカルのstatevector-based V2 reference implementations
- `qiskit_ibm_runtime.SamplerV2` / `EstimatorV2`: IBM Quantum Compute ServiceでQPU等へworkloadを送るV2 primitives

資格対策では両方を扱いますが、Runtime側についてはexecution mode、ISA circuit、PUB、options、job/result lifecycleまで含めます。

## 構成

```text
practice-bank/
├── README.md
├── exam-objectives-map.md
├── topic-tests/
│   ├── 01-quantum-operations.md
│   ├── 02-visualization-measurement-states.md
│   ├── 03-circuit-construction.md
│   ├── 04-running-circuits.md
│   ├── 05-sampler.md
│   ├── 06-estimator.md
│   ├── 07-results-analysis.md
│   └── 08-openqasm3.md
├── mock-exams/
│   └── mock-01.md
├── answers/
│   └── mock-exams/
│       └── mock-01-answers.md
└── validation/
    ├── notes.md
    ├── smoke_checks.py
    └── validate_bank.py
```

## 推奨利用順序

1. `exam-objectives-map.md` でTask-level coverageを確認する
2. topic testsを解く
3. 正解だけでなく各distractorの解説を読む
4. API依存問題は公式documentationとコードで再確認する
5. `mock-exams/mock-01.md` を90分・資料なしで解く
6. `answers/mock-exams/mock-01-answers.md` で採点・復習する
7. `python practice-bank/validation/validate_bank.py` で構造上の整合性を確認する

## Topic tests

各ファイル10問、合計80問です。各領域の公開Taskを横断し、単純暗記だけでなくコード読解・概念の区別・version-sensitive APIを扱います。

## Mock exam

`mock-01.md` は68問です。公開weightに近い領域配分を使い、正答位置はA/B/C/Dを各17問にしています。配置は規則的な繰り返しにはしていません。

## 解説方針

各問について次を説明します。

- 正答の理由
- 各誤答がなぜ不適切か
- version-sensitiveな場合の注意点
- 必要に応じて数式・コードによる検算ポイント

## 重要なversion-sensitive領域

次は特に最新版公式documentationを再確認してください。

- IBM Quantum Compute execution modes (job / session / batch)
- `SamplerV2` / `EstimatorV2` options
- resilience / dynamical decoupling / twirling等のnoise-management options
- `RuntimeJobV2` とjob retrieval / status
- dynamic circuitsのhardware support
- OpenQASM 3 import/exportおよび実行可能featureの範囲

## 公式参照

- IBM certification announcement: https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- Qiskit documentation: https://quantum.cloud.ibm.com/docs/
- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- SamplerV2: https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/sampler-v2
- EstimatorV2: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/estimator-v2
- Dynamic circuits: https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
- OpenQASM 3 interoperability: https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3
