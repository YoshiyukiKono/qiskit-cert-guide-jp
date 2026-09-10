# PR #1 revision record — 2026-09-11

## Scope and provenance

開始head: `4112db1a9e07ec69ab7b23486095e7dbbbd9198d`。
base main: `88c9a83a12383541bb5ca53484afdaa3b15874bb`。
対象ブランチ: `add-v2x-practice-bank`。

開始時にPR metadata、main ref、15変更ファイル、実diffと変更内容を確認した。前回reviewの主張を実装の正解とせず、公式資料と再現可能なテストへ分解した。変更はpractice-bankと検証workflowに限定する。全面的な難易度改訂は対象外。

## Findings disposition

| ID | 再確認と処理 |
|---|---|
| F01 | 確認・訂正。OpenQASM仕様はqubitの初期状態を未定義とする。Topic 08 Q3にresetを追加し、測定前のplus準備を明示。Mock Q66は初期状態を断定しておらず、同じ欠陥とは扱わない |
| F02 | 確認・訂正。Topic 01 A4/A6の正答labelを補い、Topic 03 Q4とTopic 06 Q10のB/Dを選択肢・解説とも交換。正答位置はA20/B21/C21/D18。validatorの集計閾値は緩めていない。旧分布自体を統計的異常と断定しない |
| F03 | 確認・訂正。Gate.controlと基底Instructionを区別。Topic 03 A6 / Mock Q25解説を修正 |
| F04 | 確認・訂正。BitArray.expectation_values(observables)は実在する。Mock Q61のAを「counts取得ではなく必須引数もない」と説明し、正答Cは維持 |
| F05 | 前回指摘の意味を限定。Z ketの厳密な演算なら元からCが正しい。キー誤りとは扱わずMock Q3の問題文に厳密statevectorを明示 |
| F06 | 前回指摘の意味を限定。resilience presetとして元の正答は正しい。個別overrideがない前提と、override可能性を設問・解説へ追加 |
| F07 | 内部mapping訂正。Q15/Q16をstate visualization、Q60をjob monitoringへ対応。T/append/inverse等の未出題を明示。ただし現行Study Guide本文との完全照合は未完了。取得できなかったという事実だけを教材の技術的誤りにはしない |
| F08 | 確認・改修。重複key、空/余分なchoice、空解説、domain誤割当を検出するparserと否定テスト。assert依存を廃止。科学的正しさや分類の意味までは検査しないと明記 |
| F09 | 確認・訂正。Topic 02 Q3/Q4のA/C位置を交換し、BDACの全列周期を解消。頻度とキーは整合。乱数性の証明とはしない |
| F10 | 大規模な出題品質改訂は依頼範囲外として保留。PUBのNone位置とbroadcasting shape例を既存解説・smokeへ補足したが、模試全体の難易度改善済みとはしない |
| F11 | 確認・訂正。OpenQASM complexは実在することをTopic 08 A2へ明示 |
| F12 | 表現を訂正。全行列比較の方針は元から妥当。数値許容誤差内でglobal phaseを区別する比較と明記し、厳密な記号計算とは呼ばない |

## Verification status at this revision

ローカル作業環境はPython 3.13.5。Qiskitは未導入でDNS通信も利用できないため、SDK実行はGitHub Actionsに分離した。構造parserの25件の人工fixture/否定テストとPython構文確認をローカルで実行した。これを実教材全体の検証とは呼ばない。

最初のCI commit `03ea390dbd4eabb49729a82711e41021800a1d4f`のpush run `34508668632`で、Qiskit 2.5.2 / Runtime 0.49.0の導入と、変更前のsmoke scriptの実行成功を確認した。変更前の構造検査は失敗。新規の回帰testファイルはそのcommitにはまだ存在せず、そのstepの失敗を教材不具合と混同しない。

公開IBM試験レコード取得jobも成功し、artifact `public-exam-record-34508668632-1`が生成された。ただし、この記録だけではStudy Guide本文の手動確認は完了していない。

**本訂正後の26件の構造回帰test・15件のSDK/client test・実教材validatorの結果は、この変更を含むheadのActions runで確認する。ここで未実行の結果を合格として固定しない。**

## Remaining acceptance items

- 現在の公式Study Guide本文を読み、Task原文/番号/weightと全出題対応を照合する。内部mappingの訂正とは別の受入項目。
- 修正後headの実行結果を確認する。CIが合格しても全148問の科学的正しさを自動認定しない。
- Runtime serviceや実QPUを使う動作検証は実施していない。API/optionの公式仕様確認とlocal clientテストの境界を維持する。
- 最終merge判断は修正担当の自己評価ではなく、更新headを対象とする独立レビューに委ねる。

## Primary references used to re-evaluate findings

確認日: 2026-09-11。資料の現在性は取得時点のもの。

- OpenQASM types/initial states/complex: https://openqasm.com/versions/3.0/language/types.html
- Reset semantics: https://openqasm.com/versions/3.0/language/insts.html
- Gate: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Gate
- Instruction: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Instruction
- BitArray: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray
- Resilience presets/overrides: https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management
- PUB/broadcasting: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Certification overview (not a substitute for Study Guide): https://www.ibm.com/quantum/blog/qiskit-v2x-developer-certification
- Official SDK release: https://github.com/Qiskit/qiskit/releases/tag/2.5.2
- Official Runtime release: https://github.com/Qiskit/qiskit-ibm-runtime/releases/tag/0.49.0
- Python CI: https://docs.github.com/en/actions/tutorials/build-and-test-code/python
