# 本文の適用範囲と参照資料の版

資料の再確認・改稿日: 2026-09-14 JST

## 改稿の範囲

[編集方針](../editorial-policy.md)に従い、読者向けの本文では、SDKはパッケージ版、言語仕様は仕様版、Runtimeサービスと実機はそれぞれの対応条件によって説明の適用範囲を示す。資料を確認した日付は、この記録に残す。

| 対象 | 改稿内容 | 改稿前に本文へ記載していた確認日 |
|---|---|---|
| [入口](../ja/README.md) | SDKの基準版、OpenQASMの仕様版、サービス・実機への依存を明示 | 2026-09-12 JST |
| [第0章のバージョン方針](../ja/00-guide.md#version-policy) | 数学、言語仕様、SDK、サービス・実機を区別。APIリファレンスとガイドの読み分けを説明 | 2026-09-12 JST |
| [第5章の機能の併用条件](../ja/05-sampler.md#sampler-compatibility) | DDの設定方法はRuntime 0.49.0のAPI、併用可否はサービス条件として説明。fractional gatesの0.42.0以降という条件と区別 | 2026-09-12 |
| [第6章のresilience](../ja/06-estimator.md#estimator-options) | Runtime 0.49.0で指定できるlevelと、サービスが割り当てる具体的な手法を区別 | 2026-09-14 |

第8章と入口のOpenQASM参照リンクは、既存と同じ3.0仕様の`index.html`を明示するURLへそろえた。仕様版の変更は行っていない。数式、掲載コード、出力例、既存の節見出しと明示アンカーを維持する。

## 本書の基準と実行確認した環境

| 項目 | 基準・検証環境 |
|---|---|
| Qiskit SDK | 2.5.2 |
| qiskit-ibm-runtime | 0.49.0 |
| OpenQASM | 言語仕様3.0。Pythonパッケージの版とは別に扱う |
| ローカル確認に用いたPython | 3.12.14 |
| ローカル確認に用いたNumPy | 2.5.3 |

改稿済みの第1章と第6章の掲載コード13例の実行検証は、[基底変換への再構成の記録](conjugation-revision-2026-09-14.md)にある。これは原稿全章の全コードや実QPUでの動作を保証するものではない。

その後、第1章全体の改稿に伴い、検証対象を第1章13例・第6章9例の合計22例へ広げた。追加した数式・コードの照合と参照資料は、[第1章全体の改稿記録](chapter1-revision-2026-09-14.md)を参照する。以下は、適用範囲の表現を見直した時点の記録として維持する。

第2章の拡充では、さらに13例と8枚の図を追加した。第1章・第2章・第6章の合計35例についての確認と、可視化の依存関係は[第2章の改稿記録](chapter2-revision-2026-09-14.md)を参照する。

今回は適用範囲の表現を改め、ローカルのRuntime 0.49.0で次を確認した。

- `EstimatorOptions(resilience_level=...)`は0・1・2を受理し、−1・3は検証エラーになる。
- `SamplerOptions`にDDの`enable=True`と`sequence_type="XY4"`を設定できる。
- 未指定の`EstimatorOptions().default_precision`は`Unset`となる。具体的なサービス既定値とは別の値である。

これらはクライアントの設定の確認であり、DDとdynamic circuitsの併用や、各levelのクラウドでの処理を実行したものではない。掲載コード・数式を変更しないため、13例の再実行は今回の変更確認には含めない。

## 参照資料と、版による限定の範囲

下記の公式資料を2026-09-14 JSTに参照した。ガイドの依存条件は原文の指定を保ち、本書で使う正確なパッケージ版と分けて示す。

| 資料 | 資料の版・掲載コードの依存条件 | 本文で参照する内容 |
|---|---|---|
| [Specify Sampler options](https://quantum.cloud.ibm.com/docs/en/guides/sampler-options) | 更新されるガイド。掲載コードは`qiskit[all]~=2.5.2`、`qiskit-ibm-runtime~=0.47.0` | DDとdynamic circuitsの併用条件、fractional gatesについて明記された0.42.0以降の条件 |
| [Specify Estimator options](https://quantum.cloud.ibm.com/docs/en/guides/estimator-options) | 更新されるガイド。掲載コードは`qiskit[all]~=2.5.2`、`qiskit-ibm-runtime~=0.47.0` | `Unset`とサーバー既定値、ガイドのPackage versionsの読み方 |
| [Configure noise management with Estimator](https://quantum.cloud.ibm.com/docs/en/guides/estimator-noise-management) | 更新されるガイド。掲載コードは`qiskit-ibm-runtime~=0.47.0` | 各resilience levelの役割、手法の割当ては保証されない旨、個別optionsの優先 |
| [EstimatorOptions](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/options-estimator-options) | URLに版を含まない「latest version」のAPIリファレンス | levelの選択肢、未指定値。本文の0.49.0という限定は、上記のローカル確認でも照合 |
| [OpenQASM 3.0 Specification](https://openqasm.com/versions/3.0/index.html) | 3.0を指定した言語仕様 | Pythonパッケージの版と独立した仕様の基準 |

ガイドの`~=0.47.0`は掲載コードの依存条件で、本書の検証版0.49.0と同一ではない。公式ガイドは掲載コードを作成した条件と、より新しい版の使用を勧める説明を併記している。一方で、ガイド全体を0.47.0の固定資料として扱ったり、参照だけで0.49.0での実行を検証したと扱ったりはしない。

Estimator optionsの設定一覧は、掲載コードのPackage versionsとは別に、最新版のoptionsを説明すると明記されている。版を含まないAPIリファレンスも固定版の資料ではない。資料上の説明と、対象パッケージ版で実行確認できた内容を分けて記録する。

サービス依存の記述は、上記ガイドの説明と照合した。SDKの版を固定しても、その説明時点のサーバー構成や実機機能が再現されるとは限らない。今後ガイドが更新された場合は、参照日と内容を再確認してこの記録を更新する。

## 文書の検証

掲載コード・出力・数式と見出し・アンカーは、作業開始時の原稿との比較で確認した。ローカルリンクは既存の[検証スクリプト](verify_sample_sections.py)の`check_links()`で確認した。本文に見える日付による限定が残っていないかも、日本語正本全体を検索した。リンク先の記録ファイル名に含まれる日付と、本文の記述は区別している。

| 確認 | 結果 |
|---|---|
| 本文の日付による限定 | 日本語正本の表示本文から解消 |
| SDKの適用範囲 | 上記のRuntime 0.49.0での設定確認が通過 |
| コード・出力・数式・見出し・アンカー | 比較対象の6ファイルで変更なし |
| ローカルリンク | 18個のMarkdownファイル内の226件が通過 |
| 差分の空白検査 | `git diff --check`が通過 |

原稿の比較とSDK設定の確認は作業時に実施した。過去の改稿で残した確認日は、履歴として各検証記録に維持している。
