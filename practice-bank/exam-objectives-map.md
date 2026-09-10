# Exam Objectives Map

IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate (C1000-179) の学習用coverage mapです。

**2026-09-11の検証状態:** IBM公式告知の8領域と試験形式を確認しました。一方、現在の公式Study Guide本文とのTask原文・番号・weightの完全照合は未完了です。旧版の「Source lock」を、完全照合済みの証拠として扱わないでください。下記のTask IDは既存教材の追跡用索引を維持したもので、公式原文の逐語引用ではありません。

公開試験レコードは`validation/collect_exam_evidence.py`から取得できます。取得成功と、その内容を読みStudy Guide本文まで検証したことは別です。非公開の実試験問題や実際の領域別出題数は推測しません。

## Domain coverage

weightは従来の教材が配分に用いた値です。最新の公式原本との照合が完了するまでは「現在の公開weightを確認済み」としません。

| # | Domain | Allocation weight | Topic test | Mock 01 | Target mock count |
|---|---|---:|---|---|---:|
| 1 | Performing quantum operations | 16% | `01-quantum-operations.md` | Q1–Q11 | 11 |
| 2 | Visualizing quantum circuits, measurements, and states | 11% | `02-visualization-measurement-states.md` | Q12–Q19 | 8 |
| 3 | Creating quantum circuits | 18% | `03-circuit-construction.md` | Q20–Q31 | 12 |
| 4 | Running quantum circuits | 15% | `04-running-circuits.md` | Q32–Q41 | 10 |
| 5 | Using the sampler primitive | 12% | `05-sampler.md` | Q42–Q49 | 8 |
| 6 | Using the estimator primitive | 12% | `06-estimator.md` | Q50–Q57 | 8 |
| 7 | Retrieving and analyzing results | 10% | `07-results-analysis.md` | Q58–Q64 | 7 |
| 8 | Operating with OpenQASM | 6% | `08-openqasm3.md` | Q65–Q68 | 4 |

上記weightに68を掛けると10.88 / 7.48 / 12.24 / 10.20 / 8.16 / 8.16 / 6.80 / 4.08問。整数部分の合計65に、最大の小数部分を持つ領域1・7・2へ1問ずつ加えると現配分になる（最大剰余方式）。これは整数化の妥当性の説明であり、weightの最新性の証明ではない。

## Task-level coverage

「直接出題」はその技能・概念を設問で選ばせること。「解説・検証のみ」はMock得点には直接含めない補助。「未出題」はこの問題集にその細目の評価問題がないことです。少なくとも1問あることをTask全体の習熟・完全coverageと同一視しません。

