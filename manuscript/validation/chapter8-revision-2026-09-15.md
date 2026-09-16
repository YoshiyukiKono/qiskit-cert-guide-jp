# 第8章の改稿・検証記録

検証日: 2026-09-15 JST

## 改稿の範囲

[第8章](../ja/08-openqasm3.md)全体を、OpenQASMの文を量子状態と古典記録の変化として読み、Qiskitとの入出力を自分で確かめる内容へ広げた。言語の説明はOpenQASM 3.0仕様、変換の説明はQiskit 2.5.2 / qiskit-qasm3-import 0.6.0を基準とする。

| 対象 | 拡充した内容 |
|---|---|
| 型と初期化 | 版の宣言とinclude、量子ビットへの参照、量子状態と古典変数の未初期化、resetの役割、bitレジスタと整数の幅、angleとcomplex、castによる値の変換 |
| プログラムの意味 | reset→H→CX→測定の状態と保存先、Bell状態の部分reset、測定後の状態と過去の古典記録の違い |
| 古典的な制御 | 最初の測定値に応じたX、両分岐の計算、条件の参照先の図、forの両端を含む範囲、固定回数の展開、回路内ループとshotsの違い |
| 文字列とファイル | dumps・loadsとdump・loadの引数と方向、追加importerの依存条件、生成した文字列の読み方、ファイルへの保存と読込み |
| 往復変換 | ユニタリ行列と測定先の対応の照合、inputからParameterへの接続、global phaseとmetadataの保持、同じ行列と全体位相を除く同値の区別 |
| 対応範囲 | 構文解析と意味、importと回路表現・exportの違い、部分対応の読み方、物理量子ビット、SDK・実行先・サービスの条件 |
| 相互運用と実行 | RESTとOpenQASMの役割、PUBやJob・Session・Batchとの関係、OpenQASM 2からQiskitを介した3への変換、後方互換の記法 |

既存の明示アンカー5個とH2見出し6個を維持した。章末には条件を変えた10問と理由付き解答を設けた。特定のMockへの言及・問題や解答へのリンクは本文へ加えていない。全角括弧は強調の外へ出している。

