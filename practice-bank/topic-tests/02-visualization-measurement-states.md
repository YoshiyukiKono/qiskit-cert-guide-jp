# Topic Test 02 — Visualization, Measurement, and States

全10問。各問1つ選択してください。

## Questions

### Q1
`QuantumCircuit` をMatplotlibベースの回路図として描画する呼び出しはどれか。

A. `plot_histogram(qc)`  
B. `qc.draw("mpl")`  
C. `Statevector(qc)`  
D. `qc.measure_all()`

### Q2
Sampler等から得た `counts = {"00": 510, "11": 514}` を棒グラフで比較したい。代表的なQiskit visualization関数はどれか。

A. `plot_state_qsphere(counts)`  
B. `plot_bloch_multivector(counts)`  
C. `qc.draw(counts)`  
D. `plot_histogram(counts)`

### Q3
Qiskitのcounts文字列`"10"`について、通常もっとも右側の文字が対応するclassical bitはどれか。

A. bit 0  
B. bit 1  
C. physical qubit 0に必ず固定される  
D. register mappingに関係なく常にbit 1になる

### Q4
Bell状態 `(|00>+|11>)/sqrt(2)` のcomputational-basis測定分布として正しいものはどれか。

A. 01と10が約50%ずつ  
B. 4通りが25%ずつ  
C. 00と11が約50%ずつ  
D. 常に00

### Q5
`plot_histogram` と `plot_distribution` の入力について最も適切な説明はどれか。

A. どちらもQuantumCircuitしか受け取れない  
B. sampled data/distributionを可視化するための関数であり、statevectorそのものの可視化とは役割が異なる  
C. どちらもbackend coupling map専用  
D. どちらもOpenQASM exporterである

### Q6
1量子ビット状態をBloch球として表示する代表的な関数はどれか。

A. `plot_histogram`  
B. `circuit_drawer`  
C. `plot_state_city`だけが唯一の方法  
D. `plot_bloch_multivector`

### Q7
`plot_state_qsphere` の表現について正しいものはどれか。

A. basis-stateに対応する点の大きさで確率、色で位相を表現できる  
B. coupling mapだけを描く  
C. countsのshot数だけを表示する  
D. circuit depthだけを表示する

### Q8
次の回路の状態ベクトルを、測定を行わずに直接求めたい。

```python
qc = QuantumCircuit(1)
qc.h(0)
```

最も直接的なのはどれか。

A. `qc.measure_all()`  
B. `plot_histogram(qc)`  
C. `Statevector.from_instruction(qc)`  
D. `qc.draw()`

### Q9
状態 `(1/sqrt(2))[1, i]` のcomputational-basis測定確率はどれか。

A. `P(0)=1, P(1)=0`  
B. `P(0)=P(1)=1/2`  
C. `P(0)=0, P(1)=1`  
D. 位相が複素数なので確率は定義できない

### Q10
mid-circuit measurementを含む回路の状態について最も適切な説明はどれか。

A. 測定後も結果に依存せず常に同じpure stateである  
B. measurementは描画上の記号にすぎない  
C. measurementを追加するとclassical informationは生成されない  
D. measurementは非ユニタリであり、post-measurement stateは結果に依存し得る

---

# Answers & Explanations

### A1 — B
- A: `plot_histogram`は測定分布用。
- B: 正解。`qc.draw("mpl")`はMatplotlib circuit drawerを使う。
- C: state representationを作る操作で、回路図描画ではない。
- D: measurement命令を追加する。

### A2 — D
- A/B: quantum state visualizationでありcounts用ではない。
- C: `draw`はcircuit visualization。
- D: 正解。bitstring frequency/countsの比較に使う。

### A3 — A
Qiskitの通常のbitstring表示ではbit 0が右端。
- A: 正解。
- B/D: 左右が逆。
- C: classical bitとphysical qubitを同一視している。measurement mappingを確認する必要がある。

### A4 — C
Bell状態の非零振幅は00と11のみで各`1/sqrt(2)`。
- A/B/D: statevectorの非零成分と一致しない。
- C: 正解。

### A5 — B
- A: circuit-only関数ではない。
- B: 正解。measurement/distribution visualizationとstate visualizationは区別する。
- C: coupling map visualizationとは別。
- D: serializationではない。

### A6 — D
- A: sampled outcomes用。
- B: circuit drawing用。
- C: `plot_state_city`もstate visualizationだが唯一ではない。
- D: 正解。各qubitについてBloch sphereを描く。

### A7 — A
- A: 正解。Q-sphereはbasis componentのprobabilityとphaseの視覚化に使える。
- B/C/D: Q-sphereの役割ではない。

### A8 — C
- A: 測定命令を追加するので目的と異なる。
- B: counts/distribution visualization。
- C: 正解。測定のない回路を初期`|0...0>`へ作用させたStatevectorを得られる。
- D: 回路を描くだけ。

### A9 — B
確率は振幅の絶対値二乗なので両方1/2。
- A/C: amplitude magnitudeが等しいことと矛盾する。
- B: 正解。
- D: complex amplitudeからBorn則で実確率を得る。

### A10 — D
- A: measurement outcomeで分岐し得る。
- B: measurementは物理的操作を表す。
- C: classical outputへ結果を保存できる。
- D: 正解。

## Official references

- Visualization API: https://quantum.cloud.ibm.com/docs/en/api/qiskit/visualization
- State visualizations: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.plot_state_qsphere
- Bit ordering: https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering
