# Exam Objectives Map

IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate (C1000-179) の公開Objectivesと、問題集の実際の出題を対応づけます。

## Source and verification boundary

**2026-09-11 JSTに、IBM公式の公開試験レコードを取得して全8領域・21項目・weightを読み、下表と照合しました。** Source: `https://www.ibm.com/training/credentials/getExam/C1000-179`。取得run `34510149269`、job `102981976567`、取得時刻 `2026-09-10T17:45:32Z`。必要な公開field、原文、確認範囲を[official-objectives-2026-09-11.json](validation/official-objectives-2026-09-11.json)へ保存しています。

公式JSONの`OBJECTIVES`と各HTML ordered listがTaskの根拠です。下表の1.1等はその順序から付けた参照用IDであり、JSONに同名のID fieldが存在するという意味ではありません。英語の原文はsnapshot、日本語の学習内容はこのmapに分離します。

**別添Study Guide PDF本文は閲覧できていません。** 公式レコードのObjectivesを検証したことと、PDF中の参考資料・細目まで確認したことを混同しません。現行公開Objectivesの欠落/追加を確認する根拠は、ブログや第三者問題集ではなく上記IBMレコードです。

## Domain coverage

| # | Public domain | Weight | Topic test | Mock 01 | Target mock count |
|---|---|---:|---|---|---:|
| 1 | Perform quantum operations | 16% | `01-quantum-operations.md` | Q1–Q11 | 11 |
| 2 | Visualize quantum circuits, measurements, and states | 11% | `02-visualization-measurement-states.md` | Q12–Q19 | 8 |
| 3 | Create quantum circuits | 18% | `03-circuit-construction.md` | Q20–Q31 | 12 |
| 4 | Run quantum circuits | 15% | `04-running-circuits.md` | Q32–Q41 | 10 |
| 5 | Use the sampler primitive | 12% | `05-sampler.md` | Q42–Q49 | 8 |
| 6 | Use the estimator primitive | 12% | `06-estimator.md` | Q50–Q57 | 8 |
| 7 | Retrieve and analyze the results of quantum circuits | 10% | `07-results-analysis.md` | Q58–Q64 | 7 |
| 8 | Operate with OpenQASM | 6% | `08-openqasm3.md` | Q65–Q68 | 4 |

weightに68を掛けると10.88 / 7.48 / 12.24 / 10.20 / 8.16 / 8.16 / 6.80 / 4.08問。整数部分の合計65に、小数部分が最大の領域1・7・2へ1問ずつ加えると現配分になる（最大剰余方式）。これは公式weightの整数近似であり、実試験の領域別問題数を公開値として主張しません。

## Task-level coverage

「直接出題」は設問でその概念・操作を評価すること。「解説・検証のみ」はMock得点に直接含めない補助。「未出題」はその細目の評価問題がないことです。1問の存在を、Task全体の習熟やあらゆる実装・細目の網羅と同一視しません。

