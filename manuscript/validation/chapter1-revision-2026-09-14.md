# 第1章全体の改稿記録

検証日: 2026-09-14 JST

## 対象と説明の設計

[第1章](../ja/01-quantum-operations.md)全体を、既存の「ゲートの合成と基底変換」の説明の粒度へそろえた。[編集方針](../editorial-policy.md)にも第1章全体への展開を記録した。

既に改稿した「ゲートの合成と基底変換」と「observableと期待値」は、本文・数式・コード・出力を維持した。それ以外の5節と章末チェックを改稿し、章の入口に学習順序とQiskit 2.5.2というコードの基準を追加した。

| 節 | 加えた説明 |
|---|---|
| 状態と複素振幅 | ketと計算基底、複素数・共役・絶対値二乗、正規化、振幅と確率の区別、Statevectorの入力と検証 |
| global phaseとrelative phase | 位相因子、全体の位相が測定で区別できない理由、Hによる干渉の途中計算、配列の一致と同値性、回路のglobal phase |
| Pauli、Hadamard、位相、回転 | 各ゲートの振幅への作用、反交換、P・S・Tの関係、Bloch球の軸、行列指数からの半角公式、逆回転と位相の違い |
| 複数量子ビット、CX、もつれ | テンソル積の展開、CXの真理値表と行列、Bell状態の生成過程、積状態へ分解できない理由、古典的混合との比較、制御付き位相の注意 |
| bit/qubit orderingとPauli label | 回路・ket・添字の対応、古典ビットへの測定先、Pauli文字列と行列積の区別、係数付き和の行列 |
| 章末チェック | 振幅・期待値、ゲートの時間順、半角とglobal phase、Pauli文字列、CX、相関を組み合わせる9問と理由付き解答 |

各節には導入、前提説明、途中計算、独立実行できるコードと出力、条件を変えた確認問題を置いた。既存の詳しい2節にも必要な前提が含まれているため、章を順に読む場合には一部の説明が再登場する。単独の節から学び直す読み方も維持するための重複である。

元のBell状態の説明にあった「同一basisで測る結果は完全相関」という一般化は修正した。本文ではZ基底とX基底の相関を具体的に示し、Z基底で00・11が半々になることだけでは、古典的な混合と区別できないことを説明した。

## 実行環境と再実行

Python 3.12.14、Qiskit 2.5.2、NumPy 2.5.3の一時仮想環境で実行した。既存の第6章の検証も同じスクリプトで行うため、qiskit-ibm-runtime 0.49.0も使用した。行列指数の独立照合にはSciPy 1.18.1を使用した。第1章の掲載コード自体にRuntimeや実機は必要ない。

リポジトリのルートから次を実行する。

```text
python manuscript/validation/verify_sample_sections.py
node manuscript/validation/verify_manuscript_render.cjs
```

[コード・数式の検証スクリプト](verify_sample_sections.py)は、原稿のPythonコードと直後の掲載出力を抽出して実行する。今回、第1章の全7節に対象を広げた。第1章の13例はすべて単独の名前空間で実行し、前のコードで定義した変数に依存しないことも確認する。

[Markdownと数式の変換スクリプト](verify_manuscript_render.cjs)は、`references/html-pdf`に既にある依存関係を使う。MarkdownIt 15.0.2、markdown-it-texmath 1.0.0、KaTeX 0.18.7で第1章と第6章を変換し、数式の構文、コードフェンス、表の列数を確認する。ketの縦線が表の区切りにならないよう、表内では`\lvert`を使った。

## 数学・コードの照合

| 対象 | 確認方法 |
|---|---|
| 複素振幅と正規化 | 掲載例と別の複素係数の正規化、絶対値二乗の計算を照合 |
| global phase | 等しくない複素振幅と複数の位相について、同値判定とゲート適用後の確率を比較 |
| 干渉 | 相対位相を変え、H適用後の確率が(1±cos φ)/2となることを照合 |
| Pauli・位相ゲート | Yの両基底状態への作用、二乗、XZとZXの符号、T²=SとT⁴=Zを照合 |
| 回転 | X・Y・Z各軸の複数角度について、Qiskitの行列とSciPyの行列指数を比較。逆回転、同軸の角度加算、π・2π回転のglobal phaseも照合 |
| CX | 4つすべての計算基底状態への作用と、制御方向を逆にした小問を照合 |
| もつれ | Bell状態の係数行列の階数と各量子ビットの縮約状態を確認。積状態の反例、CXを再適用した状態も照合 |
| 古典的な混合 | 本文の「確率を平均する」計算を、検証コードでは密度行列から独立に照合。Z基底では同分布、X基底では異なることを確認 |
| 相関の範囲 | Bell状態のYYの期待値が−1となることを確認し、任意の同一基底で結果が一致するという一般化の反例とした |
| 制御付き位相 | 制御付き−Iが全体の相対位相を変え、0+を0−へ移すことを照合 |
| bit・Pauliの順番 | Pauli文字列をKronecker積と比較。測定先を入れ替えた回路では、入力を変えた小問のcountsも実行確認 |
| 章末問題 | 正規化・期待値、回転、Pauli文字列、X基底の積の期待値などを既存検証と追加検証で照合 |

本文では一般的な関係の途中計算や証明を示し、数値検証を証明の代わりにはしていない。階数・縮約状態・密度行列は検証側で用いた方法であり、本文を読む前提知識には追加していない。

## 結果

