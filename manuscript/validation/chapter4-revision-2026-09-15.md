# 第4章の改稿・検証記録

検証日: 2026-09-15 JST

## 改稿の範囲

[第4章](../ja/04-transpile-execution.md)全体を、実行先の制約、回路の変換、測定対象の対応、実行と結果取得を順に追える説明へ広げた。第1章の行列・Pauli文字列、第2章の測定、第3章の回路構築・パラメータ・条件分岐を土台とする。

| 対象 | 拡充した内容 |
|---|---|
| preset pass manager | backendとtarget、basis gatesと測定基底の違い、接続と方向、3量子ビットのローカル実行先 |
| 回路の変換 | Hの分解と全体位相の行列計算、3個のCXによるSWAP、routingで命令が増える理由、最適化レベルとdepthの解釈 |
| layout | 最初の割当てとrouting後の対応、final_layout属性とfinal_index_layoutの違い、論理順と物理順の状態、演算子全体の比較 |
| 測定とobservable | 測定先の古典ビットを保つ変換、後からmeasure_allを加える場合、Pauli文字列の並べ替えと幅の拡張、期待値が不変になる理由 |
| 実行モード | Job・Batch・Sessionの具体的な関数、独立した入力と結果に依存する入力、Python側の反復と回路内if_testの違い |
| serviceと実行環境 | backend選択の条件とleast_busyの意味、ローカル計算とRuntime、サービスの利用条件とSDKのAPIの区別 |
| 入出力 | PUB・job・shots・結果の階層、SamplerとEstimatorの入力の違い、Estimator PUBのNoneとprecisionの位置 |
| 次章への接続 | broadcastingの用途を表で示し、配列のshapeの説明は第6章へつなぐ |

明示アンカー7個とH2見出し8個を維持した。章末に条件を変えた7問と理由付き解答を設け、特定のMockへの言及や問題・解答へのリンクは本文へ加えていない。全角括弧は強調の外へ出している。

## 実行環境と再実行

Python 3.12.14 / Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0 / NumPy 2.5.3 / Matplotlib 3.11.2 / pylatexenc 2.11 / Pillow 12.3.0を使用した。[既存の依存パッケージ](requirements.txt)を使い、追加インストールは行っていない。

リポジトリのルートで次を実行する。

```text
python -X utf8 -B manuscript/validation/verify_chapter4.py
node manuscript/validation/verify_manuscript_render.cjs
git diff --check
```

[第4章の検証スクリプト](verify_chapter4.py)は、本文のPythonブロックを直接読み取り、独立した名前空間で実行する。出力付きの9例は掲載出力と比較する。4個の関数例は、定義時に実行を開始しない構造を検査してから、ローカルbackendまたはサービスの代替オブジェクトを使って検証する。検証中のネットワーク接続は遮断する。

図は一時ディレクトリに生成する。掲載PNGを更新する場合だけ、次を使う。

```text
python -X utf8 -B manuscript/validation/verify_chapter4.py --write-figures
```

## 確認結果

| 確認 | 結果 |
|---|---|
| 掲載出力 | 9例すべてを独立実行し、掲載値・辞書・型名と一致 |
| ゲートの等式 | SXの行列の二乗とX、Rz・SXによるHの分解と全体位相、3個のCXとビット交換の行列を照合 |
| ISAへの適合 | 変換後の命令と量子ビットの組をtargetへ照合。接続にないCXが残っていないことを確認 |
| 回路全体の作用 | 最初の配置を3通りに変え、ビットの対応から独立に構成した置換行列を使って、変換前後の演算子を比較 |
| observable | routing後の位置、2から3量子ビットへの幅の拡張、複数Pauli項と複素振幅を含む例の期待値を確認 |
| 最適化 | レベル0〜3の出力を掲載値と比較し、全レベルで恒等操作を保つことを行列で確認 |
| 測定 | 物理量子ビットから古典ビットへの対応を検査し、全出力文字列の理想確率を照合。変換後にmeasure_allを加えた場合の反例も実行 |
| PUBと結果 | 2PUB・各16shotsの階層を検査。精度を4番目へ置く指定と、誤って3番目へ置いた場合のエラーを確認 |
| Runtimeのローカル実行 | 実際のSamplerV2・Batch・SessionをGenericBackendV2で動かし、Jobの結果、独立した2job、結果を使う2段階の反復を確認 |
| Runtimeの処理順 | 呼出しを記録する代替オブジェクトで、Batchが両方の送信後に結果を待つこと、Sessionが前の結果後に次を送ることを確認。更新の両方向と半分ちょうどの境界も検査 |
| backend選択 | サービスの代替オブジェクトで、最小量子ビット数、operational、simulatorの引数と戻り値を確認 |
| Markdown/KaTeX | 第4章88式・7表、第1・2・3・4・6章の合計1,459式が変換を通過 |
| 参照・体裁 | 明示アンカー・H2見出しを維持。manuscript配下と既存解答からのローカルリンク、図の存在、強調の括弧の配置、空白を確認 |

