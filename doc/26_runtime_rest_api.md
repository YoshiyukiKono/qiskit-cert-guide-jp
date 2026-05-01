了解しました。以下に **第26章 `26_runtime_rest_api.md`** を、そのままコピーして保存できる Markdown として出力します。余計な装飾や構造は入れていません。

---

# Qiskit Runtime REST API

Qiskit Runtime は Python SDK だけでなく **REST API** 経由でも操作できます。

つまり：

Notebook がなくても
Python 環境がなくても
HTTP 経由で量子ジョブを送信できます 🌐

これはクラウド量子計算の基本構造の理解として重要です。

---

# REST API とは何か

REST API とは：

HTTP リクエストを使ってリソースを操作する仕組み

です。

Qiskit Runtime では以下が可能です：

・job の送信
・job 状態確認
・result 取得
・job キャンセル

---

# Runtime の内部構造

通常の Python コード：

```python
from qiskit_ibm_runtime import Sampler

sampler = Sampler()
job = sampler.run([qc])
result = job.result()
```

この処理は内部で REST API を呼び出しています。

つまり：

Python SDK = REST API wrapper

です。

---

# 主な REST 操作

Runtime API は以下の HTTP メソッドで構成されます。

## POST

job を送信する

例：

POST /jobs

目的：

量子回路を backend に送る

---

## GET

job 状態を取得する

例：

GET /jobs/{job_id}

取得できる情報：

・RUNNING
・QUEUED
・DONE
・ERROR

---

## GET（result）

job の実行結果を取得する

例：

GET /jobs/{job_id}/results

Sampler の場合：

probability distribution

Estimator の場合：

expectation value

が返ります。

---

## DELETE

job をキャンセルする

例：

DELETE /jobs/{job_id}

長時間ジョブ停止に使用します。

---

# Runtime job lifecycle

Runtime job は次の状態を持ちます：

CREATED
QUEUED
RUNNING
DONE
ERROR
CANCELLED

試験では頻出ポイントです 📌

---

# Runtime REST API を使う理由

SDK を使わず直接 REST API を使うケース：

・Web アプリ統合
・サーバレス環境
・CI/CD pipeline
・外部クラウド連携

つまり：

量子計算を「サービス」として扱うための仕組み

です。

---

# 認証の仕組み

REST API を使うには IBM Quantum API key が必要です。

通常：

Authorization header

として送信します。

例：

```
Authorization: Bearer YOUR_API_KEY
```

---

# Sampler / Estimator と REST API

Sampler：

測定サンプリング結果取得

Estimator：

Observable expectation value 計算

どちらも REST API 経由で backend に送信されます。

---

# Runtime Session と REST API

Runtime Session を使うと：

複数 job を同じ session 内で実行可能になります。

メリット：

・queue 待ち時間削減
・通信回数削減
・クラウド実行高速化 🚀

---

# SDK と REST API の関係

整理すると：

QuantumCircuit → SDK → REST API → Backend

つまり SDK は REST API を抽象化したものです。

試験では：

SDK が内部で REST を使っている

という理解が重要です。

---

# 試験で問われるポイント

重要事項：

REST API は HTTP ベース

job 管理が可能：

POST = job submit
GET = job status
GET = job result
DELETE = job cancel

Python SDK は REST API wrapper

Runtime はクラウドサービスとして提供される

---

# まとめ

Qiskit Runtime REST API により：

Notebook なしでも量子ジョブ送信可能

Sampler / Estimator 実行可能

job lifecycle 管理可能

クラウド量子計算をアプリケーションに統合可能になります ✨
