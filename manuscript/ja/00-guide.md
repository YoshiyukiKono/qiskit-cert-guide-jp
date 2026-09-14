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

本書のSDKの説明とコードは **Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0** を基準とします。ただし、説明する内容によって、適用範囲を決めるものが異なります。

- **数学・量子計算の原理**: Born rule、unitary、tensor product、global phase、期待値などは、パッケージのバージョンに依存しない知識です。
- **言語仕様**: OpenQASMの構文や意味は、言語の仕様版を基準にします。本書ではOpenQASM 3.0仕様を参照します。
- **SDKのAPI**: import path、optionsの階層、引数に指定できる値、importerの依存関係などは、パッケージのバージョンを基準にします。
- **サービス・実機の機能**: Runtimeの既定値、resilience levelに割り当てられる具体的な手法、機能の併用条件などは、サービスの仕様やbackendにも依存します。同じパッケージ版を使うことだけでは、実機の動作条件まで固定できません。

公式資料も読み分けます。**バージョン別のAPIリファレンス**は、その版のAPIを説明します。一方、公式ガイドの**Package versions**は、掲載コードの作成に使った依存条件です。ガイド全体やRuntimeサービスの仕様が、そのパッケージ版に固定されていることを意味しません。

別のパッケージ版を使うときは、その版のAPIリファレンスで差分を確認します。実機へ送るときは、サービスの機能の組合せ条件と、実行先backendの対応状況も確認します。参照ガイドのコード基準と本書の検証環境が異なる場合や、参照先が更新される資料である場合は、その違いを[参照・検証記録](../validation/version-scope-revision-2026-09-14.md)に示します。

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
