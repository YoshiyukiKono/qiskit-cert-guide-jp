"""Verify the algorithm supplement's printed examples, math and five figures.

python -X utf8 -B manuscript/validation/verify_algorithm_examples.py
python -X utf8 -B manuscript/validation/verify_algorithm_examples.py --write-figures
Uses the pinned manuscript environment. Does not connect to a service or QPU.
"""
from __future__ import annotations

import argparse
from contextlib import chdir, redirect_stdout
from importlib.metadata import version
from io import StringIO
import os
from pathlib import Path
import re
import shutil
import tempfile
from unittest.mock import patch

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "qiskit-manuscript-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Operator, Statevector
from verify_sample_sections import ROOT, anchors, check_links, close, require
from draw_grover_geometry import draw_geometry

SOURCE = ROOT / "manuscript/ja/09-algorithm-worked-examples.md"
ASSETS = SOURCE.parent / "figures/09"
NAMES = ["kickback", "deutsch", "grover_stages", "grover_variants",
         "vqe_grid", "vqe_optimize", "vqe_readout"]
FIGURES = {"09-deutsch.png", "09-grover-probabilities.png", "09-vqe-energy.png",
           "09-grover-reflections.png", "09-grover-rotations.png"}


def run_examples(directory: Path) -> dict[str, dict]:
    source = SOURCE.read_text(encoding="utf-8")
    examples = list(re.finditer(r"<!-- example: (\w+) -->\n```python\n(.*?)\n```", source, re.S))
    require([e[1] for e in examples] == NAMES, "Example list changed")
    require(len(examples) == len(re.findall(r"^```python$", source, re.M)), "Unclassified Python fence")
    prose = re.sub(r"```.*?```", "", source, flags=re.S)
    require(not any("（" in s or "）" in s for s in re.findall(r"\*\*([^*\n]+)\*\*", prose)),
            "Full-width parentheses inside bold")
    require(not re.search(r"mock|practice-bank", source, re.I), "Specific exam reference in supplement")
    require({"algorithm-deutsch", "algorithm-grover", "algorithm-vqe", "algorithm-connections"}
            <= anchors(source), "Missing section anchor")
    namespaces = {}
    with chdir(directory):
        for example in examples:
            name, code = example[1], example[2]
            namespace = {"__name__": "__main__"}
            output = StringIO()
            with redirect_stdout(output):
                exec(compile(code, str(SOURCE), "exec"), namespace)
            expected = re.match(r"\s*出力:\s*```text\n(.*?)\n```", source[example.end():], re.S)
            require(expected is not None, f"Missing output: {name}")
            require(output.getvalue().strip() == expected[1].strip(), f"Output differs: {name}\n{output.getvalue()}")
            namespaces[name] = namespace
            plt.close("all")
            print(f"PASS printed output: {name}")
    draw_geometry(directory)
    images = {Path(p).name for p in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)}
    require(images == FIGURES == {p.name for p in directory.glob("*.png")}, "Figure output/link mismatch")
    for name in FIGURES:
        with Image.open(directory / name) as img:
            require(img.format == "PNG" and min(img.size) >= 150, "Invalid figure")
            require(any(a < b for a, b in img.convert("RGB").getextrema()), "Blank figure")
    return namespaces


