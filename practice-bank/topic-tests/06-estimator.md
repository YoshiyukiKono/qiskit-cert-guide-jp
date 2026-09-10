# Topic Test 06 — Estimator Primitive

全10問。各問1つ選択してください。

## Questions

### Q1
Estimator primitive の主目的として最も適切なのはどれか。

A. observable の期待値を推定する  
B. bitstring counts だけを返す  
C. circuit drawing を生成する  
D. OpenQASMファイルを圧縮する

### Q2
Qiskit SDK のローカル V2 Estimator 実装として代表的なのはどれか。

A. `StatevectorEstimator`  
B. `StatevectorSampler`  
C. `Target`  
D. `ClassicalRegister`

### Q3
`|0>` に対する Pauli-Z の期待値 `<Z>` はいくつか。

A. +1  
B. 0  
C. -1  
D. 1/2

### Q4
`|+>` に対する Pauli-Z の期待値 `<Z>` はいくつか。

A. +1  
B. 0  
C. -1  
D. 2

### Q5
`|+>` に対する Pauli-X の期待値 `<X>` はいくつか。

A. +1  
B. 0  
C. -1  
D. 1/2

### Q6
Estimator V2 の PUB に含まれる中心的な組み合わせはどれか。

A. circuit と observable、必要に応じて parameter values / precision  
B. circuit drawing と PNG filename  
C. counts と histogram color  
D. backend password と API token

### Q7
`SparsePauliOp` の用途として適切なのはどれか。

A. Pauli項の線形結合として observable を表す  
B. classical bitを量子ビットへ変換する  
C. network latencyを測る  
D. shot数を自動増加する

### Q8
`StatevectorEstimator` の理想的な unitary-only circuit で、Pauli observable の期待値を求める場合の特徴はどれか。

A. statevectorに基づき厳密値を得られる  
B. 必ず8192 shotsを使う  
C. countsしか得られない  
D. 量子実機への接続が必須

### Q9
Estimator の precision と Sampler の shots を概念的に区別する説明として最も良いものはどれか。

A. Estimatorでは期待値推定の精度要求、Samplerではサンプル数が中心的な制御になる  
B. 両者は必ず同じ整数でなければならない  
C. precisionはqubit数を意味する  
D. shotsはobservable数を意味する

### Q10
2量子ビット状態 `|00>` に対する observable `ZZ` の期待値はいくつか。

A. +1  
B. 0  
C. -1  
D. 2

---

# Answers & Explanations

### A1 — A
Estimator は circuit と observable の組を評価し、期待値を得る primitive。sampled bitstringを主目的とするSamplerと区別する。

### A2 — A
`qiskit.primitives.StatevectorEstimator` は V2 Estimator の参照実装。

### A3 — A
`Z|0>=+|0>` なので `|0>` は Z の固有値 +1 の固有状態。

### A4 — B
`|+>` は Z 測定で0/1が等確率。固有値 +1 と -1 の平均は0。

### A5 — A
`|+>` は X の固有値 +1 の固有状態なので `<X>=1`。

### A6 — A
Estimator PUB は circuit と observables を核に持ち、必要に応じparameter valuesやprecisionを伴う。

### A7 — A
`SparsePauliOp` は `0.5*ZI - 1.2*XX` のような Pauli basis の線形結合を表現でき、Hamiltonian/observable表現に便利。

### A8 — A
ローカルの statevector-based estimator は unitary-only の純粋状態についてPauli observableを厳密評価できる。実機noiseやsamplingとは別の性質。

### A9 — A
V2 APIではSamplerとEstimatorで結果品質を制御する概念が異なる。実装固有optionsは最新ドキュメントで確認する。

### A10 — A
Zの固有値は各`|0>`で+1。`Z⊗Z` の固有値は積で +1。
