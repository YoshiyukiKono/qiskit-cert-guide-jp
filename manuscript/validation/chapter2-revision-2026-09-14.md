# 第2章の改稿・図版検証記録

検証日: 2026-09-14 JST

## 改稿の範囲

[第2章](../ja/02-visualization-measurement.md)を、測定の目的から回路を作り、結果と図を解釈する流れへ拡充した。「測定と基底」「状態を描く」を重点的に改稿し、他の節も同じ流れにつなげた。[編集方針](../editorial-policy.md)に今回の範囲と、実際の図を使う方針を記録した。

| 対象 | 拡充した内容 |
|---|---|
| 測定と基底 | 射影と正規化、結果の確率と測定後状態、連続測定と再準備、Z・X・Y測定の回路、測定後の基底の復元、Bell状態の部分測定 |
| Statevector | 振幅・理論確率・サンプルの違い、measureとsample_countsの違い、測定前の準備回路とcounts用回路の使い分け |
| bitstringとcounts | 保存先を追う例、左右の取り違えに気付ける非対称な入力、経験確率と期待値、未観測の結果の扱い |
| 回路図 | 制御・標的・古典ビットの読み方、barrier、同じ回路の表示順を変えた比較、図から測定分布を予測する過程 |
| 測定分布 | 回数と比率の比較、shots数を残す必要、標本の揺らぎと理論値、分布だけから位相を判断できない理由 |
| 状態図 | qsphereの位相差、Bloch座標の導出、密度行列と混合、部分トレースと相関、city plotの対角・非対角要素 |
| 判断手順と章末問題 | 目的・測定・データ・軸・図の限界を順に確認する手順、条件を変えた6問と理由付き解答 |

第1章の導出へ参照を付けつつ、測定結果の記録と、その後の量子状態を別々に追える構成にした。例えばH→Z測定と、理想的なX射影測定は同じ結果の確率を与えるが、測定後状態まで対応させるには最後にHを加える必要があることを明示した。

Bloch球の中心をもつれの無条件な判定に使わないよう、全体の純粋性が既知の場合と、各量子ビットの図だけを見る場合を区別した。対角以外の密度行列要素も、もつれの一般的な判定条件にはしていない。

既存の明示アンカー6個とH2見出し8個を維持した。特定のMockや問題番号への言及・リンク、本文中の日付による仕様の限定は追加していない。

## 実行環境と再実行

Windows上のPython 3.12.14の一時仮想環境を使った。主要な依存関係は[requirements.txt](requirements.txt)に記録した。

| パッケージ | 確認した版 |
|---|---|
| Qiskit | 2.5.2 |
| NumPy / SciPy | 2.5.3 / 1.18.1 |
| Matplotlib | 3.11.2 |
| pylatexenc / seaborn / Pillow | 2.11 / 0.13.2 / 12.3.0 |
| qiskit-ibm-runtime | 0.49.0。第1章・第6章の既存検証用。第2章のコードでは不使用 |

リポジトリのルートで、検証用の環境へ依存関係を導入して実行する。

```text
python -m pip install -r manuscript/validation/requirements.txt
python -B manuscript/validation/verify_chapter2.py
python -B manuscript/validation/verify_sample_sections.py
node manuscript/validation/verify_manuscript_render.cjs
```

第2章の[検証スクリプト](verify_chapter2.py)は、原稿から13個のPythonコードと直後の掲載出力を抽出し、それぞれを独立した名前空間で実行する。図は一時ディレクトリへ生成する。原稿に掲載するPNGも更新する場合は、次を実行する。

```text
python -B manuscript/validation/verify_chapter2.py --write-figures
```

`--write-figures`を付けた場合だけ、生成したPNGを`manuscript/ja/figures/02/`へコピーする。図を作るための別の状態データや非公開の編集処理は使わず、掲載コードをそのまま再実行する。

数式の変換には[既存のMarkdown検証](verify_manuscript_render.cjs)を使い、対象に第2章を追加した。依存関係は`references/html-pdf`のMarkdownIt 15.0.2、markdown-it-texmath 1.0.0、KaTeX 0.18.7を利用する。

## 数学・コードの照合

| 対象 | 照合方法 |
|---|---|
| 射影測定 | 0・1・±・±iと不均等な複素振幅について、Z・X・Yの直接射影と基底変換後の確率を比較 |
| 測定後の状態 | 各射影を正規化し、基底変換→Z測定→復元の状態と同値であることを確認 |
| 連続測定 | Z→Zの同一結果と、Z→Xの半々の分岐を照合。章末問題の同時確率を解析的に計算 |
| measure | seedを変えて0・1の両分岐を実行。元のStatevectorが変化しないこと、戻り値の状態が対応することを確認 |
| 部分測定 | Bell状態のq0を測った両分岐について、全体が00または11となることを照合 |
| 位相と相関 | Phi+・Phi−へH⊗Hを適用した確率、古典的混合との違い、XXの期待値を照合 |
| 密度行列 | 純粋状態の外積、混合の対角行列、非対角要素、Tr(ρA)と状態ベクトルでの期待値を比較 |
| 部分トレース | Bell状態と混合の双方で各縮約状態がI/2となること、非対称な積状態で取り除く側の指定を確認 |
| Bloch座標 | 掲載例の座標(0,√3/2,1/2)を数値で確認。各量子ビットの座標と相関を区別 |
| 分布図 | Matplotlibの棒の高さを取得し、回数76・24・760・240、比率0.76・0.24と一致することを照合 |
| 反例と確認問題 | Z測定だけで位相を識別できない例、積状態の非対角要素、Y状態の虚数の行列要素などを確認 |

