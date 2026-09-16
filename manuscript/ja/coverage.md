# Objectives・Mock 01 coverage

[← 補章A](09-algorithm-worked-examples.md) | [入口](README.md)

この表は、公開試験レコードの8領域・21 Objectives（公開順に付けた参照用ID）を本書へ対応させたものです。日本語の要約と補足範囲は教材側の解釈です。

<a id="objectives-coverage"></a>
## 21 Objectives

| Domain / Objective | 公開Objectiveの要約 | 正本の主な節 | Mock 01 |
|---|---|---|---|
| 1.1 | Pauli operatorsを定義 | [Pauli label](01-quantum-operations.md#bit-pauli-order) | Q7–Q8 |
| 1.2 | quantum operationsを適用 | [基本gate](01-quantum-operations.md#basic-gates)、[phase](01-quantum-operations.md#phase)、[複数量子bit](01-quantum-operations.md#multi-entanglement) | Q1–Q6, Q9–Q11 |
| 2.1 | circuitを可視化 | [回路描画](02-visualization-measurement.md#circuit-drawing) | Q12 |
| 2.2 | measurementを可視化 | [分布plot](02-visualization-measurement.md#measurement-plots)、[bitstring](02-visualization-measurement.md#bitstrings-counts) | Q13–Q14, Q17, Q19 |
| 2.3 | stateを可視化 | [state plot](02-visualization-measurement.md#state-plots)、[Statevector](02-visualization-measurement.md#statevector) | Q15–Q16, Q18 |
| 3.1 | dynamic circuitsを構築 | [dynamic circuit](03-circuit-construction.md#dynamic-circuits)、[support境界](03-circuit-construction.md#sdk-hardware-boundary) | Q26–Q28 |
| 3.2 | parameterized circuitsを構築 | [parameters](03-circuit-construction.md#parameters) | Q23–Q24 |
| 3.3 | transpile・optimize | [preset](04-transpile-execution.md#transpile-preset)、[ISA/layout](04-transpile-execution.md#isa-layout) | Q29–Q31 |
| 3.4 | basic circuitsを構築 | [constructor](03-circuit-construction.md#construct-registers)、[測定](03-circuit-construction.md#measure-mapping)、[合成](03-circuit-construction.md#compose-control) | Q20–Q22, Q25 |
| 4.1 | execution modesを理解 | [Job/Session/Batch](04-transpile-execution.md#execution-modes)、[backend](04-transpile-execution.md#backend-selection) | Q32–Q36 |
| 4.2 | Runtime primitives、hardware、broadcasting | [local/Runtime](04-transpile-execution.md#runtime-local)、[PUB/job](04-transpile-execution.md#pub-job)、[broadcasting](04-transpile-execution.md#broadcasting-preview) | Q37–Q41 |
| 5.1 | DD等Sampler optionsを設定 | [Sampler options](05-sampler.md#sampler-options)、[compatibility](05-sampler.md#sampler-compatibility) | Q46–Q49 |
| 5.2 | Samplerの理論背景 | [目的](05-sampler.md#sampler-purpose)、[PUB](05-sampler.md#sampler-pub) | Q42–Q45 |
| 6.1 | resilience等Estimator optionsを設定 | [Estimator options](06-estimator.md#estimator-options) | Q55–Q56 |
| 6.2 | Estimatorの理論背景 | [期待値](06-estimator.md#estimator-purpose)、[PUB](06-estimator.md#estimator-pub)、[broadcasting](06-estimator.md#estimator-broadcasting) | Q50–Q54, Q57 |
| 7.1 | 過去experiment resultsを取得 | [job lifecycle](07-results-analysis.md#job-lifecycle)、[階層](07-results-analysis.md#result-hierarchy)、[BitArray](07-results-analysis.md#bitarray-counts) | Q58–Q59, Q61–Q64 |
| 7.2 | jobsをmonitor | [job lifecycle](07-results-analysis.md#job-lifecycle) | Q60 |
| 8.1 | OpenQASM 3 typesを構成 | [型](08-openqasm3.md#qasm-types) | Q65 |
| 8.2 | semanticsを解釈 | [意味を追う](08-openqasm3.md#qasm-semantics) | Q66 |
| 8.3 | QASM versionsとQiskitを相互利用 | [interop](08-openqasm3.md#qasm-qiskit-interop)、[version差](08-openqasm3.md#qasm-version-differences) | Q67 |
| 8.4 | Runtime REST APIを利用 | [support / REST境界](08-openqasm3.md#qasm-support-boundary) | Q68 |

<a id="algorithm-supplement-coverage"></a>
## 補章Aによる学習上の補足

次は、既存Objectivesの理解を深めるための総合例との対応であり、公式Objectivesやweightの追加ではありません。題材にしたアルゴリズム名の出題頻度を示す表でもありません。

| 総合例 | 関連する既存Objective | 学習上の補足 |
|---|---|---|
| [Deutschと位相キックバック](09-algorithm-worked-examples.md#algorithm-deutsch) | 1.2、3.4、5.2 | 制御ゲート・固有状態・相対位相・干渉から、関数の性質を測定で判定する |
| [2量子ビットGrover](09-algorithm-worked-examples.md#algorithm-grover) | 1.2、3.4、5.2 | オラクルと拡散の合成、振幅と確率、ビット順、回路内反復とshotsを区別する |
| [1量子ビットVQE](09-algorithm-worked-examples.md#algorithm-vqe) | 1.1、3.2、4.2、6.2 | ハミルトニアン、候補回路、PUBの角度配列、期待値と古典側の最適化をつなぐ |

VQE例はローカルのEstimatorを使い、4.2に含まれる実機実行まで検証した例ではありません。実行先への変換、Runtime options、誤差への対処は引き続き本編を参照します。

<a id="mock-coverage"></a>
## Q1〜Q68の受け皿

各問題の詳細解説には、章トップではなく以下の節粒度で「正本で深掘り」リンクを置いています。

| Questions | 主題 | 節 |
|---|---|---|
| Q1 | Hによる共役 | [ゲートの合成と基底変換](01-quantum-operations.md#matrix-order) |
| Q2–Q5 | 回転、厳密等式、phase、S† | [phase](01-quantum-operations.md#phase)、[基本gate](01-quantum-operations.md#basic-gates) |
| Q6–Q11 | CX、Pauli、observable | [複数量子bit](01-quantum-operations.md#multi-entanglement)、[Pauli label](01-quantum-operations.md#bit-pauli-order)、[期待値](01-quantum-operations.md#expectation) |
| Q12–Q19 | 回路・測定・状態の可視化 | [回路描画](02-visualization-measurement.md#circuit-drawing)〜[state plot](02-visualization-measurement.md#state-plots) |
| Q20–Q28 | constructor、測定、合成、parameter、dynamic | [回路構築](03-circuit-construction.md)の各節 |
| Q29–Q41 | transpile、ISA、mode、Runtime、PUB | [transpile・実行](04-transpile-execution.md)の各節 |
| Q42–Q49 | Sampler、shots、DD | [Sampler V2](05-sampler.md)の各節 |
| Q50–Q57 | Estimator、期待値、resilience、result | [Estimator V2](06-estimator.md)の各節 |
| Q58–Q64 | job、result階層、counts、metadata | [結果分析](07-results-analysis.md)の各節 |
| Q65–Q68 | OpenQASM 3、interop、REST境界 | [OpenQASM 3](08-openqasm3.md)の各節 |

## Coverageの限界

全ObjectiveとMock概念への参照先があることは、全API・全hardware featureの網羅や実技習熟を意味しません。特にRuntime options、backend capability、OpenQASM supportは変化するため、受験・実行直前に公式資料を確認してください。

[← 補章A](09-algorithm-worked-examples.md) | [入口](README.md)
