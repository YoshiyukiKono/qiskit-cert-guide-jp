では第10章として、**transpile（トランスパイル）**を資格試験対策レベルで体系的に解説します。
ここは **IBM Certified Associate Developer – Quantum Computation using Qiskit** 試験で確実に出題される領域です。

特に重要なのは：

* なぜ transpile が必要か
* backend とは何か
* basis gates とは何か
* optimization level の意味
* qubit mapping（レイアウト）

です。

---

# 10_transpile.md

# Part 10：transpile を完全に理解する

Qiskitでは：

```text
書いた回路はそのまま実行されない
```

必ず：

```text
transpile
```

が行われます。

---

# 1. transpileとは何か

transpileとは：

```text
回路を実行可能な形に変換する処理
```

です。

つまり：

```text
抽象回路 → 実機対応回路
```

への変換です。

---

# 2. なぜtranspileが必要なのか

理由：

量子ハードウェアは：

```text
使えるゲートが限られている
```

からです。

例：

書いた回路：

```text
H
```

実機：

```text
RX + RZ に分解
```

される場合があります。

---

# 3. 基本構文

例：

```python
from qiskit import transpile

compiled = transpile(qc, backend)
```

意味：

```text
qc を backend 用に変換
```

---

# 4. backendとは何か

backendとは：

```text
回路を実行する対象
```

です。

例：

| backend      | 内容     |
| ------------ | ------ |
| AerSimulator | シミュレータ |
| FakeBackend  | 仮想実機   |
| IBM backend  | 実機     |

---

# 5. AerSimulatorでの例

```python
from qiskit_aer import AerSimulator
from qiskit import transpile

sim = AerSimulator()

compiled = transpile(qc, sim)
```

---

# 6. basis gatesとは何か

量子コンピュータは：

```text
限られたゲートしか実行できない
```

これを：

```text
basis gates
```

と呼びます。

例：

```text
u
cx
rz
sx
```

など。

---

# 7. basis gates を指定する

例：

```python
transpile(qc, basis_gates=["rz","sx","cx"])
```

意味：

```text
指定したゲートだけで回路を再構築
```

---

# 8. なぜ分解が必要なのか

例：

元の回路：

```text
H
```

変換後：

```text
RZ
SX
RZ
```

つまり：

```text
実機対応形式に変換
```

されます。

---

# 9. optimization levelとは何か

transpileには：

```text
最適化レベル
```

があります。

指定：

```python
transpile(qc, backend, optimization_level=3)
```

---

# 10. optimization level一覧

| level | 内容     |
| ----- | ------ |
| 0     | 最適化なし  |
| 1     | 軽い最適化  |
| 2     | 中程度最適化 |
| 3     | 最大最適化  |

試験頻出です。

---

# 11. optimization levelの効果

例：

Before：

```text
H H
```

After：

```text
削除
```

理由：

```text
H² = I
```

だからです。

---

# 12. qubit mappingとは何か

実機では：

```text
すべての量子ビットが直接接続されていない
```

そのため：

```text
位置調整
```

が必要になります。

これを：

```text
layout mapping
```

と呼びます。

---

# 13. SWAPが自動追加される理由

例：

```text
q0 と q5 を操作したい
```

しかし：

```text
接続されていない
```

場合：

```text
SWAP 挿入
```

されます。

---

# 14. transpile後の回路を見る

例：

```python
compiled.draw("text")
```

すると：

```text
変換後回路
```

が確認できます。

---

# 15. coupling mapとは何か

coupling map：

```text
量子ビット接続構造
```

例：

```text
0 — 1 — 2
```

なら：

```text
0 と 2 は直接通信できない
```

---

# 16. initial layoutとは何か

指定：

```python
transpile(qc, backend, initial_layout=[0,1])
```

意味：

```text
論理ビット → 物理ビット対応
```

---

# 17. routingとは何か

routing：

```text
接続制約を満たすよう回路変更
```

例：

```text
SWAP追加
```

---

# 18. schedulingとは何か（試験軽め）

scheduling：

```text
ゲート実行タイミング調整
```

です。

通常：

```text
自動処理
```

されます。

---

# 19. よく出る試験問題

問題：

transpileの目的は？

答え：

```text
回路をbackend対応形式へ変換
```

---

問題：

basis gatesとは？

答え：

```text
実機が実行可能なゲート集合
```

---

問題：

optimization_level=0とは？

答え：

```text
最適化なし
```

---

問題：

mappingとは？

答え：

```text
論理ビット → 物理ビット対応
```

---

# 20. transpileの典型フローまとめ

transpileは：

```text
分解
↓
最適化
↓
配置
↓
routing
↓
実行可能回路生成
```

を行います。

---

# 21. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ transpileの役割を説明できる
✅ backendの意味を説明できる
✅ basis gatesを説明できる
✅ optimization levelを説明できる
✅ mappingの意味を説明できる
✅ SWAPが挿入される理由を説明できる

---

次章：

**11_simulator.md**

では：

```text
Statevector simulator
QASM simulator
shot数の違い
いつどちらを使うか
```

を扱います。

ここも資格試験でよく出る領域です。
