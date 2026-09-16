# 基本アルゴリズムの補章・検証記録

検証日: 2026-09-15 JST

## 追加の目的と範囲

[補章A](../ja/09-algorithm-worked-examples.md)を追加し、第1〜8章の知識を、問題の定義から回路の設計、途中計算、出力の解釈までの手順につないだ。対象は次の3題である。

- 位相キックバックとDeutsch: 1ビット関数の可逆なオラクル、作業ビットの固有状態、位相と最後のH、4種類の関数の分類。
- 2量子ビットGrover: 4候補・正解1個、位相オラクル、平均振幅に関する反転、Dと-D、印の位置と反復回数の変更。
- 1量子ビットVQE: Z+X/2のモデル、変分原理、Ryのansatz、Estimatorによる角度の一括評価と古典側による最適化、解析解、測定と期待値、ansatzの制限。

Python例は7件、掲載図は3枚、理由付きの条件変更問題は11問。第1〜8章のH2見出しと明示アンカーは維持した。各題材に必要な前提は本文内の参照と短い振り返りを置いた。特定の模擬試験を受けたことを前提にする導入・問題リンクは補章に加えていない。

[ルートREADME](../../README.md)は、旧稿の重複した目次や現行正本との混在を整理し、正本・補章・演習・旧稿の位置付けと、検証環境の準備を案内する形に改めた。案内した仮想環境`.venv-manuscript/`をGitの対象から除外する設定も加えた。旧稿の本文、既存演習、chatsの内容は今回の作業では変更していない。

