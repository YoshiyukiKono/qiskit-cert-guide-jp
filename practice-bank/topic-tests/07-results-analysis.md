# Topic Test 07 — Retrieving and Analyzing Results

全10問。各問1つ選択してください。

## Questions

### Q1
1000 shots の counts が `{'0': 750, '1': 250}` だった。経験的な `P(1)` はいくつか。

A. 0.25  
B. 0.5  
C. 0.75  
D. 1.0

### Q2
counts と exact probability の違いとして正しいものはどれか。

A. counts は有限shotの観測頻度、probability は理論分布を表し得る  
B. 完全に同じ概念  
C. counts は必ず複素数  
D. probability は必ず整数

### Q3
2ビット counts の `'01'` を Qiskit の通常の文字列表現として読むとき、右端は何に対応するか。

A. classical bit 0  
B. classical bit 1  
C. 常にqubit 1  
D. physical qubit番号とは無関係なので何にも対応しない

### Q4
Sampler結果を分析するとき、最初に確認すべきものの一つはどれか。

A. どの classical register にどの measurement が格納されたか  
B. Git commit hash  
C. monitor解像度  
D. Python実行ファイル名

### Q5
Estimator結果の `evs` という語が一般に指すものはどれか。

A. expectation values  
B. execution versions  
C. error vectors  
D. encoded variables

### Q6
理想的に `P(0)=0.8` の回路を100 shotsで実行し、0が76回だった。最も適切な判断はどれか。

A. 有限標本として十分あり得る  
B. 理論確率は必ず0.76に修正すべき  
C. 回路は必ず誤っている  
D. global phaseが76度になった

### Q7
ヒストグラムを描く主な目的として最も適切なのはどれか。

A. outcome frequency を視覚的に比較する  
B. statevectorを必ず復元する  
C. transpilerを不要にする  
D. QASMをコンパイルする

### Q8
期待値が `-0.98` の Pauli-Z 測定について最も自然な解釈はどれか。

A. Z=-1 側に強く偏った状態/結果  
B. 確率が負なので不正  
C. qubitが-0.98個存在する  
D. shotsが-98回

### Q9
結果の metadata を確認する意味として適切なのはどれか。

A. 実装に応じて shots、precision、execution関連情報などの補助情報を得られることがある  
B. metadataだけが量子状態そのもの  
C. metadataは常に空である  
D. metadataを読むと回路が再実行される

### Q10
countsから確率を推定する基本式はどれか。

A. `count(outcome) / total_shots`  
B. `total_shots / count(outcome)`  
C. `count(outcome)^2`  
D. `sqrt(total_shots)`

---

# Answers & Explanations

### A1 — A
250/1000=0.25。counts は頻度なので総shot数で割って経験確率を得る。

### A2 — A
理論確率が0.5でも counts が常に50/50になるわけではない。有限shotによる統計揺らぎを区別する。

### A3 — A
Qiskit の通常の bitstring 表記では bit 0 が右端。この規約は頻出の混乱点。

### A4 — A
結果の意味は measurement-to-classical-bit mapping に依存する。特に複数registerでは表示順を確認する。

### A5 — A
Estimator V2 の結果で `evs` は expectation values の略として用いられる。

### A6 — A
真の確率0.8でも100回なら76回などのずれは自然。観測頻度と母確率を同一視しない。

### A7 — A
histogram は counts/distribution の比較を視覚化するもの。状態の完全tomographyを自動で行うわけではない。

### A8 — A
Pauli observable の期待値は [-1,+1] に入り得る。負値は確率ではなく、固有値付き平均なので正常。

### A9 — A
primitive/result object の metadata は実装に応じた補助情報を保持する。APIとfieldはバージョン依存なので最新版を確認する。

### A10 — A
経験頻度は当該outcomeの回数を総試行回数で割る。
