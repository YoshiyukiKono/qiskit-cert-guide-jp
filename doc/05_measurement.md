では第5章として、**測定（measurement）**を資格試験対策レベルで体系的に解説します。
この章は非常に重要です。理由は：

* 測定＝確率の発生源
* 測定＝状態の破壊
* shots / counts の理解
* Statevectorとの違い

が試験で頻出だからです。

---

# 05_measurement.md

# Part 5：測定（measurement）を完全に理解する

量子計算では：

```text
測定するまで状態は確定しない
```

という特徴があります。

そして：

```text
測定すると状態が壊れる
```

ここが古典計算との決定的な違いです。

---

# 1. 測定とは何か

量子測定とは：

```text
量子状態 → 古典値
```

への変換です。

例：

状態

[
(|0\rangle + |1\rangle)/\sqrt{2}
]

測定すると：

```text
|0⟩ または |1⟩
```

どちらかになります。

---

# 2. 測定確率（Bornの規則）

測定確率は次で決まります：

P(0)=|a|^2,\quad P(1)=|b|^2

ここで：

[
|\psi\rangle=a|0\rangle+b|1\rangle
]

です。

つまり：

```text
振幅の2乗が確率になる
```

これを：

```text
Born rule
```

と呼びます（試験で名称が出る場合あり）。

---

# 3. 測定すると状態は壊れる

例：

初期状態：

[
(|0\rangle + |1\rangle)/\sqrt{2}
]

測定結果：

```text
|0⟩
```

になった場合：

状態は

```text
完全に |0⟩ に変わる
```

元には戻りません。

---

# 4. Qiskitで測定を書く

測定は次で書きます：

```python
qc.measure(quantum_bit, classical_bit)
```

例：

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(1,1)

qc.h(0)
qc.measure(0,0)

qc.draw("text")
```

意味：

```text
量子ビット0 → 古典ビット0
```

---

# 5. simulatorで測定結果を見る

例：

```python
from qiskit_aer import AerSimulator
from qiskit import transpile

sim = AerSimulator()

compiled = transpile(qc, sim)

result = sim.run(compiled).result()

counts = result.get_counts()

print(counts)
```

例：

```text
{'0': 512, '1': 512}
```

---

# 6. countsとは何か

countsは：

```text
測定結果の出現回数
```

です。

例：

```text
{'0': 520, '1': 504}
```

意味：

| 状態 | 回数  |
| -- | --- |
| 0  | 520 |
| 1  | 504 |

---

# 7. shotsとは何か

重要概念です ⭐

shotsとは：

```text
回路を何回実行したか
```

です。

例：

```python
sim.run(compiled, shots=1000)
```

意味：

```text
1000回測定
```

---

# 8. なぜ複数回実行するのか

理由：

量子測定は確率だからです。

1回だけ実行すると：

```text
結果がランダム
```

になります。

例：

```text
1回 → 0
```

でも：

```text
本当に100% 0とは限らない
```

---

# 9. shotsを増やすと何が起きるか

shotsを増やすほど：

```text
理論値に近づく
```

例：

| shots | 結果        |
| ----- | --------- |
| 10    | 6 / 4     |
| 100   | 52 / 48   |
| 1000  | 503 / 497 |

---

# 10. 測定しない場合どうなるか

例：

```python
qc = QuantumCircuit(1)

qc.h(0)
```

この回路は：

```text
確率を出力しない
```

代わりに：

```text
状態ベクトル
```

を持ちます。

---

# 11. Statevectorと測定の違い

比較：

| 方法          | 出力 |
| ----------- | -- |
| Statevector | 振幅 |
| measurement | 確率 |

例：

Statevector：

```text
[0.707, 0.707]
```

measurement：

```text
{'0': 512, '1': 512}
```

---

# 12. 測定は最後に行う理由

量子回路では通常：

```text
最後に測定する
```

理由：

途中で測定すると：

```text
状態が壊れる
```

からです。

---

# 13. 途中測定の例

例：

```python
qc.h(0)
qc.measure(0,0)
qc.h(0)
```

ここで：

```text
2回目のHは意味が変わる
```

なぜなら：

```text
状態が確定している
```

からです。

---

# 14. 多量子ビット測定

例：

```python
qc = QuantumCircuit(2,2)

qc.h(0)
qc.cx(0,1)

qc.measure([0,1],[0,1])
```

結果：

```text
{'00': 512, '11': 512}
```

意味：

```text
Bell状態
```

---

# 15. 測定順序に注意

例：

```python
qc.measure([0,1],[1,0])
```

意味：

```text
順番が入れ替わる
```

試験で出ます ⚠️

---

# 16. histogramの読み方

Qiskitでは：

```python
from qiskit.visualization import plot_histogram
```

で表示できます。

例：

```python
plot_histogram(counts)
```

これは：

```text
確率分布の可視化
```

です 📊

---

# 17. よく出る試験問題

問題：

次の状態の測定結果は？

[
(|0\rangle+|1\rangle)/\sqrt{2}
]

答え：

```text
50%
50%
```

---

問題：

測定後の状態は？

```text
|0⟩ または |1⟩
```

---

問題：

shotsとは？

答え：

```text
回路実行回数
```

---

問題：

測定前の状態は観測できるか？

答え：

```text
できない
```

---

# 18. 測定の数学的意味

測定とは：

```text
射影操作
```

です。

つまり：

状態：

[
|\psi\rangle
]

が：

[
|0\rangle
]

または

[
|1\rangle
]

に変わります。

---

# 19. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ 振幅の2乗が確率になると説明できる
✅ shotsの意味を説明できる
✅ countsを読める
✅ 測定後に状態が壊れると説明できる
✅ Statevectorとの違いを説明できる
✅ 測定順序の意味を理解している

---

次章：

**06_bloch.md**

では：

```text
量子状態を「回転」として理解する方法
```

を扱います。

ここから理解が一段深くなります 🧭
