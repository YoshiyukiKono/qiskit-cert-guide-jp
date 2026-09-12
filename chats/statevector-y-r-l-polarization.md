はい、`r` と `l` はその理解で合っています。**right / left** です。

由来は、量子情報だけのローカルな命名というより、**偏光（polarization）**の言葉遣いです。

Y基底の2状態

$$
|+i\rangle
=
\frac{1}{\sqrt2}
\left(
|0\rangle+i|1\rangle
\right)
$$

$$
|-i\rangle
=
\frac{1}{\sqrt2}
\left(
|0\rangle-i|1\rangle
\right)
$$

は、光の偏光でいう

* right-circular polarization
* left-circular polarization

に対応するので、Qiskit では `r` / `l` というラベルを使っています。

だから、

```python
Statevector.from_label("r")
```

は

$$
|r\rangle
=
\frac{|0\rangle+i|1\rangle}{\sqrt2}
$$

で、

```python
Statevector.from_label("l")
```

は

$$
|l\rangle
=
\frac{|0\rangle-i|1\rangle}{\sqrt2}
$$

です。

X基底の `+` / `-` が

$$
|+\rangle,\ |-\rangle
$$

という量子情報寄りの記法なのに対して、Y基底だけ `r/l` なのは少し非対称に見えますが、背景には**Bloch球上のY軸と円偏光の対応**があります。

ちなみに Bloch球では、

* $|0\rangle, |1\rangle$ → $\pm Z$
* $|+\rangle, |-\rangle$ → $\pm X$
* $|r\rangle, |l\rangle$ → $\pm Y$

という対応です。

なので、学習用の `BasisStatevector` では、表示は

$$
|+i\rangle,\ |-i\rangle
$$

にして、入力はQiskit互換で `r/l` も受け付ける、というのがかなり自然です。