数値検証は、本文の導出と説明を補助するためのものとし、有限個の入力で一般的な証明を代替してはいない。countsの例では、実行したサンプルと説明用の例示データを本文で区別した。

## 図の確認

8枚すべてを生成して開き、文字・軸・凡例・図の内容を目視確認した。

| 図 | 確認した対応 |
|---|---|
| [Z・X・Y測定回路](../ja/figures/02/02-basis-readout.png) | 共通の準備、基底変換の時間順、最後の測定と古典bit |
| [Bell回路の表示順](../ja/figures/02/02-bell-circuit.png) | 上下を逆にしてもq0のH・CX制御と測定先が同じ |
| [回数と相対度数](../ja/figures/02/02-counts-distribution.png) | shotsの凡例、異なる回数と同じ比率。右軸を相対度数と明示 |
| [Phi+のqsphere](../ja/figures/02/02-qsphere-plus.png)・[Phi−のqsphere](../ja/figures/02/02-qsphere-minus.png) | 点の大きさが同じで、00・11間の位相差が0またはπ |
| [1量子ビットのBloch球](../ja/figures/02/02-bloch-single.png) | Y・Zの正の側に向くベクトルと、本文の3座標 |
| [Bell状態のBloch球](../ja/figures/02/02-bloch-bell.png) | 各量子ビットのベクトルが0で矢印が伸びない |
| [密度行列の比較](../ja/figures/02/02-city-comparison.png) | Bellの実部に4本、混合に2本の高さ0.5の棒。虚部は双方0 |

city plotを複数のAxesへ配置する際に、Qiskit内部の自動配置から`Tight layout not applied`の警告が出る。掲載例は最後に図間の余白を指定して保存しており、完成したPNGでタイトル・目盛り・棒の判読に問題がないことを確認した。警告を非表示にする処理は追加していない。

## 結果

| 確認 | 結果 |
|---|---|
| 第2章の掲載コード | 全13例の実行出力が掲載出力と一致 |
| 図の生成 | 8枚すべてを掲載コードから生成。PNG形式・サイズ・画像参照を確認 |
| 数学と図の数値 | 上記の追加照合が通過 |
| 第1章・第6章の既存検証 | 全22例と既存の数学的照合が通過 |
| Markdown/KaTeX | 第2章226式・3表。第1章・第6章を含め合計1103式で変換が通過 |
| 既存参照 | 第2章の全明示アンカー・H2見出しを保存。本文・画像・検証記録・既存解説のローカルリンクを確認 |
| 空白検査 | 改稿した本文の`git diff --check`が通過 |

この検証では実QPUへの送信を行っていない。画像自体は目視確認したが、Markdown本文のすべての閲覧アプリでの組版や改ページを保証するものではない。

## 公式資料と版の扱い

以下の資料を2026-09-14 JSTに確認した。APIのURLは版を含まないlatest版を指すため、その資料全体を2.5.2で固定された文書として扱わず、使用する動作を導入済みQiskit 2.5.2でも照合した。

- [Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector): measureの戻り値、sample_counts、probabilities、from_instruction。
- [StatevectorSampler](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler): shotsとPUB、レジスタごとのcounts、途中測定を扱わない範囲。
- [Bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering): 更新される公式ガイド。掲載コードの依存条件は`qiskit[all]~=2.5.2`。文字列と図の順番、reverse_bitsの表示上の効果。
- [quantum_info / partial_trace](https://quantum.cloud.ibm.com/docs/en/api/qiskit/quantum_info#partial_trace): 部分トレースの対象指定。
- [circuit_drawer](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.circuit_drawer): 回路図の出力と表示オプション。
- [plot_histogram](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_histogram)・[plot_distribution](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_distribution): countsと正規化した分布の描画。
- [plot_state_qsphere](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_state_qsphere): 点の大きさと位相表示。global phaseの扱いは2.5.2の実装も確認。
- [plot_bloch_multivector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_bloch_multivector)・[plot_state_city](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_state_city): 各量子ビットのPauli期待値、密度行列の実部・虚部。
- [Mathematical formulations of measurements](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/formulations-of-measurements): 射影による確率と測定後の状態。
- [Bloch sphere](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/bloch-sphere)・[Multiple systems and reduced states](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/multiple-systems): 密度行列、球面上の純粋状態、縮約状態。

数学上の原理にはパッケージ版や確認日による限定を付けていない。可視化の依存ライブラリは導入済み2.5.2のパッケージメタデータでも確認した。