def check_deutsch(ns: dict[str, dict]) -> None:
    functions = ns["deutsch"]
    make = functions["make_deutsch_oracle"]
    deutsch = functions["deutsch"]
    minus = np.array([1, -1]) / np.sqrt(2)
    plus = np.array([1, 1]) / np.sqrt(2)
    for f0, f1 in [(0, 0), (1, 1), (0, 1), (1, 0)]:
        oracle = make((f0, f1))
        # Truth-table permutation in Qiskit's |y x> order, independent of gates.
        expected = np.zeros((4, 4))
        for x in [0, 1]:
            for y in [0, 1]:
                expected[2 * (y ^ (f0, f1)[x]) + x, 2*y + x] = 1
        close(Operator(oracle).data, expected)
        close(expected @ expected, np.eye(4))
        post_oracle = expected @ np.kron(minus, plus)
        close(post_oracle, np.kron(minus, [(-1)**f0, (-1)**f1]) / np.sqrt(2))
        qc = deutsch(oracle)
        require(qc.num_clbits == 1 and qc.find_bit(qc.data[-1].qubits[0]).index == 0,
                "Deutsch must measure input qubit into one-bit register")
        prep = qc.remove_final_measurements(inplace=False)
        output_bit = np.eye(2)[f0 ^ f1]
        close(Statevector(prep).data, (-1)**f0 * np.kron(minus, output_bit))
        # Question 1: delete the initial X, thus preparing |+> on the work qubit.
        changed = prep.copy()
        initial_x = next(i for i, item in enumerate(changed.data)
                         if item.operation.name == "x" and changed.find_bit(item.qubits[0]).index == 1)
        del changed.data[initial_x]
        close(Statevector(changed).probabilities([0]), [1, 0])
        # Question 2: remove only the readout H.
        no_readout_h = prep.copy()
        del no_readout_h.data[-1]
        close(Statevector(no_readout_h).probabilities([0]), [.5, .5])
    # General kickback with eigenvalue exp(i*phase) and complex control amplitudes.
    control = np.array([np.sqrt(.3), 1j*np.sqrt(.7)])
    for phase in [-.4, 1.1]:
        controlled_phase = QuantumCircuit(2)
        controlled_phase.cp(phase, 0, 1)
        initial = Statevector(np.kron([0, 1], control))
        expected_control = control * [1, np.exp(1j*phase)]
        close(initial.evolve(controlled_phase).data, np.kron([0, 1], expected_control))
    print("PASS all four reversible oracles, exact phases, general kickback and changed preparation/readout")


def check_grover(ns: dict[str, dict]) -> None:
    samples = ns["grover_stages"]
    d = np.ones((4, 4)) / 2 - np.eye(4)
    close(Operator(samples["diffuser"]).data, d)
    close(d.conj().T @ d, np.eye(4))
    close(samples["marked"].data, [.5, .5, .5, -.5])
    close(samples["amplified"].data, [0, 0, 0, 1])
    negative_d = samples["diffuser"].copy()
    negative_d.global_phase = 0
    close(Operator(negative_d).data, -d)
    # The average-amplitude rule also holds for complex amplitudes.
    vector = np.array([1, 2j, -2, 1j]) / np.sqrt(10)
    close(d @ vector, 2*np.mean(vector) - vector)
    variants = ns["grover_variants"]
    for target in ["00", "01", "10", "11"]:
        index = int(target, 2)
        diagonal = np.ones(4)
        diagonal[index] = -1
        o = np.diag(diagonal)
        close(Operator(variants["phase_oracle"](target)).data, o)
        for repetitions in range(7):
            expected = np.linalg.matrix_power(d @ o, repetitions) @ (np.ones(4) / 2)
            qc = variants["grover"](target, repetitions)
            close(Statevector(qc).data, expected)
            # Independent two-dimensional rotation formula, N=4 and M=1.
            close(abs(expected[index])**2, np.sin((2*repetitions+1)*np.pi/6)**2)
        measured = variants["grover"](target, 1)
        measured.measure_all()
        counts = StatevectorSampler(seed=7).run([measured], shots=16).result()[0].data.meas.get_counts()
        require(counts == {target: 16}, "Marked state/readout order")
    close(Statevector(variants["grover"]("11", 2)).data, [-.5, -.5, -.5, .5])
    # Project the four amplitudes onto the two axes shown in the new figures.
    basis = np.column_stack(([1/np.sqrt(3)]*3 + [0], [0, 0, 0, 1]))
    close(basis.T @ basis, np.eye(2))
    close(basis.T @ np.diag([1, 1, 1, -1]) @ basis, np.diag([1, -1]))
    close(basis.T @ d @ basis, [[.5, np.sqrt(3)/2], [np.sqrt(3)/2, -.5]])
    for repetitions in range(4):
        state = Statevector(variants["grover"]("11", repetitions)).data
        angle = (2*repetitions+1)*np.pi/6
        coordinates = np.array([np.cos(angle), np.sin(angle)])
        close(basis.T @ state, coordinates)
        close(basis @ coordinates, state)
    print("PASS signed geometry coordinates, two reflections and four-amplitude reconstruction")
    print("PASS every marked basis state, complex reflection, D versus -D, 0–6 iterations and readout")


