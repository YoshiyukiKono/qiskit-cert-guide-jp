# 第5章の改稿・検証記録

検証日: 2026-09-15 JST

## 改稿の範囲

[第5章](../ja/05-sampler.md)全体を、各shotの記録から集計を読み、パラメータ条件・測定先・実行設定が変わった場合も判断できる説明へ広げた。第2章の測定、第3章のパラメータと古典レジスタ、第4章の実行先への変換とPUBを土台とする。

| 対象 | 拡充した内容 |
|---|---|
| shotと集計 | ビット列の記録、counts、相対度数の対応。有限回数の揺らぎ、出現しなかった結果、相対位相をcountsだけでは区別できない例 |
| PUBと条件 | 一つのPUBに複数の角度を渡す例。入力のパラメータ軸と結果の条件の軸、各条件のshots、条件を省略した集計の違い |
| 複数パラメータ | qc.parametersの順とゲートの記述順の違い、値の各行が指定する組合せ |
| shotsの指定 | ローカルSamplerでの優先順位、Runtimeの生成と設定、異なるshotsを同じjobへ混在させる指定の非推奨化、twirlingの配分との関係 |
| 古典レジスタ | 量子ビットから保存先への対応、文字列とslice_bitsのビット順、複数レジスタの同じshot同士を対応させた相関の集計 |
| DD | 待機中の位相のずれ、Xの共役変換、時間間隔を含む行列計算、X基底測定の確率、モデルの限界とRuntimeへの指定 |
| 機能の併用 | 動的回路、DD、fractional gatesの条件。SDKでの構築・設定、実行先への変換、サービスの条件の区別 |

既存の明示アンカー5個とH2見出し7個を維持し、DDの参照用アンカーを追加した。章末には条件を変えた8問と理由付き解答を設けた。特定のMockへの言及や問題・解答へのリンクは本文に加えていない。全角括弧は強調の外へ出している。

[第6章](../ja/06-estimator.md)には、DDの途中計算への参照と、Runtime 0.49.0では異なるprecisionのPUBを同じjobへ混在させる指定も非推奨であることを補った。第6章のコード例は変更していない。

## 実行環境と再実行

Python 3.12.14 / Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0 / NumPy 2.5.3 / Matplotlib 3.11.2 / pylatexenc 2.11 / Pillow 12.3.0を使用した。[既存の依存パッケージ](requirements.txt)を使い、追加インストールは行っていない。

リポジトリのルートで次を実行する。

```text
python -X utf8 -B manuscript/validation/verify_chapter5.py
node manuscript/validation/verify_manuscript_render.cjs
git diff --check
```

[第5章の検証スクリプト](verify_chapter5.py)は本文のPythonブロックを直接読み取り、出力付きの8例を独立した名前空間で実行し、掲載出力と比較する。Runtimeの2個の関数例は、定義だけでは実行を開始しない構造を検査してから、ローカルbackendで試す。検証中のネットワーク接続は遮断する。

図は一時ディレクトリに生成する。掲載PNGを更新する場合だけ、次を使う。

```text
python -X utf8 -B manuscript/validation/verify_chapter5.py --write-figures
```

## 確認結果

| 確認 | 結果 |
|---|---|
| 掲載出力 | 8例すべてを独立実行し、掲載した記録・辞書・shape・確率と一致 |
| 理論確率と集計 | Bell状態の確率、各shotの記録を数えたcounts、位相の異なる状態が同じ計算基底の確率を与えることを照合 |
| 条件の軸 | 3条件・各32shots・1bitと、全条件を合算した96記録を区別。2パラメータ・5条件へ変えた例も実行 |
| パラメータ順 | a・zの順とゲートの記述順を区別し、複数の非自明な角度で状態とテンソル積の計算を照合 |
| 入力の誤り | shotsをPUBの2番目へ置く指定と、Samplerのrunへprecisionを渡す指定のエラーを確認 |
| 保存先とビット順 | q2→readout[0]、q0→readout[1]の対応とslice_bitsを検査。章末のq3・q1への変更も実行 |
| 同時測定の相関 | 同じshotの各レジスタの記録を結合し、反相関を確認。各レジスタの分布が同じでも、同時分布は異なり得る反例も検査 |
| DDの行列 | X Rz(α) XとRz(−α)、対称な待機時間でのXX列と恒等行列を複数の角度で照合。連続するXXやずれの速さが変わる場合の反例も計算 |
| DDの測定と図 | Hを含めた状態とcos²(φ/2)の確率、理想XX列での確率1、図の曲線との対応、正負のπ回転と全体位相を確認 |
| Runtimeのローカル実行 | GenericBackendV2と実際のSamplerV2を使い、別jobでの128・256・500shots、およびDD指定関数の32shotsの結果を取得 |
| Runtimeへの指定 | runの呼出しを記録し、DDのenable・XY4、shots、変換後の命令のtarget適合を検査。入力回路が変更されないことも確認 |
| 非推奨指定 | Runtimeの送信処理を代替して、異なるshotsと異なるprecisionのPUBを一つのrunへ渡すと、それぞれ非推奨警告が出ることを確認。掲載関数からは非推奨警告が出ない |
| Markdown/KaTeX | 第5章70式・5表、第1〜6章の合計1,529式が変換を通過 |
| 参照・体裁 | 既存アンカーとH2見出しを維持。manuscript配下と既存解答からのローカルリンク、図の存在、強調の括弧の配置、空白を確認 |

