# 第7章の改稿・検証記録

検証日: 2026-09-15 JST

## 改稿の範囲

[第7章](../ja/07-results-analysis.md)全体を、jobの状態確認、対象条件の選択、統計的な判断、記録の保存へ順に進める内容へ広げた。第5章の測定記録と第6章の期待値を土台とする。

| 対象 | 拡充した内容 |
|---|---|
| jobの取得と待機 | runとresultの役割、結果の再取得と再実行の違い、ローカルとRuntimeのstatusの型、過去jobの取得と検索、最終状態と正常終了、待機時間切れと実行失敗 |
| 結果の階層 | 2PUBのうち一つだけが3条件を持つ例、PUB番号・レジスタ・条件・shotsの区別、SamplerPubResultとPubResultの関係 |
| 条件別の集計 | 二つのパラメータを2×2の条件へ割り当てる例、get_countsの位置指定、条件を省略した集計、shotsが違う集計の重み |
| 対角な観測量 | 記録したビットとZの固有値の対応、ZI・IZ・ZZの表、手計算とexpectation_values、測定基底や保存先の前提 |
| 統計的な不確かさ | ベルヌーイ変数から平均の分散を導く過程、標準偏差と標準誤差、置換による推定、shotsとSEの関係、正規近似の95%区間 |
| 境界での推定 | 出現0回でも確率0と断定できない理由、二項分布の確率、Clopper–Pearson区間と0回の場合の上端の計算 |
| 結果の比較 | 二つの独立な推定値の差と標準誤差、差の区間、原因や実用上の良否との区別、独立性と多数の比較の注意 |
| Estimatorの解釈 | 単一Pauli測定の標準誤差との接続、状態ベクトルでのstds=0、Runtimeの誤差軽減と不確かさの項目、目標precisionとの違い |
| 記録 | 結果全体とPUBごとのmetadata、ラベルと操作の違い、JSONへの測定記録の保存、QPYへの回路保存、比較の根拠となる入力と条件 |

既存の明示アンカー5個とH2見出し6個を維持した。比較とEstimatorの不確かさへの参照用アンカーを追加し、章末には条件を変えた10問と理由付き解答を設けた。特定のMockへの言及・問題や解答へのリンクは本文へ加えていない。全角括弧は強調の外へ出している。

