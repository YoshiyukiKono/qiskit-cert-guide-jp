# qiskit-cert-guide-jp
Qiskit Certification Guide for Developers
以下は、先ほど提案したディレクトリ構成に対応した **GitHub公開用 README.md（そのまま貼り付け可能）** です。
各章タイトルは **実際の `.md` ファイルへのリンク前提** で構成しています。

---

# Qiskit Certification Guide for Developers

**IBM Certified Associate Developer – Quantum Computation using Qiskit**
合格を目的とした実践ハンズオン教材シリーズです。

対象：

* Python経験がある開発者
* 量子コンピューティング初学者
* Qiskit資格を短期間で取得したい人
* 量子回路を「読める・書ける」ようになりたい人

このリポジトリは：

* 試験範囲を完全カバー
* 実装中心
* 模擬試験付き
* GitHubポートフォリオとして利用可能

な構成になっています。

---

# 学習ロードマップ

推奨学習時間：

約20時間（2〜3週間）

| Phase | 内容                         |
| ----- | -------------------------- |
| 基礎    | qubit / H / Pauli          |
| 中級    | entanglement / measurement |
| 応用    | transpile / simulator      |
| 発展    | algorithms                 |
| 仕上げ   | mock exam                  |

---

# 目次

## Part 0 環境構築

* [00_setup](./00_setup.md)

内容：

* Python venv
* Qiskit install
* AerSimulator
* Statevector
* 回路描画

---

## Part 1 量子ビット

* [01_qubit](./01_qubit.md)

内容：

* |0⟩
* |1⟩
* 重ね合わせ
* 確率振幅
* 正規化条件

---

## Part 2 Hadamardゲート

* [02_hadamard](./02_hadamard.md)

内容：

* H|0⟩
* H|1⟩
* H × H = I
* 干渉の基礎

---

## Part 3 Pauliゲート

* [03_pauli](./03_pauli.md)

内容：

* X
* Y
* Z
* ゲート変換関係

---

## Part 4 位相ゲート

* [04_phase](./04_phase.md)

内容：

* S
* S†
* T
* T†
* 位相と確率の違い

---

## Part 5 測定

* [05_measurement](./05_measurement.md)

内容：

* 測定とは何か
* collapse
* shot
* histogram解釈

---

## Part 6 Bloch球

* [06_bloch](./06_bloch.md)

内容：

* θ
* φ
* 回転操作
* Rx
* Ry
* Rz

---

## Part 7 多量子ビット

* [07_multiqubit](./07_multiqubit.md)

内容：

* tensor product
* qubit ordering
* register構造

---

## Part 8 CNOTともつれ

* [08_cnot](./08_cnot.md)

内容：

* CXゲート
* 制御ビット
* ターゲットビット
* Bell状態

---

## Part 9 回路合成

* [09_circuit](./09_circuit.md)

内容：

* SWAP
* Toffoli
* barrier
* compose

---

## Part 10 transpile

* [10_transpile](./10_transpile.md)

内容：

* backend
* basis gates
* optimization level
* mapping

---

## Part 11 AerSimulator

* [11_simulator](./11_simulator.md)

内容：

* statevector simulator
* qasm simulator
* shot数の影響

---

## Part 12 Statevector解析

* [12_statevector](./12_statevector.md)

内容：

* amplitude抽出
* probability計算
* 位相確認

---

## Part 13 基本アルゴリズム

* [13_algorithms](./13_algorithms.md)

内容：

* Deutsch–Jozsa
* Grover（最小例）
* 位相キックバック

---

## Part 14 模擬試験

* [14_mock_exam](./14_mock_exam.md)

内容：

* 模擬問題30問
* 回路出力予測問題
* 測定結果解析問題
* transpile理解問題

---

# この教材で到達できるレベル

修了後：

以下ができるようになります

✅ 回路の出力を予測できる
✅ Bell状態を説明できる
✅ 位相ゲートの意味を理解できる
✅ transpileの役割を説明できる
✅ simulatorを使い分けできる
✅ 基本アルゴリズムを実装できる

＝

**IBM Qiskit資格 合格レベル**

---

# 想定読者

この教材は特に：

* ソフトウェアエンジニア
* インフラエンジニア
* HPCエンジニア
* GPU計算経験者
* 量子アルゴリズム初学者

に最適化されています。

---

# 関連シリーズ（推奨）

併読すると理解が深まります：

* 開発者のための量子コンピューティング実践入門
* GPU × 量子回路シミュレーション
* cuQuantumチュートリアル
* VQE / QAOA実装ガイド

---

必要なら、このREADMEに対応する **各章テンプレート（md雛形14本）** も一括生成できます。
