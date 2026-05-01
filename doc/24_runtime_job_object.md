# The Qiskit Runtime Job Object

Runtime primitive 実行結果は

job object

として返されます。

---

# Job objectとは

非同期実行結果の管理オブジェクト

例：

job = sampler.run(...)

---

# 主なメソッド

status()

job.status()

現在の状態取得

---

result()

job.result()

結果取得

---

job_id()

job.job_id()

クラウド上のID取得

---

cancel()

job.cancel()

ジョブ停止

---

# job lifecycle

CREATED
RUNNING
DONE
ERROR
CANCELLED

---

# 非同期実行モデル

Runtimeは：

submit
wait
retrieve

の流れで動きます。

---

# 試験ポイント

重要：

job.result() は

同期ブロック呼び出し

です
