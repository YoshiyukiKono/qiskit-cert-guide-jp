# PR #1 revision record — 2026-09-11

## Scope and provenance

開始head: `4112db1a9e07ec69ab7b23486095e7dbbbd9198d`。
base main: `88c9a83a12383541bb5ca53484afdaa3b15874bb`。
対象ブランチ: `add-v2x-practice-bank`。

開始時にPR metadata、main ref、全15変更ファイル、実diffと変更内容を確認した。前回reviewの主張を正解とせず、公式資料と再現可能なテストへ分解した。変更はpractice-bankと検証workflowに限定する。全面的な難易度改訂は対象外。

## Findings disposition

| ID | 再確認と処理 |
|---|---|
| F01 | 確認・訂正。OpenQASM仕様はqubitの初期状態を未定義とする。Topic 08 Q3にresetを追加し、測定前のplus準備を明示。Mock Q66は初期状態を断定せず、同じ欠陥とは扱わない |
| F02 | 確認・訂正。Topic 01 A4/A6の正答labelを補い、Topic 03 Q4とTopic 06 Q10のB/Dを選択肢・解説とも交換。正答位置A20/B21/C21/D18。validatorの集計閾値を緩めていない。旧分布自体を統計的異常とは断定しない |
| F03 | 確認・訂正。Gate.controlと基底Instructionを区別。Topic 03 A6 / Mock Q25解説を修正 |
| F04 | 確認・訂正。BitArray.expectation_values(observables)は実在する。Mock Q61のAを「counts取得ではなく必須引数もない」と説明し、正答Cは維持 |
| F05 | 前回指摘の意味を限定。Z ketの厳密な演算なら元からCが正しい。キー誤りとは扱わずMock Q3の問題文に厳密statevectorを明示 |
| F06 | 前回指摘の意味を限定。resilience presetとして元の正答は正しい。個別overrideがない前提とoverride可能性を設問・解説へ追加 |
| F07 | 内部mapping訂正に加え、今回取得した公式試験レコードの8領域・21項目・weightと照合。Q15/Q16はstate visualization、Q60はmonitoring。理論backgroundとclass識別を分離。T/append/inverse等の未出題を明記。Study Guide PDFの参考資料等は未確認 |
| F08 | 確認・改修。重複key、空/余分なchoice、空解説、domain誤割当を検出するparserと否定テスト。assert依存を廃止。科学的正しさや分類の意味までは検査しないと明記 |
| F09 | 確認・訂正。Topic 02 Q3/Q4のA/Cを交換し、BDACの全列周期を解消。頻度と解説を整合。乱数性の証明とはしない |
| F10 | 全面的な出題品質改訂は依頼範囲外として保留。公開Task 4.2/8.4の薄い箇所に限りTopic 04 Q9をshape読解、Topic 08 Q10をREST結果取得へ差し替え。計148問・各キー位置を維持 |
| F11 | 確認・訂正。OpenQASM complexは実在することをTopic 08 A2へ明示 |
| F12 | 表現を訂正。全行列比較の方針は元から妥当。数値許容誤差内でglobal phaseを区別する比較と明記し、記号的厳密計算とは呼ばない |

補足として、Mock Q38/Q45のPUBのNone位置、Q39のparameter軸を除くbroadcasting、Q6のcontrol/target表記を明示した。Topic 04 A8の`(circuit, shots)`もそのまま有効なSampler PUBではないことを説明した。

## Official Objectives verification

公式C1000-179レコードをGitHub Actions run `34510149269` / job `102981976567`で取得し、ログの実内容を読んだ。全8領域・21のlist項目・weight 16/11/18/15/12/12/10/6・68問/90分/47正答/Englishを確認した。

原文とprovenanceの必要fieldを[official-objectives-2026-09-11.json](official-objectives-2026-09-11.json)へ保存し、[map](../exam-objectives-map.md)へ対応を反映した。原文は学習用要約と区別する。公式JSONのTask listは全て対応があり、架空のTaskを公式項目として増設していない。一方、1問のcoverageをTaskの全技能習得と同一視しない。

Study Guideへの署名付き参照もレコードにあったが、PDF本文の閲覧には成功していない。したがってPDFの参考文献・細目・sample testとの比較は未完了。この制約はREADMEとmapにも明記する。以後のcollectorは関連する公開試験fieldのみ保存し、連絡先・署名付きURLを除く。

## Executed verification so far

| 対象 | 環境/commit | 観測結果 |
|---|---|---|
| Parserの25件の人工fixture/否定test | local Python 3.13.5 | 25件成功。全教材実行とは別 |
| Python構文確認 | local Python 3.13.5 | 新規・変更scriptのcompile成功。Qiskitはこの環境では未導入 |
| 変更前smoke | CI head `03ea390dbd4eabb49729a82711e41021800a1d4f`, run `34508668632` | Qiskit 2.5.2 / Runtime 0.49.0を導入し実行成功 |
| 全教材validator | CI head `95dc2553fda84204f138aeab6bcb8629c6129b31`, run `34510149269` | 成功。Topic80・Mock68・位置分布・key/解説・domainを検査 |
| 構造回帰test | 同上 | 26件成功（25件のparser test + 実教材全体を読む1件） |
| 新しいSDK smoke初回 | 同上、Python 3.12.14 / Qiskit 2.5.2 / Runtime 0.49.0 / importer 0.6.0 / NumPy 2.5.0 | 15件中14件成功、1件error。期待した例外型が不正だった |
| 公式試験レコード | 同上の別job | 取得成功に加え、今回実内容を読んでObjectivesを照合 |

SDK smokeの1件errorは教材の誤りではなく、今回追加したtest側がmid-circuit拒否を`ValueError`と想定したことが原因。公式2.5.2実装を読んで`QiskitError`と確認し、型とメッセージを検査するよう修正した。検査を削除・skipしたり、任意の例外を成功とする変更ではない。

**この例外型修正・追加の2問差し替えを含むheadのCI結果は、そのheadのActions runで確認する。本ファイルに未実行の結果を合格として固定しない。**

## Remaining boundaries

Study Guide PDFの詳細は未確認。実Runtime serviceへの送信・job取得、実QPU、hardwareのDD/ZNE/dynamic circuitsは実行していない。API資料・SDK/client testとの境界を維持する。テストが全て合格しても全148問の科学的正しさを自動認定しない。最終merge判断は更新headを対象とする独立レビューに委ねる。

## Primary references

確認日: 2026-09-11。参照時点の公式資料を使う。

- Official Exam Objectives: https://www.ibm.com/training/credentials/getExam/C1000-179
- Certification / Study Guide entry point: https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400
- OpenQASM types/initial states/complex: https://openqasm.com/versions/3.0/language/types.html
- Reset: https://openqasm.com/versions/3.0/language/insts.html
- Gate: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Gate
- Instruction: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Instruction
- BitArray: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray
- Resilience presets: https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management
- PUB/broadcasting: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- REST endpoints: https://quantum.cloud.ibm.com/docs/en/api/qiskit-runtime-rest/tags/jobs
- SDK release: https://github.com/Qiskit/qiskit/releases/tag/2.5.2
- Runtime release: https://github.com/Qiskit/qiskit-ibm-runtime/releases/tag/0.49.0
- StatevectorSampler error type: https://github.com/Qiskit/qiskit/blob/2.5.2/qiskit/primitives/statevector_sampler.py
- Python CI: https://docs.github.com/en/actions/tutorials/build-and-test-code/python