掲載コードから生成したPNGを開き、図の内容と文字の欠け・重なりを確認した。

- [古典レジスタへの保存](../ja/figures/05/05-readout-register.png): q2の測定を古典ビット0、q0の測定を古典ビット1へ保存する対応を照合した。
- [DDの理想モデル](../ja/figures/05/05-dd-echo-model.png): T/4と3T/4のXパルス、同じ合計待機時間、位相のずれとX基底測定の確率の関係を確認した。理想モデルの計算であり、実機でのDDの性能測定ではないことを本文に明記した。

PNGの目視確認とMarkdown・KaTeXの変換を行った範囲であり、VS CodeのプレビューやPDF全ページの組版を確認したという意味ではない。

## ローカル検証の限界

この環境にはqiskit-aerを導入していない。GenericBackendV2での実行には、`Aer not found using BasicSimulator and no noise`という警告が出る。小規模回路をノイズなしで実行し、入出力の接続と測定回数を確認した。

Runtimeのローカル実行では、DDとtwirlingの設定に`have no effect in local testing mode`という警告も出る。設定が関数から正しく渡ることと、実機でその設定が誤差を抑えることは別である。twirlingによるshotsの配分や、サービス側の機能の併用条件は、この実行から実証したものではない。

アカウントへの接続、実機backendの取得、QPUへの送信は行っていない。DDの数値検証は本文のモデルと導出を補助するものであり、実機のすべてのノイズに対する保証や、有限個の角度による数学一般の証明として扱わない。

## 参照資料と対象版

本文の実行対象はQiskit 2.5.2 / qiskit-ibm-runtime 0.49.0である。以下のAPI URLはlatest版であり、ページ全体をそのパッケージ版で固定された資料とは扱わない。掲載例の引数・戻り値・非推奨警告・DDの設定項目は、導入済みの基準版のシグネチャ・docstring・実装と実行結果でも照合した。

- [Sampler input/output](https://quantum.cloud.ibm.com/docs/en/guides/sampler-input-output): PUBの3要素、条件の軸、古典レジスタごとのBitArray。掲載コードの依存条件は`qiskit[all]~=2.5.2` / `qiskit-ibm-runtime~=0.47.0`。
- [Sampler options](https://quantum.cloud.ibm.com/docs/en/guides/sampler-options): shotsの優先順位、twirlingの固定した回数の積が要求shotsより小さい場合の条件、機能の組合せ。掲載コードの依存条件は`qiskit[all]~=2.5.2` / `qiskit-ibm-runtime~=0.47.0`。
- [StatevectorSampler](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler) / [BitArray](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray): ローカルSampler、get_counts・get_bitstringsの条件の位置、ビット数・shots数・shape・slice_bitsの意味。
- [Runtime release notes](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/release-notes): 0.48.0での、Samplerの異なるshotsとEstimatorの異なるprecisionの同一jobへの混在の非推奨化。基準版0.49.0でも警告を照合した。
- [DynamicalDecouplingOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-dynamical-decoupling-options): XX・XpXm・XY4の符号を含むパルス列、スケジューリング、余った待機時間の配分。
- [TwirlingOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-twirling-options): 有効化、randomizationsと各変種のshotsの指定。
- [Error mitigation and suppression techniques](https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques): DDの目的とパルスの誤差による限界、Pauli twirlingの考え方。掲載コードの依存条件は`qiskit-ibm-runtime~=0.47.0`。本文のDDの途中計算と図は、本書の仮定を明示した例として構成した。

公式ガイドのPackage versionsは、そのページのコードの依存条件であり、本書の実行対象のRuntime 0.49.0とは分けて記録する。動的回路とDDの併用条件など、サービスに依存する情報を、この依存条件だけで固定された仕様とは扱わない。本文には適用条件を記し、確認日は本記録へ集約した。
