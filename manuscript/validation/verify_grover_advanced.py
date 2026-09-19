"""Verify the trusted local Advanced Grover manuscript and its two figures.

Execute the four tagged Python examples, compare their printed output, and
check their operators and probabilities independently. No network is needed.
Install manuscript/validation/requirements.txt before running this script.
Figures are rendered in a temporary directory for validation; use
--write-figures to copy the verified PNGs into the manuscript afterwards.
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
    "advanced_core", "advanced_sampling", "advanced_general", "advanced_library",
)
FIGURE_NAMES = ("10-grover-probabilities.png", "10-grover-subspaces.png")
BASELINE = {"qiskit": "2.5.2", "numpy": "2.5.3", "matplotlib": "3.11.2"}


@contextmanager
def offline_temporary_working_directory(directory: Path):
    """Keep example writes temporary and reject outgoing socket connections."""
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


def extract_examples(markdown: str):
    """Read only named code blocks from the explicitly supplied local source."""
    pattern = re.compile(
        r"<!-- example: ([a-z_]+) -->\s*\n```python\r?\n(.*?)\r?\n```"
        r"\s*\n出力:\s*\n```text\r?\n(.*?)\r?\n```",
        re.DOTALL,
    )
    examples = pattern.findall(markdown)
    names = tuple(name for name, _, _ in examples)
    if names != EXAMPLE_NAMES:
        raise AssertionError(f"Expected examples {EXAMPLE_NAMES}; found {names}")
    if len(re.findall(r"^```python\s*$", markdown, flags=re.MULTILINE)) != 4:
        raise AssertionError("Expected exactly four executable Python blocks")
    return examples


def execute_examples(markdown: str, source: Path):
    namespace = {"__name__": "__main__"}
    for name, code, expected in extract_examples(markdown):
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


def expect_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return
    raise AssertionError(f"Expected ValueError from {function.__name__}{args!r}")


def verify_math(namespace):
    import numpy as np
    from numpy.testing import assert_allclose
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import grover_operator
    from qiskit.quantum_info import Operator, Statevector

    phase_oracle = namespace["phase_oracle"]
    diffuser = namespace["diffuser"]
    grover_circuit = namespace["grover_circuit"]
    choose_repetitions = namespace["repetitions_for_known_count"]

    marked_sets = (
        ["0"], ["1"], ["0", "1"], ["10"], ["01", "10"],
        ["111"], ["011", "100"], ["001", "110"],
    )
    for solutions in marked_sets:
        dimension = 2 ** len(solutions[0])
        diagonal = np.ones(dimension)
        diagonal[[int(bits, 2) for bits in solutions]] = -1
        assert_allclose(Operator(phase_oracle(solutions)).data, np.diag(diagonal),
                        atol=1e-12, rtol=0)
    for invalid in ([], [""], ["01", "1"], ["0a"], ["11", "11"]):
        expect_value_error(phase_oracle, invalid)
    for n in (1, 2, 3):
        dimension = 2 ** n
        s = np.ones(dimension) / np.sqrt(dimension)
        assert_allclose(Operator(diffuser(n)).data,
                        2 * np.outer(s, s) - np.eye(dimension), atol=1e-12, rtol=0)
    expect_value_error(grover_circuit, phase_oracle(["011", "100"]), -1)
    expect_value_error(grover_circuit, phase_oracle(["011", "100"]), 1.5)
    print("PASS: oracle signs, bit order, input validation, and exact diffuser phase")

    cases = (
        (["011", "100"], (0, 1, 2, 3)),
        (["0000011", "0100101", "1010010", "1111001"], (0, 1, 4, 5)),
    )
    for solutions, repetitions in cases:
        n = len(solutions[0])
        dimension, count = 2 ** n, len(solutions)
        indices = [int(bits, 2) for bits in solutions]
        s = np.ones(dimension) / np.sqrt(dimension)
        a1 = np.zeros(dimension)
        a1[indices] = 1 / np.sqrt(count)
        a0 = np.ones(dimension)
        a0[indices] = 0
        a0 /= np.sqrt(dimension - count)
        theta = math.asin(math.sqrt(count / dimension))
        diagonal = np.ones(dimension)
        diagonal[indices] = -1
        expected_g = (2 * np.outer(s, s) - np.eye(dimension)) @ np.diag(diagonal)
        oracle = phase_oracle(solutions)
        manual_g = QuantumCircuit(n)
        manual_g.compose(oracle, inplace=True)
        manual_g.compose(diffuser(n), inplace=True)
        assert_allclose(Operator(manual_g).data, expected_g, atol=1e-11, rtol=0)
        for t in repetitions:
            state = Statevector(grover_circuit(oracle, t))
            expected = np.linalg.matrix_power(expected_g, t) @ s
            coordinates = np.array([math.cos((2 * t + 1) * theta),
                                    math.sin((2 * t + 1) * theta)])
            assert_allclose(state.data, expected, atol=1e-11, rtol=0)
            assert_allclose(state.data, coordinates[0] * a0 + coordinates[1] * a1,
                            atol=1e-11, rtol=0)
            assert_allclose([np.vdot(a0, state.data), np.vdot(a1, state.data)],
                            coordinates, atol=1e-11, rtol=0)
            assert_allclose(state.probabilities()[indices],
                            np.full(count, coordinates[1] ** 2 / count),
                            atol=1e-11, rtol=0)
        assert_allclose(Statevector(s).evolve(oracle).data,
                        math.cos(theta) * a0 - math.sin(theta) * a1,
                        atol=1e-11, rtol=0)
    print("PASS: N=8/M=2 and N=128/M=4 matrices, signed coordinates, and probabilities")

    counts = namespace["counts"]
    assert sum(counts.values()) == namespace["shots"] == 512
    assert set(counts) == {"011", "100"}
    assert all(isinstance(value, int) and value > 0 for value in counts.values())
    assert namespace["hits"] == 512
    assert choose_repetitions(2, 1) == 1
    assert choose_repetitions(3, 2) == 1
    assert choose_repetitions(3, 1) == 2
    assert choose_repetitions(7, 4) == 4
    assert choose_repetitions(3, 4) == 0
    assert choose_repetitions(3, 5) == 0
    assert choose_repetitions(3, 8) == 0
    for n, count in ((0, 1), (-1, 1), (1.5, 1), (3, 0), (3, -1), (3, 9), (3, 1.5)):
        expect_value_error(choose_repetitions, n, count)
    for solutions in (["0", "1"], ["000", "001", "010", "011"],
                      [f"{x:03b}" for x in range(8)]):
        n = len(solutions[0])
        state = Statevector(grover_circuit(phase_oracle(solutions),
                                          choose_repetitions(n, len(solutions))))
        actual = sum(state.probabilities()[int(bits, 2)] for bits in solutions)
        assert_allclose(actual, len(solutions) / (2 ** n), atol=1e-12, rtol=0)
    assert_allclose(Operator(namespace["g"]).data, Operator(namespace["manual_g"]).data,
                    atol=1e-12, rtol=0)
    assert_allclose(Statevector(namespace["library_qc"]).data,
                    namespace["amplified"].data, atol=1e-12, rtol=0)
    for solutions in (["10"], ["011", "100"]):
        n = len(solutions[0])
        oracle = phase_oracle(solutions)
        manual_g = QuantumCircuit(n)
        manual_g.compose(oracle, inplace=True)
        manual_g.compose(diffuser(n), inplace=True)
        assert_allclose(Operator(grover_operator(oracle)).data, Operator(manual_g).data,
                        atol=1e-12, rtol=0)
    print("PASS: 512-shot sampling, known-count boundaries, and library matrix equality")

    probabilities = np.stack([namespace[name].probabilities()
                              for name in ("initial", "marked", "amplified")])
    expected = np.full((3, 8), 1 / 8)
    expected[2] = 0
    expected[2, [3, 4]] = 0.5
    assert_allclose(probabilities, expected, atol=1e-12, rtol=0)
    return probabilities


def verify_figures(markdown: str, directory: Path, probabilities):
    from PIL import Image
    from draw_grover_advanced import draw_figures

    references = re.findall(r"!\[[^\]]*\]\((figures/10/[^)]+)\)", markdown)
    expected_references = [f"figures/10/{name}" for name in FIGURE_NAMES]
    if sorted(references) != sorted(expected_references):
        raise AssertionError(f"Expected two figure references; found {references}")
    draw_figures(directory, probabilities)
    for name in FIGURE_NAMES:
        path = directory / name
        with Image.open(path) as image:
            if image.format != "PNG" or min(image.size) < 1000:
                raise AssertionError(f"Unexpected image format or size: {name}")
            image.verify()
    print("PASS: both figure references and rendered PNG files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).resolve().parents[1] / "ja" / "10-grover-advanced.md")
    parser.add_argument("--write-figures", action="store_true")
    parser.add_argument("--figure-dir", type=Path,
                        help="Destination for --write-figures; default is source/figures/10")
    args = parser.parse_args()
    source = args.source.resolve()
    markdown = source.read_text(encoding="utf-8-sig")
    actual_versions = {package: version(package) for package in BASELINE}
    print("Versions: " + ", ".join(f"{package} {value}" for package, value in actual_versions.items()))
    if actual_versions != BASELINE:
        raise RuntimeError(f"Validation baseline is {BASELINE}; found {actual_versions}")
    with tempfile.TemporaryDirectory(prefix="grover-advanced-validation-") as temporary:
        workdir = Path(temporary)
        with offline_temporary_working_directory(workdir):
            namespace = execute_examples(markdown, source)
            probabilities = verify_math(namespace)
            figure_directory = workdir / "figures"
            verify_figures(markdown, figure_directory, probabilities)
        # Do not update deliverables until every source and numerical check passes.
        if args.write_figures:
            destination = (args.figure_dir or source.parent / "figures" / "10").resolve()
            destination.mkdir(parents=True, exist_ok=True)
            for name in FIGURE_NAMES:
                shutil.copy2(figure_directory / name, destination / name)
            print(f"Wrote validated figures: {destination}")
    print("PASS: Advanced Grover validation completed offline")


if __name__ == "__main__":
    main()
