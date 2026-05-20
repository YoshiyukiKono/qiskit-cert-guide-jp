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

---

了解しました。
以下に **Markdown構造が崩れない完全フラット版 README.md** をそのまま掲載します。
このまま `README.md` に貼り付けて使用できます。

---

# Qiskit Certification Training — 開発者のための量子プログラミング実践教材

このリポジトリは：

**IBM Certified Associate Developer – Quantum Computation using Qiskit**

合格レベルに到達するための体系的トレーニング教材です。

対象読者：

* 量子コンピューティング初学者
* Pythonエンジニア
* Qiskit資格受験者
* Sampler / Estimator / Runtime を理解したい開発者

特徴：

* 理論解説（chapters）
* 実行型演習（exercises）
* 模擬試験（mock exams）
* 回路読解ドリル（circuit drills）

すべて含まれています。

---

# 学習ロードマップ

推奨順序：

```
chapters/
↓
exercises/
↓
mock_exam_01.md
↓
mock_exam_02.md
↓
mock_exam_03.md
↓
circuit_reading_drills.md
```

到達目標：

```
回路が読める
状態が予測できる
Samplerが使える
Estimatorが使える
Runtimeが理解できる
```

---

# ディレクトリ構成

```
qiskit-certification-training/

├── chapters/
│   ├── 01_qubit.md
│   ├── ...
│   └── 22_exam_strategy.md
│
├── exercises/
│   ├── ex01_hadamard.py
│   ├── ex02_pauli.py
│   ├── ...
│   └── ex18_mock_exam_practice.py
│
├── mock_exam_01.md
├── mock_exam_02.md
├── mock_exam_03.md
│
├── circuit_reading_drills.md
│
├── README_exercises.md
├── requirements.txt
└── run_all.sh
```

---

# セットアップ

## 仮想環境

Mac / Linux

```
python3 -m venv qiskit_env
source qiskit_env/bin/activate
```

Windows

```
python -m venv qiskit_env
qiskit_env\Scripts\activate
```

---

# 依存関係インストール

```
pip install -r requirements.txt
```

---

# 演習の実行

```
cd exercises
python ex01_hadamard.py
```

または：

```
bash run_all.sh
```

---

# カバー範囲

この教材は試験範囲を網羅しています。

## 基本ゲート

* X
* Z
* H
* S
* T

---

## multi-qubit

* CX
* CZ
* CP
* SWAP
* Bell states

---

## 位相理解

* phase kickback
* interference
* basis change

---

## アルゴリズム

* QFT
* Grover
* VQE
* QAOA

---

## Primitives（最新版）

* Sampler
* Estimator
* Parameterized circuits
* Observable
* Runtime Session

---

## コンパイル・実機理解

* transpile
* basis_gates
* optimization_level
* noise simulation

---

# 模擬試験

3段階構成：

| File            | 難易度       |
| --------------- | --------- |
| mock_exam_01.md | 基礎        |
| mock_exam_02.md | 応用        |
| mock_exam_03.md | Runtime特化 |

---

# 回路読解ドリル

```
circuit_reading_drills.md
```

目的：

回路を見て出力を即答できるようになること。

試験得点に最も直結します。

---

# この教材で身につくスキル

完走すると：

```
量子状態の追跡
回路簡約
entanglement理解
phase理解
Sampler操作
Estimator操作
Runtime理解
```

が可能になります。

---

# 想定合格ライン

以下が理解できれば合格圏です：

* HZH = X
* HXH = Z
* Bell状態の測定結果
* Samplerの役割
* Estimatorの役割
* Observableの意味
* Parameterized circuits
* Runtime Session

---

# 推奨学習時間

目安：

| レベル       | 時間      |
| --------- | ------- |
| 初学者       | 10–15時間 |
| Python経験者 | 6–8時間   |
| 量子経験者     | 3–5時間   |

---

# ライセンス

MIT License

---

# 参考資料

* IBM Quantum Documentation
* Qiskit SDK Documentation
* Quantum Computation and Quantum Information（Nielsen & Chuang）

---

# 次のステップ（合格後）

推奨：

```
Estimator primitive 深掘り
Variational algorithms
Quantum simulation
Error mitigation
Tensor network simulation
GPU-based simulation（cuQuantum）
```

量子アプリケーション開発への橋渡しになります。


