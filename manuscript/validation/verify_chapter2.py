"""Execute Chapter 2 examples, check measurement mathematics and regenerate figures.

Requires the manuscript baseline plus matplotlib, pylatexenc, seaborn and Pillow.
    python manuscript/validation/verify_chapter2.py
    python manuscript/validation/verify_chapter2.py --write-figures

Examples are trusted repository code. They run in an isolated temporary directory.
Only --write-figures copies the generated PNGs into the manuscript.
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

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "qiskit-manuscript-mpl"))
import matplotlib
matplotlib.use("Agg")
import numpy as np
from PIL import Image
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, SGate
from qiskit.quantum_info import DensityMatrix, Operator, Pauli, Statevector, partial_trace

from verify_sample_sections import ROOT, check_links, close, require

SOURCE = ROOT / "manuscript/ja/02-visualization-measurement.md"
ASSETS = SOURCE.parent / "figures/02"


def run_examples(directory: Path) -> list[dict]:
    source = SOURCE.read_text(encoding="utf-8")
    examples = list(re.finditer(r"```python\n(.*?)\n```\s*出力:\s*```text\n(.*?)\n```", source, re.S))
    require(len(examples) == len(re.findall(r"^```python$", source, re.M)) == 13,
            "Every Chapter 2 Python example must have a checked output")
    namespaces = []
    with chdir(directory):
        for index, example in enumerate(examples, 1):
            namespace = {"__name__": "__main__"}
            stdout = StringIO()
            with redirect_stdout(stdout):
                exec(compile(example[1], str(SOURCE), "exec"), namespace)
            require(stdout.getvalue().strip() == example[2].strip(),
                    f"Example {index} differs from printed output:\n{stdout.getvalue()}")
            namespaces.append(namespace)
            print(f"PASS Chapter 2 printed output: example {index}")
    images = {Path(name).name for name in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source)}
    require(images == {path.name for path in directory.glob("*.png")}, "Figures and source image links differ")
    for name in sorted(images):
        with Image.open(directory / name) as img:
            require(img.format == "PNG" and min(img.size) >= 400, f"Invalid or small figure: {name}")
            extrema = img.convert("RGB").getextrema()
            require(any(low < high for low, high in extrema), f"Blank figure: {name}")
        with Image.open(directory / name) as img:
            img.verify()
    print(f"PASS {len(images)} generated PNGs and manuscript image references")
    return namespaces


def check_measurement() -> None:
    h, s = Operator(HGate()).data, Operator(SGate()).data
    basis = np.eye(2, dtype=complex)
    states = [Statevector.from_label(label) for label in ("0", "1", "+", "-", "r", "l")]
    states.append(Statevector([np.sqrt(3) / 2, 1j / 2]))
    for u in (np.eye(2), h, s @ h):
        # A direct projector and rotate-measure-restore implement the same instrument.
        for state in states:
            rotated = state.evolve(u.conj().T)
            for b in (0, 1):
                target = u[:, b]
                projector = np.outer(target, target.conj())
                projected = projector @ state.data
                probability = float(np.vdot(projected, projected).real)
                close(rotated.probabilities()[b], probability)
                if probability > 1e-12:
                    direct_post = Statevector(projected / np.sqrt(probability))
                    require(direct_post.equiv(Statevector(target)), "Projector normalization")
                    raw_post = Statevector(basis[b])
                    require(raw_post.evolve(u).equiv(direct_post), "Restore original basis after readout")
                    close(direct_post.evolve(u.conj().T).probabilities(), basis[b].real)
    psi = Statevector([np.sqrt(3) / 2, 1j / 2])
    original = psi.data.copy()
    observed = set()
    for seed in range(12):
        psi.seed(seed)
        b, post = psi.measure()
        observed.add(b)
        close(post.probabilities(), basis[int(b)].real)
        close(post.evolve(h).probabilities(), [0.5, 0.5])
        close(psi.data, original)
    require(observed == {"0", "1"}, "Both measurement branches must be exercised")
    # Exact sequential joint distributions, with the first result written on the left.
    plus = Statevector.from_label("+")
    zz, zx = np.zeros((2, 2)), np.zeros((2, 2))
    for b in (0, 1):
        zz[b] = plus.probabilities()[b] * Statevector(basis[b]).probabilities()
        zx[b] = plus.probabilities()[b] * Statevector(basis[b]).evolve(h).probabilities()
    close(zz, [[0.5, 0], [0, 0.5]])
    close(zx, np.full((2, 2), 0.25))
    close(Statevector.from_label("l").evolve(h @ s.conj().T).probabilities(), [0, 1])
    require(Statevector.from_label("1").evolve(s @ h).equiv(Statevector.from_label("l")), "Y restoration")
    print("PASS Z/X/Y projectors, normalization, both branches, repeat measurement and restoration")


def check_states_and_figures(namespaces: list[dict]) -> None:
    basis = np.eye(4)
    phi_plus = Statevector((basis[0] + basis[3]) / np.sqrt(2))
    phi_minus = Statevector((basis[0] - basis[3]) / np.sqrt(2))
    mixed = DensityMatrix(np.diag([0.5, 0, 0, 0.5]))
    readout = QuantumCircuit(2)
    readout.h(0)
    readout.h(1)
    close(phi_plus.evolve(readout).probabilities(), [0.5, 0, 0, 0.5])
    close(phi_minus.evolve(readout).probabilities(), [0, 0.5, 0.5, 0])
    close(mixed.evolve(readout).probabilities(), [0.25] * 4)
    for seed in (0, 2):
        phi_plus.seed(seed)
        b, post = phi_plus.measure([0])
        close(post.probabilities(), basis[0 if b == "0" else 3])
    for state in (phi_plus, mixed):
        for remove in ([0], [1]):
            close(partial_trace(state, remove).data, np.eye(2) / 2)
    close(phi_plus.expectation_value(Pauli("XX")), 1)
    close(mixed.expectation_value(Pauli("XX")), 0)
    close(DensityMatrix(phi_plus).data[0, 3], 0.5)
    close(mixed.data[0, 3], 0)
    require(DensityMatrix(Statevector.from_label("++")).data[0, 3] != 0,
            "Off-diagonal entries do not prove entanglement")
    close(DensityMatrix(Statevector.from_label("r")).data[0, 1], -0.5j)
    close(partial_trace(Statevector.from_label("+0"), [1]).data, [[1, 0], [0, 0]])
    for label in ("0", "+", "r"):
        psi = Statevector.from_label(label)
        rho = DensityMatrix(psi)
        for p in ("X", "Y", "Z"):
            close(np.trace(rho.data @ Pauli(p).to_matrix()), psi.expectation_value(Pauli(p)))
    psi = Statevector([np.sqrt(3) / 2, 1j / 2])
    close([psi.expectation_value(Pauli(p)) for p in ("X", "Y", "Z")], [0, np.sqrt(3) / 2, 0.5])
    close(np.sqrt(0.25 * 0.75 / np.array([100, 1000])), [0.043301270189, 0.013693063938])
    plot = namespaces[8]  # The counts/distribution comparison uses the same example data.
    close(sorted(patch.get_height() for patch in plot["axes"][0].patches), [24, 76, 240, 760])
    close(sorted(patch.get_height() for patch in plot["axes"][1].patches), [0.24, 0.24, 0.76, 0.76])
    close(namespaces[10]["coordinates"], [0, np.sqrt(3) / 2, 0.5])
    print("PASS Bell phase/correlation, reduced states, density matrices, Bloch coordinates and plotted values")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-figures", action="store_true")
    args = parser.parse_args()
    require(version("qiskit") == "2.5.2", "Use Qiskit 2.5.2")
    print(" / ".join(f"{name} {version(name)}" for name in ("qiskit", "numpy", "matplotlib", "pylatexenc")))
    with tempfile.TemporaryDirectory(prefix="qiskit-chapter2-") as tmp:
        directory = Path(tmp)
        namespaces = run_examples(directory)
        check_measurement()
        check_states_and_figures(namespaces)
        if args.write_figures:
            ASSETS.mkdir(parents=True, exist_ok=True)
            for png in directory.glob("*.png"):
                shutil.copy2(png, ASSETS / png.name)
            print(f"WROTE figures: {ASSETS}")
    check_links()


if __name__ == "__main__":
    main()