| 教材Task索引 | 学習内容（要約） | 直接出題 | 深さ・不足点 |
|---|---|---|---|
| 1.1 | Pauli operators・labels・線形結合 | Topic 01 Q8,Q10; Mock Q7,Q8 | label orderingとSparsePauliOpを識別。任意operatorの構築演習は限定的 |
| 1.2 | Quantum operations | Topic 01 Q1–Q7,Q9; Mock Q1–Q6,Q9–Q11 | H/S-dagger/X/Y/Z/rotations/phase。T gateは未出題 |
| 2.1 | Circuit visualization | Topic 02 Q1; Mock Q12 | mpl drawer識別。描画図の読解は薄い |
| 2.2 | Measurement visualization・distribution | Topic 02 Q2–Q5; Mock Q13,Q14,Q17,Q19 | histogram・bit order・測定分布。backend gate/error mapは未出題 |
| 2.3 | State visualization・state representation | Topic 02 Q6–Q10; Mock Q15,Q16,Q18 | Q-sphere/Bloch/Statevector。Q15,Q16をこの索引にも正しく配置 |
| 3.1 | Dynamic circuits | Topic 03 Q7,Q8; Mock Q26–Q28 | if_testの読解、SDKとhardwareの境界。実QPU上の動作をテストしたという意味ではない |
| 3.2 | Parameterized circuits | Topic 03 Q4,Q5; Mock Q23,Q24 | Parameter/assign_parameters。複数parameterのbinding順は未出題 |
| 3.3 | Transpilation・optimization | Topic 03 Q9,Q10; Mock Q29–Q31 | preset/ISA/level。observable.apply_layoutの実行検証は補助のみ |
| 3.4 | Basic circuit construction | Topic 03 Q1–Q3,Q6; Mock Q20–Q22,Q25 | constructor/measure/compose/control。append/inverseは未出題 |
| 4.1 | Execution modes・backend selection | Topic 04 Q1–Q5; Mock Q32–Q36 | Job/Session/Batch用途。Study Guideの語との逐語対応は原本確認が必要 |
| 4.2 | Runtime V2・PUB・broadcasting・job lifecycle | Topic 04 Q6–Q10; Mock Q37–Q41 | 一般形と概念。shape計算例はMock Q39解説・smokeのみ |
| 5.1 | Sampler options | Topic 05 Q6–Q9; Mock Q46–Q49 | default_shots/DD/compatibility。あらゆるoptionを網羅したわけではない |
| 5.2 | Sampler V2の役割・入力・出力 | Topic 05 Q1–Q5,Q10; Mock Q42–Q45 | local/Runtime/PUB/BitArray。get_countsはTopic 07 Q5/Mock Q61にも出題 |
| 6.1 | Estimator options | Topic 06 Q6–Q9; Mock Q55,Q56 | resilience preset/precision。presetの個別上書きは解説・client testにも記載 |
| 6.2 | Estimator V2の役割・期待値・入力 | Topic 06 Q1–Q5,Q10; Mock Q50–Q54,Q57 | local/Runtime/PUB/evs。一般Hamiltonianの評価は薄い |
| 7.1 | Results・previous jobs・analysis | Topic 07 Q1–Q5,Q7–Q10; Mock Q58,Q59,Q61–Q64 | job/jobs/result/counts/uncertainty。filter引数やarray indexingは薄い |
| 7.2 | Job monitoring | Topic 07 Q6; Mock Q60 | status method。Q60をmonitoringへ明示し、結果統計の問題を代用しない |
| 8.1 | OpenQASM 3 types | Topic 08 Q1,Q2; Mock Q65 | declarations/classical types。complexは解説で明示。width/castingは未出題 |
| 8.2 | OpenQASM semantics | Topic 08 Q3–Q5; Mock Q66 | reset/H/measurement/include/if概念。if programの出力追跡は未出題 |
| 8.3 | Qiskit/OpenQASM interoperability | Topic 08 Q6–Q8; Mock Q67 | dump/dumps/load/loads/optional importer。round-tripは補助test |
| 8.4 | OpenQASM/Compute support boundary・REST | Topic 08 Q9,Q10; Mock Q68 | supportの層・REST modes。具体的なHTTP payload作成は未出題 |

この一覧で「T gate/append/inverse等を扱う予定」と「設問で実際に評価している」を分離しました。未出題細目が公式Taskの必須要件かどうかを原本で判断し、必要なら追加・差し替えを行ってください。現時点で「公式Taskの欠落ゼロ」「非公式Taskの追加ゼロ」とは認定していません。

## Execution-mode terminology

現行ComputeガイドではJob / Session / Batchを区別する。Jobはbackendをmodeに指定する通常のjob、Sessionは結果依存の反復などに向くactiveな専有実行window、Batchは独立した複数jobの実行に向く。Pythonガイドの分類と、REST session resourceの`dedicated` / `batch`という値を区別する。

既存教材がStudy Guideに帰属させていた「session / dedicated / priority / batch」という表現は、原文を再確認するまで逐語引用として使用しない。現行のservice semanticsを説明することと、過去の試験資料の語を対応づけることは別の検証である。

## Cross-cutting concepts

bitstringのclassical-bit order、Pauli labelのqubit order、複数registerの名前・順序は区別する。Statevectorの厳密な等号とglobal phaseまでの物理状態の同値も区別する。

local StatevectorSampler/StatevectorEstimatorはRuntime/QPUそのものではない。Runtime QPUへ送るcircuitはISAに合わせ、Estimator observableも必要に応じてlayoutを適用する。SDKでcontrol flowを表現できることは全hardwareでの実行可能性を保証しない。

## Source references

- Official certification announcement: https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- Official certification and Study Guide entry point: https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400
- Public exam record: https://www.ibm.com/training/credentials/getExam/C1000-179
- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- REST modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api
- Primitive inputs/outputs: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Dynamic circuits: https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
- QASM feature table: https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table
- Source/check status: [revision report](validation/revision-report-2026-09-11.md)