| Task | 公開Objectiveの日本語要約 | 直接出題 | 深さ・未出題細目・補助 |
|---|---|---|---|
| 1.1 | Pauli operatorsを定義する | Topic 01 Q8,Q10; Mock Q7,Q8 | label orderingとSparsePauliOpの構築。任意operatorの構築演習は限定的 |
| 1.2 | Quantum operationsを適用する | Topic 01 Q1–Q7,Q9; Mock Q1–Q6,Q9–Q11 | H/S-dagger/X/Y/Z/rotations/phase。T gateは未出題 |
| 2.1 | Circuitを可視化する | Topic 02 Q1; Mock Q12 | mpl drawer識別。描画図の読解は薄い |
| 2.2 | Measurementを可視化する | Topic 02 Q2–Q5; Mock Q13,Q14,Q17,Q19 | histogram・bit order・測定分布。backend gate/error mapは未出題 |
| 2.3 | Stateを可視化する | Topic 02 Q6–Q10; Mock Q15,Q16,Q18 | Q-sphere/Bloch/Statevector。Q15,Q16を正しくこのTaskへ対応 |
| 3.1 | Dynamic circuitsを構築する | Topic 03 Q7,Q8; Mock Q26–Q28 | if_test読解、SDK/hardware境界。実QPUで検証したという意味ではない |
| 3.2 | Parameterized circuitsを構築する | Topic 03 Q4,Q5; Mock Q23,Q24 | Parameter/assign_parameters。複数parameterのbinding順は未出題 |
| 3.3 | Transpile・optimizeする | Topic 03 Q9,Q10; Mock Q29–Q31 | preset/ISA/level。observable.apply_layoutの実行は補助test |
| 3.4 | Basic circuitsを構築する | Topic 03 Q1–Q3,Q6; Mock Q20–Q22,Q25 | constructor/measure/compose/control。append/inverseは未出題 |
| 4.1 | Execution modesを理解する | Topic 04 Q1–Q5; Mock Q32–Q36 | 下記で公式Objectiveのdedicated/priorityと現行mode名を区別 |
| 4.2 | Runtime primitivesで実hardware向けに実行し、broadcasting rulesを適用する | Topic 04 Q6–Q10; Mock Q37–Q41 | ISA/PUB/jobに加えTopic 04 Q9を具体的なshape読解に差し替え。localの数値はsmokeで検証。QPUの実行実績ではない |
| 5.1 | DD等のSampler optionsを設定する | Topic 05 Q6–Q9; Mock Q46–Q49 | default_shots/DD/compatibility。あらゆるoptionを網羅しない |
| 5.2 | Samplerの理論的背景を理解する | Topic 05 Q1,Q4,Q5,Q10; Topic 02 Q4; Topic 07 Q9; Mock Q17,Q42,Q45 | 測定のsample/分布/PUB。実装class識別だけを理論coverageとみなさない |
| 6.1 | Resilience levels等のEstimator optionsを設定する | Topic 06 Q6–Q9; Mock Q55,Q56 | preset/precision。個別上書きは解説・client testでも区別 |
| 6.2 | Estimatorの理論的背景を理解する | Topic 06 Q1,Q4,Q5; Mock Q11,Q50,Q53,Q54 | observableと期待値。一般Hamiltonianの評価は薄い |
| 7.1 | 過去のexperiment resultsを取得する | Topic 07 Q1–Q5; Mock Q58,Q59,Q61 | job/jobs/result/counts。統計解析はTopic 07 Q7–Q10等の補助 |
| 7.2 | Jobsをmonitorする | Topic 07 Q6; Mock Q60 | status method。結果統計の問題をmonitoringの代用にしない |
| 8.1 | OpenQASM 3 programでtypesを構成する | Topic 08 Q1,Q2; Mock Q65 | declarations/classical types。complexを解説。width/castingは未出題 |
| 8.2 | OpenQASM semanticsを解釈する | Topic 08 Q3–Q5; Mock Q66 | reset/H/measurement/include/if概念。if programの結果追跡は未出題 |
| 8.3 | 異なるOpenQASM versionsとQiskitを相互利用する | Topic 08 Q6–Q8; Mock Q67 | qasm2/qasm3の境界とimport/export。round-tripは補助test |
| 8.4 | Qiskit IBM Runtime REST APIを利用する | Topic 08 Q10; Mock Q68 | Topic Q10を具体的なGET結果endpointへ差し替え。APIの存在・support境界だけで代用しない |

公開レコードの21項目は全てこの表に対応し、存在しない項目を公式Taskとして追加していません。ただし出題の深さには差があります。T/append/inverseや図の読解等の未出題細目を明記し、完全な実技習得・全参考資料coverageは主張しません。PDFの参考資料一覧との照合は別途必要です。

## Execution-mode terminology

公式Objective 4.1には`session with dedicated, priority, and batch mode`という表現があります。この文言を4つの現行Python mode名として暗記しません。

現行Computeガイドは**Job / Session / Batch**の3つを区別します。Jobはbackendをmodeに指定する通常のjob、Sessionは結果依存の反復等に向くactiveな専有実行window、Batchは独立した複数jobに向きます。Sessionがactiveである間の専有・優先的な実行特性と、REST session resourceの`dedicated` / `batch`という値を区別してください。`priority`という独立した第4のPython execution modeを追加する説明はしません。

## Cross-cutting concepts

bitstringのclassical-bit order、Pauli labelのqubit order、複数registerの名前・順序は区別する。Statevectorの厳密な等号とglobal phaseまでの物理状態の同値も区別する。

local StatevectorSampler/StatevectorEstimatorはRuntime/QPUそのものではない。Runtime QPUへ送るcircuitはISAに合わせ、Estimator observableも必要に応じてlayoutを適用する。SDKでcontrol flowを表現できることは全hardwareでの実行可能性を保証しない。

## Source references

- Current public Exam Objectives: https://www.ibm.com/training/credentials/getExam/C1000-179
- Certification / Study Guide entry point: https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400
- Certification announcement: https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- REST modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api
- Primitive input/output: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- REST job endpoints: https://quantum.cloud.ibm.com/docs/en/api/qiskit-runtime-rest/tags/jobs
- Dynamic circuits: https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
- QASM feature table: https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table
- Source / validation status: [revision report](validation/revision-report-2026-09-11.md)
