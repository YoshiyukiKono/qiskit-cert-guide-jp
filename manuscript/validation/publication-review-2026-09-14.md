# 改稿内容のPR準備・検証記録

確認日: 2026-09-14 JST

## 公開範囲

第1・2・6章の改稿、読者による文言・強調の調整、第2章の図8枚、対象バージョンとサービス依存条件の整理をまとめて公開する。[編集方針](../editorial-policy.md)に読者との確認で得られた説明上の基準を追加し、[今後の計画](../revision-plan.md)に残りの章の優先順と完了条件を記録した。

関連する変更として、Mock 01の解答への問題文の追記と本文参照の位置調整、ポケットリファレンスの交換子の定義、`chats/commutator.md`の学習記録を含める。学習記録のローカル環境に依存するリンクは相対リンクへ修正し、定義追記前の対話であったことを補った。

VS Codeのプレビュー設定は、作業ツリーにある共通指定・個別指定の`width: 80%`を保持し、値と一致していなかったコメントを修正した。元の画像のサイズは変更していない。Pythonの生成キャッシュは`.gitignore`で除外する。

第3・4・5・7・8章全体の拡充は未実施である。章間の接続やコードの前提に残る課題も、今後の計画で未完了として扱う。

## 再実行手順

Python 3.12.14、Qiskit 2.5.2、qiskit-ibm-runtime 0.49.0のローカル環境を利用する。原稿の依存関係は[requirements.txt](requirements.txt)、演習の依存関係は[演習側のrequirements.txt](../../practice-bank/validation/requirements.txt)に記録している。Markdownの依存関係は[既存のpackage-lock.json](../../references/html-pdf/package-lock.json)を使う。

リポジトリのルートから次を実行する。

```text
python -m pip install -r manuscript/validation/requirements.txt -r practice-bank/validation/requirements.txt
npm ci --prefix references/html-pdf
python -X utf8 -B manuscript/validation/verify_sample_sections.py
python -X utf8 -B manuscript/validation/verify_chapter2.py
node manuscript/validation/verify_manuscript_render.cjs
python -X utf8 -B practice-bank/validation/validate_bank.py
python -X utf8 -B practice-bank/validation/test_validate_bank.py
python -X utf8 -B practice-bank/validation/smoke_checks.py
git diff --check
```

第2章の検証で図は一時ディレクトリへ再生成する。掲載済みPNGの更新を意図するときだけ`--write-figures`を指定する。

## 今回の確認結果

| 対象 | 結果 |
|---|---|
| 第1章・第6章の掲載コード | 14例・9例の計23例で、実行出力が掲載出力と一致 |
| 第2章の掲載コードと図 | 全13例の出力が一致し、図8枚を一時ディレクトリへ再生成。掲載済みPNG8枚も形式・サイズを確認 |
| 数式と動作の追加照合 | 共役変換、期待値、位相、テンソル積と演算順序、測定・密度行列、broadcasting、optionsなどの既存検証が通過 |
| Markdown/KaTeX | 第1章871式・9表、第2章226式・3表、第6章109式・7表。合計1,206式で変換が通過 |
| 編集文書・設定 | 編集方針・計画・学習記録・検証記録の11ファイルもMarkdown/KaTeX変換が通過。VS Code設定のJSONを確認 |
| ローカルリンク | 原稿・編集文書・検証記録・Mock解答の22ファイルにある307リンクが通過。学習記録の相対リンク1件も別途確認 |
| 既存アンカー | 第1・2・6章にあった明示アンカー7・6・5個をすべて維持 |
| Mock解答の差分 | 全68問の追記した問題文が問題本体と一致。正答表・解説・本文へのリンク先を変更していないことを比較で確認 |
| 演習の構造検査 | 分野別80問・Mock 68問が通過 |
| 演習の既存テスト | 構造検証器の回帰テスト26件、Qiskitローカル検証15件がすべて通過 |
| 空白・生成物 | 空白だけの行を修正し、`git diff --check`が通過。Pythonキャッシュを公開対象から除外 |

第2章のcity plot生成では、既存の記録と同じ`Tight layout not applied`警告が出る。図生成と数値照合は通過しており、掲載コードは最後に余白を指定して保存する。警告を隠す変更や、掲載済みの画像データの変更は加えていない。

以前の検証記録にある例数・式数は、その改稿段階での件数である。読者との確認後の第1章への補足も含めた、今回の掲載コードの合計は36例となる。

## 検証の範囲

今回の再検証はローカルの数式・掲載コード・出力・図生成・Markdown構造・参照と、演習の既存チェックを対象とする。公式資料の照合範囲は、[参照資料と版の記録](version-scope-revision-2026-09-14.md)および各章の改稿記録に残している。

実QPUへの送信やRuntimeの誤差軽減処理そのものは、この再検証では実行していない。Markdown/KaTeXの変換チェックは、VS CodeやPDFの全ページの組版確認を代替しない。図の目視確認は[第2章の記録](chapter2-revision-2026-09-14.md)を参照する。外部の公開試験情報を取得するGitHub Actionsのジョブは、ローカルのコード検証とは別に結果を確認する。
