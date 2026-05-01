# Error Mitigation & Suppression

量子コンピュータはノイズを含みます。

そのため実機実行では：

結果 ≠ 理論値

になります。

これを補正する技術が：

error mitigation
error suppression

です。

---

# Error mitigationとは

実行後に補正する方法：

measurement correction
zero-noise extrapolation
probabilistic error cancellation

などがあります。

特徴：

ノイズを除去するのではなく

統計的に補正する

---

# Error suppressionとは

実行前にノイズを減らす方法：

dynamical decoupling
pulse optimization
layout optimization

---

# Dynamical Decoupling

idle時間に追加ゲートを挿入して

位相エラーを減らす

例：

X I X I

のような補正列を挿入

---

# Measurement mitigation

測定誤差補正：

例：

|0⟩ → 1 と誤判定

確率行列を推定して補正

---

# 試験で問われるポイント

重要：

mitigation = post-processing
suppression = circuit-level improvement

---

# まとめ

| 方法 | タイミング |
|------|-----------|
| mitigation | 実行後 |
| suppression | 実行前 |
