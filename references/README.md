# Portable reference materials

このディレクトリには、既存の`doc/`、`exams/`、`practice-bank/`を変更せずに追加した、印刷・携帯向けの横断資料を置きます。

## Files

- [qiskit-pocket-reference.md](qiskit-pocket-reference.md): 編集可能な原稿。数式はインライン `$...$`、独立表示 `$$...$$` のLaTeX形式
- [qiskit-pocket-reference.pdf](qiskit-pocket-reference.pdf): A5・16ページの印刷用PDF。A4用紙へ2ページ/面・両面印刷や冊子印刷をしやすい構成
- [build_pocket_reference.py](build_pocket_reference.py): PDF再生成スクリプト
- [requirements-pdf.txt](requirements-pdf.txt): PDF生成スクリプトの直接依存パッケージ。検証済みversionを固定
- [qiskit-pocket-reference-html.pdf](qiskit-pocket-reference-html.pdf): HTML・KaTeX・headless Chromeで生成する、数式を画像化しない別版PDF
- [html-pdf/build.mjs](html-pdf/build.mjs): HTML版PDF再生成スクリプト
- [html-pdf/package.json](html-pdf/package.json): HTML版の固定Node.js依存関係
- [build_quantum_operations_notebook.py](build_quantum_operations_notebook.py): Notebook再生成スクリプト
- [quantum_operations_drill.ipynb](../notebooks/references/quantum_operations_drill.ipynb): 量子演算を予想・計算・検証するNotebook

## 方針

- 数学的に長期間変わらない内容と、Qiskitのversionに依存する内容を明確に分離する。
- `=`は厳密なベクトル・行列等式にのみ使い、global phaseまでの同値には`~`を使う。
- 暗記表だけでなく、短時間で式を復元するための手順も載せる。
- API依存ページには基準versionと確認日を表示する。

## PDFの再生成

`build_pocket_reference.py`はMarkdown原稿を読み、LaTeX数式をZiamathで組版し、CairoSVGで透過PNGへ変換してからReportLabでA5 PDFへ配置する専用生成スクリプトです。

見出し、数式、表、コードフェンスをPDF用に個別レイアウトします。コードフェンスは淡い背景色、外枠、左側のアクセント線を付け、本文と区別して出力します。

表内に分数や列ベクトルなど背の高い数式がある場合は、数式の実寸に合わせて行高を自動調整します。

表のタイトル行は青背景・白文字で統一します。タイトルセル内の数式、リンク、インラインコードにも白文字を強制し、個別の色指定によるコントラスト低下を防ぎます。

- 入力: `references/qiskit-pocket-reference.md`
- 出力: `references/qiskit-pocket-reference.pdf`（既存ファイルを上書き）
- 実行場所: repository root
- 検証環境: CPython 3.11.15 / Windows

### venvとpipを使う場合

PowerShellで次を実行します。

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r references/requirements-pdf.txt
python references/build_pocket_reference.py
```

### uvを使う場合

環境を常設せずに、固定済み依存関係で実行できます。

```powershell
uv run --isolated --with-requirements references/requirements-pdf.txt python references/build_pocket_reference.py
```

正常終了時は`Created ...\references\qiskit-pocket-reference.pdf`と表示されます。インラインの`$...$`と独立行の`$$...$$`は、いずれも同じZiamathエンジンとSTIX Two Mathで組版します。添字・上付き文字・括弧・行列・演算子を同じ字形で描画し、システムへのLaTeX導入は不要です。

### フォント要件

現在のスクリプトはWindows用です。日本語TrueTypeフォントを次の順で探索します。

1. BIZ UDゴシック
2. Noto Sans JP
3. メイリオ

いずれも`C:\Windows\Fonts`にない場合は`A Japanese TrueType font was not found.`で終了します。

日本語本文には上記のフォントを使用します。数式は本文フォントから分離し、Ziamath同梱のSTIX Two Mathで統一して描画します。そのため、`\mapsto`（↦）を含む数式も個別のfallback処理なしで組版されます。

### Markdown表内の数式

Markdown表では`|`が列区切りとして解釈されます。ketを表内へ記述するときは、`$|0\rangle$`ではなく`$\lvert0\rangle$`を使用してください。生成スクリプトもこの誤りを検出して終了します。

## HTML・KaTeX版PDFの再生成

HTML版は同じ`qiskit-pocket-reference.md`をmarkdown-itでHTMLへ変換し、KaTeXで数式をHTML/MathMLとして組版した後、Playwright CoreからローカルのChromeまたはEdgeを使ってPDF化します。数式をPNGへ変換しないため、ブラウザの表レイアウト内でbaselineとセル配置が計算されます。既存のReportLab版とは別の出力ファイルを使用し、相互に上書きしません。

- 入力: `references/qiskit-pocket-reference.md`
- 出力: `references/qiskit-pocket-reference-html.pdf`
- 必要環境: Node.js 20以上、Google ChromeまたはMicrosoft Edge
- 実行場所: `references/html-pdf`

初回だけ依存パッケージを導入します。

```powershell
cd references/html-pdf
npm ci
```

以後は次のコマンドで再生成できます。

```powershell
npm run build
```

ChromeとEdgeを標準位置から検出できない場合は、実行ファイルを明示します。

```powershell
npm run build -- --browser "D:\path\to\chrome.exe"
```

HTML版の中間ファイルと専用browser profileは`tmp/pdfs/`へ作成し、生成終了時に削除します。HTML版で使用する依存versionは`html-pdf/package-lock.json`で固定します。

## Notebookの実行

検証基準と同じversionを使う場合は、先に次をインストールします。

```powershell
python -m pip install -r practice-bank/validation/requirements.txt
python -m pip install jupyter nbformat nbclient ipykernel
jupyter nbconvert --execute --to notebook --inplace notebooks/references/quantum_operations_drill.ipynb
```

Notebookそのものを再生成する場合は、`nbformat`を導入した環境で次を実行します。

```powershell
python references/build_quantum_operations_notebook.py
```