| 確認 | 結果 |
|---|---|
| 第1章の掲載コード | 全13例の実行出力が掲載出力と一致 |
| 既存の第6章を含む掲載コード | 全22例が一致 |
| 数式と確認問題 | 上記の追加照合と、既存の共役変換・期待値・Estimatorの検証が通過 |
| Markdown/KaTeX | 第1章768式・8表、第6章109式・7表が通過。合計877式 |
| 既存の詳しい説明 | 作業開始時の原稿との比較で、ゲートの合成と基底変換・期待値の2節が一致 |
| 参照の継続性 | 既存の明示アンカーと全H2見出しを維持。旧「行列と演算順序」のアンカーも維持 |
| ローカルリンク | manuscript配下のMarkdownと既存の解答からの参照について、ファイル・アンカーの存在を確認 |
| 読者向けの本文 | 特定のMockへの言及・リンク、日付による仕様の限定を追加していない |
| 差分の空白検査 | `git diff --check`が通過 |

過去の改稿記録にあるコード例数は、その改稿時点の記録として維持している。今回の検証は第1章全体へ対象を広げた後の結果である。

## 参照資料と版の扱い

公式資料の確認日と、本書のコードの対象版は分けて扱う。以下の資料を2026-09-14 JSTに確認した。

| 資料 | 資料の版・条件 | 照合した内容 |
|---|---|---|
| [Bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering) | 更新されるガイド。掲載コードの依存条件は`qiskit[all]~=2.5.2` | q0の表示位置、整数・文字列・配列の順番、CX、drawのreverse_bits |
| [Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector) | URLに版を含まないlatest版API | 正規化の確認、確率、evolve、equiv、全0からの回路適用 |
| [RXGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RXGate)・[RYGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RYGate)・[RZGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RZGate) | URLに版を含まないlatest版API | 回転の定義と行列 |
| [CXGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.CXGate) | URLに版を含まないlatest版API | 制御と標的、基底順に対応する行列 |
| [Pauli](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Pauli) | URLに版を含まないlatest版API | 各Pauli行列、文字列の右端がq0であること |
| [StatevectorSampler](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler) | URLに版を含まないlatest版API | ローカルでの状態計算、shots、レジスタ別の測定結果とcounts |

取得できたAPIページは固定版の資料ではないため、参照だけをQiskit 2.5.2の動作保証とはしていない。掲載コードと使用するAPIの振る舞いを、上記の2.5.2環境でも照合した。`QuantumCircuit.global_phase`は導入済み2.5.2のdocstringと行列への作用で確認した。ガイドのPackage versionsも、ガイド全体を固定した版と読み替えない。

共役変換・期待値の既存部分の参照は、[基底変換の記録](conjugation-revision-2026-09-14.md)と[期待値の記録](expectation-revision-2026-09-14.md)を引き継ぐ。

この検証は理想的なローカル計算を対象とする。QPUへの送信や実機の誤差は検証していない。Markdown/KaTeXの検証は構文と表の構造の確認であり、すべての閲覧アプリでの組版を目視保証するものではない。

## 追補: 異なる量子ビットへの作用とゲートの順番

検証日: 2026-09-14 JST。対象は[追加した小節](../ja/01-quantum-operations.md#different-qubit-order)。Pauli labelと行列積の違いを説明した直後へ置き、基本ゲートの反交換の説明から参照を追加した。

演算子のテンソル積を積状態へ一段ずつ適用し、`(A ⊗ B)(C ⊗ D) = AC ⊗ BD`を導いた。計算基底の重ね合わせにも成り立つことを説明したうえで、XとZが別々の量子ビットへ作用する場合は交換し、同じ量子ビットへ作用する場合は反交換することを比較した。異なる量子ビットへの作用では、入力がもつれた状態でも等式が成り立ち、global phaseを除く必要がないことを明記した。

Qiskitのコード1例と掲載出力、HとYへ条件を変えた確認問題・理由付き解答を追加した。読者が修正した反交換・global phase・Pauliゲートの合成の説明は維持した。

| 確認 | 結果 |
|---|---|
| 実行環境 | Python 3.12.14 / Qiskit 2.5.2 / NumPy 2.5.3。既存の検証と同じ環境 |
| 掲載コード | 第1章14例、第6章9例の計23例を実行し、すべて掲載出力と一致 |
| 対象量子ビットと行列 | 追加した2回路を、00→10、01→−11、10→00、11→−01という基底状態への作用から構成した行列と照合 |
| もつれた入力 | Bell状態と、振幅が`[1, 2i, −3, 4i] / √30`の状態について、二つの実行順の出力を成分ごとの計算と照合 |
| 確認問題 | HとYを別々の量子ビットへ適用する場合の交換、同じ量子ビットへ適用する場合の反交換を照合 |
| Markdown/KaTeX | 第1章864式・9表、第2章226式・3表、第6章109式・7表の変換が通過 |
| リンク | 追加した明示アンカーへの参照を含め、ローカルリンクの検証が通過 |

APIは[Operator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator)の回路入力・`data`と、[Bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)の量子ビット順序を確認した。前者は版を固定しないlatest版API、後者は掲載コードの依存条件が`qiskit[all]~=2.5.2`の更新されるガイドである。参照日は上記の検証日とし、実行結果は本書の基準版Qiskit 2.5.2で照合した。

上の初回改稿時点の例数・変換数は履歴として維持する。追補後の再実行コマンドも、同じ`verify_sample_sections.py`と`verify_manuscript_render.cjs`である。
