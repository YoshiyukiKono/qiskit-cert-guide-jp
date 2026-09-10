# Qiskit v2.X Practice Bank

IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate (C1000-179) 向けのオリジナル演習セットです。既存の`exams/`は変更せず、教材は`practice-bank/`で完結します。CI設定は`.github/workflows/practice-bank-validation.yml`です。

## 基準と確認範囲

**2026-09-11 JSTにIBM公式の公開試験レコードから8領域・21のObjectives・weight・試験形式を確認しました。** [Exam Objectives Map](exam-objectives-map.md)は、公式の原文と教材の出題内容を分離し、未出題の細目も明記しています。公式レコードの必要fieldを[JSON](validation/official-objectives-2026-09-11.json)へ保存しました。

別添Study Guide PDF本文は未閲覧です。公開Objectivesの確認を、PDF内の全参考資料や細目まで検証したことと同一視しません。また、構造validatorや一部のSDKテストの合格は、全148問の技術的一意性や本試験相当の難易度の証明ではありません。

APIの正しさは現行IBM Quantum / Qiskit公式資料とOpenQASM仕様を基準にし、本問題集や過去のレビューと矛盾する場合は公式情報を優先してください。今回の訂正・再検証・残る制約は[revision report](validation/revision-report-2026-09-11.md)に記録しています。

## 試験形式

公式C1000-179レコードの確認値は68問、90分、47正答で合格、英語です。本問題集は実試験問題、dump、非公開問題の再現ではありません。模試の得点が実試験の合否を保証するものでもありません。

## 公開領域とweight

| Domain | Weight | Mock 01 |
|---|---:|---:|
| Perform quantum operations | 16% | 11 |
| Visualize quantum circuits, measurements, and states | 11% | 8 |
| Create quantum circuits | 18% | 12 |
| Run quantum circuits | 15% | 10 |
| Use the sampler primitive | 12% | 8 |
| Use the estimator primitive | 12% | 8 |
| Retrieve and analyze the results of quantum circuits | 10% | 7 |
| Operate with OpenQASM | 6% | 4 |

合計68問。最大剰余方式による整数近似です。実試験の領域別問題数を公開値として示したものではありません。

## LocalとRuntimeの区別

`qiskit.primitives.StatevectorSampler` / `StatevectorEstimator`はlocal statevector-based V2実装です。`qiskit_ibm_runtime.SamplerV2` / `EstimatorV2`はRuntime側の実装で、QPU workflowではISA circuit、observable layout、execution mode、options、job/result lifecycleも考慮します。V2 interfaceが同じでも、実装の機能・実行環境がすべて同じとは限りません。

## 構成

```text
practice-bank/
├── README.md
├── exam-objectives-map.md
├── topic-tests/                         # 8ファイル × 10問 = 80問
├── mock-exams/mock-01.md                # 68問
├── answers/mock-exams/mock-01-answers.md
└── validation/
    ├── notes.md
    ├── requirements.txt
    ├── validate_bank.py
    ├── test_validate_bank.py
    ├── smoke_checks.py
    ├── run_check.py
    ├── collect_exam_evidence.py
    ├── official-objectives-2026-09-11.json
    └── revision-report-2026-09-11.md
```

## 利用方法

最初にObjective mapで出題範囲と薄い細目を確認し、Topic testsを解き、正答だけでなくdistractorの説明も読んでください。その後、Mock 01を資料なし・90分で解き、別ファイルの解答で復習します。TopicとMockには重複した概念があり、独立した実力測定としての限界があります。

各問は1つ選択です。MockのA/B/C/Dは各17問。Topic全体の位置分布はA20/B21/C21/D18です。全列を説明する短周期をvalidatorで検査しますが、配置の乱数性を証明するものではありません。

## 検証

Python 3.12の環境で、repository rootから次を実行します。構造検査とその回帰テストにはQiskitは不要です。

```bash
python practice-bank/validation/validate_bank.py
python practice-bank/validation/test_validate_bank.py
python -m pip install -r practice-bank/validation/requirements.txt
python practice-bank/validation/smoke_checks.py
```

主要依存はQiskit 2.5.2、qiskit-ibm-runtime 0.49.0、qiskit-qasm3-import 0.6.0です。詳細は[Validation Notes](validation/notes.md)を参照してください。

GitHub Actionsでは対象head SHAをcheckoutして、全教材の構造検査、26件のvalidator回帰テスト、15件のSDK/client smoke testsを実行し、version・command・終了コード・ログをartifactに残します。実行成功/失敗はそのSHAのrunで確認してください。workflowを置いたことだけを実行成功とはしません。

SDK/client testsは認証不要です。実Runtime serviceへの送信・job取得や実QPUの挙動は検証しません。公式試験レコードのネットワーク取得jobも、教材の技術的合格判定とは分離しています。

## Version-sensitiveな範囲

Runtime execution modes、Sampler/Estimator options、DD/ZNE/twirling、job/result API、dynamic circuitsのhardware support、OpenQASM import/export・実行可能featureは試験直前にも公式資料を再確認してください。

## 公式参照

- Current Exam Objectives: https://www.ibm.com/training/credentials/getExam/C1000-179
- Certification / Study Guide entry point: https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400
- Qiskit documentation: https://quantum.cloud.ibm.com/docs/
- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- SamplerV2: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/sampler-v2
- EstimatorV2: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/estimator-v2
- Dynamic circuits: https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow
- OpenQASM 3: https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3
