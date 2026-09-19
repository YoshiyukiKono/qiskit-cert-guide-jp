# Markdown表内の数式を修正する

`fix_markdown_table_math.py` はPython 3.10以降の標準ライブラリだけで動きます。
通常実行では差分を表示するだけです。原本は変更しません。

```powershell
py -3 -X utf8 -B scripts/fix_markdown_table_math.py chats/deutsch-algorithm-phase-kickback.md
```

別ファイルへ保存する場合:

```powershell
py -3 -X utf8 -B scripts/fix_markdown_table_math.py chats/deutsch-algorithm-phase-kickback.md --output chats/deutsch-algorithm-phase-kickback.preview.md
```

既存の出力先は上書きしません。入力と同じパスも拒否します。
macOS/Linuxでは `py -3` を `python3` に置き換えてください。
`py` が `No installed Python found!` を返す環境では、使用するPython実行ファイルのフルパスで実行してください。この作業環境では、次の同梱Pythonで検証しています。

```powershell
& "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" -X utf8 -B scripts/fix_markdown_table_math.py chats/deutsch-algorithm-phase-kickback.md
```

## 変換と保護範囲

- 表内の単一ドル記号 `$...$` に囲まれた数式の、未エスケープの `|` だけを `\vert ` に変換します。末尾の空白はTeXコマンドの終端です。
- 例: `$|0\rangle$` → `$\vert 0\rangle$`。数式の意味は変えませんが、Markdown原文は変更されるため、原文保存用ファイルと表示用ファイルを分けてください。
- 表外の文・数式、バッククォートまたはチルダによるフェンスコードブロック、既存の `\|`・`\vert` は変更しません。
- UTF-8のBOM、改行コード、末尾改行の有無を保持します。再適用しても結果は変わりません。
- 対象は行頭・行末に `|` を持ち、区切り行の各セルに3個以上の `-` があるトップレベルの表です。引用・リスト内の表、HTML内の表、複数行の数式など、Markdown全構文を扱う汎用パーサーではありません。
- ドル記号の不一致、列数の不一致、表内の `$$...$$`、コード内の未エスケープの `|` は推測で直さず、エラー終了します。その場合、出力ファイルを作りません。
- すべてのMarkdown拡張・TeXマクロに対する無副作用を保証するものではありません。最初に差分を確認してください。

VS Code標準プレビューは[KaTeXを使用](https://code.visualstudio.com/docs/languages/markdown#_math-formula-rendering)します。`\vert` は[KaTeXがサポートする縦棒表記](https://katex.org/docs/supported)です。プレビューの数式表示が無効になっている場合や、別の拡張機能独自の問題は、このツールでは変更しません。

## 検証

```powershell
py -3 -X utf8 -B -m unittest discover -s scripts -p "test_*.py"
```
