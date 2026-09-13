SU(2) は、量子計算で非常によく出てくる **2×2 の特殊ユニタリ行列の集まり**です。

少し分解すると、

$$
SU(2)=\{U\in \mathbb{C}^{2\times2}\mid U^\dagger U=I,\ \det U=1\}
$$

です。

ここで

* $U^\dagger U=I$
  → ユニタリ行列。量子状態の長さを保つ変換
* $\det U=1$
  → “special” の条件

という意味です。

量子ビットの状態

$$
|\psi\rangle=
\begin{pmatrix}
\alpha\\
\beta
\end{pmatrix}
$$

に対して、SU(2) の行列をかけると、

$$
|\psi'\rangle=U|\psi\rangle
$$

となり、これは1量子ビット状態の回転に対応します。

特に重要なのが、Pauli 行列です。

$$
X=
\begin{pmatrix}
0&1\\
1&0
\end{pmatrix},
\qquad
Y=
\begin{pmatrix}
0&-i\\
i&0
\end{pmatrix},
\qquad
Z=
\begin{pmatrix}
1&0\\
0&-1
\end{pmatrix}.
$$

「Pauli は SU(2) の生成子」というのは、ざっくり言うと、

> $X,Y,Z$ を材料にして、SU(2) の任意の連続回転を作れる

という意味です。

具体的には、任意の方向

$$
\vec n=(n_x,n_y,n_z)
$$

のまわりに角度 $\theta$ だけ回転する演算は、

$$
R_{\vec n}(\theta)
=
e^{-i\theta(n_xX+n_yY+n_zZ)/2}
$$

と書けます。

例えば、

$$
R_x(\theta)=e^{-i\theta X/2}
$$

$$
R_y(\theta)=e^{-i\theta Y/2}
$$

$$
R_z(\theta)=e^{-i\theta Z/2}
$$

です。

なので、最近見ていた

$$
R_z(\theta)
$$

と $Z$ ゲートの関係は、まさに SU(2) の話の一部です。

ただし、ここで1点だけ厳密に言うと、

> Pauli 行列そのものが SU(2) の元

という言い方は少し注意が必要です。

例えば

$$
\det X=\det Y=\det Z=-1
$$

なので、$X,Y,Z$ 自体は $\det=1$ ではなく、そのままでは SU(2) の元ではありません。

一方、

$$
-iX,\quad -iY,\quad -iZ
$$

は SU(2) の回転と直接つながります。

数学的には、SU(2) に対応する Lie algebra $\mathfrak{su}(2)$ の生成子として

$$
\frac{X}{2},\quad
\frac{Y}{2},\quad
\frac{Z}{2}
$$

あるいは

$$
-\frac{iX}{2},\quad
-\frac{iY}{2},\quad
-\frac{iZ}{2}
$$

を使います。

なので、学習段階では、

> **SU(2) = 1量子ビットの連続回転全体**
> **Pauli $X,Y,Z$ = その回転を作る基本方向**

と捉えるとかなり分かりやすいです。

Bloch球との対応までつなげると、SU(2) がなぜ「回転群」と呼ばれるのかが一気に見えます。

# Bloch球との対応

はい。ここをつなぐと、**SU(2)・Pauli 行列・Bloch球がほぼ一つの話**として見えてきます。

1量子ビットの純粋状態は、全体位相を除けば

$$
|\psi\rangle
=
\cos\frac{\theta}{2}|0\rangle
+
e^{i\phi}\sin\frac{\theta}{2}|1\rangle
$$

と書けます。

この $\theta,\phi$ を普通の球面座標だと思うと、

$$
\vec r
=
\begin{pmatrix}
\sin\theta\cos\phi\\
\sin\theta\sin\phi\\
\cos\theta
\end{pmatrix}
$$

という3次元ベクトルが得られます。これが **Blochベクトル**で、先端が Bloch球面上の一点になります。

たとえば、

$$
|0\rangle
\leftrightarrow
\begin{pmatrix}
0\\0\\1
\end{pmatrix}
$$

$$
|1\rangle
\leftrightarrow
\begin{pmatrix}
0\\0\\-1
\end{pmatrix}
$$

$$
|+\rangle
\leftrightarrow
\begin{pmatrix}
1\\0\\0
\end{pmatrix}
$$

$$
|+i\rangle
\leftrightarrow
\begin{pmatrix}
0\\1\\0
\end{pmatrix}
$$

です。

ここで Pauli 行列が登場します。密度行列は

