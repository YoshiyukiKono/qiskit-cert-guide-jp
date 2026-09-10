# Validation Notes

教材内容の訂正、構造検査、SDK/clientの実行検証、公式Objectivesとの照合は別の作業です。どれか1つの合格から残りも合格とは推定しません。

## Reproducible commands

repository rootから実行します。Python 3.10以降が必要です。CIはPython 3.12と、Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0 / qiskit-qasm3-import 0.6.0を指定しています。推移的依存は解決されたversionを導入ログに残します。これは全依存のlockfileではありません。

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShellの場合は .venv\Scripts\Activate.ps1
python -m pip install -r practice-bank/validation/requirements.txt
python practice-bank/validation/validate_bank.py
python practice-bank/validation/test_validate_bank.py
python practice-bank/validation/smoke_checks.py
```

## Structural validator

`validate_bank.py`は標準ライブラリのみで実行できます。実際のMarkdownから、Topic各10問、Mock68問、番号の一意性・順序、A-Dの選択肢の非空性・重複、解答キーの重複、キーと解説見出しの一致、各ラベルへの非空の解説を確認します。コードフェンス内の例は問題見出し・選択肢と誤認しません。

正答位置の既存基準（Topicごと最多6、全Topic最多最少差5以内、Mock各17）を維持します。加えて、列全体を説明できる周期1–4の反復を拒否します。この限定された検査は「ランダム性の証明」ではありません。

Mock各問の`<!-- domain: N -->`から教材側のprimary domain割当を読み、IDと領域範囲、実集計11/8/12/10/8/8/7/4、map tableの範囲・問題数と照合します。著者の分類の意味的妥当性や、weightの現行公式原本との一致を自動判定するものではありません。

失敗は明示的な例外と非ゼロ終了にします。`assert`に依存させないため、`python -O`でも検査が無効化されません。

## Regression tests

`test_validate_bank.py`は正常fixture、余分なE、空/重複/欠落choice、同値/矛盾する重複key、欠落/不正key、解説見出し不一致、空/重複/欠落/不正解説label、欠落/重複/誤ったdomain、map count不一致、不正question ID、空のstem、code-fence処理、周期、`python -O`での拒否を含む25件と、実教材全体を読む1件を実行します。

人工fixtureの合格だけを全教材の通し実行とは報告しません。実教材testは必要なファイルが欠けていれば失敗します。

## SDK and Runtime-client smoke checks

`smoke_checks.py`は15件のunittestです。必要packageがなければimportで失敗し、skipや合格へ置き換えません。

対象はH conjugation、Rx/Rz(pi)、厳密ベクトルと物理状態、Bell振幅/確率/相対位相、Pauli ordering、compose/assign_parameters、GateとInstruction、local Sampler/shots、BitArray、複数register、Estimator数値/broadcasting、fake Target/observable layout、if_test表現とlocal Sampler制約、Runtime client option objects、QASM3 round-trip、明示resetによる準備です。

行列はglobal phaseを同一視せず、`rtol=0, atol=1e-12`の数値許容誤差内で比較します。浮動小数点計算を記号的な厳密証明とは呼びません。StatevectorSamplerのmid-circuit拒否は、公式SDK 2.5.2が返す`QiskitError`の型とメッセージを検査します。

Runtime serviceの認証、job送信/取得、実QPU、server scheduling、hardware上のdynamic circuitsやDD/ZNEの効果は実行しません。local clientがoptionを受け付けることはserver動作の検証ではありません。

## CI and evidence

`.github/workflows/practice-bank-validation.yml`はread-only権限で対象headをcheckoutします。mainへの書き込み、PRコメント、service credentials、QPU課金を必要としません。

`run_check.py`はcheckout SHA、Python/package versions、command、終了コード、出力を`validation-output/`へ保存し、Actions artifactへ残します。失敗を成功へ書き換えません。workflowの設置と実行成功も別です。

`collect_exam_evidence.py`はIBMの公開C1000-179レコードを取得する補助です。外部サイトの可用性に依存するためコード検査gateから分離し、job/step結果を個別確認します。保存・表示は試験形式とObjectivesの関連公開fieldに限定し、担当者連絡先や期限付き署名URLは含めません。ネットワーク取得の成功だけを教材との内容照合完了とはしません。

2026-09-11の確認では、取得した公式レコードの8領域・21項目・weightを実際に読み、[snapshot](official-objectives-2026-09-11.json)と[map](../exam-objectives-map.md)へ反映しました。別添Study Guide PDFの本文・参考資料一覧は未閲覧です。

## Limitations and status

全148問の技術的一意性、distractorのもっともらしさ、公開Task内のあらゆる細目のcoverageは、構造validatorと15件のsmokeだけでは保証しません。訂正と実行結果は[revision report](revision-report-2026-09-11.md)を参照してください。

## Official references

- Qiskit release: https://github.com/Qiskit/qiskit/releases/tag/2.5.2
- Runtime release: https://github.com/Qiskit/qiskit-ibm-runtime/releases/tag/0.49.0
- StatevectorSampler source: https://github.com/Qiskit/qiskit/blob/2.5.2/qiskit/primitives/statevector_sampler.py
- Gate: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Gate
- Instruction: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Instruction
- BitArray: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray
- Primitive I/O: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Resilience presets: https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management
- OpenQASM types: https://openqasm.com/versions/3.0/language/types.html
- Qasm3: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qasm3
