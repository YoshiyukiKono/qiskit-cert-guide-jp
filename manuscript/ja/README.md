# Qiskit v2.x 開発者認定 日本語正本

このディレクトリは、IBM Certified Quantum Computation using Qiskit v2.X Developer – Associate（C1000-179）の公開Objectivesを学ぶための、本リポジトリにおける正本です。Python経験者が量子計算を初めて学ぶ前提で、数式、Qiskitコード、実行結果の読み方を一つの流れにしました。

> **対象バージョンと適用範囲**: SDKの説明とコードは **Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0**、OpenQASMの説明は **OpenQASM 3.0仕様**を基準とします。Runtimeの既定値や機能の組合せ、実機での対応状況は、サービスの仕様と実行先backendにも依存します。詳しくは[バージョンによる適用範囲](00-guide.md#version-policy)を参照してください。

参照資料の版・掲載コードの依存条件と、実行確認した例の範囲は[参照・検証記録](../validation/version-scope-revision-2026-09-14.md)にまとめています。全例を実QPUで実行したという意味ではありません。試験Objectivesは公開範囲の説明であり、この教材の補足をIBM公式要件として主張しません。実試験問題の再現でも合格保証でもありません。

<a id="reading-order"></a>
## 推奨読書順

1. [学び方・境界](00-guide.md)
2. [量子状態と演算](01-quantum-operations.md)
3. [測定と可視化](02-visualization-measurement.md)
4. [回路の構築](03-circuit-construction.md)
5. [transpile・ISA・実行方式](04-transpile-execution.md)
6. [Sampler V2](05-sampler.md)
7. [Estimator V2](06-estimator.md)
8. [jobと結果分析](07-results-analysis.md)
9. [OpenQASM 3](08-openqasm3.md)
10. [Objectives・Mock 01 coverage](coverage.md)

各章末のチェックを解き、次にMock 01を解いてください。誤答時は解答解説にある「正本で深掘り」リンクから該当節へ戻ります。

<a id="notation"></a>
## 記法

- 数学表現とプログラム上の表現を、次のように使い分けます。
  - **数式ブロック**（`$$ ... $$`）：状態の定義、行列、重要な等式、計算方法を示す式。本文から独立させ、区切りの前後に空行を置きます。
  - **インライン数式**（`$ ... $`、実際には区切りの内側に空白を入れない）：文章中の短い記号、状態、等式。
  - **コード表記**（バッククォート）：API名、変数名、コード、文字列、bitstring、配列shapeなど、プログラム上の表現。
- 状態ベクトルはket $|\psi\rangle$、複素共役転置は $\dagger$、期待値は $\langle\psi|A|\psi\rangle$ と書きます。行列は行・列を持つ形で、指数・添字・分数は数式として組版します。
- 例えばPauli labelの文字列 `"XZ"` と、対応する演算子 $X\otimes Z$ を区別します。コード例の中は実行可能な構文を保ちます。
- `q0` はQiskitのindex 0のqubit、`c0` はindex 0のclassical bitです。
- bitstring、整数、回路図、Pauli labelでは見せ方が違います。文字列の左右だけで判断せず、対象の規約を確認します。
- 「厳密に等しい」と「global phaseを除き物理的に同じ」を区別します。

## 一次情報

- [公開試験レコード](https://www.ibm.com/training/credentials/getExam/C1000-179)
- [Qiskit bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)
- [Primitive input/output](https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output)
- [Execution modes](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes)
- [Sampler options](https://quantum.cloud.ibm.com/docs/en/guides/sampler-options)
- [Estimator options](https://quantum.cloud.ibm.com/docs/en/guides/estimator-options)
- [OpenQASM 3.0 specification](https://openqasm.com/versions/3.0/index.html)

[次: 学び方・境界 →](00-guide.md)