$$
\rho
=
\frac12
\left(
I+xX+yY+zZ
\right)
$$

と書けます。

つまり Bloch球の座標

$$
(x,y,z)
$$

は、実は

$$
X,\ Y,\ Z
$$

という Pauli 行列の係数そのものです。

これはかなり重要です。

---

そして SU(2) のユニタリ変換

$$
U
=
e^{-i\theta\,\vec n\cdot\vec\sigma/2}
$$

を量子状態に作用させるとします。

ここで

$$
\vec\sigma=(X,Y,Z)
$$

です。

すると、状態ベクトルには SU(2) の行列が作用しますが、**Blochベクトル側では普通の3次元空間の回転**になります。

つまり

$$
|\psi\rangle
\overset{U}{\longrightarrow}
|\psi'\rangle
$$

に対応して、

$$
\vec r
\overset{R}{\longrightarrow}
\vec r'
$$

となります。

この $R$ は普通の3次元回転行列で、

$$
R\in SO(3)
$$

です。

要するに、

$$
\boxed{
SU(2)\text{ の作用}
\quad\longleftrightarrow\quad
Bloch球上の3次元回転
}
$$

です。

具体例を見るともっと分かりやすいです。

### $R_z(\theta)$

$$
R_z(\theta)
=
e^{-i\theta Z/2}
$$

を状態に作用させます。

Bloch球では、

> **z軸を中心に角度 $\theta$ 回転**

します。

たとえば

$$
|+\rangle
$$

は Bloch球上では $+x$ 方向です。

ここに

$$
R_z\left(\frac{\pi}{2}\right)
$$

をかけると、

$$
+x \to +y
$$

となるので、

$$
|+\rangle\to |+i\rangle
$$

になります。厳密には全体位相を除いて、です。

同じように、

$$
R_x(\theta)=e^{-i\theta X/2}
$$

は x 軸まわり、

$$
R_y(\theta)=e^{-i\theta Y/2}
$$

は y 軸まわりの回転です。

だから Pauli 行列 $X,Y,Z$ は、

> Bloch球における **x, y, z 各軸まわりの回転の生成子**

と考えられます。

---

ここで少し面白い点があります。

普通の3次元回転は $SO(3)$ ですが、量子ビットには $SU(2)$ が作用します。そして

$$
SU(2)\to SO(3)
$$

という対応は **1対1ではなく2対1** です。

具体的には、

$$
U
$$

と

$$
-U
$$

は、Bloch球上では**同じ回転**を表します。

なぜなら、状態に作用させると

$$
U|\psi\rangle
$$

と

$$
-U|\psi\rangle
$$

は全体位相 $-1=e^{i\pi}$ しか違わず、同じ物理状態だからです。

これは、直前に話していた

> **全体位相は物理状態を変えない**

という話とそのままつながっています。

さらに有名なのが $2\pi$ 回転です。

Bloch球を一周、つまり

$$
\theta=2\pi
$$

回転すると、

$$
R_{\vec n}(2\pi)
=
e^{-i\pi\,\vec n\cdot\vec\sigma}
=
-I
$$

となります。

状態ベクトルは

$$
|\psi\rangle\to -|\psi\rangle
$$

となる。

でもこれは全体位相だけの違いなので、Bloch球上では元の点に戻っています。

そしてさらにもう一周、

$$
\theta=4\pi
$$

なら、

$$
R_{\vec n}(4\pi)=I
$$

となります。

つまり、

* Bloch球上では $2\pi$ 回転で元に戻る
* 状態ベクトルそのものは $4\pi$ で完全に元に戻る

という、量子力学特有の構造があります。

これが

$$
SU(2)
$$

が

$$
SO(3)
$$

の **double cover（二重被覆）** だと言われる意味です。

今までの流れに合わせるなら、次の図式で覚えるとかなり整理できます。

$$
\boxed{
X,Y,Z
\;\to\;
\mathfrak{su}(2)\text{ の生成子}
\;\to\;
SU(2)\text{ の回転}
\;\to\;
Bloch球上では }SO(3)\text{ の回転}
}
$$

そしてさらに、

$$
\boxed{
\text{全体位相を無視する}
}
$$

ことで、SU(2) の $U$ と $-U$ が同じ Bloch球回転に見えます。

この対応が分かると、以前見ていた

$$
Z
\quad\text{と}\quad
R_z(\pi)
$$

が「全体位相だけ違って物理的には同じ」という話も、かなり自然に見えるようになります。