[第3章](../ja/03-circuit-construction.md#sdk-hardware-boundary)に、分岐とループのOpenQASM表現への案内を補った。[第7章](../ja/07-results-analysis.md#metadata)には、QPYによる保存とOpenQASMの往復変換を使い分ける案内を補った。両章のコードは変更していない。

## 実行環境と再実行

Python 3.12.14 / Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0 / qiskit-qasm3-import 0.6.0 / openqasm3 1.0.1 / antlr4-python3-runtime 4.13.2 / NumPy 2.5.3 / Matplotlib 3.11.2 / pylatexenc 2.11 / Pillow 12.3.0を使用した。

importerとparserの依存は既存の検証用仮想環境に導入済みだったため、追加インストールは行っていない。再現に必要な`qiskit-qasm3-import==0.6.0`、`openqasm3[parser]==1.0.1`、`antlr4-python3-runtime==4.13.2`を[依存一覧](requirements.txt)に追記した。他の基準版は変更していない。

リポジトリのルートで次を実行する。

```text
python -X utf8 -B manuscript/validation/verify_chapter8.py
node manuscript/validation/verify_manuscript_render.cjs
git diff --check
```

[第8章の検証スクリプト](verify_chapter8.py)は、本文のPythonブロック11例を直接読み、独立した名前空間で実行して掲載出力と比較する。独立して掲載したQASMブロック4例は、Python例に埋め込んだプログラムとの一致と構文を確認する。検証中のネットワーク接続は遮断する。

図とQASMファイルは一時ディレクトリへ生成する。掲載PNGを更新する場合だけ、次を使う。例が書き出すQASMファイルをリポジトリへ複製する指定ではない。

```text
python -X utf8 -B manuscript/validation/verify_chapter8.py --write-figures
```

## 確認結果

| 確認 | 結果 |
|---|---|
| 掲載出力 | 11例を独立実行し、ビット数、命令列、counts、密度行列の値、文字列、入出力、位相、例外の型と一致 |
| QASMとPython | 掲載QASM4例と埋込み文字列の一致、版の宣言、構文を確認。inputの例と生成・変換した3のテキストも構文を確認 |
| Bell状態と初期化 | HとCXによる状態と測定先を照合。0以外の複素振幅の入力からも、明示したresetを経てBell状態を準備できることを密度行列で確認 |
| reset | Bell状態のq0をresetした結果を、二つのKraus演算子から独立に計算した密度行列と照合。0・1・+の入力に対するresetも確認 |
| 条件分岐 | 最初と最後の測定先、条件が参照する古典ビット、ifのX、elseがないことを確認。両測定分岐と条件を反転した章末問題を計算 |
| 動的回路の往復 | import→export→import後も測定先と条件の参照先を保持。StatevectorSamplerがControlFlowOpを拒否することを確認 |
| ループ | [0:2]が0・1・2であること、展開したXの個数、範囲の終端を変えた偶奇と測定値、章末の[1:3]を確認 |
| ファイル入出力 | dumpのNone、生成ファイル、loadとloadsの一致を確認。loadsへファイル名を渡す場合、dumpへストリームでなく文字列を渡す場合のエラーも確認 |
| 行列と保存先 | 測定前の2量子ビットのユニタリ行列を往復前後で照合し、量子ビット0→古典ビット1、量子ビット1→古典ビット0の対応を確認 |
| パラメータ | inputの名前、読み戻したParameterへの束縛、複数の非自明な角度での理論確率を確認。値なしのSampler入力が拒否され、同名でもParameterの同一性は保持されないことを確認 |
| 位相とmetadata | 例のglobal phase 0.3が0へ変わり、metadataが空になる基準版の挙動を確認。行列の不一致と全体位相を除く同値、制御化後はその同値も成り立たないことを照合 |
| gphase | 明示的なgphaseを含むプログラムは基準版で読み込め、元の位相付き行列を表すことを確認。言語の表現能力とexportの保持を分けた |
| 古典型 | 初期化とcastの例の構文、およびimporterが古典ビットの初期化を拒否する理由を確認。整数5→6、章末の1010→10、angleの刻みは独立した算術で照合 |
| OpenQASM 2と3 | Bell回路を2から3へ変換し、測定先と測定前の密度行列を照合。3.0でもqreg・creg・矢印の測定を受け付けることを確認 |
| 物理量子ビット | $2の構文を4量子ビットの回路へ読み込み、添字2に対応することを確認。実機の対応を確認したものではない |
| Markdown/KaTeX | 第8章41式・7表、第1〜8章の合計1,669式が変換を通過 |
| 参照と体裁 | 既存アンカー・H2見出し、manuscript配下と既存解答からのローカルリンク、図の存在、強調の括弧の配置、空白を確認 |

[条件分岐の回路図](../ja/figures/08/08-qasm-feedback.png)は、掲載コードで生成したPNGを開き、最初の測定先0、条件の古典ビット0、X、最後の測定先1が読めることを確認した。命令、条件ラベル、配線に欠けや重なりはない。

PNGの目視確認とMarkdown・KaTeXの変換を行った範囲であり、VS CodeのプレビューやPDF全ページの組版を確認したという意味ではない。

## 検証の前提と限界

OpenQASM 3.0の宣言だけでは量子状態も未初期化の古典値も定まらない。そのため完結した量子プログラムにresetを置き、古典ビットは代入後に利用する説明へ改めた。ユニタリ部分の往復を比較する例は、初期状態を別に用意する回路の保存例として区別した。

openqasm3のparserで構文が通ることは、型・スコープ・意味の規則をすべて確認したことではない。また、parserの版やversion文字列の取得だけで3.0仕様への適合を証明したとは扱わない。古典型の例は3.0の型・cast・代入の仕様と照合し、値を手計算とPythonの算術で確認した。汎用のOpenQASM古典実行環境でそのプログラムを実行した検証ではない。

測定後の条件分岐は、回路構造と各分岐の理想状態を確認した。動的回路そのものを対応シミュレータやQPUで実行した結果とは扱わない。ループのローカル実行は、固定回数を展開した後の回路を使っている。

Qiskit 2.5.2のglobal phaseとmetadataについて記した結果は、本章の具体的なexport経路で確認した挙動である。すべてのゲート定義、annotation、importerの版、将来のexportに対して一般化しない。annotationを含む任意のプログラムの往復保証も検証対象外である。

実機backendの取得、アカウントへの接続、RESTリクエストやQPUへの送信は行っていない。機能表やREST資料は、役割と適用条件の照合に使った。掲載したローカル例の成功から、サービス側の実行可否を確認済みとはしない。

## 参照資料と対象版

言語は版が固定されたOpenQASM 3.0仕様を参照する。

- [版の宣言とinclude](https://openqasm.com/versions/3.0/language/comments.html): 版の宣言が省略可能であること、書く場合の位置と回数、includeの意味。
- [型とcast](https://openqasm.com/versions/3.0/language/types.html): 量子ビット・古典値の未初期化、幅、ビット順、angle、complex、bool、型変換。
- [初期化と測定](https://openqasm.com/versions/3.0/language/insts.html): reset、Z基底測定、レジスタの各添字への対応、後方互換の矢印形式。
- [古典的な処理](https://openqasm.com/versions/3.0/language/classical.html): 代入、古典条件、forの両端を含む範囲、制御フロー。
- [ゲート](https://openqasm.com/versions/3.0/language/gates.html): ゲートの作用とgphase、制御化した場合の位相。
- [inputとoutput](https://openqasm.com/versions/3.0/language/directives.html): 外から与える入力値とプログラムの実行の関係。
- [参照文法](https://openqasm.com/versions/3.0/grammar/index.html): 構文解析の役割と、意味解析は別であること。

以下のSDKのAPI URLはlatest版であり、ページ全体をQiskit 2.5.2で固定された資料とは扱わない。関数の引数、戻り値、変換の挙動は導入済みの基準版でも照合した。

- [Qiskitとの相互運用](https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3): importerの導入、文字列とファイルの入出力。掲載コードの依存条件は`qiskit[all]~=2.5.2`。
- [qasm3 API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qasm3): dumps・dump・loads・loadの引数と戻り値、追加importerと変換の範囲。
- [UnrollForLoops](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.transpiler.passes.UnrollForLoops): 既知の反復範囲を展開する変換パス。
- [QASM feature table](https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table): SDK列の対応の定義、部分対応の注記、サービス列との違い。
- [RESTの実行モード](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api) / [Sampler REST](https://quantum.cloud.ibm.com/docs/en/guides/sampler-rest-api) / [Estimator REST](https://quantum.cloud.ibm.com/docs/en/guides/estimator-rest-api): 回路と実行依頼の違い、PUB、Job・Session・Batch、認証・実行先・結果取得の役割。本文では実行用のpayloadを提示せず、具体的なAPIの項目は対応するサービス資料へ案内した。

Package versionsはガイドの掲載コードの依存条件として扱う。サービスの機能表やRESTの条件を、SDKやimporterの版だけで固定された仕様とはしない。確認日は本記録へ集約した。