[正本の目次](../ja/README.md)、[第0章](../ja/00-guide.md)、第1・5・6章の関連節、第8章の次への案内、[coverage](../ja/coverage.md#algorithm-supplement-coverage)から補章へ接続した。既存章のPython例は変更していない。[編集方針](../editorial-policy.md)と[改稿計画](../revision-plan.md)へ、選定理由、追加済みの範囲、読者確認と発展候補を記録した。

## 試験との関係を確認した範囲

補章の方針を検討した際に、[IBMの公式公開試験レコード](https://www.ibm.com/training/credentials/getExam/C1000-179)を再取得し、8領域・21項目とweightが[保存済みのObjectives](../../practice-bank/validation/official-objectives-2026-09-11.json)と一致することを確認した。個別アルゴリズム名を明示したObjectiveはないが、同レコードの推奨リソースにはFundamentals of quantum algorithmsが含まれている。

この確認を根拠に、本編の構成を保ち、アルゴリズムを既習事項の総合例として追加した。教材側の題材選定を新しい公式試験領域や出題頻度とは扱わない。別添Study Guide PDF本文や非公開試験問題を確認したという意味でもない。

QFT・位相推定は次の追加候補、Shor全体やQAOAの詳説は発展学習とし、今回の本文拡充や実行検証の対象に含めていない。

## 環境と再実行

Qiskit 2.5.2 / NumPy 2.5.3 / SciPy 1.18.1 / Matplotlib 3.11.2 / pylatexenc 2.11 / Pillow 12.3.0を、既存のPython 3.12.14検証環境で使用した。依存は導入済みで、追加インストールは行っていない。基準は[requirements.txt](requirements.txt)に従う。補章のコードはqiskit-ibm-runtimeを呼び出さない。

リポジトリのルートから実行する。

```text
python -X utf8 -B manuscript/validation/verify_algorithm_examples.py
node manuscript/validation/verify_manuscript_render.cjs
git diff --check
```

[検証スクリプト](verify_algorithm_examples.py)は、本文の7つのPythonブロックをそれぞれ独立した名前空間で実行し、掲載出力と比較する。ネットワーク接続を遮断し、一時ディレクトリに図を生成する。掲載PNGを更新する場合は次の指定を使う。

```text
python -X utf8 -B manuscript/validation/verify_algorithm_examples.py --write-figures
```

図の書出しはコード・数値の検証を通過してから行う。共有のリンク検証へ追加ファイルを指定できる引数を加え、補章の検証ではルートREADMEも対象にした。既存の引数なしの呼出しは従来どおり使える。

## 確認結果

| 対象 | 確認内容 |
|---|---|
| 掲載コード | 7例の標準出力が掲載結果と一致。前の例の変数を使わず実行できる |
| Deutschのオラクル | 全4関数の真理値表から4×4置換行列を独立に組み立て、SDKの行列と照合。可逆性、XOR先、ビット順を確認 |
| 位相キックバック | オラクル直後の振幅と、最終状態の全体位相を保持した式を照合。複素振幅の制御側と任意角度の位相を使う一般形、作業ビットを+へ変える場合、最後のHを取り除く場合も確認 |
| Groverの反射 | 独立に作ったD行列との一致、ユニタリ性、複素振幅への平均反転則、全体位相を省いた-Dを確認 |
| Groverの変更条件 | 全4候補のオラクル行列と、一回反復の測定結果を確認。0〜6回の各反復を行列累乗と回転の確率式で照合。二回反復後の符号も確認 |
| VQEのモデル | ハミルトニアンの行列、複数の非自明な角度でのRy状態とエネルギー、入力(9, 1)・出力(9,)の対応を確認 |
| 最適化 | Estimatorを複数回問い合わせ、9点の最小値を改善することを確認。各候補の評価を解析式と照合し、最適角度と最小固有値を比較 |
| 基底状態 | 最適状態がハミルトニアンの固有方程式を満たすこと、Z・Xそれぞれの理論確率を確認 |
| 有限shots | 二つの測定回路を512shotsずつ実行。各countsの総数、±1への変換、重み付きエネルギーを照合。推定値と真の期待値を区別 |
| ansatzの制約 | Rzだけで準備すると任意の角度でエネルギーが1となること、ハミルトニアンをZだけにした確認問題の答えを照合 |
| 参照と体裁 | 補章のアンカー、画像、全角括弧と強調を確認。本文・検証記録・既存解答・ルートREADMEの30ファイル、475ローカルリンクが通過 |
| 数式と表 | 補章193式・3表が通過。第1〜8章、補章、入口・対応表の合計1,866式をMarkdown・KaTeXで確認 |

関連する第1・6章と共有の検証関数については、`verify_sample_sections.py`も再実行し、既存例の出力、数学的な照合、従来の引数なしのリンク検証が通ることを確認した。

今回の有限shotsの例では推定エネルギーが約-1.138672となり、真の最小固有値約-1.118034を下回った。この値をより低いエネルギーの状態として扱わず、有限標本の揺らぎと変分原理の適用対象を説明した。

## 図と表示の確認

以下の図は掲載コードから生成し、PNGを開いて確認した。

- [Deutschの回路](../ja/figures/09/09-deutsch.png): 作業ビットのX・H、入力のH、Uf、最後のH、入力ビットから古典ビットへの測定線が読み取れる。
- [Groverの理論確率](../ja/figures/09/09-grover-probabilities.png): 初期・オラクル直後の均等分布と、拡散後の11の確率1を同じ縦軸で比較できる。
- [VQEのエネルギー](../ja/figures/09/09-vqe-energy.png): 角度、解析曲線、初期の評価点、最適化中の評価点、厳密な基底エネルギーを識別できる。

ラベルの欠けや読解を妨げる重なりはない。既存のVS Code用画像CSSを利用し、画像幅のユーザー設定は変更していない。PNGの目視確認とMarkdown・KaTeXの構文検証を行った範囲であり、VS CodeプレビューやPDF全ページの組版を確認したという意味ではない。

## 一次資料と適用範囲

- [Deutschのアルゴリズム](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/quantum-query-algorithms/deutsch-algorithm): 問題の定義、可逆な関数評価、位相キックバックと最終測定。本文のコードは独自に基本ゲートから組み立てた。
- [Groverのアルゴリズム](https://quantum.cloud.ibm.com/learning/en/modules/computer-science/grovers): オラクルと振幅増幅、2量子ビット例、問い合わせ回数の位置付け。公式モジュールの依存条件はQiskit 2.1.0以上などで、本補章の固定環境とは区別する。
- [変分法の目的関数](https://quantum.cloud.ibm.com/learning/en/courses/variational-algorithm-design/cost-functions): ハミルトニアンの期待値、基底エネルギーを求める目的。1量子ビットのモデルの解析解は本文で導出した。
- [StatevectorEstimator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorEstimator): PUB、結果、ユニタリな回路に対する状態ベクトルによる評価。URLはlatestであり、掲載APIと挙動はQiskit 2.5.2でも照合した。
- [SciPy minimize_scalar](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html) / [bounded法](https://docs.scipy.org/doc/scipy/reference/optimize.minimize_scalar-bounded.html): 有限区間の一変数最小化、停止条件、局所最小化としての位置付け。参照ページはSciPy 1.18.0表記、ローカル実行は1.18.1。

外部資料の依存条件を、試験で要求されるパッケージ版とは読み替えない。全体位相を含む行列・状態の照合、有限標本の出力、最適化の許容誤差はそれぞれ役割を分けた。

実機の取得、認証、QPU送信、Runtime Sessionの実行、実機ノイズ下の最適化は行っていない。数値チェックの通過を、一般の量子優位性、任意のオラクルの効率、任意のVQEの収束、教材の学習効果の保証としては扱わない。読者による説明の確認は改稿計画の未完了項目として残す。