図は掲載コードから生成したPNGを開き、文字、命令、制御と標的、測定先に欠けや重なりがないことを確認した。

- [変換前後の回路](../ja/figures/04/04-transpile-before-after.png): Hの分解、全体位相、SWAPを表す3個のCX、最後の隣接CXを確認。上下の回路で文字が過大になったり、ラベルが切れたりしないよう描画領域を調整した。左端の割当てが初期layoutであることと、図の√XがSXであることを本文に補った。
- [配置と測定先](../ja/figures/04/04-layout-readout.png): p1→古典ビット0、p0→古典ビット1、p2→古典ビット2という対応を照合した。

PNGの目視確認とMarkdown・KaTeXの変換を行った範囲であり、VS CodeのプレビューやPDF全ページの組版を確認したという意味ではない。

## ローカル検証の限界

この環境にはqiskit-aerを導入していない。GenericBackendV2を使うRuntimeのローカル実行では、`Aer not found using BasicSimulator and no noise`という警告が出る。BasicSimulatorへの切替えを記録したうえで、ノイズを含まない小規模回路として実行結果を確認した。

Session・Batchのローカル実行は、サービスでの専有、優先、待ち行列、時間上限を再現する検証ではない。アカウントへの接続、実機backendの取得、QPUへの送信、実機でのノイズや利用条件の確認は行っていない。サービス選択関数の検査も引数と処理の接続を確かめるもので、認証の成功を確認したものではない。

数値検証は本文の導出を補助する。特定の入力を調べることと演算子全体を比較することを区別し、有限個の計算結果を数学一般の証明とは扱わない。

## 参照資料と対象版

本文の実行対象はQiskit 2.5.2 / qiskit-ibm-runtime 0.49.0である。以下のAPI URLはlatest版であり、ページ全体をそのパッケージ版で固定された資料とは扱わない。掲載例が使う引数・戻り値・動作は、導入済みの基準版のシグネチャ・docstring・実装と実行結果でも照合した。

- [Transpile to ISA circuits](https://quantum.cloud.ibm.com/docs/en/guides/transpile): targetへの適合、変換の各段階と役割。
- [GenericBackendV2](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.providers.fake_provider.GenericBackendV2): 構成、basis_gates、coupling_map、noise_info、ローカル実行先の作成。
- [TranspileLayout](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.transpiler.TranspileLayout): initial_index_layout、final_index_layout、routingの置換と入力からの最終対応の違い。
- [Execution modes](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes): Job・Session・Batchの用途、最初のjobの待ち行列、Batchの順序や専有についての条件。
- [Run jobs in a session](https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-session) / [Run jobs in a batch](https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-batch): modeへの指定、コンテキストの終了とjobの取消しの違い、max_timeとサービスの制約。掲載コードの依存条件は両方とも`qiskit[all]~=2.5.2` / `qiskit-ibm-runtime~=0.47.0`で、本書の実行対象のRuntime 0.49.0とは分けて扱う。Sessionのページにはさらに`scipy~=1.17.1`がある。
- [QiskitRuntimeService](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service): 保存したアカウントからの初期化、least_busyの条件と選択基準。
- [Set up your IBM Cloud account](https://quantum.cloud.ibm.com/docs/en/guides/cloud-setup): アカウント・instance・保存した設定と接続の前提。本文からのセットアップの参照先として確認した。
- [Local testing mode](https://quantum.cloud.ibm.com/docs/en/guides/local-testing-mode): ローカルで再現される処理と、サービスの実行枠や設定の効果の違い。掲載コードの依存条件は`qiskit[all]~=2.5.2` / `qiskit-ibm-runtime~=0.47.0` / `qiskit-aer~=0.17`。本書の検証環境にはAerがなく、前述のBasicSimulatorへの切替えを使った。
- [Primitive inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output): PUB、run、job、結果オブジェクトの対応。掲載コードの依存条件は`qiskit[all]~=2.5.2`。更新されるガイドとして参照し、掲載例は本書の基準版で独自に構成・検証した。

公式ガイドのPackage versionsは、そのページのコードの依存条件を表す。Sessionの利用プランや時間上限などのサービス情報を、その依存条件だけで固定された仕様とは扱っていない。本文には適用条件を記し、確認日は本記録へ集約した。
