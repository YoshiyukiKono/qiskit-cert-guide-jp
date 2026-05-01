では第11章として、**シミュレータ（AerSimulator / Statevector / QASM）**を資格試験対策レベルで体系的に解説します。
この章は：

* simulatorの種類の違い
* いつどれを使うか
* Statevectorとの関係
* shotsとの関係
* 実機との違い

を整理する重要パートです。

---

# 11_simulator.md

# Part 11：Simulator（Statevector / QASM / Aer）を完全に理解する

量子回路は：

```text id="y0fwcy"
必ずしも実機で動かす必要はない
```

まずは：

```text id="i8mzv9"
シミュレータ
```

で検証できます。

資格試験でも：

```text id="97v53q"
どの simulator を使うべきか
```

が問われます。

---

# 1. Simulatorとは何か

Simulatorとは：

```text id="u02yfp"
量子コンピュータを古典計算機で模擬する仕組み
```

です。

目的：

```text id="4rgf8g"
回路の動作確認
```

---

# 2. Qiskitの代表的Simulator

代表例：

| Simulator    | 内容      |
| ------------ | ------- |
| Statevector  | 振幅を出力   |
| QASM         | 測定結果を出力 |
| AerSimulator | 高性能統合版  |

---

# 3. AerSimulatorとは何か

AerSimulatorは：

```text id="vr23l1"
標準の量子回路シミュレータ
```

です。

使用例：

```python id="4vcv2t"
from qiskit_aer import AerSimulator

sim = AerSimulator()
```

---

# 4. 基本的な実行方法

例：

```python id="x3q9oj"
from qiskit import transpile

compiled = transpile(qc, sim)

result = sim.run(compiled).result()

counts = result.get_counts()

print(counts)
```

---

# 5. Statevector simulatorとは何か

Statevector simulatorは：

```text id="3f5f1e"
量子状態そのものを出力
```

します。

例：

```python id="0h7kh4"
from qiskit.quantum_info import Statevector

state = Statevector.from_instruction(qc)

print(state)
```

出力：

```text id="xl6x7g"
[0.707, 0.707]
```

---

# 6. QASM simulatorとは何か

QASM simulatorは：

```text id="pm6sy3"
測定結果を確率的に出力
```

します。

例：

```python id="0ysv2o"
counts = result.get_counts()
```

出力：

```text id="xihwkg"
{'0': 512, '1': 512}
```

---

# 7. StatevectorとQASMの違い

比較：

| Simulator   | 出力   |
| ----------- | ---- |
| Statevector | 振幅   |
| QASM        | 測定結果 |

つまり：

```text id="4kfxi2"
Statevector = 理論状態
QASM = 実験結果
```

です。

---

# 8. なぜ2種類必要なのか

理由：

Statevector：

```text id="n0pkkm"
理論確認
```

QASM：

```text id="kmgl2k"
実機挙動の模擬
```

---

# 9. 測定がない回路の場合

例：

```python id="5d8i7u"
qc = QuantumCircuit(1)

qc.h(0)
```

この回路では：

```text id="9lq0jt"
counts は取得できない
```

理由：

```text id="kpzqso"
測定がない
```

からです。

---

# 10. 測定を追加する

例：

```python id="f2o3vb"
qc.measure(0,0)
```

すると：

```text id="m5xzbs"
counts が取得可能
```

になります。

---

# 11. shotsの意味（復習）

例：

```python id="bdb8q0"
sim.run(compiled, shots=1000)
```

意味：

```text id="znvq5j"
1000回測定
```

---

# 12. shotsを変えるとどうなるか

例：

shots=10

```text id="nt7q31"
{'0':6,'1':4}
```

shots=1000

```text id="o4k9y1"
{'0':503,'1':497}
```

つまり：

```text id="cxt7l5"
理論値に収束
```

します。

---

# 13. AerSimulatorのmode

AerSimulatorは：

```text id="4k6e0v"
複数の実行方式
```

を持ちます。

例：

| mode           | 内容            |
| -------------- | ------------- |
| statevector    | 状態出力          |
| density_matrix | ノイズ対応         |
| stabilizer     | Clifford回路高速化 |

---

# 14. statevector mode

例：

```python id="v7ktwi"
AerSimulator(method="statevector")
```

意味：

```text id="8k9v6k"
振幅を直接計算
```

---

# 15. density matrix mode

例：

```python id="k6vrzt"
AerSimulator(method="density_matrix")
```

意味：

```text id="8tqzw7"
ノイズ込みシミュレーション
```

---

# 16. stabilizer mode

例：

```python id="k8z7n0"
AerSimulator(method="stabilizer")
```

特徴：

```text id="fvg7zl"
高速
```

ただし：

```text id="33dbw5"
Clifford回路限定
```

---

# 17. 実機との違い

Simulator：

```text id="zk1p1g"
理想状態
```

実機：

```text id="c6mj4o"
ノイズあり
```

つまり：

```text id="aj1z5k"
結果が一致しないことがある
```

---

# 18. FakeBackendとは何か

FakeBackend：

```text id="f07jgx"
実機構造を模擬
```

例：

```python id="2x7f7r"
from qiskit.providers.fake_provider import FakeManila
```

意味：

```text id="4d3p9y"
実機に近い検証
```

---

# 19. よく出る試験問題

問題：

Statevector simulatorの出力は？

答え：

```text id="v4p4l7"
振幅
```

---

問題：

QASM simulatorの出力は？

答え：

```text id="1cvtfh"
counts
```

---

問題：

shotsとは？

答え：

```text id="mkn62q"
測定回数
```

---

問題：

測定なし回路でcounts取得できる？

答え：

```text id="4bznbc"
できない
```

---

# 20. simulator選択の指針まとめ

| 目的    | simulator      |
| ----- | -------------- |
| 状態確認  | Statevector    |
| 確率確認  | QASM           |
| 実機模擬  | AerSimulator   |
| ノイズ検証 | density_matrix |

---

# 21. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ Statevector simulatorを説明できる
✅ QASM simulatorを説明できる
✅ AerSimulatorを説明できる
✅ shotsの意味を説明できる
✅ FakeBackendを説明できる
✅ simulatorと実機の違いを説明できる

---

次章：

**12_statevector.md**

では：

```text id="fwvz3v"
Statevectorの読み方
振幅の解釈
位相の意味
確率の計算
```

を扱います。

ここまで理解すると回路出力予測問題が解けるようになります。
