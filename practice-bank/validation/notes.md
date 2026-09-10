# Validation Notes

このディレクトリは、問題文のうちコードで再確認しやすい主張を Qiskit で spot-check するための補助資料です。

## 方針

- 問題の正答を「実行結果だけ」に依存させず、数学的理由も解説する。
- API 依存の問題は現行 Qiskit v2.x の公式ドキュメントで再確認する。
- `smoke_checks.py` は資格問題の全問自動テストではなく、主要な状態変換・Primitives・QASM3 export の sanity check。
- IBM 実機への資格情報やネットワーク接続は不要なローカル検証だけを含める。

## 推奨環境

2026-09 の教材初版では Qiskit v2.x を想定しています。

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "qiskit>=2,<3"
python practice-bank/validation/smoke_checks.py
```

OpenQASM 3 import (`load` / `loads`) を別途試す場合は、現行ドキュメントに従って import package も追加してください。

```bash
pip install qiskit-qasm3-import
```

## バージョン差に注意する対象

特に以下は更新が入りやすいため、問題集より公式 API reference を優先します。

- Primitive V2 の result data / metadata の具体的な属性
- IBM managed service 側の Sampler / Estimator class 名や import path
- backend selection / execution workflow
- OpenQASM 3 import/export の対応範囲
- transpiler preset pass manager の細かな引数

## 安定した概念とAPI依存知識を分ける

比較的安定:

- Pauli/H/S/T の数学的作用
- Born rule
- Bell state の相関
- Sampler と Estimator の役割の違い
- transpilation の目的
- OpenQASM 3 の `OPENQASM 3.0;`, `qubit`, `bit` という基本概念

API確認を伴う:

- exact class/import names
- result object の field access
- optional dependency
- provider-specific options

試験直前には IBM が公開する certification study guide と Qiskit API reference を再確認してください。
