# 第3〜8章とアルゴリズム補章のPR準備・検証記録

確認日: 2026-09-16 JST

## 公開する変更

第3・4・5・7・8章を、目的と前提、途中計算、コード、出力の読み方、条件を変えた確認問題まで説明する内容へ拡充した。第1・2・6章には関連する説明への参照や適用条件の補足を加えた。

[補章A](../ja/09-algorithm-worked-examples.md)には、位相キックバックとDeutsch、2量子ビットGrover、1量子ビットVQEを追加した。公開Objectivesの理解をつなぐ総合例として扱い、新たな公式領域や出題頻度を主張するものではない。

関連して、ルートREADME、正本の目次、第0章、coverage、編集方針と改稿計画を整えた。掲載コードから生成した新規PNG12枚、再実行用スクリプトと各章の検証記録、OpenQASM importerの固定依存を含める。

読者による画像幅の調整と、[量子測定・期待値の学習記録](../../chats/quantum-measurement-expectation-values.md)も、従来の合意に沿って同じPRへ含める。学習記録はステージ後の検査で行末空白が検出されたため、空の引用行の空白を除去し、意図的な改行はMarkdownのバックスラッシュ形式に置き換えて保持した。対話の文言は変更していない。

VS Codeの画像幅は作業ツリーの共通・個別指定とも60%を保持し、値と一致していなかったコメントだけを修正した。画像ファイルの寸法を変更する設定ではない。

## 再実行した検証

Python 3.12.14 / Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0の既存環境を使用した。補章ではNumPy 2.5.3 / SciPy 1.18.1、OpenQASMではqiskit-qasm3-import 0.6.0 / openqasm3 1.0.1を使用する。固定依存は[requirements.txt](requirements.txt)、Markdownの依存は[package-lock.json](../../references/html-pdf/package-lock.json)に記録している。

リポジトリのルートから次の検証を実行し、すべて通過した。

```text
python -X utf8 -B manuscript/validation/verify_sample_sections.py
python -X utf8 -B manuscript/validation/verify_chapter2.py
python -X utf8 -B manuscript/validation/verify_chapter3.py
python -X utf8 -B manuscript/validation/verify_chapter4.py
python -X utf8 -B manuscript/validation/verify_chapter5.py
python -X utf8 -B manuscript/validation/verify_chapter7.py
python -X utf8 -B manuscript/validation/verify_chapter8.py
python -X utf8 -B manuscript/validation/verify_algorithm_examples.py
node manuscript/validation/verify_manuscript_render.cjs
git diff --check
```

| 対象 | 結果 |
|---|---|
| 第1・6章 | 掲載出力23例と、位相・共役変換・期待値・テンソル積・broadcastingなどの照合が通過 |
| 第2章 | 掲載出力13例、図8枚、測定後状態・密度行列・可視化の照合が通過 |
| 第3章 | 掲載出力14例、図2枚、回路合成・引数の対応・逆演算・パラメータ・分岐の照合が通過 |
| 第4章 | 掲載出力9例と関数例4件、図2枚、transpile・layout・PUB・ローカルRuntimeの照合が通過 |
| 第5章 | 掲載出力8例とRuntime関数2件、図2枚、shots・レジスタ・DDのモデルと指定の照合が通過 |
| 第7章 | 掲載出力10例とRuntime関数3件、図2枚、job API・統計・結果保存の照合が通過 |
| 第8章 | 掲載出力11例、QASM4例、図1枚、初期化・条件分岐・ループ・往復変換の照合が通過 |
| 補章A | 掲載出力7例、図3枚、Deutschの全4関数・Groverの変更条件・VQEの解析解と最適化の照合が通過 |
| Markdown・KaTeX | 本編・補章と入口の計1,866式、表の列構造、数式とコードの区切りが通過 |
| ローカルリンク | 原稿・編集文書・各検証記録・既存模試解答・ルートREADMEの参照先とアンカーを確認 |
| Gitの差分 | 空白の検査が通過。仮想環境や生成キャッシュを公開対象へ含めない |

掲載出力を照合した例は合計95件。関数例9件は別に確認している。図は合計20枚を一時ディレクトリへ生成し、今回の再実行では掲載PNGを書き換えていない。目視確認の対象と結果は、各章および[補章Aの記録](algorithm-supplement-2026-09-15.md)を参照する。

第2章のcity plotで既存の`Tight layout not applied`警告が出た。第4・5章のローカルRuntimeでは、Aerを使わないシミュレーション、DD・twirling設定がローカルでは作用しない旨の警告が出た。いずれも検証記録にある適用範囲と一致し、警告を消すための本文やコードの変更は行っていない。

## 確認の限界と次の作業

今回の再実行はローカル検証であり、実QPUへの送信、サービス側のスケジューリングや誤差軽減、実機での成功率・収束を検証したものではない。動的回路の各分岐の計算と、動的回路そのものの実機実行も区別する。

Markdown・KaTeXの構文検査を、VS CodeやPDF全ページの組版確認とは扱わない。読者による説明の確認、全章の通読点検、coverageの管理方法、HTML・PDF出力の整備は[改稿計画](../revision-plan.md)で未完了として残す。

学習記録は対話の保存であり、正本と同じコード・出力・記述の検証を全面的に適用した資料ではない。既存のpractice-bankの本文と検証器はこのPRでは変更していない。

既存GitHub Actionsはpractice-bankおよびそのworkflowの変更を起動条件にしている。本PRの変更はその条件に含まれないため、ここに示したローカル検証をPRの検証根拠とする。
