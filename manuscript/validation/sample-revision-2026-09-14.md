# 見本2節の改稿・検証記録

確認日: 2026-09-14 JST

この記録の検証数・対象範囲は、最初の見本2節の改稿時点のもの。再実行スクリプトには、後続の期待値節、第6章全体、基底変換への再構成の検証も追加されている。現在の依存環境と検証範囲は[基底変換の改稿記録](conjugation-revision-2026-09-14.md)を参照する。

## 対象と変更内容

[編集方針](../editorial-policy.md)に基づき、次の2節を見本として改稿した。

| 節 | 加えた説明 | 読者が確認すること |
|---|---|---|
| [ゲートの合成と基底変換](../ja/01-quantum-operations.md#matrix-order)（当時の節名：行列と演算順序） | ketと列ベクトル、行列積の順序、二つの基底状態の追跡、線形性、行列の直接計算、実行例、理由付き小問 | 途中計算から等式を導き、順序やゲートを変えた場合も考えられるか |
| [broadcastingをshapeで読む](../ja/06-estimator.md#estimator-broadcasting) | 目的の組合せ表、軸とbinding shape、右端からの比較、実行例、各出力の意味、期待値の導出、対応方式の比較、理由付き小問 | shapeと各要素の意味を対応させ、全組合せと同じ位置どうしの対応を区別できるか |

見本への読者フィードバックを受け、2節の導入・節末から特定のMock名・問題番号への言及と、問題・解答への計6リンクを削除した。本文が独立した教材として読める導入に整え、編集方針にも反映した。数式・コード・確認問題は維持し、この修正ではリンクと差分の空白を再確認した。

## 実行環境

一時仮想環境でQiskitを固定し、ローカルで確認した。Pythonの標準コマンドが利用できなかったため、Codexに同梱されたPythonから仮想環境を作成した。

| 項目 | バージョン |
|---|---|
| Python | 3.12.14 |
| Qiskit | 2.5.2 |
| NumPy | 2.5.3 |
| SciPy | 1.18.1 |
| rustworkx | 0.18.1 |
| dill | 0.4.1 |
| stevedore | 5.9.1 |
| typing-extensions | 4.16.0 |

この2節の例は`qiskit-ibm-runtime`、認証、実QPUを必要としない。Runtime/QPU実行の検証は今回の対象に含めていない。

## 再実行方法

現在のスクリプトはQiskit 2.5.2、qiskit-ibm-runtime 0.49.0、NumPyを必要とする。リポジトリのルートから次を実行する。

```bash
python manuscript/validation/verify_sample_sections.py
python practice-bank/validation/validate_bank.py
git diff --check
```

[検証スクリプト](verify_sample_sections.py)は、原稿の対象節からPythonコードと掲載出力を直接読み取る。最初の例は節ごとに独立した名前空間で実行し、続きの例は同じ節の名前空間を引き継ぐ。別ファイルに複製したコードだけが通る状態を避けるための構成である。信頼するリポジトリ内のコードを実行するスクリプトとして扱う。

## 検証結果

| 確認 | 結果 |
|---|---|
| 掲載コードと出力 | 3コードブロックを原稿から抽出し、掲載出力との一致を確認 |
| HZHの導出 | 二つの基底状態の全中間状態、複素振幅を含む入力、行列の一致を確認 |
| 行列の厳密な関係 | Hの分母を外した整数行列を使い、HZH=XとHXH=Zを整数演算で確認 |
| broadcastingの値と添字 | 2行3列の全6要素を、個別に値を割り当てた状態の期待値、およびcos・sinの式と照合 |
| 類題と誤りの例 | 同じ位置どうしの2要素、全組合せの4要素、行の交換、互換でないshapeの拒否、確認問題のshapeを確認 |
| ローカルリンク | 正本・編集方針・本記録・Mock解答の計14 Markdownファイルにある185リンクのファイルとアンカーを確認 |
| 既存構造の維持 | Gitの改稿前本文と照合し、対象2節の外側の本文、既存の明示アンカー、レベル2見出しが一致することを確認 |
| 数式の組版 | 変更した2章全体をMarkdownからHTMLへ変換し、129個の数式をKaTeXで処理。構文エラーなし |
| 問題集の構造 | 既存の`validate_bank.py`が成功。Topic 80問とMock 68問の構造を確認 |
| 差分の空白 | `git diff --check`でエラーなし |

数式の組版確認には、既存の`references/html-pdf/`用のmarkdown-it、markdown-it-texmath、KaTeXを使用し、KaTeXの`throwOnError`を有効にした。これは変換時の構文確認であり、GitHubや各閲覧アプリでの表示をすべて目視確認したという意味ではない。

再実行スクリプトは、掲載コード・数値・ローカルリンクの確認を担当する。改稿前後の範囲比較とKaTeX変換は今回の作業時に別途実行した。Mock解答ファイルはリンク・構造の読み取り対象とし、この改稿では編集していない。

## 一次資料との照合

新しい例のAPI仕様は、次の公式資料で確認した。説明と小問はこの教材のために作成した。

- [Operator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator): 回路・ゲートの行列表現と`data`。
- [Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector): 入力状態の作成と回路による状態の変化。
- [StatevectorEstimator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorEstimator): PUB入力、job/result、ローカル期待値計算。
- [Primitive inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output#broadcasting-rules): parameter軸とbroadcasting、PUBごとの結果。
- [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html): 右端からのshape比較と互換性。
- [RYGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RYGate): 回転行列と符号・半角の規約。

既存の外部参照URLすべての到達性や、他の節の技術内容を再検証した記録ではない。

## 見本レビューの観点

見本を読む際には、記号の導入、途中計算、説明の重複、出力の読みやすさを確認する。今回の自動検証は数値・構造の確認であり、初学者による読解テストの代わりにはならない。全章への展開は未実施。
