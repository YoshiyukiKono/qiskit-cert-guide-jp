"""Verify the trusted local manuscript about Grover search with unknown M.

Run the four tagged examples directly from the manuscript, compare their
output, and independently check the probabilities, stopping rules, and figures.
Install manuscript/validation/requirements.txt before running this script.
Validation is local: sockets are disabled and working files stay temporary.
Use --write-figures to copy the newly verified PNGs into the manuscript.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager, redirect_stdout
import difflib
from importlib.metadata import version
import io
import math
import os
from pathlib import Path
import re
import shutil
import socket
import tempfile


EXAMPLE_NAMES = (
    "unknown_probability", "unknown_fixed", "unknown_growing", "unknown_cases",
)
FIGURE_NAMES = ("11-grover-random-iterations.png", "11-grover-growing-range.png")
BASELINE = {"qiskit": "2.5.2", "numpy": "2.5.3", "matplotlib": "3.11.2"}


@contextmanager
def offline_temporary_working_directory(directory: Path):
    previous_cwd = Path.cwd()
    previous_connect = socket.socket.connect
    previous_connect_ex = socket.socket.connect_ex

    def reject_connection(*args, **kwargs):
        raise RuntimeError("network connections are disabled during validation")

    socket.socket.connect = reject_connection
    socket.socket.connect_ex = reject_connection
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(previous_cwd)
        socket.socket.connect = previous_connect
        socket.socket.connect_ex = previous_connect_ex


def execute_examples(markdown: str, source: Path):
    pattern = re.compile(
        r"<!-- example: ([a-z_]+) -->\s*\n```python\r?\n(.*?)\r?\n```"
        r"\s*\n出力:\s*\n```text\r?\n(.*?)\r?\n```", re.DOTALL,
    )
    examples = pattern.findall(markdown)
    names = tuple(name for name, _, _ in examples)
    if names != EXAMPLE_NAMES:
        raise AssertionError(f"Expected examples {EXAMPLE_NAMES}; found {names}")
    if len(re.findall(r"^```python\s*$", markdown, flags=re.MULTILINE)) != 4:
        raise AssertionError("Expected exactly four executable Python blocks")
    namespace = {"__name__": "__main__"}
    for name, code, expected in examples:
        output = io.StringIO()
        with redirect_stdout(output):
            exec(compile(code, f"{source}:{name}", "exec"), namespace)
        actual = output.getvalue().replace("\r\n", "\n").strip()
        expected = expected.replace("\r\n", "\n").strip()
        if actual != expected:
            difference = "\n".join(difflib.unified_diff(
                expected.splitlines(), actual.splitlines(),
                fromfile="printed manuscript", tofile="actual execution", lineterm="",
            ))
            raise AssertionError(f"Output mismatch in {name}:\n{difference}")
    print("PASS: all four example outputs match the manuscript")
    return namespace


def mean_probability(size: int, count: int, limit: int) -> float:
    if count == 0:
        return 0.0
    if count == size:
        return 1.0
    theta = math.asin(math.sqrt(count / size))
    return 0.5 - math.sin(4 * limit * theta) / (4 * limit * math.sin(2 * theta))


def capped_schedule(size: int, cap_trials: int):
    """List trial range sizes, assuming all earlier candidates were rejected."""
    cap = math.ceil(math.sqrt(size))
    m, completed = 1.0, 0
    limits = []
    while completed < cap_trials:
        limit = math.ceil(m)
        limits.append(limit)
        if limit == cap:
            completed += 1
        m = min(1.25 * m, cap)
    return limits


def verify_probability_bounds(namespace):
    import numpy as np
    from numpy.testing import assert_allclose

    for n in range(1, 10):
        size = 2**n
        cap = math.ceil(math.sqrt(size))
        for count in range(size + 1):
            theta = math.asin(math.sqrt(count / size))
            for limit in range(1, cap + 1):
                direct = np.mean(np.sin((2 * np.arange(limit) + 1) * theta)**2)
                average = mean_probability(size, count, limit)
                assert_allclose(average, direct, atol=1e-12, rtol=0)
                assert -1e-12 <= average <= 1 + 1e-12
            average = mean_probability(size, count, cap)
            if count:
                assert average >= 0.25 - 1e-12
            for epsilon in (0.05, 0.01):
                k = namespace["failure_budget"](epsilon)
                limits = capped_schedule(size, k)
                fixed_failure = (1 - average)**k
                growing_failure = math.prod(
                    (1 - count / size) * (1 - mean_probability(size, count, limit))
                    for limit in limits
                )
                assert limits.count(cap) == k
                if count:
                    assert fixed_failure <= epsilon + 1e-12
                    assert growing_failure <= epsilon + 1e-12
                else:
                    assert fixed_failure == growing_failure == 1
    assert capped_schedule(8, 11).index(3) + 1 == 5
    assert capped_schedule(32, 11).index(6) + 1 == 9
    assert_allclose(mean_probability(8, 2, 3), 0.5, atol=1e-12, rtol=0)
    assert namespace["failure_budget"](0.05) == 11
    assert namespace["failure_budget"](0.01) == 17
    assert 0.75**11 <= 0.05 < 0.75**10
    assert 0.75**17 <= 0.01 < 0.75**16
    print("PASS: n=1..9/all M finite sums, closed form, fixed/growing failure bounds")


def verify_operators(namespace):
    import numpy as np
    from numpy.testing import assert_allclose
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import grover_operator
    from qiskit.quantum_info import Operator, Statevector

    make = namespace["oracle_from_predicate"]
    for n in range(1, 5):
        size = 2**n
        for count in range(size + 1):
            check = lambda x, count=count: x < count
            oracle = make(n, check)
            signs = np.array([-1 if check(x) else 1 for x in range(size)])
            assert_allclose(Operator(oracle).data, np.diag(signs), atol=1e-12, rtol=0)
            uniform = np.ones(size) / np.sqrt(size)
            exact_step = (2 * np.outer(uniform, uniform) - np.eye(size)) @ np.diag(signs)
            step = grover_operator(oracle)
            assert_allclose(Operator(step).data, exact_step, atol=1e-12, rtol=0)
            theta = math.asin(math.sqrt(count / size))
            for t in range(math.ceil(math.sqrt(size))):
                circuit = QuantumCircuit(n)
                circuit.h(range(n))
                for _ in range(t):
                    circuit.compose(step, inplace=True)
                state = Statevector.from_instruction(circuit)
                assert_allclose(state.data, np.linalg.matrix_power(exact_step, t) @ uniform,
                                atol=1e-11, rtol=0)
                probability = sum(state.probabilities()[x] for x in range(count))
                assert_allclose(probability, math.sin((2*t + 1)*theta)**2,
                                atol=1e-11, rtol=0)
    example_oracle = make(3, lambda x: x*x % 8 == 4)
    expected = np.ones(8)
    expected[[2, 6]] = -1
    assert_allclose(Operator(example_oracle).data, np.diag(expected), atol=1e-12, rtol=0)
    print("PASS: n=1..4/all M oracle signs, Grover matrices, states, and bit order")


def expect_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return
    raise AssertionError(f"Expected ValueError from {function.__name__}")


def verify_searches(namespace):
    make = namespace["oracle_from_predicate"]
    checks = (lambda x: x*x % 8 == 4, lambda x: x*x % 8 == 1,
              lambda x: True, lambda x: False)
    real_trial = namespace["one_trial"]
    for method in ("find_fixed", "find_growing"):
        for check in checks:
            oracle = make(3, check)
            calls, trials = [], []

            def instrumented(x):
                calls.append(x)
                return check(x)

            def recording_trial(oracle, t, seed):
                trials.append((t, seed))
                return real_trial(oracle, t, seed)

            namespace["one_trial"] = recording_trial
            try:
                answer = namespace[method](oracle, instrumented, epsilon=0.05, seed=7)
            finally:
                namespace["one_trial"] = real_trial
            assert answer["predicate_queries"] == len(calls) == len(answer["trace"])
            assert answer["phase_queries"] == sum(row[0] for row in trials)
            assert answer["phase_queries"] == sum(
                row[2] for row in answer["trace"] if row[1] == "grover")
            assert len(trials) == len({seed for _, seed in trials})
            assert answer["rounds"] == answer["trace"][-1][0]
            for _, _, _, bits, good in answer["trace"]:
                assert good == check(int(bits, 2))
            if answer["status"] == "found":
                assert check(answer["candidate"])
            else:
                assert answer["candidate"] is None
                assert answer["rounds"] == (11 if method == "find_fixed" else 15)
            assert answer == namespace[method](oracle, check, epsilon=0.05, seed=7)

    class AlwaysZeroRandom:
        def __init__(self, seed):
            pass

        def randrange(self, stop):
            return 0

    # Exercise a possible sequence of failed measurements even when M=1.
    # Stubs affect the verification harness only, and are restored afterwards.
    real_random = namespace["Random"]
    namespace["Random"] = AlwaysZeroRandom
    namespace["one_trial"] = lambda oracle, t, seed: 0
    try:
        for n in (3, 5):
            check = lambda x: x == 1
            oracle = make(n, check)
            fixed = namespace["find_fixed"](oracle, check)
            growing = namespace["find_growing"](oracle, check)
            assert fixed["status"] == growing["status"] == "not_found"
            assert fixed["candidate"] is growing["candidate"] is None
            assert fixed["rounds"] == fixed["predicate_queries"] == 11
            expected_rounds = len(capped_schedule(2**n, 11))
            assert growing["rounds"] == expected_rounds
            assert growing["predicate_queries"] == 2 * expected_rounds
            assert fixed["phase_queries"] == growing["phase_queries"] == 0
    finally:
        namespace["Random"] = real_random
        namespace["one_trial"] = real_trial

    for bad in (0, 1, -0.1, 2):
        expect_value_error(namespace["failure_budget"], bad)
    for bad in (0, -1, 1.5):
        expect_value_error(make, bad, lambda x: False)
    for bad in (-1, 1.5):
        expect_value_error(real_trial, make(1, lambda x: x == 1), bad, 7)
    for bad in (1, 4/3, 0):
        expect_value_error(namespace["find_growing"], make(1, lambda x: True),
                           lambda x: True, growth=bad)
    print("PASS: sampled traces, query counts, fresh seeds, budgets, and input validation")
    print("PASS: not_found for forced misses with M=1, and stopping at the capped range")


def verify_figures(markdown: str, directory: Path):
    import numpy as np
    from numpy.testing import assert_allclose
    from PIL import Image
    from draw_grover_unknown import draw_figures, probability_rows, range_schedule

    references = re.findall(r"!\[[^\]]*\]\((figures/11/[^)]+)\)", markdown)
    expected_references = [f"figures/11/{name}" for name in FIGURE_NAMES]
    if sorted(references) != sorted(expected_references):
        raise AssertionError(f"Expected two figure references; found {references}")
    expected = np.array([
        [math.sin((2*t + 1) * math.asin(math.sqrt(count/32)))**2 for t in range(6)]
        for count in (1, 4)
    ])
    assert_allclose(probability_rows(), expected, atol=1e-12, rtol=0)
    assert_allclose(expected.mean(axis=1), [mean_probability(32, m, 6) for m in (1, 4)],
                    atol=1e-12, rtol=0)
    m_values, limits = range_schedule()
    assert_allclose(m_values, [min(1.25**i, 6) for i in range(11)], atol=1e-12, rtol=0)
    assert list(limits) == capped_schedule(32, 3)
    assert list(limits).index(6) + 1 == 9
    expect_value_error(range_schedule, 0)
    draw_figures(directory)
    for name in FIGURE_NAMES:
        with Image.open(directory / name) as image:
            if image.format != "PNG" or min(image.size) < 1000:
                raise AssertionError(f"Unexpected image format or size: {name}")
            image.verify()
    print("PASS: figure data, range schedule, two references, and rendered PNG files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).resolve().parents[1] / "ja" /
                        "11-grover-unknown-solutions.md")
    parser.add_argument("--write-figures", action="store_true")
    parser.add_argument("--figure-dir", type=Path,
                        help="Destination for --write-figures; default is the source's figures/11")
    args = parser.parse_args()
    source = args.source.resolve()
    markdown = source.read_text(encoding="utf-8-sig")
    actual_versions = {package: version(package) for package in BASELINE}
    print("Versions: " + ", ".join(f"{package} {value}" for package, value in actual_versions.items()))
    if actual_versions != BASELINE:
        raise RuntimeError(f"Validation baseline is {BASELINE}; found {actual_versions}")
    with tempfile.TemporaryDirectory(prefix="grover-unknown-validation-") as temporary:
        workdir = Path(temporary)
        with offline_temporary_working_directory(workdir):
            namespace = execute_examples(markdown, source)
            verify_probability_bounds(namespace)
            verify_operators(namespace)
            verify_searches(namespace)
            figure_directory = workdir / "figures"
            verify_figures(markdown, figure_directory)
        # Copy only after every example, numerical check, and figure has passed.
        if args.write_figures:
            destination = (args.figure_dir or source.parent / "figures" / "11").resolve()
            destination.mkdir(parents=True, exist_ok=True)
            for name in FIGURE_NAMES:
                shutil.copy2(figure_directory / name, destination / name)
            print(f"Wrote validated figures: {destination}")
    print("PASS: unknown-count Grover validation completed offline")


if __name__ == "__main__":
    main()
