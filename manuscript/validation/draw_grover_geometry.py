"""Draw Grover's two-dimensional geometry for N=4 and one marked state.

Run from any directory, for example::

    python manuscript/validation/draw_grover_geometry.py
    python manuscript/validation/draw_grover_geometry.py --output-dir /tmp/figures

The default destination is manuscript/ja/figures/09 when this file is in
manuscript/validation.  NumPy and Matplotlib are the only dependencies.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "grover-mpl"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Arc, Circle, FancyArrowPatch
import numpy as np


BLUE = "#286a9a"
ORANGE = "#b44425"
INK = "#263442"
MUTED = "#6d7883"
FAINT = "#d9e0e6"
THETA = np.arcsin(1 / np.sqrt(4))


def _font() -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in ("Yu Gothic", "Meiryo", "Noto Sans CJK JP", "IPAexGothic"):
        if name in available:
            return name
    return "DejaVu Sans"


def _point(angle: float, radius: float = 1) -> np.ndarray:
    return radius * np.array([np.cos(angle), np.sin(angle)])


def _plane(ax: plt.Axes, *, axis_labels: bool = True) -> None:
    ax.set_aspect("equal")
    ax.set_xlim(-1.29, 1.29)
    ax.set_ylim(-1.29, 1.29)
    ax.axis("off")
    ax.add_patch(Circle((0, 0), 1, fill=False, color=FAINT, lw=1.25, zorder=0))
    for end in ((1.2, 0), (0, 1.2)):
        start = (-1.19, 0) if end[0] else (0, -1.19)
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=11,
                                    color=MUTED, lw=0.9, zorder=1))
    ax.scatter([0], [0], s=13, color=INK, zorder=5)
    ax.text(-0.065, -0.095, "0", ha="right", va="top", fontsize=11, color=MUTED)
    if axis_labels:
        ax.text(1.22, -0.11, r"$\alpha\ (|A_0\rangle)$", ha="right", va="top",
                fontsize=14, color=INK)
        ax.text(0.06, 1.205, r"$\beta\ (|A_1\rangle)$", ha="left", va="center",
                fontsize=14, color=INK)


def _vector(ax: plt.Axes, angle: float, color: str, *, alpha: float = 1,
            linewidth: float = 2.8, zorder: int = 5) -> None:
    end = _point(angle)
    ax.add_patch(FancyArrowPatch((0, 0), end, arrowstyle="-|>",
                                mutation_scale=18, lw=linewidth, color=color,
                                alpha=alpha, shrinkA=0, shrinkB=0, zorder=zorder))


def _angle(ax: plt.Axes, start: float, end: float, radius: float,
           label: str | None = None, *, label_radius: float | None = None,
           color: str = MUTED, arrow: bool = False) -> None:
    ax.add_patch(Arc((0, 0), 2 * radius, 2 * radius,
                     theta1=np.degrees(start), theta2=np.degrees(end),
                     color=color, lw=1.25, zorder=3))
    if arrow:
        before = _point(end - np.deg2rad(5), radius)
        tip = _point(end, radius)
        ax.add_patch(FancyArrowPatch(before, tip, arrowstyle="-|>",
                                    mutation_scale=10, color=color, lw=0.8,
                                    shrinkA=0, shrinkB=0, zorder=4))
    if label:
        xy = _point((start + end) / 2, label_radius or radius + 0.13)
        ax.text(*xy, label, color=color, ha="center", va="center", fontsize=13,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.0},
                zorder=6)


def _reflections(directory: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.5))
    fig.subplots_adjust(left=0.035, right=0.97, top=0.83, bottom=0.1, wspace=0.19)

    ax = axes[0]
    _plane(ax)
    ax.set_title(r"1. $O_f$ による反射", fontsize=18, color=INK, pad=31)
    ax.plot([-1.17, 1.17], [0, 0], color=INK, lw=1.4, zorder=2)
    _vector(ax, THETA, BLUE)
    _vector(ax, -THETA, ORANGE)
    x, y = _point(THETA)
    ax.plot([x, x], [-y, y], color=FAINT, lw=1.2, linestyle=(0, (3, 3)), zorder=0)
    ax.text(x + 0.04, y + 0.04, r"$|s\rangle$", color=BLUE, fontsize=19,
            ha="left", va="bottom")
    ax.text(x + 0.04, -y - 0.04, r"$O_f|s\rangle$", color=ORANGE, fontsize=17,
            ha="left", va="top")
    ax.text(-0.12, y, r"$+\frac{1}{2}$", ha="right", va="center",
            color=BLUE, fontsize=16)
    ax.text(-0.12, -y, r"$-\frac{1}{2}$", ha="right", va="center",
            color=ORANGE, fontsize=16)
    ax.plot([0, x], [y, y], color=BLUE, lw=1, alpha=0.6, linestyle=(0, (3, 3)))
    ax.plot([0, x], [-y, -y], color=ORANGE, lw=1, alpha=0.6, linestyle=(0, (3, 3)))
    _angle(ax, 0, THETA, 0.30, r"$30^\circ$", label_radius=0.48)
    _angle(ax, -THETA, 0, 0.30, r"$30^\circ$", label_radius=0.48)
    ax.text(0, -1.42, r"$|A_0\rangle$ の軸を鏡にして、$\beta$ の符号を反転",
            ha="center", va="center", fontsize=13.2, color=INK)

    ax = axes[1]
    _plane(ax)
    ax.set_title(r"2. $D$ による反射", fontsize=18, color=INK, pad=31)
    low, high = _point(THETA, -1.2), _point(THETA, 1.23)
    ax.plot([low[0], high[0]], [low[1], high[1]], color=MUTED,
            lw=1.5, linestyle=(0, (5, 3)), zorder=2)
    _vector(ax, -THETA, BLUE)
    _vector(ax, 3 * THETA, ORANGE)
    ax.text(x + 0.03, -y - 0.04, r"$O_f|s\rangle$", color=BLUE, fontsize=17,
            ha="left", va="top")
    ax.text(-0.09, 1.0, r"$G|s\rangle=|A_1\rangle$", color=ORANGE,
            fontsize=16, ha="right", va="bottom")
    ax.text(high[0] - 0.02, high[1] + 0.055, r"$|s\rangle$ の直線",
            fontsize=13.2, color=MUTED, ha="right", va="bottom")
    _angle(ax, -THETA, THETA, 0.4, r"$60^\circ$", label_radius=0.62)
    _angle(ax, THETA, 3 * THETA, 0.4, r"$60^\circ$", label_radius=0.62)
    ax.text(0, -1.42, r"$|s\rangle$ の直線を鏡にして、正解の方向へ反射",
            ha="center", va="center", fontsize=13.2, color=INK)

    fig.savefig(directory / "09-grover-reflections.png", dpi=180,
                facecolor="white", bbox_inches="tight", pad_inches=0.17)
    plt.close(fig)


def _rotations(directory: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 11.0))
    fig.subplots_adjust(left=0.07, right=0.95, top=0.91, bottom=0.11,
                        wspace=0.16, hspace=0.46)
    signed_labels = (r"$+\frac{1}{2}$", r"$+1$", r"$+\frac{1}{2}$", r"$-\frac{1}{2}$")
    probabilities = (r"$P_0=1/4$", r"$P_1=1$", r"$P_2=1/4$", r"$P_3=1/4$")

    for t, ax in enumerate(axes.flat):
        angle = (2 * t + 1) * THETA
        alpha, beta = _point(angle)
        _plane(ax, axis_labels=False)
        ax.text(1.17, -0.10, r"$\alpha$", ha="right", va="top", fontsize=16, color=INK)
        ax.text(0.09, 1.17, r"$\beta$", ha="left", va="center", fontsize=16, color=INK)
        ax.set_title(rf"$t={t}$   $({30 + 60 * t}^\circ)$", fontsize=18,
                     color=INK, pad=22)
        if t:
            previous = angle - 2 * THETA
            _vector(ax, previous, MUTED, alpha=0.23, linewidth=2.2, zorder=2)
            _angle(ax, previous, angle, 0.45, r"$+60^\circ$",
                   label_radius=0.7, color=MUTED, arrow=True)
        else:
            _angle(ax, 0, THETA, 0.43, r"$30^\circ$", label_radius=0.66)
        ax.plot([0, alpha], [beta, beta], color=ORANGE, lw=1.5,
                linestyle=(0, (3, 3)), zorder=3)
        ax.scatter([0], [beta], color=ORANGE, s=30, zorder=6)
        _vector(ax, angle, BLUE)
        label_x = -0.13 if alpha >= -0.01 else 0.13
        ax.text(label_x, beta, signed_labels[t], color=ORANGE,
                ha="right" if label_x < 0 else "left", va="center", fontsize=18,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5}, zorder=7)
        ax.text(0, -1.52, probabilities[t], color=INK,
                ha="center", va="center", fontsize=19)

    fig.text(0.50, 0.023, r"青：状態の方向    橙：正解の振幅 $\beta$    成功確率：$P_t=\beta^2$",
             ha="center", va="bottom", fontsize=14, color=INK)
    fig.savefig(directory / "09-grover-rotations.png", dpi=180,
                facecolor="white", bbox_inches="tight", pad_inches=0.17)
    plt.close(fig)


def draw_geometry(directory: Path) -> None:
    """Write the two geometry diagrams to *directory*."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({"font.family": _font(), "font.size": 14,
                         "mathtext.fontset": "dejavusans",
                         "axes.unicode_minus": False,
                         "savefig.facecolor": "white"}):
        _reflections(directory)
        _rotations(directory)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "ja" / "figures" / "09")
    args = parser.parse_args()
    draw_geometry(args.output_dir)


if __name__ == "__main__":
    main()
