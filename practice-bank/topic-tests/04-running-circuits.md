# Topic Test 04 — Running Quantum Circuits

全10問。各問1つ選択してください。

## Questions

### Q1
transpilation の主目的として最も適切なのはどれか。

A. 回路をターゲットの命令セットや接続制約に適合させる  
B. 測定確率を必ず50%にする  
C. 古典ビットを削除する  
D. 量子アルゴリズムを自動発見する

### Q2
`basis_gates` が表すものとして最も近いのはどれか。

A. ターゲットが直接扱う基本ゲート集合  
B. 測定結果の基底状態一覧  
C. Bloch球の軸  
D. Pythonの組み込み関数

### Q3
物理デバイスの coupling map を考慮する理由はどれか。

A. すべての量子ビット対で2量子ビットゲートが直接実行できるとは限らないから  
B. shot数を決めるため  
C. Statevectorの正規化のため  
D. OpenQASMの文法チェックのため

### Q4
最適化レベルを上げた transpilation について一般に正しいものはどれか。

A. より多くの最適化処理を試みる可能性がある  
B. 必ず量子ビット数を半分にする  
C. 必ず実行結果を変える  
D. 測定命令を禁止する

### Q5
理想的なローカル statevector simulation と実機実行の違いとして正しいものはどれか。

A. 実機ではデバイスノイズや有限shotの影響を考える必要がある  
B. 実機は複素振幅を直接返すことしかできない  
C. statevector simulation は量子回路を扱えない  
D. 両者は常に完全に同一結果になる

### Q6
`generate_preset_pass_manager(...)` の役割として最も適切なのはどれか。

A. ターゲットに応じた標準的な transpilation pipeline を生成する  
B. Sampler のshotを生成する  
C. IBMアカウントを作る  
D. 測定結果をヒストグラム化する

### Q7
transpiled circuit に SWAP 相当の操作が増える典型的理由はどれか。

A. 論理量子ビット間の必要な相互作用を物理接続に合わせてルーティングするため  
B. global phaseをゼロにするため  
C. shotsを増やすため  
D. classical registerを可視化するため

### Q8
「論理回路が同じ意味を保つ」ことと「ゲート列が同じ」であることの関係として正しいものはどれか。

A. transpilation後はゲート列が変わっても、意図した論理作用を保つことが目的  
B. ゲート列が1文字でも変われば必ず別アルゴリズム  
C. transpilationは回路を測定結果に置換する処理  
D. 論理作用は考慮されない

### Q9
有限 shots で確率を推定する場合、shots を増やす主な効果はどれか。

A. 統計的ばらつきを減らす方向に働く  
B. qubit数が増える  
C. gate depthが必ず減る  
D. global phaseが観測可能になる

### Q10
実行先に応じた transpilation を行う際、最も重要な情報の一つはどれか。

A. backend/target の命令・接続制約  
B. Markdownのテーマ  
C. Gitのbranch名  
D. Pythonファイル名

---

# Answers & Explanations

### A1 — A
transpiler は抽象的な回路をターゲットが実行できる形へ変換する。basis、接続、最適化などが主な論点。

### A2 — A
basis gates はターゲットで基本命令として利用できるゲート集合。任意の高水準ゲートは必要に応じてこの集合へ分解される。

### A3 — A
実デバイスでは2量子ビット相互作用の接続性が制限される。必要な論理接続を満たすため routing が必要になる。

### A4 — A
最適化レベルはコンパイル努力と結果の品質のトレードオフに関係する。高レベルでも「必ず」特定の改善が起こるわけではない。

### A5 — A
理想 simulator はデバイスノイズを無視できる一方、実機ではノイズ、readout error、shot noise などを考える必要がある。

### A6 — A
preset pass manager は一般的な transpilation stage を組み合わせた pass manager を作る。ターゲットや optimization level と合わせて使う。

### A7 — A
非隣接な論理量子ビット間の相互作用を物理トポロジーで実現するため、routing によってSWAP等が挿入されることがある。

### A8 — A
コンパイルは表現を変えても計算の意味を保つことを目指す。物理的な近似やノイズまで含めれば実測分布は変動し得るが、論理変換としての目的は等価性維持。

### A9 — A
独立サンプル数が増えるほど頻度による確率推定の標準誤差は一般に小さくなる。

### A10 — A
target/backend properties は、どの命令がどこで実行できるかを決めるため transpilation の中心情報。
