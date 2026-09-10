# Exam Objectives Map

このファイルは、IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate (C1000-179) の公開Study GuideをTask単位まで分解し、`practice-bank/` のcoverageを追跡するための学習用マップです。

**Source lock:** 2026-09-10。Exam ObjectivesとweightはIBM公開Study Guideを基準とし、APIの意味は同日時点のIBM Quantum Documentationで再検証します。

> このmapは公開objectiveのcoverageを管理するためのものです。非公開の実試験問題、実際の問題数内訳、採点ロジックを推測しません。

## Domain coverage

| # | Public domain | Weight | Topic test | Mock 01 | Target mock count |
|---|---|---:|---|---|---:|
| 1 | Performing quantum operations | 16% | `01-quantum-operations.md` | Q1–Q11 | 11 |
| 2 | Visualizing quantum circuits, measurements, and states | 11% | `02-visualization-measurement-states.md` | Q12–Q19 | 8 |
| 3 | Creating quantum circuits | 18% | `03-circuit-construction.md` | Q20–Q31 | 12 |
| 4 | Running quantum circuits | 15% | `04-running-circuits.md` | Q32–Q41 | 10 |
| 5 | Using the sampler primitive | 12% | `05-sampler.md` | Q42–Q49 | 8 |
| 6 | Using the estimator primitive | 12% | `06-estimator.md` | Q50–Q57 | 8 |
| 7 | Retrieving and analyzing the results of quantum circuits | 10% | `07-results-analysis.md` | Q58–Q64 | 7 |
| 8 | Operating with OpenQASM | 6% | `08-openqasm3.md` | Q65–Q68 | 4 |

## Task-level coverage

### 1. Performing quantum operations — 16%

#### Task 1.1 — Define Pauli operators

最低限扱うもの: `Pauli` / Pauli strings、tensor-product ordering、`SparsePauliOp`につながるobservable表現。

Coverage: Topic 01 Q8–Q10、Mock Q8–Q11。

#### Task 1.2 — Apply quantum operations

最低限扱うもの: X/Y/Z/H/S/Tとdagger、controlled gates、rotation gates、global/relative phase、gate identitiesと状態追跡。

Coverage: Topic 01 Q1–Q7、Mock Q1–Q7。

### 2. Visualizing quantum circuits, measurements, and states — 11%

#### Task 2.1 — Visualize quantum circuits

`QuantumCircuit.draw()`、text / mpl outputの区別。

Coverage: Topic 02 Q1、Mock Q12。

#### Task 2.2 — Visualize quantum measurements

`plot_histogram`、counts / sampled distributionの読み方、bit ordering。

Coverage: Topic 02 Q2–Q5、Mock Q13–Q16。

#### Task 2.3 — Visualize quantum states

`Statevector`、`plot_bloch_multivector`、`plot_state_qsphere`、amplitude / probability / phaseの区別。

Coverage: Topic 02 Q6–Q10、Mock Q17–Q19。

### 3. Creating quantum circuits — 18%

#### Task 3.1 — Construct dynamic circuits

mid-circuit measurement、classical feedforward、`QuantumCircuit.if_test`、SDKで表現できるcontrol flowと実QPU supportの区別。

Coverage: Topic 03 Q7–Q8、Mock Q27–Q28。

#### Task 3.2 — Construct parameterized circuits

`Parameter`、`assign_parameters`、parameterized circuitをPrimitiveへ渡す考え方。

Coverage: Topic 03 Q4–Q5、Mock Q23–Q24。

#### Task 3.3 — Transpile and optimize circuits

`generate_preset_pass_manager`、`optimization_level`、target / coupling / basis、ISA circuit。

Coverage: Topic 03 Q9–Q10、Mock Q29–Q31。

#### Task 3.4 — Construct basic quantum circuits

registers / bits、gate application、measurement、`append` / `compose`、`inverse` / control。

Coverage: Topic 03 Q1–Q3、Q6、Mock Q20–Q22、Q25–Q26。

### 4. Running quantum circuits — 15%

#### Task 4.1 — Demonstrate understanding of execution modes

公開Study Guideでは execution modes の例として **session / dedicated / priority / batch** が挙げられています。2026-09-10時点のIBM Quantum Documentationでは、ユーザーが選択するexecution modeを **Job / Session / Batch** と整理しています。

対応関係を次のように理解します。

- **Job mode**: 単発job。primitiveへ`mode=backend`を渡す代表的workflow。
- **Session mode**: 複数jobを扱うdedicated/exclusive execution window。sessionがactiveな間はそのsession内workloadがscheduling上priorityを得る。前jobの結果を次jobへ反映するiterative workloadに向く。
- **Batch mode**: 互いに独立して実行できる複数jobをまとめるworkload manager。
- REST `/sessions` APIではsession resourceの`mode`として`dedicated`または`batch`を使う。このREST上の値とPython guideのJob/Session/Batchという分類を混同しない。

