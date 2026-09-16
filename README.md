# Qiskit v2.X 開発者認定 日本語学習ガイド

IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate（C1000-179）の試験対策を目的とする教材です。Python経験があり、量子計算を初めて学ぶ読者が、数式・回路・コード・実行結果を順序立てて理解することを目指します。

**学習の入口は [manuscript/ja の日本語正本](manuscript/ja/README.md)です。** 章末の確認問題には理由付きの解答があり、本文だけでも学び進められます。基本的な操作を説明できるようになったら、補章の総合例と演習で、条件を変えて考えます。

## 本編と総合例

| 章 | 内容 |
|---|---|
| [第0章](manuscript/ja/00-guide.md) | 学び方、公開Objectives、バージョンと適用範囲 |
| [第1章](manuscript/ja/01-quantum-operations.md) | 量子状態、ゲートの合成、位相、もつれ、期待値 |
| [第2章](manuscript/ja/02-visualization-measurement.md) | 測定基底、状態と確率、回路・測定結果・状態の可視化 |
| [第3章](manuscript/ja/03-circuit-construction.md) | 回路の設計と合成、パラメータ、動的回路 |
| [第4章](manuscript/ja/04-transpile-execution.md) | transpile、ISA、layout、実行モード、PUBとjob |
| [第5章](manuscript/ja/05-sampler.md) | Sampler、shots、測定記録、DDと実行条件 |
| [第6章](manuscript/ja/06-estimator.md) | Estimator、broadcasting、精度、誤差軽減 |
| [第7章](manuscript/ja/07-results-analysis.md) | jobの取得、結果の集計、不確かさ、記録の保存 |
| [第8章](manuscript/ja/08-openqasm3.md) | OpenQASMの型と意味、Qiskitとの入出力、対応範囲 |
| [補章A](manuscript/ja/09-algorithm-worked-examples.md) | 位相キックバックとDeutsch、2量子ビットGrover、1量子ビットVQE |

補章Aは、問題の定義から途中計算、回路、結果の解釈までを通して学ぶ総合例です。第1〜8章の知識をつなぐために追加した教材であり、新しい公式試験領域や、個別アルゴリズムの出題頻度を示すものではありません。

QFT・位相推定は今後の追加候補です。Shor全体やQAOAの詳説は発展学習に位置付け、現行正本で詳説済みとは扱いません。

## 演習と参照資料

- [Practice Bank](practice-bank/README.md): 公開Objectivesに対応させたオリジナルの分野別演習と模擬試験。理解の確認や、つまずいた内容の学び直しに使えます。
- [Objectivesと教材の対応表](manuscript/ja/coverage.md): 本編の参照先と、補章による学習上の補足を確認できます。
- [Qiskitポケットリファレンス](references/README.md): 印刷・携帯向けのMarkdown、PDF、再生成手順とNotebook。

試験範囲との対応は[IBMの公開試験レコード](https://www.ibm.com/training/credentials/getExam/C1000-179)を基準にします。対応表に参照先があることは、すべての細目の習熟や合格を保証するものではありません。

## コードを試す環境

正本のSDKの基準はQiskit 2.5.2 / qiskit-ibm-runtime 0.49.0です。例の再現にはPython 3.12と[検証用の依存一覧](manuscript/validation/requirements.txt)を使います。以下の`python`がPython 3.12を指す環境で、リポジトリのルートから新しい仮想環境へ導入します。

```text
python -m venv .venv-manuscript
```

Windows PowerShellでの導入と、補章Aの検証は次のとおりです。

```powershell
.\.venv-manuscript\Scripts\python.exe -m pip install -r manuscript/validation/requirements.txt
.\.venv-manuscript\Scripts\python.exe -X utf8 -B manuscript/validation/verify_algorithm_examples.py
```

macOS・Linuxでは、上記のPython実行ファイルを`.venv-manuscript/bin/python`へ置き換えます。ローカル例の実行にIBM Quantumの認証は不要です。Runtimeの実機例については、各章で関数を呼び出す条件と実行先の前提を確認してください。

補章Aの掲載コード・数式・図の確認範囲は[検証記録](manuscript/validation/algorithm-supplement-2026-09-15.md)にまとめています。編集の基準と残る作業は[編集方針](manuscript/editorial-policy.md)・[改稿計画](manuscript/revision-plan.md)で管理します。

## 旧稿・既存資料の位置付け

`doc/`、`exercises/`、`exams/`は、正本を整える前の教材・演習として残しています。正本とはAPIの基準や説明の検証状況が異なるため、現在の学習案内と確認済みの例は`manuscript/ja/`を基準にしてください。旧稿の「頻出」「合格基準」などの記述を、現行試験の公式な出題情報としては扱いません。

旧稿にある[QFT](doc/16_qft_intro.md)・[位相推定](doc/17_qpe.md)・[QAOA](doc/20_qaoa.md)も、現行正本の詳説範囲へ移行済みという意味ではありません。`chats/`には学習中の議論を残しています。

## 一次情報

- [IBMの試験紹介](https://www.ibm.com/jp-ja/think/insights/qiskit-v2x-developer-certification)
- [IBM Quantum Learning](https://quantum.cloud.ibm.com/learning/en/courses)
- [Qiskitの公式ドキュメント](https://quantum.cloud.ibm.com/docs/en)

## ライセンス

[MIT License](LICENSE)
