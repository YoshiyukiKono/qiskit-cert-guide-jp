"""Verify Chapter 7 examples, job states, statistics, plots and saved records.

Uses manuscript/validation/requirements.txt; no credentials or QPU required.
    python -X utf8 -B manuscript/validation/verify_chapter7.py
    python -X utf8 -B manuscript/validation/verify_chapter7.py --write-figures

Runtime methods are exercised with local response fixtures, not a service.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from contextlib import chdir, redirect_stdout
from importlib.metadata import version
from io import StringIO
from itertools import product
import inspect
import json
from math import comb
import os
from pathlib import Path
import re
import shutil
import tempfile
from unittest.mock import Mock, patch

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "qiskit-manuscript-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.stats import binomtest
from qiskit import qpy
from qiskit.primitives import StatevectorSampler
from qiskit.primitives.containers import BitArray
from qiskit.quantum_info import Statevector, Pauli
from qiskit_ibm_runtime import RuntimeJobV2, QiskitRuntimeService
from qiskit_ibm_runtime.decoders.result_decoder import ResultDecoder
from qiskit_ibm_runtime.json import RuntimeEncoder
from qiskit_ibm_runtime.exceptions import (
    RuntimeInvalidStateError, RuntimeJobFailureError, RuntimeJobMaxTimeoutError,
)
from verify_sample_sections import ROOT, anchors, check_links, close, require

SOURCE = ROOT / "manuscript/ja/07-results-analysis.md"
ASSETS = SOURCE.parent / "figures/07"
NAMES = (
    "local_job", "inspect_past_job", "list_finished_jobs", "wait_for_result",
    "hierarchy", "grid_counts", "diagonal", "normal_interval", "repeated_estimates",
    "exact_interval", "comparison", "estimator", "archive",
)
FUNCTIONS = {"inspect_past_job", "list_finished_jobs", "wait_for_result"}
ORIGINAL_ANCHORS = {"job-lifecycle", "result-hierarchy", "bitarray-counts", "empirical-analysis", "metadata"}
ORIGINAL_HEADINGS = ["jobを取得・監視する", "result階層", "BitArrayからcountsを得る",
                     "経験確率と不確かさ", "metadataを読む", "章末チェック"]


def run_examples(directory: Path) -> dict[str, dict]:
    source = SOURCE.read_text(encoding="utf-8")
    require(ORIGINAL_ANCHORS <= anchors(source), "Original anchor removed")
    require(re.findall(r"^## (.+)$", source, re.M) == ORIGINAL_HEADINGS, "H2 headings changed")
    prose = re.sub(r"```.*?```", "", source, flags=re.S)
    require(not any("（" in s or "）" in s for s in re.findall(r"\*\*([^*\n]+)\*\*", prose)),
            "Parenthesis inside bold")
    require(not re.search(r"mock|practice-bank|PLACEHOLDER", source, re.I), "Unwanted reference or placeholder")
    examples = list(re.finditer(r"```python\n(.*?)\n```", source, re.S))
    require(len(examples) == len(NAMES), "Unclassified Python block")
    namespaces = {}
    with chdir(directory):
        for name, example in zip(NAMES, examples, strict=True):
            namespace = {"__name__": "__main__"}
            tree = ast.parse(example[1])
            if name in FUNCTIONS:
                require(len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef), "Definition only")
                function = tree.body[0]
                require(function.name == name and not function.decorator_list, "Unexpected function")
                require(all(isinstance(d, ast.Constant) for d in function.args.defaults), "Executable default")
                require(source[:example.start()].rstrip().endswith("<!-- validation: runtime-function -->"),
                        "Missing function marker")
            stdout = StringIO()
            with redirect_stdout(stdout):
                exec(compile(tree, str(SOURCE), "exec"), namespace)
            if name in FUNCTIONS:
                require(not stdout.getvalue(), "Definition produced output")
            else:
                expected = re.match(r"\s*出力:\s*```text\n(.*?)\n```", source[example.end():], re.S)
                require(expected is not None, f"Missing printed output: {name}")
                require(stdout.getvalue().strip() == expected[1].strip(), f"Output differs: {name}\n{stdout.getvalue()}")
                print(f"PASS Chapter 7 printed output: {name}")
            namespaces[name] = namespace
            plt.close("all")
    images = {Path(link).name for link in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)}
    require(images == {p.name for p in directory.glob("*.png")}, "Figure outputs and links differ")
    for name in images:
        with Image.open(directory / name) as img:
            require(img.format == "PNG" and min(img.size) >= 180, "Invalid PNG")
            require(any(lo < hi for lo, hi in img.convert("RGB").getextrema()), "Blank PNG")
        with Image.open(directory / name) as img:
            img.verify()
    print("PASS 2 figures, 5 preserved explicit anchors and 6 preserved H2 headings")
    return namespaces


def runtime_fixture(status: str, result) -> RuntimeJobV2:
    # Keep actual 0.49.0 status/result/wait/error methods. Replace only remote
    # responses and initialize fields normally populated from the service.
    job = object.__new__(RuntimeJobV2)
    job._job_id = f"local-fixture-{status}"
    job._status = status
    job._session_id = None
    job._reason = None
    job._reason_code = None
    job._error_message = "Example execution failure" if status == "ERROR" else None
    job._set_status_and_error_message = Mock()
    job._api_client = Mock()
    job._api_client.job_results.return_value = json.dumps(result, cls=RuntimeEncoder)
    job._result_decoders = [ResultDecoder]
    return job


def check_jobs(ns: dict[str, dict]) -> None:
    local = ns["local_job"]
    require(local["job"].status().name == "DONE", "Local JobStatus")
    require(local["again"] is local["result"], "Local result should be reused, not resampled")
    inspect_past = ns["inspect_past_job"]["inspect_past_job"]
    result = local["result"]
    for status in ["INITIALIZING", "QUEUED", "RUNNING", "DONE", "ERROR", "CANCELLED"]:
        job = runtime_fixture(status, result)
        service = Mock(spec=QiskitRuntimeService)
        service.job.return_value = job
        output = StringIO()
        with redirect_stdout(output):
            returned = inspect_past(service, job.job_id())
        require(returned is job and isinstance(job.status(), str), "Runtime returns string status")
        service.job.assert_called_once_with(job.job_id())
        require(f"status: {status}" in output.getvalue(), "Status not shown")
        if status == "DONE":
            require("PUB results: 1" in output.getvalue(), "Completed result not read")
            job._api_client.job_results.assert_called_once_with(job_id=job.job_id())
        else:
            job._api_client.job_results.assert_not_called()
        if status == "ERROR":
            require("Example execution failure" in output.getvalue(), "Failure reason missing")
    service = Mock(spec=QiskitRuntimeService)
    jobs = [runtime_fixture(s, result) for s in ["DONE", "ERROR", "CANCELLED"]]
    service.jobs.return_value = jobs
    found = ns["list_finished_jobs"]["list_finished_jobs"](service, "example_backend")
    kwargs = dict(backend_name="example_backend", pending=False, limit=5, descending=True)
    inspect.signature(QiskitRuntimeService.jobs).bind(service, **kwargs)
    service.jobs.assert_called_once_with(**kwargs)
    require(found == [(j.job_id(), j.status()) for j in jobs], "List includes terminal failures/cancellations")
    service.jobs.return_value = []
    require(ns["list_finished_jobs"]["list_finished_jobs"](service, "example_backend", limit=2) == [], "Empty search")
    require(service.jobs.call_args.kwargs["limit"] == 2, "Limit forwarded")

    wait = ns["wait_for_result"]["wait_for_result"]
    done = runtime_fixture("DONE", result)
    returned = wait(done, timeout=0)
    require(returned[0].data.meas.get_counts() == result[0].data.meas.get_counts(), "Decoded Runtime result")
    pending = runtime_fixture("QUEUED", result)
    with patch.object(RuntimeJobV2, "cancel", autospec=True) as cancel, redirect_stdout(StringIO()) as output:
        require(wait(pending, timeout=0) is None, "Client wait timeout should return None")
        cancel.assert_not_called()
    require(pending._status == "QUEUED" and pending.job_id() in output.getvalue(), "Timeout retained job")
    pending._api_client.job_results.assert_not_called()
    # Same ID can later complete: no new run or job is created.
    pending._status = "DONE"
    require(wait(pending, timeout=0)[0].data.meas.num_shots == 16, "Read result after client timeout")
    for status, reason_code, expected in [
        ("ERROR", None, RuntimeJobFailureError),
        ("ERROR", 1305, RuntimeJobMaxTimeoutError),
        ("CANCELLED", None, RuntimeInvalidStateError),
    ]:
        job = runtime_fixture(status, result)
        job._reason_code = reason_code
        try:
            wait(job, timeout=0)
        except expected:
            pass
        else:
            raise AssertionError(f"Must propagate {expected.__name__}")
    job = runtime_fixture("QUEUED", result)
    job._set_status_and_error_message.side_effect = ConnectionError("Local communication failure")
    try:
        wait(job, timeout=0)
    except ConnectionError:
        pass
    else:
        raise AssertionError("Must not swallow communication failure")
    print("PASS actual Runtime methods with local responses: six states, search arguments, timeout/retrieval and failures")


def check_results(ns: dict[str, dict]) -> None:
    result = ns["hierarchy"]["result"]
    require(len(result) == 2, "PUB count")
    require(result[0].data.readout.shape == (3,) and result[1].data.meas.shape == (), "PUB condition shapes")
    require(sum(result[0].data.readout.get_counts().values()) == 192, "Three conditions each 64 shots")
    grid = ns["grid_counts"]
    bits = grid["bits"]
    combined = Counter()
    for loc in np.ndindex(bits.shape):
        a, b = grid["values"][loc]
        state = Statevector(grid["qc"].remove_final_measurements(inplace=False).assign_parameters([a, b]))
        close(state.data, np.kron([np.cos(b/2), np.sin(b/2)], [np.cos(a/2), np.sin(a/2)]))
        close(state.probabilities()[3], np.sin(a/2)**2 * np.sin(b/2)**2)
        records = bits.get_bitstrings(loc)
        require(len(records) == 100 and Counter(records) == bits.get_counts(loc), "Counts location")
        combined.update(records)
    require(dict(combined) == bits.get_counts(), "Pooled versus selected counts")
    # An asymmetric 2 x 3 grid checks the axes in the changed-condition question.
    values = np.array([[[a, b] for b in [0, np.pi/2, np.pi]] for a in [0, np.pi]])
    changed = StatevectorSampler(seed=7).run([(grid["qc"], values)], shots=200).result()[0].data.meas
    require(changed.shape == (2, 3) and sum(changed.get_counts().values()) == 1200, "Changed grid dimensions")
    require(changed.get_counts((1, 2)) == {"11": 200}, "Question's row and column selection")
    close((20+720)/(100+900), 0.74)
    close((20+180)/(100+300), 0.5)
    diagonal = ns["diagonal"]
    for label in ["ZI", "IZ", "ZZ"]:
        eigenvalues = np.diag(Pauli(label).to_matrix()).real
        expected = sum(eigenvalues[int(key, 2)] * n for key, n in diagonal["counts"].items()) / 100
        close(diagonal["bits"].expectation_values(label), expected)
    try:
        diagonal["bits"].expectation_values("XX")
    except ValueError:
        pass
    else:
        raise AssertionError("Nondiagonal observable accepted")
    # ZI/IZ must differ when classical bit destinations are reversed.
    reversed_bits = BitArray.from_counts({key[::-1]: n for key, n in diagonal["counts"].items()}, num_bits=2)
    close(reversed_bits.expectation_values(["ZI", "IZ", "ZZ"]), [0.2, 0, 0.4])
    estimator = ns["estimator"]
    state = Statevector(estimator["qc"])
    close(state.probabilities(), [0.75, 0.25])
    close(estimator["pub"].data.evs, [0.5, np.sqrt(3)/2])
    close(estimator["pub"].data.stds, [0, 0])
    print("PASS PUB/condition axes, pooled counts, changed grid, diagonal expectations and Estimator interpretation")


def check_statistics(ns: dict[str, dict]) -> None:
    # Explicitly enumerate Bernoulli sequences: independent of the variance formula.
    for n in [1, 4, 7]:
        records = np.array(list(product([0, 1], repeat=n)))
        hits = records.sum(axis=1)
        for p in [0.01, 0.24, 0.5, 0.98]:
            weights = p**hits * (1-p)**(n-hits)
            estimates = hits/n
            close(weights.sum(), 1)
            close(weights @ estimates, p)
            variance = weights @ (estimates-p)**2
            close(variance, p*(1-p)/n)
            means = 1-2*estimates
            close(weights @ (means-(1-2*p))**2, (1-(1-2*p)**2)/n)
    normal = ns["normal_interval"]
    close(normal["se"], np.sqrt(0.1824/1000))
    require(normal["low"] < 0.25 < normal["high"], "Reference probability not in interval")
    close(np.sqrt(.24*.76/900), np.sqrt(.24*.76/100)/3)
    interval = ns["exact_interval"]["interval"]
    close(interval.low, 0)
    close(interval.high, 1-0.025**(1/100))
    opposite = binomtest(100, 100).proportion_ci(confidence_level=.95, method="exact")
    close([opposite.low, opposite.high], [1-interval.high, 1])
    # Finite grid check of the exact interval's coverage under a binomial model.
    n = 20
    intervals = [binomtest(k, n).proportion_ci(confidence_level=.95, method="exact") for k in range(n+1)]
    for p in [.001, .01, .24, .5, .9, .999]:
        covered = sum(comb(n, k)*p**k*(1-p)**(n-k) for k, ci in enumerate(intervals) if ci.low <= p <= ci.high)
        require(covered >= .95-1e-12, "Exact interval coverage under chosen model")
    comparison = ns["comparison"]
    close(comparison["difference"], .06)
    close(comparison["se_difference"]**2, (.24*.76+.3*.7)/1000)
    require(comparison["low"] > 0, "Example difference interval includes zero")
    # Independent differences versus reusing the same observations.
    pa, pb = .2, .7
    outcomes = np.array(list(product([0, 1], repeat=2)))
    weights = np.array([(pa if a else 1-pa)*(pb if b else 1-pb) for a, b in outcomes])
    differences = outcomes[:, 1]-outcomes[:, 0]
    close(weights @ (differences-(pb-pa))**2, pa*(1-pa)+pb*(1-pb))
    close(outcomes[:, 0]-outcomes[:, 0], np.zeros(4))
    # The plotted data and interval endpoints must match the computations.
    repeated = ns["repeated_estimates"]
    for ax, n in zip(repeated["axes"], [100, 400, 1600], strict=True):
        xy = np.asarray(ax.collections[0].get_offsets())
        close(xy[:, 0], np.arange(1, 41))
        close(xy[:, 1]*n, np.rint(xy[:, 1]*n))
        require(np.all((xy[:, 1] >= ax.get_ylim()[0]) & (xy[:, 1] <= ax.get_ylim()[1])), "Clipped experiment point")
        close(ax.lines[0].get_ydata(), [.24, .24])
    individual_bars = comparison["axes"][0].collections[0].get_segments()
    for index, segment in enumerate(individual_bars):
        close(segment[:, 1], comparison["p_hat"][index] + np.array([-1, 1])*1.96*comparison["se"][index])
    difference_bar = comparison["axes"][1].collections[0].get_segments()[0]
    close(difference_bar[:, 1], [comparison["low"], comparison["high"]])
    print("PASS Bernoulli variance derivation, SE scaling, exact interval endpoints/coverage, comparisons and plot data")


def check_archive(ns: dict[str, dict], directory: Path) -> None:
    example = ns["archive"]
    record = json.loads((directory / "07-analysis-record.json").read_text(encoding="utf-8"))
    require(Counter(record["bitstrings"]) == record["counts"], "Archived raw records/counts mismatch")
    require(len(record["bitstrings"]) == record["num_shots"] == record["requested_shots"] == 32, "Archived shot count")
    require(record["condition_shape"] == [] and record["num_bits"] == 1, "Archived condition/bit axes")
    require(record["packages"] == {name: version(name) for name in ["qiskit", "numpy"]}, "Package manifest")
    require(record["pub_metadata"]["circuit_metadata"]["basis"] == "Z", "Circuit metadata lost")
    with open(directory / record["circuit_file"], "rb") as stream:
        restored = qpy.load(stream)
    require(len(restored) == 1 and restored[0] == example["qc"], "QPY circuit round trip")
    require(restored[0].metadata == example["qc"].metadata, "QPY metadata round trip")
    # Labels alone must not change the circuit's state preparation.
    changed = restored[0].copy()
    changed.metadata = {"basis": "X"}
    close(Statevector(changed.remove_final_measurements(inplace=False)).data,
          Statevector(restored[0].remove_final_measurements(inplace=False)).data)
    print("PASS JSON raw records/metadata and QPY round trip; labels do not alter gates")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-figures", action="store_true")
    args = parser.parse_args()
    require(version("qiskit") == "2.5.2" and version("qiskit-ibm-runtime") == "0.49.0", "Use baseline versions")
    print("Versions:", ", ".join(f"{p}={version(p)}" for p in ["qiskit", "qiskit-ibm-runtime", "numpy", "scipy", "matplotlib"]))
    with tempfile.TemporaryDirectory(prefix="qiskit-chapter7-") as temporary:
        directory = Path(temporary)
        with patch("socket.socket.connect", side_effect=AssertionError("Network forbidden in Chapter 7 checks")):
            ns = run_examples(directory)
            check_jobs(ns)
            check_results(ns)
            check_statistics(ns)
            check_archive(ns, directory)
        if args.write_figures:
            ASSETS.mkdir(parents=True, exist_ok=True)
            for figure in directory.glob("*.png"):
                shutil.copy2(figure, ASSETS / figure.name)
            print("WROTE Chapter 7 figures")
    check_links()
    print("PASS Chapter 7: 10 printed examples and 3 Runtime functions; no service connection or QPU submissions")


if __name__ == "__main__":
    main()
