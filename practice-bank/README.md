# Qiskit v2.X Practice Bank

IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate 向けの、独立した本格演習セットです。

既存の `exams/` は変更せず、本ディレクトリだけで完結します。

## 目的

- 現行 v2.X 試験の公開された8主要領域を横断して練習する
- 単なる正誤確認ではなく、なぜ正しいか／なぜ他が誤りかまで理解する
- コード読解、回路追跡、Primitives、OpenQASM 3 をバランスよく扱う
- 68問・90分形式の模擬試験で時間配分を練習する

## 重要な前提

この問題集は IBM の公開試験領域と公開ドキュメントを基に作成した**オリジナル問題**です。実際の認定試験問題、いわゆる dump、受験者から得た非公開問題の再現ではありません。

2026-09 時点の Qiskit v2.x 系を前提とし、特に V2 Primitives (`StatevectorSampler`, `StatevectorEstimator`) と OpenQASM 3 を意識しています。API は将来変わり得るため、学習時には IBM Quantum Documentation の最新版も確認してください。

## 構成

```text
practice-bank/
├── README.md
├── exam-objectives-map.md
├── topic-tests/
│   ├── 01-quantum-operations.md
│   ├── 02-visualization-measurement-states.md
│   ├── 03-circuit-construction.md
│   ├── 04-running-circuits.md
│   ├── 05-sampler.md
│   ├── 06-estimator.md
│   ├── 07-results-analysis.md
│   └── 08-openqasm3.md
├── mock-exams/
│   └── mock-01.md
├── answers/
│   └── mock-exams/
│       └── mock-01-answers.md
└── validation/
    ├── notes.md
    └── smoke_checks.py
```

## 推奨利用順序

1. `exam-objectives-map.md` を読む
2. topic test を領域ごとに解く
3. 各 topic test の後半にある解答・解説で復習する
4. 間違えたコード系問題は `validation/smoke_checks.py` や自分の REPL で再現する
5. 最後に `mock-exams/mock-01.md` を **90分・資料なし** で解く
6. `answers/mock-exams/mock-01-answers.md` で採点・復習する

## Topic tests

各ファイル10問、合計80問です。topic test は学習用途を優先し、同一ファイルの後半に解答・解説を置いています。

## Mock exam

`mock-01.md` は68問です。解答は別ファイルに分離しているため、本番同様に通しで使えます。

目安としては、1問平均約79秒です。難問に固執せず、見直し用に印を付けて先へ進む練習を推奨します。

## 採点の考え方

このリポジトリ独自の練習基準として、次を目安にします。

- 90%以上: 本番形式へ進んでよい
- 80–89%: 合格圏を狙えるが弱点補強推奨
- 70–79%: 領域別復習を優先
- 69%以下: 基礎章と topic tests を再学習

これは IBM の公式合格基準を表すものではありません。

## 参照の優先順位

1. IBM の当該 certification / assessment の公式案内
2. IBM Quantum Documentation の最新 Qiskit API
3. OpenQASM 3 公式仕様
4. 本リポジトリの解説

本問題集と公式ドキュメントが食い違う場合は、公式情報を優先してください。
