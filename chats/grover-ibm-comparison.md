はい、**同じGroverのアルゴリズムです。原稿は、スライドの一般的な説明を「2量子ビット・4候補・正解1個」に具体化したもの**です。操作の順序も、全体位相を含めた演算子の定義も一致しています。

ただし、扱う範囲と説明方法には違いがあります。また、照合中にスライド側の注意点が2か所見つかりました。

以下のページ番号は、こちらのPDFの表紙を1ページとして数えています。:codex-file-citation{path="C:/work-codex/quantum/ibm-quantum-course-runtime-check/courses/fundamentals-of-quantum-algorithms/slides/08-Grover-algorithm.pdf" purpose="source"}

比較した原稿は、[09-algorithm-worked-examples.md のGrover節](C:/work-codex/quantum/qiskit-cert-guide-jp/manuscript/ja/09-algorithm-worked-examples.md:266)です。

まず、**記号が違う部分を対応させると、同じ式になります。**

| 意味 | スライド | 原稿 |
|---|---|---|
| 一様な重ね合わせ | $\lvert u\rangle=H^{\otimes n}\lvert0^n\rangle$ | $\lvert s\rangle=H^{\otimes2}\lvert00\rangle$ |
| 正解の符号を反転する操作 | $Z_f$ | $O_f$ |
| 一様状態を軸とする反射 | $H^{\otimes n}Z_{\mathrm{OR}}H^{\otimes n}$ | $D=2\lvert s\rangle\langle s\rvert-I$ |
| 1回のGrover反復 | $G=H^{\otimes n}Z_{\mathrm{OR}}H^{\otimes n}Z_f$ | $G=DO_f$ |

スライド11ページでは、

$$
Z_{\mathrm{OR}}=2|0^n\rangle\langle0^n|-I
$$

なので、

$$
H^{\otimes n}Z_{\mathrm{OR}}H^{\otimes n}
=2|u\rangle\langle u|-I
$$

と導いています。これは原稿の拡散演算子 $D$ そのものです。**$Z_{\mathrm{OR}}$ 単独ではなく、前後のHを含めた部分が $D$ に対応する**点が、読み比べる際の要点です。

具体的な違いは、次のとおりです。

| 比較点 | スライド | 原稿 |
|---|---|---|
| 問題の規模 | 一般の $n$ 量子ビット、$N=2^n$ 候補 | 2量子ビット、4候補 |
| 正解の数 | 正解1個、複数個、個数不明の場合を扱う | 正解1個に限定 |
| 説明方法 | 正解・不正解の重ね合わせが張る平面内での「反射と回転」 | 4個の振幅を使う「平均振幅に関する反転」 |
| オラクルの実装 | 抽象的な $Z_f$ と、$U_f$・補助ビットによる実現方法 | 正解`11`に対してCZを直接使う |
| 反復回数 | 一般式から回数と成功確率を導出 | 0〜3回を具体的に計算 |
| 実行・測定 | 候補を測定し、$f(x)=1$ か確認する手順 | Qiskitで状態ベクトルとshotsを確認 |

**「回転」と「平均振幅に関する反転」は、同じ操作を異なる見方で説明しています。**

スライド8〜19ページでは、不正解の一様な重ね合わせを $|A_0\rangle$、正解の一様な重ね合わせを $|A_1\rangle$ としています。原稿の例なら、

$$
|A_0\rangle
=\frac{|00\rangle+|01\rangle+|10\rangle}{\sqrt3},
\qquad
|A_1\rangle=|11\rangle
$$

です。

原稿は4個の振幅それぞれについて $a_x\mapsto2\bar a-a_x$ を計算します。スライドは、その状態変化を上の2方向にまとめて追跡します。異なる増幅方法を使っているわけではありません。

**原稿で1回の反復により成功確率が100％になることも、スライドの一般式と一致します。**

正解数を $M$ と書くと、スライド21〜22ページの式は、

$$
\theta=\arcsin\sqrt{\frac{M}{N}},
\qquad
P_t=\sin^2((2t+1)\theta),
\qquad
t=\left\lfloor\frac{\pi}{4\theta}\right\rfloor
$$

です。原稿の $N=4,\ M=1$ を代入すると、

$$
\theta=\frac{\pi}{6},\qquad t=1,\qquad
P_1=\sin^2\frac{\pi}{2}=1
$$

になります。さらに $t=0,1,2,3$ の成功確率は、

$$
\frac14,\quad1,\quad\frac14,\quad\frac14
$$

となり、[原稿の実行結果](C:/work-codex/quantum/qiskit-cert-guide-jp/manuscript/ja/09-algorithm-worked-examples.md:457)と一致します。スライド25ページの表にも、$N=4$ の成功確率は1と記載されています。

**ゲート実装では、原稿のほうが符号の扱いを具体的に説明しています。**

[原稿の全体位相の説明](C:/work-codex/quantum/qiskit-cert-guide-jp/manuscript/ja/09-algorithm-worked-examples.md:333)にある

```text
H → X → CZ → X → H
```

という回路だけでは、実装されるのは $-D$ です。原稿は `global_phase = np.pi` によって全体に $-1$ を掛け、スライドと同じ $D$ にそろえています。

したがって、**原稿のコードは「測定確率だけ同じ」という以上に、演算子の符号までスライドと一致**しています。補助ビットを使わない点も、位相オラクルをCZで直接実装できる、この小さな例の特徴です。

原稿で省略されている主な内容は、スライドの一般的な反復回数の導出、複数正解の場合の $O(\sqrt{N/M})$、正解数が不明な場合の探索手順です。一方、原稿にはQiskitのビット順、全体位相、回路内の反復とshotsの区別が詳しく書かれています。

最後に、**アルゴリズムの違いとは別に、スライド側には次の2点があります。**

- **13ページの途中式に誤植があります。**  
  $G|A_1\rangle$ の展開で、最後から2行目の括弧の外にある $\sqrt{|A_0|/N}$ は、正しくは $\sqrt{|A_1|/N}$ です。そのページの最終式と、次ページの行列は正しいです。

- **29ページの「少なくとも40％」という保証は、記載された条件だけでは成立しません。**  
  例えば $N=4$、正解3個なら、記載された範囲から選べる反復回数は $t=1$ だけです。しかし、
  $$
  \theta=\frac{\pi}{3},\qquad P_1=\sin^2(\pi)=0
  $$
  になります。この記述には条件の補足か手順の修正が必要です。原稿の「正解1個」の例には影響しません。

- 原稿にスライドとの対応を追記する
- 4候補の例を回転の図で理解する
- スライドの注意点を詳しく検証する