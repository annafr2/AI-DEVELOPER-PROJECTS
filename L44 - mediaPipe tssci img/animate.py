"""
animate.py — Create an animated flyer GIF showing:
  Left  : stick-figure skeleton (updates each frame)
  Right : TSSCI image built row-by-row (time axis fills in)
  Bottom: joint X-coordinate graph with moving cursor
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation, PillowWriter
from config import (
    ANIMATED_FLYER_GIF, CONNECTIONS, NUM_FRAMES,
)

BG = "#0d0d1a"
DOT_C = "#00FF80"
LINE_C = "#FFD700"
GRAPH_C = "#00BFFF"
CURSOR_C = "#FF4500"


def _draw_skeleton(ax, lm: np.ndarray) -> None:
    """Render stick figure on a matplotlib axis (dark background)."""
    ax.clear()
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 0)   # image coordinates: y=0 at top
    ax.set_aspect("equal")
    ax.axis("off")
    for a, b in CONNECTIONS:
        if lm[a, 2] > 0.3 and lm[b, 2] > 0.3:
            ax.plot([lm[a, 0], lm[b, 0]], [lm[a, 1], lm[b, 1]],
                    color=LINE_C, lw=2, zorder=1)
    mask = lm[:, 2] > 0.3
    ax.scatter(lm[mask, 0], lm[mask, 1], c=DOT_C, s=28, zorder=2)
    ax.set_title("Skeleton", color="white", fontsize=8, pad=3)


def create_animated_flyer(skeleton_data: list, tssci: np.ndarray) -> None:
    """Render and save the animated flyer as a GIF."""
    # Sample the same 49 frames used for TSSCI
    total = len(skeleton_data)
    indices = np.linspace(0, total - 1, NUM_FRAMES, dtype=int)
    sampled = [skeleton_data[i] for i in indices]

    # Joint 11 (left shoulder) X across time — used in bottom graph
    shoulder_x = np.array([f["landmarks"][11, 0] for f in sampled])
    time_ax = np.arange(NUM_FRAMES)

    # --- Figure layout ---
    fig = plt.figure(figsize=(10, 5), facecolor=BG)
    gs = gridspec.GridSpec(
        2, 2, figure=fig, hspace=0.45, wspace=0.3, height_ratios=[3, 1]
    )
    ax_skel  = fig.add_subplot(gs[0, 0])
    ax_tssci = fig.add_subplot(gs[0, 1])
    ax_graph = fig.add_subplot(gs[1, :])

    for ax in (ax_tssci, ax_graph):
        ax.set_facecolor(BG)
        for sp in ax.spines.values():
            sp.set_color("#334466")

    # TSSCI panel
    tssci_im = ax_tssci.imshow(
        np.zeros((NUM_FRAMES, NUM_FRAMES, 3)),
        aspect="auto", interpolation="nearest",
    )
    ax_tssci.set_title("TSSCI Building", color="white", fontsize=8, pad=3)
    ax_tssci.set_xlabel("Keypoint (DFS)", color="#8888aa", fontsize=7)
    ax_tssci.set_ylabel("Frame (time)", color="#8888aa", fontsize=7)
    ax_tssci.tick_params(colors="#8888aa", labelsize=6)

    # Graph panel
    y_lo = max(0.0, shoulder_x.min() - 0.05)
    y_hi = min(1.0, shoulder_x.max() + 0.05)
    ax_graph.set_xlim(0, NUM_FRAMES - 1)
    ax_graph.set_ylim(y_lo, y_hi)
    ax_graph.set_title("Left Shoulder X  (landmark 11)", color="white", fontsize=8, pad=3)
    ax_graph.set_xlabel("Frame", color="#8888aa", fontsize=7)
    ax_graph.tick_params(colors="#8888aa", labelsize=6)
    # Ghost trace (full curve, dim)
    ax_graph.plot(time_ax, shoulder_x, color="#334466", lw=1)
    graph_line, = ax_graph.plot([], [], color=GRAPH_C, lw=2)
    cursor,     = ax_graph.plot([], [], "o", color=CURSOR_C, ms=6)

    fig.suptitle("MediaPipe  |  TSSCI Image Generator  |  L44",
                 color="white", fontsize=11, y=1.01)

    def update(fi: int):
        lm = sampled[fi]["landmarks"]
        _draw_skeleton(ax_skel, lm)

        # Build TSSCI row-by-row
        partial = np.zeros_like(tssci)
        partial[:fi + 1] = tssci[:fi + 1]
        tssci_im.set_data(partial)

        graph_line.set_data(time_ax[:fi + 1], shoulder_x[:fi + 1])
        cursor.set_data([fi], [shoulder_x[fi]])
        return tssci_im, graph_line, cursor

    ani = FuncAnimation(fig, update, frames=NUM_FRAMES, interval=120, blit=False)
    writer = PillowWriter(fps=8)
    ani.save(ANIMATED_FLYER_GIF, writer=writer, dpi=90)
    plt.close()
    print(f"Animated flyer saved: {ANIMATED_FLYER_GIF}")