def check_vqe(ns: dict[str, dict]) -> None:
    sample = ns["vqe_grid"]
    h = np.array([[1., .5], [.5, -1.]])
    close(sample["hamiltonian"].to_matrix(), h)
    close(sample["energies"], np.cos(sample["angles"]) + .5*np.sin(sample["angles"]))
    require(sample["values"].shape == (9, 1) and sample["energies"].shape == (9,), "Grid shapes")
    # Include negative angles, periodic endpoints and states outside the grid.
    for angle in [-3.1, -.41, 0, .27, np.pi, 3.6, 2*np.pi, 8.7]:
        vector = np.array([np.cos(angle/2), np.sin(angle/2)])
        bound = sample["ansatz"].assign_parameters({sample["theta"]: angle})
        close(Statevector(bound).data, vector)
        close(vector @ h @ vector, np.cos(angle) + .5*np.sin(angle))
    optimized = ns["vqe_optimize"]
    result = optimized["optimized"]
    ground = -np.sqrt(5) / 2
    require(result.success and len(optimized["evaluations"]) > 1, "Optimizer must query multiple points")
    require(result.fun < sample["energies"].min(), "Refinement should improve on grid")
    require(abs(result.x - (np.pi + np.arctan(.5))) < 1e-6, "Optimal angle")
    close(result.fun, ground)
    close(optimized["exact"], ground)
    for angle, energy in optimized["evaluations"]:
        close(energy, np.cos(angle) + .5*np.sin(angle))
        require(energy >= ground - 1e-12, "Variational bound")
        require(optimized["left"] <= angle <= optimized["right"], "Bounded interval")
    readout = ns["vqe_readout"]
    state = readout["state"]
    close(h @ state.data, ground * state.data)
    close(state.probabilities(), [(1 - 2/np.sqrt(5))/2, (1 + 2/np.sqrt(5))/2])
    x_circuit = readout["x_circuit"].remove_final_measurements(inplace=False)
    close(Statevector(x_circuit).probabilities(), [(1 - 1/np.sqrt(5))/2, (1 + 1/np.sqrt(5))/2])
    # This sample estimate need not satisfy the variational bound; verify its
    # construction from separate X and Z experiments instead of exact equality.
    means = []
    for result_item in readout["results"]:
        counts = result_item.data.meas.get_counts()
        require(sum(counts.values()) == 512, "Shots per basis")
        means.append((counts.get("0", 0) - counts.get("1", 0))/512)
    close(readout["means"], means)
    for angle in [-np.pi, 0, .73, 3.9]:
        rz = QuantumCircuit(1)
        rz.rz(angle, 0)
        close(Statevector(rz).expectation_value(sample["hamiltonian"]), 1)
    # Question 1: H=Z instead, same Ry ansatz.
    close(np.array([0., 1.]) @ np.diag([1, -1]) @ np.array([0., 1.]), -1)
    print("PASS analytic energies, grid/PUB shapes, adaptive minimization, eigenstate, two-basis sampling and ansatz limit")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-figures", action="store_true")
    args = parser.parse_args()
    baseline = {"qiskit": "2.5.2", "numpy": "2.5.3", "scipy": "1.18.1"}
    for name, expected in baseline.items():
        require(version(name) == expected, f"Use {name}=={expected}")
    print("Versions:", ", ".join(f"{n}={version(n)}" for n in baseline))
    with tempfile.TemporaryDirectory(prefix="qiskit-algorithm-examples-") as temporary:
        directory = Path(temporary)
        with patch("socket.socket.connect", side_effect=AssertionError("Network forbidden")):
            ns = run_examples(directory)
            check_deutsch(ns)
            check_grover(ns)
            check_vqe(ns)
        if args.write_figures:
            ASSETS.mkdir(parents=True, exist_ok=True)
            for name in FIGURES:
                shutil.copy2(directory / name, ASSETS / name)
            print(f"WROTE {len(FIGURES)} supplement figures")
    check_links((ROOT / "README.md",))
    print("PASS 7 independent examples, changed-condition questions and 5 figures; no QPU submission")


if __name__ == "__main__":
    main()
