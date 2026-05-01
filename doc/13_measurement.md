では第13章として、**measurement（測定）の数理・collapse（収縮）・部分測定・古典レジスタとの関係**を資格試験対策レベルで体系的に解説します。

この章は非常に重要です。理由：

```text id="4y8qps"
量子回路の最終出力は measurement で決まる
```

ためです。

試験では：

* 測定後の状態
* 測定確率
* 部分測定の影響
* classical register の意味

が頻出です。

---

# 13_measurement.md

# Part 13：measurement（測定）を完全に理解する

量子回路は：

```text id="c5q7ax"
measurement しない限り classical result は得られない
```

ここが古典計算との最大の違いです。

---

# 1. measurementとは何か

measurementとは：

```text id="5sj1m3"
量子状態を classical bit に変換する操作
```

です。

つまり：

```text id="hzsj9j"
確率的に 0 または 1 が出る
```

---

# 2. Bornの規則（試験最重要）

測定確率は：

P(i)=|\langle i|\psi\rangle|^2

つまり：

```text id="f0kp2n"
振幅の2乗が測定確率
```

です。

---

# 3. 測定後に何が起きるか（collapse）

測定すると：

```text id="6gls4x"
状態が確定する
```

例：

測定前：

[
(|0\rangle+|1\rangle)/\sqrt{2}
]

測定後：

```text id="tqq3q6"
50% → |0⟩
50% → |1⟩
```

になります。

---

# 4. collapseとは何か

collapse：

```text id="4dqkqv"
重ね合わせが消える
```

ことです。

つまり：

```text id="gxk4h1"
測定後は superposition ではなくなる
```

---

# 5. 測定を2回するとどうなるか

例：

初回測定：

```text id="2n7rwx"
|0⟩
```

2回目測定：

```text id="g7f9xv"
必ず |0⟩
```

理由：

```text id="ypp4c9"
collapse 済み
```

だからです。

---

# 6. Qiskitでmeasurementを書く

構文：

```python
qc.measure(qubit, classical_bit)
```

例：

```python
qc.measure(0,0)
```

意味：

```text id="wq7r3a"
qubit0 → classical bit0
```

---

# 7. classical registerとは何か

classical register：

```text id="kzfxkt"
測定結果の保存領域
```

です。

例：

```python
QuantumCircuit(1,1)
```

意味：

```text id="t5vq0x"
1 quantum bit
1 classical bit
```

---

# 8. なぜclassical bitが必要なのか

理由：

measurement結果は：

```text id="cbsl8s"
量子状態ではなく古典値
```

だからです。

---

# 9. 複数量子ビット測定

例：

```python
qc.measure([0,1],[0,1])
```

意味：

```text id="0z0u4u"
2つの qubit を同時測定
```

---

# 10. Bell状態の測定例

状態：

[
(|00\rangle+|11\rangle)/\sqrt{2}
]

測定結果：

| 出力 | 確率  |
| -- | --- |
| 00 | 50% |
| 11 | 50% |

重要：

```text id="qkzyxg"
01 と 10 は出ない
```

---

# 11. 部分測定とは何か（重要）

例：

状態：

[
(|00\rangle+|11\rangle)/\sqrt{2}
]

qubit0だけ測定：

結果：

```text id="m7l9sm"
0 または 1
```

そして：

残りの状態は：

```text id="ryhv6a"
自動的に決まる
```

---

# 12. 部分測定の具体例

もし：

```text id="w7qp7l"
qubit0 = 0
```

なら：

```text id="22j1mv"
qubit1 = 0
```

もし：

```text id="oj3c8q"
qubit0 = 1
```

なら：

```text id="pf4qxy"
qubit1 = 1
```

つまり：

```text id="vjlwmh"
測定が他の量子ビットに影響する
```

---

# 13. separable状態の部分測定

状態：

[
(|00\rangle+|01\rangle)/\sqrt{2}
]

qubit0測定：

```text id="kvtq1y"
影響なし
```

理由：

```text id="d5v9v5"
entangled ではない
```

---

# 14. measurement順序の意味

例：

```python
qc.measure(0,0)
qc.measure(1,1)
```

順序：

```text id="wrzfr3"
左から右
```

ただし：

```text id="3qzpgz"
同時測定扱い
```

になります。

---

# 15. measure_all()

便利関数：

```python
qc.measure_all()
```

意味：

```text id="n2lm9y"
全 qubit 測定
```

---

# 16. measurementなしで実行するとどうなるか

例：

```python
qc.h(0)
```

結果：

```text id="6p1ps5"
counts は取得できない
```

理由：

```text id="4q2gqz"
classical register がない
```

---

# 17. 測定結果の取得方法

例：

```python
result.get_counts()
```

出力：

```text id="zaz1h1"
{'0':512,'1':512}
```

---

# 18. bit順序に注意（試験頻出）

例：

```python
qc.measure([0,1],[0,1])
```

出力：

```text id="kq2s1p"
'10'
```

意味：

```text id="6w9nyv"
q1 q0 の順
```

です。

重要：

```text id="p8pyzz"
little endian 表記
```

---

# 19. よく出る試験問題

問題：

measurementの結果は何で決まる？

答え：

```text id="i0o5fq"
振幅の2乗
```

---

問題：

measurement後の状態は？

答え：

```text id="c5r0lt"
collapse する
```

---

問題：

部分測定すると何が起きる？

答え：

```text id="3d6i5s"
残りの状態が変化する場合がある
```

---

問題：

measurementなしでcounts取得できる？

答え：

```text id="q0z3qr"
できない
```

---

# 20. measurementの流れまとめ

measurementは：

```text id="i9y6l8"
振幅
↓
確率
↓
collapse
↓
classical bit 出力
```

というプロセスです。

---

# 21. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ Born rule を説明できる
✅ collapse を説明できる
✅ 部分測定の影響を説明できる
✅ classical register を説明できる
✅ counts取得条件を理解している
✅ little endian を理解している

---

次章：

**14_phase.md**

では：

```text id="s6v9cf"
Zゲート
Sゲート
Tゲート
phase kickback
位相が計算を変える仕組み
```

を扱います。

ここから **量子アルゴリズム理解の核心領域** に入ります。
