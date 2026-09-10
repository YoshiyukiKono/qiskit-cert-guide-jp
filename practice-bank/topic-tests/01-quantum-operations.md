# Topic Test 01 — Quantum Operations

全10問。各問1つ選択してください。Qiskit v2.xのAPI表記と、状態ベクトルとしての厳密な等式を区別してください。

## Questions

### Q1
`H` を同じ量子ビットに2回連続で適用した操作と等価なのはどれか。

A. X  
B. Z  
C. I  
D. S

### Q2
状態 `(|0> + i|1>)/sqrt(2)` に `S†` を適用した結果はどれか。

A. `|1>`  
B. `|->`  
C. `(|0>-i|1>)/sqrt(2)`  
D. `|+>`

### Q3
`Rx(pi)` を行列として評価したとき正しいものはどれか。

A. `Rx(pi)=X`  
B. `Rx(pi)=-iX`  
C. `Rx(pi)=Z`  
D. `Rx(pi)=iZ`

### Q4
`H Z H` と等価なのはどれか。

A. X  
B. Y  
C. Z  
D. S

### Q5
グローバル位相について最も正しい説明はどれか。

A. `e^{iφ}` を掛けると必ずcomputational-basis確率が変わる  
B. 相対位相と同じ情報なので干渉で常に区別できる  
C. Qiskitではglobal phaseを持つ回路を表現できない  
D. 状態全体に同じ位相を掛けても単独の物理状態としては区別されない

### Q6
`Z|+>` の結果はどれか。

A. `|0>`  
B. `i|+>`  
C. `|->`  
D. `|1>`

### Q7
computational basisでcontrol=`0`のとき、`CX(control, target)` のtargetへの作用はどれか。

A. Zを適用する  
B. targetを変化させない  
C. 常にXを適用する  
D. targetを測定する

### Q8
Qiskitの2-qubit Pauli label `"XZ"` の文字とqubitの対応について正しいものはどれか。

A. 左端のXがq0、右端のZがq1  
B. XもZもq0へ順番に作用する  
C. Pauli labelにはqubit orderingが存在しない  
D. 右端のZがq0、左端のXがq1

### Q9
**グローバル位相を省略せず、行列積として厳密に** `Y|0>` と等しいものはどれか。

A. `|1>`  
B. `-i|1>`  
C. `i|1>`  
D. `-|1>`

### Q10
`SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])` が表すものとして最も適切なのはどれか。

A. Pauli stringの線形結合 `0.5 ZI - XX`  
B. 2つの測定counts  
C. 2つのQuantumCircuitを連結したもの  
D. ZとXの固有値だけを保存したclassical array

---

# Answers & Explanations

### A1 — C
`H^2=I`。
- A: Xではない。例えば`|0>`へ2回Hを作用させると`|0>`へ戻る。
- B: Zでもない。
- C: 正解。Hadamardは自己逆。
- D: Sは位相ゲートで作用が異なる。

### A2 — D
`S†=diag(1,-i)` なので `i(-i)=1`、結果は`(|0>+|1>)/sqrt(2)=|+>`。
- A/B/C: `|1>`成分への係数計算と一致しない。
- D: 正解。

### A3 — B
`Rx(theta)=exp(-i theta X/2)` なので `Rx(pi)=-iX`。
- A: 物理状態への作用をglobal phaseまで無視すればX相当だが、行列等式としては不足。
- B: 正解。
- C/D: 回転軸がXなのでZにはならない。

### A4 — A
Hadamard conjugationでXとZが交換され、`HZH=X`。
- B/D: 対応する恒等式ではない。
- C: Hで挟むことでZのままではない。

### A5 — D
状態全体への共通因子`e^{iφ}`はrayとして同じ物理状態を表す。
- A: Born則の絶対値二乗で共通位相は消える。
- B: 相対位相は成分間の差でありglobal phaseとは異なる。
- C: Qiskitの回路はglobal phaseを保持できる。
- D: 正解。

### A6 — C
`|+>=(|0>+|1>)/sqrt(2)`で、Zは`|1>`成分だけ符号反転するため`|->`。
- A/D: 重ね合わせがbasis stateへ直接collapseする操作ではない。
- B: Zの作用ではない。

### A7 — B
CXはcontrolが1のときだけtargetへXを作用させる。
- A: controlled-Zとは異なる。
- B: 正解。
- C: control条件を無視している。
- D: CXはmeasurementではない。

### A8 — D
QiskitのPauli stringでは右端がq0、左へ向かって高いqubit indexに対応する。
- A: orderingが逆。
- B/C: Pauli labelはtensor-product operatorを表し、qubit orderingを持つ。
- D: 正解。

### A9 — C
`Y=[[0,-i],[i,0]]`より`Y|0>=i|1>`。
- A/B/D: 物理rayとしてはglobal phaseだけの違いを含むものもあるが、設問は行列積として厳密な等式を要求している。
- C: 正解。

### A10 — A
`SparsePauliOp`はPauli stringsの疎な線形結合を表すobservable表現。
- A: 正解。
- B: countsではない。
- C: circuit compositionではない。
- D: classical eigenvalue arrayではない。

## Official references

- Pauli / quantum information: https://quantum.cloud.ibm.com/docs/en/api/qiskit/quantum_info
- Qiskit bit ordering: https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering
- `SparsePauliOp`: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.SparsePauliOp
