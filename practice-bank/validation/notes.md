# Validation Notes

このディレクトリは、practice bankの技術的主張と構造を再確認するための補助資料です。

## Validation layers

### 1. `validate_bank.py`

Qiskitをimportせずに実行できる教材構造チェックです。

- topic testsが各10問であること
- 各問題にA–Dの4 choicesがあること
- 各topicに10個のanswer headingsがあること
- topic testsの正答位置が一つのletterへ極端に集中していないこと
- Mock 01が68問であること
- Mock 01のanswer keyが68問分あること
- Mock 01の正答位置がA/B/C/D各17問であること
- Mock 01の各解説がA–Dすべてに言及していること
- 公開weightを近似したdomain rangesが11/8/12/10/8/8/7/4であること

実行:

```bash
python practice-bank/validation/validate_bank.py
```

### 2. `smoke_checks.py`

Qiskit SDKだけで再現可能な主張をlocalで検証します。

- H/Z/HとH/X/Hのoperator identity
- `Rx(pi)=-iX` の厳密な行列等式
- Bell-state probabilities
- `compose()`のdefault / `inplace=True` semantics
- local `StatevectorSampler`
- local `StatevectorEstimator`
- OpenQASM 3 export

実行環境の一例:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "qiskit[all]~=2.5.2"
python practice-bank/validation/smoke_checks.py
```

OpenQASM 3 import (`load` / `loads`) もlocalで試す場合:

```bash
pip install qiskit-qasm3-import
```

IBM Quantum Compute Serviceのコードを手元で試す場合は、別途current `qiskit-ibm-runtime` とIBM Quantum credentials/service accessが必要です。このvalidation directoryはcredentialsを要求しません。

## Runtime/API claimsの検証方針

以下はlocal smoke testだけでは正しさを保証できないため、2026-09-10時点の公式IBM Quantum Documentationと照合しています。

- `qiskit_ibm_runtime.SamplerV2` / `EstimatorV2`
- Job / Session / Batch execution modes
- backend ISAへtranspileしたcircuit/observableをRuntimeへ渡すworkflow
- PUB structureとbroadcasting
- Sampler `default_shots` / `run(..., shots=...)`
- Sampler dynamical decoupling options
- Estimator precision / `resilience_level`
- `QiskitRuntimeService.job()` / `jobs()`
- `RuntimeJobV2.status()` / `result()`
- OpenQASM 3 feature supportとREST execution modes

これらはversion-sensitiveなので、試験直前にも公式資料を再確認してください。

## 以前のfalse-positiveと修正

旧`smoke_checks.py`では`HXH=Z`をcomputational-basis statesへ作用させ、`Statevector.equiv()`で比較していました。しかし`equiv()`はglobal phaseを無視するため、basis stateだけではIdentityとの違いを見逃せます。

現在は`Operator`の行列を`np.allclose`で**厳密に比較**し、global phaseまで区別します。

## Official references

- Qiskit / IBM Quantum docs: https://quantum.cloud.ibm.com/docs/
- Execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes
- Primitive I/O: https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
- Sampler options: https://quantum.cloud.ibm.com/docs/en/guides/sampler-options
- Estimator options: https://quantum.cloud.ibm.com/docs/en/guides/estimator-options
- Runtime service API: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service
- OpenQASM 3 interoperability: https://quantum.cloud.ibm.com/docs/en/guides/interoperate-qiskit-qasm3
- OpenQASM feature table: https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table
- REST execution modes: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes-rest-api
