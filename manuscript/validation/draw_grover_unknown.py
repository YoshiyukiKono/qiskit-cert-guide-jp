"""Reproducible analytic figures for Grover search with unknown solution count.

Requires NumPy and Matplotlib. No quantum device or sampled data is used.
The fixed example is N=32. Success probabilities follow
sin((2*t+1)*arcsin(sqrt(M/N)))**2 for integer t.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
import numpy as np


BLUE = "#286a9a"
ORANGE = "#b44425"
INK = "#263445"
GRAY = "#bcc5cc"
LIGHT = "#edf1f4"


def _configure_style() -> bool:
    """Use a Japanese font if available; otherwise use English labels."""
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


def probability_rows() -> np.ndarray:
    """Return rows M=1 and M=4, with integer columns t=0,...,5."""
    theta = np.arcsin(np.sqrt(np.array([1, 4], dtype=float) / 32))
    t = np.arange(6)
    return np.sin((2 * t[None, :] + 1) * theta[:, None]) ** 2


def range_schedule(rounds: int = 11) -> tuple[np.ndarray, np.ndarray]:
    """Return m and ceil(m) at each trial, conditional on previous failures.

    Start m=1 and multiply by 5/4 after failure, capped at ceil(sqrt(32))=6.
    The range has size 6 starting with trial 9, before m itself reaches 6.
    """
    if not isinstance(rounds, int) or rounds < 1:
        raise ValueError("rounds must be a positive integer")
    values = []
    m = 1.0
    for _ in range(rounds):
        values.append(m)
        m = min(1.25 * m, 6.0)
    m_values = np.asarray(values)
    return m_values, np.ceil(m_values).astype(int)


def _draw_random_iterations(directory: Path, japanese: bool) -> None:
    rows = probability_rows()
    t = np.arange(6)
    fig, axes = plt.subplots(2, 1, figsize=(10.6, 8.6))
    fig.subplots_adjust(left=0.105, right=0.975, top=0.80, bottom=0.15, hspace=0.54)
    fig.suptitle(
        "反復回数を変えると、成功確率も変わる" if japanese
        else "Success probability depends on the iteration count",
        fontsize=21, y=0.975,
    )
    fig.text(0.5, 0.907,
             r"$N=32,\quad t\in\{0,1,2,3,4,5\},\quad \Pr(t)=1/6$",
             ha="center", fontsize=19)
    fig.text(0.5, 0.856,
             "点は整数回の反復、破線は t を無作為に選んだときの平均成功確率。"
             if japanese else "Dots: integer iteration counts. Dashed line: uniform-random average.",
             ha="center", fontsize=14)

    for ax, m, row, color, marker in zip(axes, (1, 4), rows, (BLUE, ORANGE), ("o", "s")):
        ax.set_title(f"正解 {m} 個（M = {m}）" if japanese else f"M = {m} marked candidate(s)",
                     loc="left", fontsize=18, pad=12)
        mean = float(row.mean())
        ax.axhline(mean, color=INK, linestyle=(0, (5, 4)), linewidth=1.6, zorder=2)
        ax.vlines(t, 0, row, color=color, linewidth=1.5, alpha=0.6, zorder=2)
        ax.scatter(t, row, s=83, color=color, marker=marker, zorder=4)
        ax.scatter([4], [row[4]], s=255, facecolors="none", edgecolors=INK,
                   linewidths=1.5, marker="o", zorder=5)
        for x, y in zip(t, row):
            offset = 0.10 if y < 0.06 else (0.06 if y < 0.91 else -0.105)
            ax.text(x, y + offset, f"{100*y:.2f}%",
                    ha="center", va="center", fontsize=14, color=color)
        ax.text(5.47, mean + 0.047, "平均" if japanese else "Mean",
                ha="left", va="bottom", fontsize=15)
        ax.text(5.47, mean - 0.035, f"{100*mean:.2f}%",
                ha="left", va="top", fontsize=15)
        ax.set_xlim(-0.35, 6.75)
        ax.set_ylim(-0.035, 1.07)
        ax.set_xticks(t, [str(value) for value in t])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
        ax.tick_params(axis="both", labelsize=14, length=0, pad=6)
        ax.set_ylabel("成功確率" if japanese else "Success probability", fontsize=16, labelpad=10)
        ax.grid(axis="y", color="#dde2e7", linewidth=0.9, zorder=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRAY)
        ax.set_xlabel("Grover 反復回数 t" if japanese else "Grover iterations t", fontsize=15, labelpad=5)

    fig.text(0.5, 0.055,
             "丸で囲った t = 4：M = 1 なら約99.92%、M = 4 なら約1.22%。"
             if japanese else "Circled t = 4: about 99.92% for M = 1, but 1.22% for M = 4.",
             ha="center", fontsize=15)
    fig.text(0.5, 0.018,
             "平均は理論値。1回の試行で、6種類の回路をすべて実行するわけではない。"
             if japanese else "These are analytic means; a trial executes one randomly chosen circuit.",
             ha="center", fontsize=13)
    fig.savefig(directory / "11-grover-random-iterations.png", dpi=180)
    plt.close(fig)


def _draw_growing_range(directory: Path, japanese: bool) -> None:
    _, sizes = range_schedule()
    count = len(sizes)
    rows = np.arange(count)
    first_cap = int(np.flatnonzero(sizes == 6)[0])
    fig, ax = plt.subplots(figsize=(10.6, 9.1))
    fig.subplots_adjust(left=0.25, right=0.98, top=0.675, bottom=0.19)
    fig.suptitle("失敗したら、反復回数を選ぶ範囲を広げる" if japanese
                 else "After failure, widen the range of iteration counts", fontsize=21, y=0.976)
    fig.text(0.5, 0.914,
             r"$N=32,\quad m=1,\quad \lambda=5/4,\quad L=\lceil m\rceil,\quad L_{\max}=6$",
             ha="center", fontsize=18)
    fig.text(0.5, 0.864,
             r"$m\leftarrow\min(\lambda m,6),\qquad t\in\{0,\ldots,L-1\}$",
             ha="center", fontsize=18)
    legend = [
        Line2D([0], [0], marker="o", markersize=8, linestyle="none", color=BLUE,
               label="各点から等確率 1/L で選ぶ" if japanese else "Each filled dot is chosen with probability 1/L"),
        Line2D([0], [0], marker="o", markersize=8, linestyle="none", color=GRAY,
               markerfacecolor="white", label="範囲の外" if japanese else "Outside the range"),
    ]
    fig.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, 0.827),
               ncol=2, frameon=False, fontsize=14)
    ax.axhspan(first_cap - 0.48, count - 0.5, facecolor=LIGHT, zorder=0)
    for index, size in enumerate(sizes):
        ax.scatter(np.arange(6), np.full(6, index), facecolors="white", edgecolors=GRAY,
                   s=75, linewidths=1.3, zorder=2)
        ax.scatter(np.arange(size), np.full(size, index), color=BLUE, s=80, zorder=3)
        if index >= first_cap:
            label = f"上限で {index-first_cap+1} 回目" if japanese else f"At cap: trial {index-first_cap+1}"
            ax.text(5.45, index, label, va="center", fontsize=13)
    ax.set_xlim(-0.5, 7.0)
    ax.set_ylim(count - 0.45, -0.62)
    ax.set_xticks(np.arange(6), [str(value) for value in range(6)])
    ax.set_yticks(rows, [
        (f"第 {index+1:>2} 試行   L = {size}" if japanese else f"Trial {index+1:>2}   L = {size}")
        for index, size in enumerate(sizes)
    ])
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set_xlabel("選ぶ Grover 反復回数 t" if japanese else "Possible Grover iteration count t",
                  fontsize=16, labelpad=13)
    ax.tick_params(axis="both", labelsize=14, length=0, pad=10)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    for row in rows:
        ax.hlines(row + 0.5, -0.48, 6.95, color="#e3e7eb", linewidth=0.65, zorder=1)
    fig.text(0.5, 0.136,
             "…　上限の範囲で最大 K 回試す。範囲が同じでも、t は毎回選び直す。"
             if japanese else "... Try at most K times at the capped range, choosing t afresh each time.",
             ha="center", fontsize=15)
    fig.text(0.5, 0.080,
             "失敗が続いた場合の予定。成功時は途中で停止。"
             if japanese else "Schedule conditional on continuing failure. Stop immediately upon success.",
             ha="center", fontsize=15)
    fig.text(0.5, 0.038,
             "各試行で古典候補を確認し、未発見なら選んだ回路を1回測定して検証する。"
             if japanese else "Check a classical candidate first; if unsuccessful, measure one chosen circuit and verify.",
             ha="center", fontsize=13)
    fig.savefig(directory / "11-grover-growing-range.png", dpi=180)
    plt.close(fig)


def draw_figures(output_dir: Path) -> None:
    """Save both analytic manuscript figures to output_dir."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    japanese = _configure_style()
    _draw_random_iterations(output_dir, japanese)
    _draw_growing_range(output_dir, japanese)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "ja" / "figures" / "11")
    args = parser.parse_args()
    draw_figures(args.output_dir)
