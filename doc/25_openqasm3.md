了解しました。
以下に **完全フラットな Markdown 本文のみ** を出力します。
コードブロックは使いません。装飾も入れません。
このまま全文コピーして `25_openqasm3.md` に保存できます。

---

# OpenQASM 3

OpenQASM は量子回路を記述するための低レベル言語です。

Qiskit は内部的に OpenQASM を利用して回路を表現しています。

特に OpenQASM 3 は従来の OpenQASM 2 を拡張し、

・classical control
・loops
・variables
・dynamic circuits

を扱えるようになりました。

これは現在の Qiskit Runtime と密接に関係しています。

---

# OpenQASM とは何か

OpenQASM は Quantum Assembly Language の略です。

つまり、

量子回路をハードウェアに近い形で記述する言語

です。

役割としては次のような位置関係になります。

Python（Qiskit）
↓
OpenQASM
↓
量子ハードウェア

つまり Python と量子ハードウェアの中間層です。

---

# OpenQASM 2 と OpenQASM 3 の違い

OpenQASM 2 は静的回路のみ記述可能でした。

例えば：

・ループ不可
・条件分岐制限あり
・classical variable 不可

OpenQASM 3 は動的回路を記述できます。

---

# OpenQASM 3 の基本構造

最小例：

OPENQASM 3;

qubit q;

h q;

measure q;

これは：

1量子ビット作成
Hadamard適用
測定

を意味します。

---

# classical control

OpenQASM 3 では条件分岐が可能です。

例：

if (c == 1) {
x q;
}

これは

測定結果が 1 の場合だけ X を適用

という意味になります。

---

# ループ構造

OpenQASM 3 は for 文をサポートします。

例：

for i in [0:3] {
h q[i];
}

複数量子ビットに同じ操作を適用できます。

---

# dynamic circuits

OpenQASM 3 の最大の特徴は

測定結果に応じて回路を変更できる

ことです。

例：

measure
↓
条件分岐
↓
次のゲート決定

これは dynamic circuit と呼ばれます。

---

# なぜ dynamic circuits が重要か

従来は

量子回路は実行前に固定されていました

しかし

測定結果に応じて回路を変えられる

ようになりました。

これにより次が可能になります。

・error correction
・adaptive algorithms
・feedback control

---

# Qiskit と OpenQASM 3

Qiskit では QuantumCircuit を OpenQASM に変換できます。

例：

qc.qasm()

また OpenQASM 文字列から回路を生成することも可能です。

---

# OpenQASM 3 と Runtime の関係

Qiskit Runtime は dynamic circuits をサポートしています。

つまり OpenQASM 3 と密接に連携しています。

---

# 試験で問われるポイント

重要事項：

OpenQASM は量子回路記述言語

OpenQASM 3 は

classical control をサポート
dynamic circuits をサポート
ループ構造をサポート

---

# まとめ

OpenQASM 3 の特徴：

・条件分岐が可能
・ループが可能
・classical variable が使える
・dynamic circuit を記述できる

これによりハードウェアに近い柔軟な回路制御が可能になります。

---

必要なら続けて **第26章 Runtime REST API** も同じ形式で出します。
