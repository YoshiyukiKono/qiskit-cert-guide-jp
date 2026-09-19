# 正解数が不明なGrover探索・検証記録

検証日: 2026-09-18 JST

## 追加した内容

[発展編（Advanced）: 正解数が不明なGrover探索](../ja/11-grover-unknown-solutions.md)を独立した原稿として追加した。固定範囲からのランダムな反復回数の選択と、範囲を徐々に拡大する方法を、候補の検証・有限の打ち切りまで含めて実装した。本文はスライドへの直接の言及なしで読める構成にした。

掲載コード4ブロック、図2枚、確認問題7問と理由付き解答を含む。コードはQiskitのStatevectorSamplerで一試行につき1shotを取り、探索側へ正解数を渡さない。教材用オラクルの構築は全候補を列挙するため、その準備込みの実用的な高速化を主張しない。

[正本の入口](../ja/README.md)へリンクを加え、[Markdown・数式の検証器](verify_manuscript_render.cjs)の対象へ追加した。既存の補章Aと既知正解数の発展編は変更していない。作業前後に次のSHA-256の一致を確認した。

| 既存ファイル | SHA-256 |
|---|---|
| 09-algorithm-worked-examples.md | cee2d9f7ef411582a4918faad01ee00a1836163049ba3264bddc8e3d5bb9c1c8 |
| 10-grover-advanced.md | d2fc1b2a3961c8510b6880b8c93e4d11bf27054b21a2797dba6bb72d4f11bc22 |

## 参照スライドとの対応と調整点

参照したのは、ユーザー指定の[08-Grover-algorithm.pdf](../../../ibm-quantum-course-runtime-check/courses/fundamentals-of-quantum-algorithms/slides/08-Grover-algorithm.pdf)。ページ番号はPDF先頭を1と数える。29ページは画像に描画し、式・箇条書き・タイトルを目視確認した。

