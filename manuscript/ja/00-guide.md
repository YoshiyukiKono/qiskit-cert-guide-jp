# 0. 学び方・試験範囲・変化するAPI

[← 入口](README.md) | [次: 量子状態と演算 →](01-quantum-operations.md)

<a id="objectives-boundary"></a>
## 公開Objectivesと教材の補足

公開試験レコードには8領域・21 Objectivesとweightがあります。本書の章・例・判断手順は、それらを理解しやすく並べ直した**教材側の解釈**です。Objective番号も公開順を参照するためのローカルな番号です。公開Objectiveの文言、Mock 01のオリジナル問題、本書の補足説明を混同しないでください。

試験対策では、API名だけでなく次の順で考えます。

1. 何を入力し、何を出力したいか（状態、samples、期待値）。
2. 数学的に何が起きるか（unitary、測定、observable）。
3. SDKでどう表現するか（circuit、PUB、result）。
4. localかIBM Quantum Runtimeか、hardware制約があるか。
5. 問いが厳密な等式か、物理的同値か、経験的推定か。

<a id="version-policy"></a>
## 固定知識とversion-sensitive事項

Born rule、unitary、tensor product、global phase、期待値などは固定知識です。一方、import path、options階層、利用可能なresilience level、hardware feature compatibility、serviceのexecution mode、OpenQASM importerの依存関係はversion-sensitiveです。

本書の基準は **Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0、確認日2026-09-12 JST** です。受験・実装直前には公式API referenceで再確認してください。公式ガイドのコードが別のruntime minor versionを掲げている場合も、概念と特定versionの表面APIを切り分けます。

<a id="three-layers"></a>
## 三つのレイヤーを混ぜない

| レイヤー | 例 | 何を保証しないか |
|---|---|---|
| 言語・仕様 | OpenQASM 3に`while`がある | IBM QPUでそのまま実行可能とは限らない |
| SDK表現 | `QuantumCircuit.if_test`でcontrol flowを作れる | 全backendがそのconstructを受理するとは限らない |
| service / hardware | backend targetが命令をsupportする | 他backendや将来versionのsupportまでは保証しない |

同様に、`StatevectorSampler` / `StatevectorEstimator`はローカル参照実装で、`qiskit_ibm_runtime.SamplerV2` / `EstimatorV2`によるQPU実行とは別物です。

## 章末チェック

1. 「Qiskitで表現可能」を「全QPUで実行可能」と言い換えてよいですか。
2. `resilience_level`の選択肢は固定知識ですか。

答え: 1. いいえ。backend/service supportを別確認します。2. いいえ。version-sensitiveです。

[← 入口](README.md) | [次: 量子状態と演算 →](01-quantum-operations.md)