[第2章](../ja/02-visualization-measurement.md#measurement-plots)からの案内を、標準誤差の推定と区間を使う比較へ具体化した。[第6章](../ja/06-estimator.md#estimator-result)には、比較例と記録の保存への参照を補った。両章のコードは変更していない。第5章から経験確率の節への既存リンクも維持した。

## 実行環境と再実行

Python 3.12.14 / Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0 / NumPy 2.5.3 / SciPy 1.18.1 / Matplotlib 3.11.2 / Pillow 12.3.0を使用した。[既存の依存パッケージ](requirements.txt)を使い、追加インストールは行っていない。

リポジトリのルートで次を実行する。

```text
python -X utf8 -B manuscript/validation/verify_chapter7.py
node manuscript/validation/verify_manuscript_render.cjs
git diff --check
```

[第7章の検証スクリプト](verify_chapter7.py)は、本文のPythonブロックを直接読み、出力付きの10例を独立した名前空間で実行して掲載出力と比較する。Runtimeの3関数は、定義時に処理を開始しない構造を検査したうえで、ローカルに用意した応答を使って検証する。検証中のネットワーク接続は遮断する。

図とJSON・QPYは一時ディレクトリへ生成する。掲載PNGを更新する場合だけ、次を使う。JSON・QPYの例示出力をリポジトリへ複製する指定ではない。

```text
python -X utf8 -B manuscript/validation/verify_chapter7.py --write-figures
```

## 確認結果

| 確認 | 結果 |
|---|---|
| 掲載出力 | 10例を独立実行し、掲載した状態、型名、辞書、shape、確率、区間、保存内容と一致 |
| ローカルjob | resultの再取得が同じ結果を返し、新たな標本を生成しないこと、完了後のJobStatusを確認 |
| Runtimeの状態 | サービス応答をローカルで代替し、RuntimeJobV2の実際のメソッドを使って6状態を確認。DONEだけで結果を取り出し、ERRORでは理由を表示 |
| job検索 | 基準版のシグネチャと引数を照合。backend_name、pending、limit、descendingの指定、成功・失敗・取消しを含む応答、空の応答を検査 |
| 待機と失敗 | 実際のresultとwait_for_final_stateを使い、timeout=0で待機を打ち切る分岐を検査。cancelが呼ばれないこと、同じIDが後で完了した場合の結果取得、実行失敗・実行時間超過・取消し・通信例外の伝播を確認 |
| PUBと条件 | 2PUBと一方の3条件、各64shotsを確認。2×2の条件と合算を照合し、2×3・各200shotsへ変えた章末の条件も実行 |
| 観測量と保存先 | ZI・IZ・ZZの固有値の行列とcountsによる平均を照合。XXの入力が拒否されること、ビットの保存先を逆にするとZIとIZの解釈が変わることも確認 |
| 分散の導出 | 1・4・7回の0/1列を全列挙し、複数のpで確率を付けて平均と分散を直接計算。p(1−p)/N、Pauliの平均への変換、SEのshots依存と一致 |
| 区間の計算 | 240/1000の正規近似、0/100のClopper–Pearson区間と閉じた式の上端、100/100との対称性を照合。N=20の全出現回数と複数のpで、exact区間が真値を含む確率も確認 |
| 差の不確かさ | 独立な二変数の結果を列挙して差の分散を確認。本文の差0.06と約95%区間、同じ記録を二度使う場合の反例を検査 |
| 図の数値 | 各実験の位置と相対度数、点が表示範囲内にあること、真のp、個々の区間と差の区間の端点を計算と照合 |
| Estimator | 期待値1/2と√3/2、stds=0、実際のZ測定での理論確率3/4と1/4を照合 |
| 保存と読込み | JSONの各shotとcounts・shots・shape・パッケージ版・metadataを照合。QPYを読み直し回路とmetadataが一致すること、metadataのラベルだけでは状態が変わらないことを確認 |
| Markdown/KaTeX | 第7章99式・3表、第1〜7章の合計1,628式が変換を通過 |
| 参照と体裁 | 既存アンカー・H2見出し、manuscript配下と既存解答からのローカルリンク、図の存在、強調の括弧の配置、空白を確認 |

図は掲載コードから生成したPNGを開き、文字や点の欠け、ラベルの重なり、軸と凡例を確認した。

- [繰り返す実験とSE](../ja/figures/07/07-repeated-estimates.png): 100・400・1,600shotsの各40実験を、同じ縦軸で表示。一点が一実験の相対度数、帯が既知のpの上下1SEであることを本文に明記した。
- [二つの推定値と差の区間](../ja/figures/07/07-comparison-intervals.png): 個々の推定値と差の区間を分け、右図に差0の基準線を置いた。棒が正規近似による約95%区間であることを図中と本文の両方へ記した。

PNGの目視確認とMarkdown・KaTeXの変換を行った範囲であり、VS CodeのプレビューやPDF全ページの組版を確認したという意味ではない。

## 検証の前提と限界

Runtimeの関数は、認証、実サービスの検索、待ち行列、実機の実行を試したものではない。基準版のRuntimeJobV2へローカルな応答を与え、実際のstatus・result・wait_for_final_state・error_messageの処理を検証した。service.jobsの検証は、引数と返された一覧の扱いの確認であり、サービス側の検索処理を再現するものではない。QPUへの送信は行っていない。

待機の検証ではtimeout=0を使い、実時間の長い待機は行っていない。Runtime 0.49.0のresultから呼ばれるwait_for_final_stateがRuntimeJobTimeoutErrorを送出することを実装で確認した。resultのAPI説明に挙がるRuntimeJobMaxTimeoutErrorとは区別し、サービスの実行時間超過を表す分岐も別に検査した。

統計の式は独立で一定の確率という前提を持つ。正規近似と二項分布に基づく区間を区別し、実機の偏り、時間変化、校正の共有、誤差軽減後の複雑な推定を、単純な二項モデルだけで検証したとは扱わない。有限個の数値での確認は、本文の導出を補助するものであり、すべての標本サイズ・確率に対する数学的な証明を代替しない。

## 参照資料と対象版

APIのURLはlatest版であり、ページ全体をQiskit 2.5.2 / Runtime 0.49.0で固定された資料とは扱わない。引数、戻り値、例外、結果の形式は導入済みの基準版の実装と実行結果でも照合した。

- [QiskitRuntimeService](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service): jobの取得とjobsの検索条件。
- [RuntimeJobV2](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/runtime-job-v2): 文字列のstatus、最終状態、result、wait_for_final_state、error_message、待機と失敗時の処理。
- [Primitive inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output): PUBと結果の対応、条件のshape、実装による項目の違い。掲載コードの依存条件は`qiskit[all]~=2.5.2`。
- [BitArray](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray): get_counts・get_bitstringsのloc、条件の軸、from_counts、対角observableのexpectation_values。
- [Estimator inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output): evsと不確かさの項目、twirling・ZNEによる計算方法、結果全体とPUBごとのmetadata。掲載コードの依存条件は`qiskit[all]~=2.5.2` / `qiskit-ibm-runtime~=0.47.0`。
- [SciPyのproportion_ci](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html): confidence_levelとmethod、exactがClopper–Pearson法を表すこと。参照先はSciPy 1.18.0のマニュアルとして表示され、本書の実行は1.18.1で照合した。
- [NISTの二項比率の信頼区間](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm): 二項分布に基づく区間と近似の背景。パッケージ版による限定を付ける資料ではない。
- [QPY](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qpy): 回路の保存・読込み、形式の版と互換性。

公式ガイドのPackage versionsは掲載コードの依存条件であり、ガイド全体の版とは読み替えない。確認日は本記録へ集約し、本文では実装の基準版、統計モデルの前提、サービスへの依存を示した。