Coverage: Topic 04 Q1–Q5、Mock Q32–Q36。

#### Task 4.2 — Run with Runtime V2 primitives and PUB/broadcasting

`qiskit_ibm_runtime.SamplerV2` / `EstimatorV2`、ISA circuit / observable、PUB、parameter/observable broadcasting、asynchronous job result。

Coverage: Topic 04 Q6–Q10、Mock Q37–Q41。

### 5. Using the sampler primitive — 12%

#### Task 5.1 — Configure Sampler options

`SamplerOptions`、`default_shots`、dynamical decoupling、feature compatibilityを固定暗記せずcurrent docsで確認する姿勢。

Coverage: Topic 05 Q6–Q10、Mock Q46–Q49。

#### Task 5.2 — Understand and use Sampler V2

sampled classical outputs、local `StatevectorSampler` とRuntime `SamplerV2` の違い、PUB / parameter values / shots、`BitArray` / output register。

Coverage: Topic 05 Q1–Q5、Mock Q42–Q45。

### 6. Using the estimator primitive — 12%

#### Task 6.1 — Configure Estimator options

`EstimatorOptions`、`resilience_level`、current levels 0 / 1 / 2、precisionとshotsを混同しない、ZNE / twirling等との関係。

> 古いstudy/sample materialに数値levelの例が残っていても、version-sensitiveなAPI値はcurrent IBM Quantum Documentationを優先します。

Coverage: Topic 06 Q6–Q10、Mock Q54–Q57。

#### Task 6.2 — Understand and use Estimator V2

circuit + observable、expectation value、`SparsePauliOp`、local `StatevectorEstimator` とRuntime `EstimatorV2` の違い、`data.evs`。

Coverage: Topic 06 Q1–Q5、Mock Q50–Q53。

### 7. Retrieving and analyzing results — 10%

#### Task 7.1 — Retrieve results and previous jobs

`job.result()`、`QiskitRuntimeService.job(job_id)`、`QiskitRuntimeService.jobs(...)`、Sampler / Estimator result structure。

Coverage: Topic 07 Q1–Q5、Mock Q58–Q61。

#### Task 7.2 — Monitor jobs and analyze output

`job.status()`、job lifecycle、counts / `BitArray` / `evs`、metadata、statistical interpretation。

Coverage: Topic 07 Q6–Q10、Mock Q62–Q64。

### 8. Operating with OpenQASM — 6%

#### Task 8.1 — Structure types in OpenQASM 3

`qubit`, `bit`、classical scalar/array types such as `int`, `float`, `angle`。

Coverage: Topic 08 Q1–Q2、Mock Q65。

#### Task 8.2 — Interpret OpenQASM semantics

measurement assignment、`if` / control-flow semantics、`stdgates.inc`。

Coverage: Topic 08 Q3–Q5、Mock Q66。

#### Task 8.3 — Interoperate OpenQASM and Qiskit

`qiskit.qasm3.dump` / `dumps`、`load` / `loads`、`qiskit-qasm3-import` optional dependency、QASM2とQASM3 APIを混同しない。

Coverage: Topic 08 Q6–Q8、Mock Q67。

#### Task 8.4 — OpenQASM and IBM Quantum Compute interoperability

OpenQASM 3 supportはfeatureごとに差がある、SDKでparse/represent/exportできることとQPUで実行できることを区別する、REST API経由のexecution modesが存在する。

Coverage: Topic 08 Q9–Q10、Mock Q68。

## Cross-cutting concepts

### Endianness / bit ordering

Qiskitのbitstring、Pauli string、register表示は同じ「左右」の直感で雑に扱わない。問題文がどのorderingを指すかを明示する。

### Local vs Runtime

`StatevectorSampler` / `StatevectorEstimator` はV2 reference implementationだが、IBM QPU executionを表すものではない。Runtime側は `qiskit_ibm_runtime.SamplerV2` / `EstimatorV2` を扱う。

### ISA boundary

IBM Quantum Compute primitivesへ送る回路・observableはbackendのISA/layoutへ合わせる必要がある。local statevector reference primitivesは抽象命令を直接扱える場合がある。

### Dynamic circuits

Qiskit SDKは複数のcontrol-flow constructを表現できるが、実QPU側のsupportは別問題でありcurrent documentationを確認する。

## Source references

- IBM certification: https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- IBM Quantum Documentation: https://quantum.cloud.ibm.com/docs/
- Dynamic circuits: https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- Primitives: https://quantum.cloud.ibm.com/docs/en/guides/primitives
- Sampler options: https://quantum.cloud.ibm.com/docs/en/guides/sampler-options
- Estimator options: https://quantum.cloud.ibm.com/docs/en/guides/estimator-options
- Runtime service API: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service
- OpenQASM 3 interop: https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3
- OpenQASM 3 feature table: https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table
- REST execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api
