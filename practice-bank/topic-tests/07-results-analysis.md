# Topic Test 07 — Retrieving and Analyzing Results

全10問。Runtime job retrieval / monitoringとSampler・Estimator resultの読み方を扱います。

## Questions

### Q1
`job = sampler.run(pubs)` で得たjobの最終結果を取得する代表的な呼び出しはどれか。

A. `job.result()`  
B. `job.counts()`  
C. `job.transpile()`  
D. `job.observable()`

### Q2
既知のRuntime job IDから過去のjob objectを取得する代表的なAPIはどれか。

A. `RuntimeJobV2.from_id(job_id)`  
B. `QiskitRuntimeService().job(job_id)`  
C. `SamplerV2.job(job_id)`  
D. `QuantumCircuit.load_job(job_id)`

### Q3
複数の過去Runtime jobsを一覧・条件付きで取得する用途として最も適切なのはどれか。

A. `service.jobs(...)`  
B. `job.result(all=True)`  
C. `qc.jobs()`  
D. `Statevector.jobs()`

### Q4
Sampler V2のPUB resultに `data.meas` があるとき、その典型的な読み方はどれか。

A. `meas`というobservableのexpectation value  
B. `meas`というclassical output registerに対応するresult data  
C. backendのmeasurement calibration table  
D. transpilerのmeasurement pass

### Q5
`pub_result.data.meas.get_counts()` が返すものとして最も適切なのはどれか。

A. measurement outcomeごとのcount辞書  
B. exact statevector amplitudes  
C. observable coefficients  
D. backend instruction durations

### Q6
Runtime jobの現在の状態を確認する代表的なmethodはどれか。

A. `job.progress()`だけ  
B. `job.statevector()`  
C. `job.status()`  
D. `job.measure()`

### Q7
Estimator V2のPUB resultで `data.evs` と `data.stds` の関係として最も適切なのはどれか。

A. `evs`はexpectation values、`stds`は対応するstandard-error/standard-deviation information  
B. `evs`はevent strings、`stds`はstatevectors  
C. 両方ともbitstring counts  
D. 両方ともbackend names

### Q8
countsが `{'0': 760, '1': 240}`、total shotsが1000なら経験的な `P(1)` はどれか。

A. 0.76  
B. 0.50  
C. 0.24  
D. 0.32

### Q9
1000 shotsで理論的に50/50の回路から `{'0': 487, '1': 513}` が得られた。最も適切な解釈はどれか。

A. global phaseが13度ずれた証拠  
B. 理論確率を0.487/0.513へ変更すべき  
C. 有限shotの統計揺らぎとして自然  
D. Estimatorへ自動的に切り替わった証拠

### Q10
Primitive resultのmetadataについて正しい説明はどれか。

A. metadataだけから未知の量子状態を完全復元できる  
B. metadataは常に空である  
C. metadataへアクセスするとjobが再実行される  
D. shots、precision、execution関連などの補助情報を実装に応じて含み得る

---

# Answers & Explanations

### A1 — A
- A: 正解。`run()`が返したjob handleから`result()`で結果を取得する。
- B: countsはSampler result内のclassical dataから取得する。
- C/D: RuntimeJobV2の結果取得methodではない。

### A2 — B
- A: 現行の代表的なservice APIではない。
- B: 正解。`QiskitRuntimeService.job(job_id)`で既存jobを取得する。
- C/D: job retrieval APIではない。

### A3 — A
- A: 正解。`service.jobs(...)`は過去jobsの一覧・filterに使う。
- B/C/D: 複数Runtime jobsを検索するAPIではない。

### A4 — B
- A: Estimator observable resultとの混同。
- B: 正解。Sampler V2 resultはclassical register名に対応するdata fieldを持つ。
- C/D: calibrationやtranspiler passではない。

### A5 — A
- A: 正解。`BitArray`等からcounts辞書を得る代表的なmethod。
- B: sampled outcomesからexact amplitudesは復元できない。
- C/D: resultの意味が異なる。

### A6 — C
- A: current representative methodではない。
- B/D: job lifecycle確認ではない。
- C: 正解。`job.status()`で現在のjob statusを確認する。

### A7 — A
- A: 正解。Estimator resultの`evs`はexpectation values、`stds`は対応する不確かさ情報。
- B/C/D: fieldの意味と一致しない。

### A8 — C
`240/1000=0.24`。
- A: P(0)に相当する。
- B/D: countsから得られない値。
- C: 正解。

### A9 — C
- A: counts差はglobal phaseを直接示さない。
- B: finite sample frequencyと理論母確率を同一視している。
- C: 正解。50/50でも有限sampleでは揺らぐ。
- D: primitiveが自動切替されることはない。

### A10 — D
- A: metadataはquantum stateそのものではない。
- B: implementationによって情報を含む。
- C: 読み取りだけで再実行されない。
- D: 正解。fieldはversion/implementation-sensitiveなのでcurrent APIを確認する。

## Official references

- Runtime service API: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service
- RuntimeJobV2: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/runtime-job-v2
- Primitive input/output: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Estimator input/output: https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output
