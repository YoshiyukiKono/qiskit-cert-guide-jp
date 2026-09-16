# 第3章の改稿・検証記録

検証日: 2026-09-15 JST

## 改稿の範囲

[第3章](../ja/03-circuit-construction.md)全体を、目的から回路を組み立て、出力から設計を確認する説明へ広げた。第1・2章の状態・ゲート・測定を土台とし、APIの構文と、それを選ぶ理由を結び付けている。

| 対象 | 拡充した内容 |
|---|---|
| 量子・古典ビット | 操作に必要な個数と保存する結果の個数、レジスタ名と結果の項目、構築と実行の区別 |
| 測定mapping | 一部の測定、ビットの並べ替え、measure_allの保存先と既定値、途中の結果の上書き |
| 合成と部品化 | 部品のビットと本体の対応、操作の時間順序、戻り値と変更、GateとInstruction、qargsとcargs |
| 逆操作・制御 | 積の逆行列と逆回路、不可逆な操作、制御と標的の対応、量子制御と測定後の条件分岐 |
| パラメータ | 回転角と確率、雛形の再利用、名前順とゲートの登場順、部分束縛、共通記号と式 |
| 動的回路 | flagとreadoutの分離、if/else、構築時と実行時、分岐確率、混合とBell状態の違い、回路内のループ |
| 実行の境界 | 構造・理想的動作・実行先の対応を区別する確認手順、StatevectorSamplerの対応範囲 |

既存の明示アンカー6個とH2見出し7個を維持し、節ごとの確認問題と理由付き解答、条件を変えた章末6問を加えた。本文は特定のMockや問題番号を前提にしていない。

回路の合成と動的回路の2枚の図を追加し、ビットの対応と測定結果の保存先を図からも確認できるようにした。

## 実行環境と再実行

Python 3.12.14 / Qiskit 2.5.2 / NumPy 2.5.3 / Matplotlib 3.11.2 / pylatexenc 2.11を使用した。追加の依存パッケージはなく、[既存の検証環境](requirements.txt)を使う。qiskit-ibm-runtime 0.49.0は既存章の検証に使用し、第3章のコードはRuntimeへ送信しない。

リポジトリのルートから実行する。

```text
python -X utf8 -B manuscript/validation/verify_chapter3.py
node manuscript/validation/verify_manuscript_render.cjs
python -X utf8 -B manuscript/validation/verify_sample_sections.py
git diff --check
```

[第3章の検証スクリプト](verify_chapter3.py)は、掲載コードと直後の出力を抽出し、各例を独立した名前空間で実行する。図は一時ディレクトリへ保存する。掲載するPNGを更新したい場合だけ、`--write-figures`を指定する。

## 確認結果

| 確認 | 結果 |
|---|---|
| 掲載コード | 全14例を独立して実行し、掲載出力と一致 |
| 測定と保存先 | 一部の測定、入れ替えた対応、新規・既存レジスタへの保存、保存先不足、章末の4量子ビットの例を確認 |
| 合成・部品化 | 真理値表から独立に作ったCX行列とテンソル積により、3量子ビット全体の合成行列を照合。frontの時間順序、量子・古典ビットの対応も確認 |
| 逆操作・制御 | 複素共役転置と恒等行列を照合し、測定・resetの逆操作とゲート化が拒否されること、制御と標的を逆にした場合の行列を確認 |
| パラメータ | 掲載値と別の角度を解析式と比較。辞書・リスト・部分束縛・同じ記号を使う式・ParameterVectorの順序を確認 |
| 動的回路 | 射影で各分岐の確率と状態を求め、掲載回路に記録された条件と操作対象を照合。if/elseの同時確率、混合とBell状態の違い、条件付きXをZへ変えた問題も確認 |
| 実行手段の境界 | 固定ループの合成行列を確認。StatevectorSamplerが途中測定と制御フローを拒否することを確認 |
| Markdown/KaTeX | 第3章165式・7表を含め、第1・2・3・6章の計1,371式が変換を通過 |
| 既存章の回帰確認 | 第1章・第6章の掲載コード23例と、既存の数式・動作の照合が通過 |
| 参照と体裁 | 元のH2見出し7個と明示アンカー6個を維持。本文・図・検証記録・解答からのローカルリンク、強調の括弧の配置、空白を検査 |

図は掲載コードから生成したPNGを開き、文字・操作・測定先に欠けや重なりがないことを目視確認した。

- [合成と量子ビットの対応](../ja/figures/03/03-compose-mapping.png): 本体のq1のX、部品から写したq2のHとCX制御、q0の標的を確認。異なる量子ビットのHとXが同じ列に描かれる理由も本文へ補った。
- [古典的フィードフォワード](../ja/figures/03/03-feedforward.png): flagへの途中測定、値1を使う条件、q1のX、別のreadoutへの最終測定を確認。条件ラベルの16進数表記も本文で説明した。

数値検証は本文の導出を補助するものとし、有限個の入力を使うチェックを一般的な証明の代わりとは扱っていない。図の確認はPNG自体の確認であり、VS CodeやPDFの全ページの組版確認を行ったという意味ではない。

## 参照資料と対象版

次のAPIリファレンスはURLに版を含まないlatest版であり、ページ全体をQiskit 2.5.2で固定された資料とは扱っていない。対象のAPIの引数・既定値と動作は、導入済みQiskit 2.5.2のdocstring・実装および上記コードの実行でも照合した。

- [QuantumCircuit API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit): レジスタ、measure/measure_all、compose/append、inverse、to_gate/to_instruction、assign_parameters、制御フロー。Web取得ではページの容量制限があったため、検索で確認できる記載に加え、導入済みSDKのドキュメントと実装を照合した。
- [Gate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Gate): ユニタリなゲート、制御ゲート化とInstructionとの区別。
- [Parameter](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Parameter): 数値を未定にした記号と、実行時の値を定める必要。
- [StatevectorSampler](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler): 状態ベクトルを使うサンプリングと、途中測定の非対応。
- [回路の構築](https://quantum.cloud.ibm.com/docs/en/guides/construct-circuits): 回路を組み立てる基本操作。掲載コードの依存条件は`qiskit[all]~=2.5.2`。更新されるガイドであり、本文の例は本書の基準版で独自に構成・検証した。
- [古典的フィードフォワードと制御フロー](https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow): ガイドの掲載コードの依存条件は`qiskit[all]~=2.5.2`。if/else・switch・for/whileを回路へ記録する方法を参照した。
- [動的回路の実行](https://quantum.cloud.ibm.com/docs/en/guides/execute-dynamic-circuits): SDKの表現能力とサービス・実機の対応を分けるための参照先。ガイドが示すサービス側の制御フローの対応はif。掲載コードの依存条件は`qiskit[all]~=2.5.2` / `qiskit-ibm-runtime~=0.47.0`で、本書の検証環境のRuntime 0.49.0とは区別した。特定のbackendでの実行を今回確認したわけではない。
- [Samplerの機能の組合せ条件](https://quantum.cloud.ibm.com/docs/en/guides/sampler-options#feature-compatibility): 更新されるサービス側の条件の参照先。掲載コードの依存条件は`qiskit[all]~=2.5.2` / `qiskit-ibm-runtime~=0.47.0`。

数学上の恒等式、状態の変化、分岐の確率には、SDKの版や確認日による限定を付けていない。動的回路は構造の検査と、射影による各分岐の独立した理想計算を行う。実QPUや動的回路対応シミュレータでの回路全体の実行は、この検証には含めない。