| PDFページ・タイトル | 新原稿で追える内容 |
|---|---|
| 7: Algorithm description | 測定した候補をfで検証し、不成功なら状態を準備し直して再試行 |
| 16: Rotation by an angle | 初期角度θ、反復後の角度(2t+1)θ。前の発展編の回転図とも接続 |
| 21–22: Setting the target | 成功確率sin²((2t+1)θ)、正解数を知らないと適切なtを直接決められないこと |
| 28: Number of queries | 正解数Mに応じた問い合わせ数O(√(N/M))と、期待値・最悪値の区別 |
| 29: Unknown number of solutions — A simple approach | [固定範囲でのランダム化](../ja/11-grover-unknown-solutions.md#unknown-grover-fixed)、検証と繰返しによる見逃し率の低減 |
| 29: Unknown number of solutions — A more sophisticated approach | [選択範囲の段階的な拡大](../ja/11-grover-unknown-solutions.md#unknown-grover-growing)、増加率5/4、上限、正解数が不明でも期待問い合わせ数を抑える考え方 |

概念の対応を保ちながら、次の箇所は検証可能な条件へ調整した。スライドと完全に同じアルゴリズム・定数であるとは扱わない。

1. **固定範囲と成功確率の定数**。スライド29ページではtを1からfloor(π√N/4)まで一様に選び、成功率40％以上とする。しかしN=4、M=3ではその集合はt=1だけで、θ=π/3からsin²(3θ)=0となる。したがって無条件の保証としては採用しなかった。本文ではL=ceil√N、t=0,…,L−1とし、平均成功確率が少なくとも1/4という下限を導出した。この反例と本文の定数の区別は、説明の簡略化ではなく正確性のための調整である。
2. **範囲拡大の端点と丸め**。本文はBBHTの0回を含む選択範囲を使う。実数mを5/4倍し、L=ceil(m)で整数の選択肢を作る。スライドの整数Tへの切り上げ更新を、そのまま同じコードと表現しない。
3. **正解が半数より多い場合**。各試行の冒頭で古典的な一様候補を確認する。これにより高い正解密度でも期待O(1)の評価ができ、一般のMでO(√(N/M))という説明に条件の欠落がない。
4. **解なしの場合の停止と誤り**。スライドの「解なし」を報告する短い説明に対し、本文は上限の範囲でK回試して未発見ならnot_foundを返す。正解が存在するのに未発見となる確率はε以下だが、不存在の確定証明でも、未発見後の不存在の事後確率でもないことを明記した。
5. **問い合わせ数の意味**。成功まで継続する場合の期待O(√(N/M))と、打ち切り版の最悪O(√N(1+log(1/ε)))を区別した。固定した誤差なら後者はO(√N)。位相オラクルの呼出しと候補検証を数え、教材用オラクルの構築や内部ゲート数とは分けた。

## 数学の確認

BBHT原論文の§4、Lemma 2にある平均成功確率の式と照合した。本文では三角関数の差を足して途中項が消える導出を示し、Lsin(2θ)≥1なら平均成功率が1/4以上になることを説明した。L=ceil√Nの場合は、整数1≤M≤N−1でM(N−M)≥N−1を使えば条件を満たす。M=0とM=Nは別に扱う。

範囲拡大では、M≤N/2のしきい値m*=1/sin(2θ)以後、失敗確率の上界3/4と費用の増加率λの積が1未満になることを確認した。λ=5/4なら15/16。M>N/2では古典候補の確認により失敗率は1/2未満なので、比は5/8以下になる。候補の確認も含めた各試行の平均費用はO(m)。有限打ち切り版は、同じ乱数列で成功まで続ける版より費用が増えないが、見逃しを許す。

ε=0.05ではK=11、(3/4)^11≈0.042235。ε=0.01ではK=17、(3/4)^16≈0.010023なので16回では不足する。これらは本文の確認問題とも照合した。

## 実行環境と再実行

Python 3.12.14 / Qiskit 2.5.2 / NumPy 2.5.3 / Matplotlib 3.11.2 / Pillow 12.3.0。前の発展編の検証で用意した一時ディレクトリの基準版パッケージを再利用し、既存のPython環境は変更していない。

リポジトリのルートから、依存一覧に対応する環境で次を実行する。

```text
python -X utf8 -B manuscript/validation/verify_grover_unknown.py
node manuscript/validation/verify_manuscript_render.cjs
```

[専用検証器](verify_grover_unknown.py)は掲載コードを原稿から抽出し、標準出力を照合する。一時作業ディレクトリで実行し、外向きのソケット接続を禁止する。

図は[再生成スクリプト](draw_grover_unknown.py)で作成した。数式から計算する理論図であり、実機測定や有限shotsの集計図ではない。日本語フォントYu Gothicを使用し、利用できない環境では英語へ切り替える。

```text
python -X utf8 -B manuscript/validation/draw_grover_unknown.py
```

## 検査した対象

| 対象 | 確認内容 |
|---|---|
| 掲載コード | 4ブロックの実行と全出力の一致 |
| Qiskit回路 | n=1〜4の各正解数について、オラクルの対角符号・状態ベクトル・確率式を独立照合 |
| 平均と誤差 | n=1〜9の各正解数について、有限和と閉形式、1/4下限、固定法と範囲拡大法の理想的な失敗率を照合 |
| 探索の制御 | 実際の候補検証回数、反復数の合計、候補とビット順、乱数の再現性、正解あり・なしと打ち切りの分岐 |
| 範囲拡大 | N=8では第5試行、N=32では第9試行から上限範囲のK回を数えること |
| 境界 | 正解0個・全候補が正解、ε・増加率・回路反復数の入力条件 |
| 図 | 2枚の計算値と原稿との一致、画像を開いて文字・凡例・注記・端点を目視確認 |
| 表示と参照 | 新規作成時の原稿155式・1表のMarkdown/KaTeX検査、既存全章の表示検証、ローカルリンクとアンカー |

図1のN=32、t=0,…,5の平均成功確率は、M=1で約0.607955、M=4で約0.456970。t=4だけならそれぞれ約0.999182と0.012207。作図時には有理数の振幅更新でも独立に確率を照合した。図2の範囲の大きさは1,2,2,2,3,4,4,5,6,6,6で、整数への丸めと上限到達位置を確認した。

正解がない実行例は固定法11回、拡大法15回で停止する。拡大法の15回には上限到達前の4回を含む。成功例の一回の実行履歴を平均計算量の実証とは扱っていない。

## 一次資料と限界

- [Boyer・Brassard・Høyer・Tapp, Tight bounds on quantum searching](https://arxiv.org/pdf/quant-ph/9605034): 1996年のarXiv版、§4（PDF3〜4ページ）、平均成功確率のLemma 2、範囲拡大と期待費用の解析を確認。
- [IBM公式コース Choosing the number of iterations](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/grover-algorithm/number-of-iterations): 2026-09-18閲覧。Unknown number of solutionsにスライドと同じ固定40％の記述があるが、上述の反例があるため本文の保証として採用していない。
- [grover_operator API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.grover_operator): 版を固定しないlatestのURL。位相オラクルと一回の反復の関係を確認し、実装はQiskit 2.5.2で検証。
- [StatevectorSampler API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler): 同じく更新されるURL。shots、seed、結果の取り出し方を確認し、掲載コードの基準版で実行した。

実機実行、QPUへの送信、実機ノイズ下の確率保証、PDF組版は今回の対象ではない。数値検査は本文の一般的な証明を補うもので、有限個の例だけを証明の代わりにはしていない。

## 末尾コラムの追記（2026-09-18）

利用者の希望により、原稿の最後へ[IBMコースとの対応を読む補足コラム](../ja/11-grover-unknown-solutions.md#unknown-grover-ibm-column)を追加した。既存本文、コード4例と掲載出力、図、確認問題はそのまま保持した。追加部分を取り除くと、追記前の原稿とバイト単位で一致することを確認した。

コースの正解数sと本文M、初期状態uと本文s、コースで回転行列を指すM、集合と正規化した量子状態、位相オラクルZ_fとO_f、Z_ORと前の発展編のO_0の符号を対応付けた。p(N,s)、任意の反復数でのP_t、ランダム化後の平均確率を区別し、固定範囲・範囲拡大・打ち切りの調整点をまとめた。

一次資料には既存の参照に加え、[IBMコース Analysis](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/grover-algorithm/analysis)を使用した。共有PDFの8〜11・16・21〜22・28〜29ページと、AnalysisおよびChoosing the number of iterationsの定義を再照合した。

コラム追加後の原稿226式・3表のMarkdown・KaTeX表示と表の列数、ローカルリンク・アンカーを検証した。コードは変更していないため、新しい数値テストは追加していない。
