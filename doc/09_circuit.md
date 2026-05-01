では第9章として、**回路合成（SWAP / Toffoli / barrier / compose / 回路読み取り力）**を資格試験対策レベルで体系的に解説します。
この章は：

* 多量子ビット回路を読む力
* 合成ゲートの意味
* 等価回路変換
* 回路構造の理解

を完成させる重要パートです。

---

# 09_circuit.md

# Part 9：回路合成（SWAP / Toffoli / barrier / compose）を完全に理解する

ここまでで：

* 単一量子ビット
* CNOT
* entanglement

を学びました。

この章では：

```text id="sxxv84"
複雑な回路をどう組み立てるか
```

を理解します。

資格試験では：

```text id="6s1hhl"
回路の意味を読む問題
```

として頻出です。

---

# 1. SWAPゲートとは何か

SWAPは：

```text id="bzpn3m"
2つの量子ビットを入れ替える
```

ゲートです。

変換：

SWAP|ab\rangle=|ba\rangle

例：

```text id="5n5hsj"
|01⟩ → |10⟩
```

---

# 2. QiskitでSWAPを書く

例：

```python id="aehg65"
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)

qc.swap(0,1)

qc.draw("text")
```

---

# 3. SWAPはCNOT3個で作れる（頻出）

重要関係：

SWAP=CX_{12}CX_{21}CX_{12}

つまり：

```text id="1fnp4o"
SWAPは基本ゲートで分解可能
```

---

# 4. なぜSWAPが重要なのか

理由：

量子ハードウェアでは：

```text id="mbgqk4"
隣接ビットしか操作できない
```

ことが多いためです。

つまり：

```text id="a3grvd"
位置調整に使う
```

---

# 5. Toffoliゲートとは何か

Toffoli：

```text id="p7q4q5"
2つのcontrol
1つのtarget
```

を持つゲートです。

別名：

```text id="n0m1y5"
CCX
```

---

# 6. Toffoliの動作

変換：

```text id="tpx5ym"
control1=1
control2=1
```

のときだけ：

```text id="b4rj79"
targetを反転
```

つまり：

古典ANDの量子版です。

---

# 7. QiskitでToffoliを書く

例：

```python id="w5v29m"
qc = QuantumCircuit(3)

qc.ccx(0,1,2)
```

意味：

```text id="wmc4u9"
q0,q1 が control
q2 が target
```

---

# 8. Toffoliは可逆AND

古典回路：

```text id="95vtfk"
ANDは不可逆
```

量子回路：

```text id="pp2kjp"
Toffoliは可逆
```

ここが重要です。

---

# 9. barrierとは何か

barrier：

```text id="fxqf3p"
回路の区切り
```

です。

例：

```python id="l8t8q9"
qc.barrier()
```

意味：

```text id="x4lz4h"
ここで最適化しない
```

---

# 10. barrierが必要な理由

理由：

transpilerが：

```text id="w60l9i"
回路を書き換える
```

からです。

barrierを入れると：

```text id="2faj4n"
構造を保持できる
```

---

# 11. composeとは何か

compose：

```text id="e0cw8y"
回路を結合する
```

操作です。

例：

```python id="yo2vtn"
qc1.compose(qc2)
```

意味：

```text id="4a1mwi"
qc1 の後に qc2 を実行
```

---

# 12. appendとの違い

append：

```text id="r0mx86"
ゲート追加
```

compose：

```text id="qqd8rf"
回路追加
```

---

# 13. 回路の順序の読み方（重要）

量子回路は：

```text id="dlv9d5"
上から下ではない
```

正しくは：

```text id="fsf7xu"
左から右
```

です。

例：

```
H → CX → measure
```

の順に実行されます。

---

# 14. 複合回路の例

例：

```python id="x20p86"
qc = QuantumCircuit(2)

qc.h(0)
qc.cx(0,1)
qc.swap(0,1)
```

順序：

```text id="hxozvt"
H
↓
CX
↓
SWAP
```

---

# 15. 等価回路（試験頻出）

例：

次の回路：

```
CX(0,1)
CX(1,0)
CX(0,1)
```

結果：

```text id="xqhtnp"
SWAP
```

---

# 16. Toffoliの応用

Toffoliは：

```text id="6vruym"
古典計算を量子回路に変換
```

できます。

つまり：

```text id="d0r0sn"
論理回路の量子化
```

に使われます。

---

# 17. 制御ゲートの一般化

例：

| ゲート | control数 |
| --- | -------- |
| X   | 0        |
| CX  | 1        |
| CCX | 2        |

つまり：

```text id="9bln2i"
controlは増やせる
```

---

# 18. multi-control gate

Qiskitでは：

```python id="dfz83l"
qc.mcx([0,1,2],3)
```

のように書けます。

意味：

```text id="8i0gdt"
3 control
1 target
```

---

# 19. よく出る試験問題

問題：

SWAPは何個のCXで作れる？

答え：

```text id="zoxd0r"
3個
```

---

問題：

Toffoliとは？

答え：

```text id="4yfgzd"
CCX
```

---

問題：

barrierの役割は？

答え：

```text id="9qbl34"
最適化防止
```

---

問題：

composeとは？

答え：

```text id="vr39nj"
回路結合
```

---

# 20. この章のチェックリスト（合格基準）✅

次ができればOK：

✅ SWAPの意味を説明できる
✅ SWAP=CX3個を理解している
✅ Toffoliの動作を説明できる
✅ barrierの役割を説明できる
✅ composeの意味を説明できる
✅ 回路順序を正しく読める

---

次章：

**10_transpile.md**

では：

```text id="eumh4p"
なぜtranspileが必要なのか
basis gatesとは何か
optimization levelとは何か
backendとは何か
```

を扱います。

ここは資格試験で確実に出題される重要領域です。
