"""Reproducible figures for the advanced Grover manuscript.

Requires NumPy and Matplotlib. The optional probabilities argument is a
(3, 8) array in the order: initial, after the oracle, after one full iteration.
Basis-state columns are ordered 000, 001, ..., 111 (q2 q1 q0).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Arc, FancyArrowPatch, Patch
import numpy as np


BLUE = "#286a9a"
ORANGE = "#b44425"
INK = "#263445"
GRAY = "#bcc5cc"


def _configure_style() -> bool:
    """Use a Japanese font where available; return whether Japanese is usable."""
    font_path = Path("C:/Windows/Fonts/YuGothM.ttc")
    if font_path.exists():
        font_manager.fontManager.addfont(str(font_path))
        font_name = font_manager.FontProperties(fname=str(font_path)).get_name()
    else:
        available = {font.name for font in font_manager.fontManager.ttflist}
        font_name = next(
            (name for name in ("Noto Sans CJK JP", "IPAexGothic", "Yu Gothic", "Meiryo")
             if name in available),
            "DejaVu Sans",
        )
    plt.rcParams.update({
        "font.family": font_name,
        "font.size": 16,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "mathtext.fontset": "dejavusans",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.unicode_minus": False,
    })
    return font_name != "DejaVu Sans"


def _draw_subspaces(directory: Path, japanese: bool) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 6.3))
    fig.subplots_adjust(left=0.045, right=0.98, top=0.80, bottom=0.26, wspace=0.18)
    fig.suptitle(
        "正解の割合が同じなら、回転角も同じ" if japanese
        else "The same marked fraction gives the same rotation angle",
        fontsize=21, y=0.965,
    )
    fig.text(0.5, 0.878, r"$M/N=1/4 \quad\Rightarrow\quad \theta=30^\circ,\quad 2\theta=60^\circ$",
             ha="center", fontsize=19)

    for ax, n, m, basis in zip(
        axes, (4, 8), (1, 2),
        (r"$|A_1\rangle=|11\rangle$",
         r"$|A_1\rangle=(|011\rangle+|100\rangle)/\sqrt{2}$"),
    ):
        ax.set_xlim(-0.18, 1.34)
        ax.set_ylim(-0.10, 1.31)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{n}候補・正解{m}個" if japanese else f"N = {n}, M = {m}",
                     fontsize=18, pad=7)
        for endpoint in ((1.14, 0), (0, 1.18)):
            ax.add_patch(FancyArrowPatch((0, 0), endpoint,
                                        arrowstyle="->", mutation_scale=15,
                                        color=INK, linewidth=1.2))
        ax.text(1.17, -0.02, r"$|A_0\rangle$", ha="left", va="center", fontsize=17)
        ax.text(0, 1.24, r"$|A_1\rangle$", ha="center", fontsize=17)
        for endpoint, color in (((np.sqrt(3) / 2, 0.5), BLUE), ((0, 1), ORANGE)):
            ax.add_patch(FancyArrowPatch((0, 0), endpoint,
                                        arrowstyle="-|>", mutation_scale=22,
                                        linewidth=3.0, color=color, zorder=4))
        ax.text(0.82, 0.57, "初期" if japanese else "initial",
                ha="center", fontsize=16, color=BLUE)
        ax.text(0.08, 1.04, "1回後" if japanese else "after G",
                color=ORANGE, fontsize=16)
        ax.add_patch(Arc((0, 0), 0.52, 0.52, theta1=0, theta2=30,
                         color=BLUE, linewidth=1.7))
        ax.text(0.31, 0.08, r"$\theta=30^\circ$", color=BLUE, fontsize=15)
        angles = np.linspace(np.pi / 6, np.pi / 2, 100)
        ax.plot(0.76 * np.cos(angles), 0.76 * np.sin(angles),
                color=ORANGE, linewidth=1.9)
        ax.add_patch(FancyArrowPatch(
            (0.76 * np.cos(angles[-5]), 0.76 * np.sin(angles[-5])),
            (0.76 * np.cos(angles[-1]), 0.76 * np.sin(angles[-1])),
            arrowstyle="-|>", mutation_scale=15, linewidth=1.5, color=ORANGE,
        ))
        ax.text(0.36, 0.90, r"$+60^\circ$", color=ORANGE, fontsize=17)
        ax.text(0.5, -0.10, basis, transform=ax.transAxes,
                ha="center", fontsize=15 if m == 2 else 18)
        probability_text = (
            ("合計確率：1　各正解：1" if m == 1 else "合計確率：1　各正解：1/2")
            if japanese else ("Total success: 1 / each: 1" if m == 1 else "Total success: 1 / each: 1/2")
        )
        ax.text(0.5, -0.24, probability_text, transform=ax.transAxes,
                ha="center", fontsize=15)

    fig.text(0.5, 0.045,
             "軸は、それぞれの問題で正規化した不正解・正解の重ね合わせ。"
             if japanese else "Each panel uses its own normalized unmarked and marked superpositions.",
             ha="center", fontsize=14, color=INK)
    fig.savefig(directory / "10-grover-subspaces.png", dpi=180)
    plt.close(fig)


def _draw_probabilities(directory: Path, probabilities: np.ndarray, japanese: bool) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(10.6, 8.4))
    fig.subplots_adjust(left=0.11, right=0.975, top=0.82, bottom=0.10, hspace=0.70)
    fig.suptitle("8候補の確率分布：オラクルと拡散の役割" if japanese
                 else "Eight-candidate probabilities: oracle and diffusion", fontsize=21, y=0.98)
    fig.legend(
        handles=[Patch(facecolor=BLUE, label="不正解" if japanese else "Unmarked"),
                 Patch(facecolor=ORANGE, hatch="//", edgecolor="white",
                       label="正解 011・100" if japanese else "Marked: 011, 100")],
        loc="upper center", bbox_to_anchor=(0.5, 0.93), ncol=2, frameon=False,
        fontsize=16,
    )
    titles = (
        ("初期状態：すべて 1/8", "オラクル直後：すべて 1/8 のまま", "拡散後（1回の反復完了）：正解がそれぞれ 1/2")
        if japanese else
        ("Initial state: all 1/8", "After oracle: all remain 1/8", "After diffusion (one iteration): each solution has probability 1/2")
    )
    for ax, row, title in zip(axes, probabilities, titles):
        bars = ax.bar(np.arange(8), row,
                      color=[ORANGE if i in (3, 4) else BLUE for i in range(8)], width=0.65,
                      zorder=3)
        for i in (3, 4):
            bars[i].set_hatch("//")
            bars[i].set_edgecolor("white")
        ax.set_title(title, loc="left", fontsize=17, pad=12)
        ax.set_xlim(-0.6, 7.6)
        ax.set_ylim(0, 0.55)
        ax.set_xticks(np.arange(8), [f"{i:03b}" for i in range(8)])
        ax.set_yticks([0, 0.125, 0.5], ["0", "1/8", "1/2"])
        ax.tick_params(axis="both", labelsize=16, length=0, pad=7)
        ax.set_ylabel("確率" if japanese else "Prob.", fontsize=16, labelpad=10)
        ax.grid(axis="y", color="#dde2e7", linewidth=0.9, zorder=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRAY)
        for label in ax.get_xticklabels():
            if label.get_text() in ("011", "100"):
                label.set_color(ORANGE)
                label.set_weight("bold")
    fig.text(0.5, 0.025,
             "オラクルは正解の振幅の符号だけを反転する。確率が変わるのは、その後の拡散。"
             if japanese else "The oracle flips marked amplitudes; diffusion then changes probabilities.",
             ha="center", fontsize=14)
    fig.savefig(directory / "10-grover-probabilities.png", dpi=180)
    plt.close(fig)


def draw_figures(directory: Path, probabilities=None) -> None:
    """Save both manuscript figures in directory (create it if necessary).

    Optional input must contain normalized probabilities of shape (3, 8).
    If omitted, use the analytic values for marked strings 011 and 100.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    if probabilities is None:
        probabilities = np.full((3, 8), 1 / 8)
        probabilities[2] = 0
        probabilities[2, [3, 4]] = 0.5
    probabilities = np.asarray(probabilities, dtype=float)
    if probabilities.shape != (3, 8):
        raise ValueError("probabilities must have shape (3, 8)")
    if not np.all(np.isfinite(probabilities)) or np.any(probabilities < -1e-12):
        raise ValueError("probabilities must be finite and nonnegative")
    if not np.allclose(probabilities.sum(axis=1), 1):
        raise ValueError("each probability row must sum to 1")
    expected = np.full((3, 8), 1 / 8)
    expected[2] = 0
    expected[2, [3, 4]] = 0.5
    if not np.allclose(probabilities, expected, atol=1e-10):
        raise ValueError("figure annotations require the N=8, marked={011,100} example")
    japanese = _configure_style()
    _draw_subspaces(directory, japanese)
    _draw_probabilities(directory, probabilities, japanese)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "ja" / "figures" / "10")
    args = parser.parse_args()
    draw_figures(args.output_dir)
