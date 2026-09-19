# 複数正解のGrover発展編・検証記録

検証日: 2026-09-18 JST

## 目的と範囲

[発展編（Advanced）](../ja/10-grover-advanced.md)を独立したファイルとして追加した。主題は3量子ビット・8候補・正解011と100の二つである。手計算、正解・不正解をまとめる二次元表示、一般化した位相オラクル、Sampler、既知の正解数による反復回数の選択を扱う。

本文にはコード4ブロック、図2枚、理由付き解答のある確認問題6問を掲載した。最初のコードは単独で実行でき、残る3ブロックはその関数・変数を使う続きとして明示している。正解数不明の探索は次の学習課題として説明し、探索手順や成功確率の保証の実装は対象に含めていない。

[正本の入口](../ja/README.md)へ任意の発展学習としてリンクを加えた。補章Aの09-algorithm-worked-examples.mdは、この追加作業では変更していない。作業前後のSHA-256は次の値で一致した。

```text
cee2d9f7ef411582a4918faad01ee00a1836163049ba3264bddc8e3d5bb9c1c8
```

## 実行環境

Python 3.12.14 / Qiskit 2.5.2 / NumPy 2.5.3 / SciPy 1.18.1 / Matplotlib 3.11.2 / pylatexenc 2.11 / Pillow 12.3.0を使用した。本書の基準版のパッケージを一時ディレクトリへ取得し、既存のPython環境を更新せずに実行した。

図の日本語フォントはYu Gothic。再生成用スクリプトは、日本語フォントが利用できない場合に英語ラベルへ切り替える。

## 検証と再実行

[専用検証器](verify_grover_advanced.py)は、原稿のタグ付きPythonブロックを掲載順に実行し、実際の標準出力と原稿の出力を比較する。コード実行中はネットワーク接続を遮断し、計算と作図をローカルで行う。

基準版の環境を用意した上で、リポジトリのルートから次を実行する。

```text
python -X utf8 -B manuscript/validation/verify_grover_advanced.py
node manuscript/validation/verify_manuscript_render.cjs
```

図を原稿のフォルダーへ再出力する場合は、検証器に`--write-figures`を付ける。作図だけを再実行する場合は次を使う。

```text
python -X utf8 -B manuscript/validation/draw_grover_advanced.py
```

検証器は[作図スクリプト](draw_grover_advanced.py)へ、Qiskitで求めた初期・オラクル直後・拡散後の理論確率を渡す。作図スクリプトの単独実行では、同じ例の解析的な確率を使う。

| 対象 | 確認内容 |
|---|---|
| 掲載コード | 4ブロックを順に実行し、全出力が原稿と一致 |
| 位相オラクル | 基底状態ごとの対角要素を独立に作った±1と比較。複数正解、ビット順、1量子ビットの場合、入力の重複・不正な文字列を確認 |
| 拡散演算子 | 回路の行列と独立に作った2ss†−Iの一致を、全体位相を保持して確認 |
| 回転と振幅 | 正規直交した二つの軸への射影、各候補への振幅の復元、複数反復の符号と正解確率を確認 |
| 反復回数 | 正解数0の拒否、半数のときの0回の選択、全候補が正解のケース、候補数・正解数が異なる例を確認 |
| Sampler | 512shotsの合計、正解以外の文字列が出ていないこと、各正解の頻度を確認 |
| ライブラリ | grover_operatorと手作りのGrover反復が行列・状態で一致 |
| 図 | 2枚の生成と原稿の画像参照が一致。PNGを開き、ラベル、回転角、正解全体と各正解の確率、文字の重なり・欠けを目視確認 |
| 数式と表 | 発展編119式・2表をMarkdownとKaTeXで確認。既存の正本全体の表示検証にも発展編を追加 |
| 参照 | 原稿、入口、検証記録のローカルリンクとアンカーを確認 |

主な数値は、8候補・正解2個・1回反復で各正解の確率1/2、正解全体1。128候補・正解4個・4回反復では正解全体約0.999182。512shotsの例では011が241回、100が271回となり、各理論確率1/2と有限標本の頻度を区別した。

## 一次資料と確認の限界

- [IBMのGroverチュートリアル](https://quantum.cloud.ibm.com/docs/en/tutorials/grovers-algorithm): 複数の正解を持つ位相オラクル、grover_operator、反復回数、Samplerによる実行の位置付けを確認。
- [grover_operator API（2.2）](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.circuit.library.grover_operator): 位相オラクル・初期状態の準備・拡散演算子の関係を確認。閲覧したAPI資料の版と、コードを実行したQiskit 2.5.2は区別している。基準版での符号を含む行列の一致はローカルで検証した。
- [QuantumCircuit API（2.2）](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.circuit.QuantumCircuit): 基本ゲート、mcx、回路合成の参照。
- [反復回数の選択](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/grover-algorithm/number-of-iterations): 正解数が既知の場合の回転角と確率式を確認。本文の数式は独立に導出・数値照合した。正解数不明の場合については、同ページの固定した成功確率の主張を本文の保証として使っていない。

実機実行、QPUへの送信、実機ノイズ下の成功確率、PDF組版は今回の確認対象に含まない。正解一覧から構築する教材用オラクルであり、この小さなシミュレーションを実用上の高速化の実証とは扱っていない。
