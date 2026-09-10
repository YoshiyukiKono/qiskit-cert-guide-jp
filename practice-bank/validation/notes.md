# Validation Notes

教材内容の訂正、構造検査、SDK/clientの実行検証、公式objectiveとの照合は別の作業です。どれか1つの合格から残りも合格とは推定しません。

## Reproducible commands

repository rootから実行します。Python 3.10以降が必要です。CIはPython 3.12と、2026-09-11に公式リリースを確認したQiskit 2.5.2 / qiskit-ibm-runtime 0.49.0を指定しています。optional importer・推移的依存は解決されたversionをログに残します（完全なdependency lockではありません）。

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

Mock各問に1つ付けた`<!-- domain: N -->`から教材側のprimary domain割当を読み、IDと領域範囲、実集計11/8/12/10/8/8/7/4、map tableの範囲・問題数と照合します。著者の分類の意味的妥当性や、weightの現行公式原本との一致を自動判定するものではありません。

検査失敗は明示的な例外と非ゼロ終了にします。検査を`assert`に依存させないため、`python -O`でも無効化されません。

## Regression tests

`test_validate_bank.py`には、正常fixture、余分なE、空/重複/欠落choice、同値/矛盾する重複key、欠落/不正key、解説見出し不一致、空/重複/欠落/不正解説label、欠落/重複/誤ったdomain、map count不一致、不正question ID、空のstem、code-fence処理、周期、`python -O`での拒否を含む25件のparser testと、実教材全体を読む1件のtestがあります。

人工fixtureの合格だけを「全教材の通し実行」と報告しません。実教材のtestはファイルが欠けていれば失敗します。

## SDK and Runtime-client smoke checks

`smoke_checks.py`は15件のunittestを実行します。Qiskitや必要なpackageがなければimportで失敗し、skipや合格へ置き換えません。

対象は、H conjugation、Rx/Rz(pi)、厳密ベクトルと物理状態、Bell振幅/確率/相対位相、Pauli ordering、compose/assign_parameters、GateとInstruction、local Sampler/shots、BitArray、複数register、Estimatorの数値/broadcasting、fake Target/observable layout、if_test表現とlocal Samplerの制約、Runtime client option objects、OpenQASM3 import/export round-trip、明示resetによる準備です。

行列はglobal phaseを同一視せず、`rtol=0, atol=1e-12`の数値許容誤差内で比較します。浮動小数点計算を記号的な厳密証明とは呼びません。

Runtime serviceの認証、job送信/取得、実QPU、server scheduling、実hardware上のdynamic circuitsやDD/ZNEの効果は実行しません。local clientがoptionを受け付けることは、server側の動作検証ではありません。

## CI and evidence

`.github/workflows/practice-bank-validation.yml`はread-only権限で対象headをcheckoutします。mainへの書き込み、PRコメント、service credentials、QPU課金を必要としません。

`run_check.py`は実際のcheckout SHA、Python/package versions、command、終了コード、出力を`validation-output/`へ保存し、Actions artifactへ残します。失敗を成功へ書き換えません。workflowの設置と実行成功も別です。

`collect_exam_evidence.py`はIBMの公開C1000-179レコードをネットワーク取得する補助です。このjobは外部サイトの可用性に依存するためコード検査のgateとは分離し、job/step結果を個別確認します。JSON取得成功もStudy Guideの完全照合を意味しません。公式PDFの本文、Task番号/原文、weight、確認日を人手で照合して初めてcoverage判定を更新します。

## Limitations and status

全148問の技術的一意性、各distractorのもっともらしさ、公式Taskの完全coverageは、この構造validatorと15件のsmokeだけでは保証しません。訂正と確認の結果は[revision report](revision-report-2026-09-11.md)に記録します。

## Official references

- Qiskit 2.5.2 release: https://github.com/Qiskit/qiskit/releases/tag/2.5.2
- Runtime 0.49.0 release: https://github.com/Qiskit/qiskit-ibm-runtime/releases/tag/0.49.0
- Gate: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Gate
- Instruction: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Instruction
- BitArray: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray
- Primitive I/O: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Resilience presets: https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management
- OpenQASM types: https://openqasm.com/versions/3.0/language/types.html
- Qasm3: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qasm3
