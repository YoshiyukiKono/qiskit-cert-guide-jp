# 第6章の追加改稿と検証

検証日: 2026-09-14 JST

この記録の検証数は第6章改稿時点のもの。後続の検証追加と現在の再実行範囲は[基底変換の改稿記録](conjugation-revision-2026-09-14.md)を参照する。

## 対象と説明の設計

[編集方針](../editorial-policy.md)に従い、[第6章 Estimator V2](../ja/06-estimator.md)のうち、見本として改稿済みのbroadcasting以外の節と章末チェックを拡充した。broadcastingの説明を基準にし、略語の意味、計算の途中経過、設定の目的、出力の読み方を補った。読者が行った強調の調整は、そのまま反映している。

| 節 | 加えた説明と読者が確かめること |
|---|---|
| 期待値を評価する | 測定値と平均、Samplerとの役割の違い、回路と観測量、ローカル実装とQPU実行 |
| Estimator PUB | 各要素の位置と省略、観測量の配列と和、複数PUB、測定の共有、回路と観測量のlayout |
| precision、shots、resilience | 標準誤差の導出、偏りとの違い、ZNEの外挿、TREXの校正、twirlingとDD、presetと個別指定、precisionの優先関係 |
| Estimator result | PUB番号と配列の添字、scalar、期待値と不確かさ、ZNEの追加データ、metadata |
| 章末チェック | 異なる数値や条件で考える8問と理由付き解答 |

ZNEの表と直線当てはめは説明用の仮想データであり、実機の結果として扱わない。TREXの補正式は、対称な読み出し誤差という単純化したモデルの説明と、Runtimeの手法そのものを区別した。本文は特定のMockの受験を前提にせず、問題番号や問題・解答へのリンクを追加していない。

## 再実行方法

Qiskit 2.5.2、qiskit-ibm-runtime 0.49.0、NumPyを入れた環境で、リポジトリのルートから次を実行する。バージョンは既存の[検証用requirements](../../practice-bank/validation/requirements.txt)に合わせている。

```text
python manuscript/validation/verify_sample_sections.py
```

[検証スクリプト](verify_sample_sections.py)は原稿のPythonコードと掲載出力を直接抽出する。この時点では、第6章の全9例と、第1章の改稿済み3例を合わせた12例が対象。broadcastingの後半だけは明記された続きとして実行し、ほかは各例を独立した名前空間で実行する。Runtimeの設定例は仮のbackendで設定を保持するところまでとし、jobの送信は行わない。

## 検証範囲

- Python 3.12.14、Qiskit 2.5.2、qiskit-ibm-runtime 0.49.0、NumPy 2.5.3で掲載コードの出力を照合する。
- PUBの位置指定、precisionの選択、観測量の和、layoutの適用前後の期待値を確認する。非対称な状態を使い、観測する量子ビットを取り違えると値が変わることも照合する。
- ZNEの直線の傾き・切片を別計算で求め、変更条件の設問も確認する。gate foldingの理想演算の同値性と、DDで例示するXXの同値性を行列で照合する。
- 明示的な確率分布から分散を計算し、標準誤差と測定回数の関係、対称な読み出し誤差による平均の縮小と補正を照合する。
- scalarと配列のshape、PUB数、各添字、ローカルの`stds`と一回の測定の分散の違いを確認する。第1章とbroadcastingの既存の数学検証も継続する。
- 原稿内の相対リンクと、既存の解答から原稿への参照を検証する。改稿前の明示アンカーと第2レベル見出しを保つ。
- 第1章・第6章を既存のMarkdown/KaTeX依存で変換し、数式の構文エラーと表示数式の区切りを確認する。

## 検証結果

| 確認 | 結果 |
|---|---|
| 掲載コードと出力 | 第6章9例、第1章3例、計12例が一致 |
| 数式・設定・配列の追加照合 | すべて通過 |
| ローカルリンク | 16個のMarkdownファイル内の206件が通過 |
| Markdown/KaTeX変換 | 第1章・第6章の数式327個で構文エラーなし |
| 参照の継続性 | 第6章の既存の明示アンカー5個と第2レベル見出し6個を維持 |
| 改稿済みbroadcasting | 作業開始時の本文・強調と一致 |
| 差分の空白検査 | `git diff --check`が通過 |

改稿前後の比較とMarkdown/KaTeX変換は、再実行スクリプトとは別に作業時に実施した。

QPU実行、クラウドでの誤差軽減、shotsの割当て、実機結果のmetadataは実測していない。それらの説明は下記の公式資料と照合した。数式の変換は組版構文の検証であり、すべての閲覧アプリでの目視検証ではない。教材としての詳しさは本文と理由付き解答でレビューできるようにしたもので、学習効果を自動検証で保証するものではない。

## APIの一次資料と実装の照合

- [Estimator input/output](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output): PUBと結果、観測量のグループ化、実装に応じた付随情報。
- [Primitive inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output): PUBの4要素とパラメータ配列。
- [StatevectorEstimator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorEstimator): ローカル計算とprecision。
- [SparsePauliOp](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp): 観測量の和と`apply_layout`。
- [Estimator options](https://quantum.cloud.ibm.com/docs/en/guides/estimator-options): precisionの優先関係、`Unset`、機能の組合せ条件。
- [Estimator noise management](https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management): resilience levelと個別指定。
- [Error mitigation and suppression techniques](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques): ZNE、TREX、twirling、DDの仕組み。
- [EstimatorOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-estimator-options)、[TwirlingOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-twirling-options)、[ZneOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-zne-options): 設定値、shotsの単位、ZNEの追加配列。

公式ガイドの「作成時にoptionsをコピーする」という記述に対し、0.49.0の実装では`EstimatorOptions`の入れ子のオブジェクトが共有されることを確認した。本文では元のoptionsの変更が伝わるかを断定せず、作成後の変更先を`estimator.options`に統一する説明とした。twirlingの有効・無効の既定値についてもガイド内の記述が一様でないため、無条件の既定値としては記載せず、presetと個別設定を確認する書き方にした。
