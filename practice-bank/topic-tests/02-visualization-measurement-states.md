# Topic Test 02 — Visualization, Measurement, and States

全10問。各問1つ選択してください。

## Questions

### Q1
次の回路を実行前の状態ベクトルとして得たい。最も直接的な方法はどれか。

```python
qc = QuantumCircuit(1)
qc.h(0)
```

A. `Statevector.from_instruction(qc)`  
B. `qc.measure_all()`  
C. `transpile(qc)`  
D. `qc.draw()`

### Q2
`|+>` を computational basis で多数回測定したときの理想的な結果はどれか。

A. 常に0  
B. 常に1  
C. 0と1が約50%ずつ  
D. 測定できない

### Q3
Bell状態 `(|00>+|11>)/sqrt(2)` を computational basis で測定した結果として理想的なのはどれか。

A. 00, 01, 10, 11 が各25%  
B. 00 と 11 が各50%程度  
C. 01 と 10 が各50%程度  
D. 常に00

### Q4
Qiskit の counts で2ビット文字列 `'10'` を見るとき、通常もっとも右側の文字が対応する classical bit はどれか。

A. bit 0  
B. bit 1  
C. qubit 1 に固定  
D. backend 次第で定義されない

### Q5
`qc.draw("mpl")` の目的として最も適切なのはどれか。

A. 回路をMatplotlibベースで描画する  
B. 状態ベクトルを計算する  
C. 回路を実機で実行する  
D. OpenQASM 3を読み込む

### Q6
状態ベクトル `(1/sqrt(2))[1, i]` の computational basis 測定確率はどれか。

A. P(0)=1, P(1)=0  
B. P(0)=0, P(1)=1  
C. P(0)=P(1)=1/2  
D. 位相 i のため確率は定義できない

### Q7
単一量子ビットの pure state を Bloch 球上で表すとき、`|0>` は通常どこに置かれるか。

A. +Z 軸  
B. -Z 軸  
C. +X 軸  
D. +Y 軸

### Q8
測定を回路の途中に入れた場合について正しいものはどれか。

A. どの statevector simulator でも純粋状態として最後まで一意に扱える  
B. 測定は一般に非ユニタリであり、その後の状態は測定結果に依存し得る  
C. 測定は単なる描画命令である  
D. 測定しても classical bit は不要

### Q9
`Statevector.probabilities_dict()` が返すものとして最も適切なのはどれか。

A. 基底状態ごとの確率の辞書  
B. gate error rate  
C. transpiler の pass 一覧  
D. backend の calibration data

### Q10
`|->=(|0>-|1>)/sqrt(2)` を H で変換した後 computational basis で測定すると理想的にはどうなるか。

A. 常に0  
B. 常に1  
C. 50/50  
D. 25/75

---

# Answers & Explanations

### A1 — A
`Statevector.from_instruction(qc)` は、測定を含まない回路を `|0...0>` に作用させた状態を直接構成できる。
- B は測定命令の追加。
- C は変換。
- D は可視化。

### A2 — C
`|+>` の振幅は0,1とも `1/sqrt(2)` なので Born 則により各1/2。

### A3 — B
Bell状態に存在する computational basis 成分は `00` と `11` のみで、それぞれ振幅 `1/sqrt(2)`。

### A4 — A
Qiskit のビット文字列表現では classical bit 0 が通常右端に表示される。ここは回路図のワイヤ順と混同しやすい。

### A5 — A
`draw("mpl")` は回路図を Matplotlib 形式で表示するための描画機能。

### A6 — C
確率は振幅の絶対値二乗。`|1/sqrt(2)|^2=1/2`、`|i/sqrt(2)|^2=1/2`。位相だけでは computational basis の確率は変わらない。

### A7 — A
標準的な Bloch 球では `|0>` が北極(+Z)、`|1>` が南極(-Z)。

### A8 — B
projective measurement は一般に非ユニタリで、得られた古典結果によって post-measurement state が分岐する。

### A9 — A
`probabilities_dict()` は basis label とその確率を対応させる。測定を実際にshot samplingした countsとは区別する。

### A10 — B
`H|->=|1>`。したがって理想的な computational basis 測定では1が100%。

## Score guide

bit ordering と phase を伴う確率解釈で間違えた場合は、その2点を優先して復習してください。
