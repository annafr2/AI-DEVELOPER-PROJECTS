# visualize.py — competition dashboard: Q-Learning vs Bellman (Value Iteration)

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from config import GRID_SIZE, SAVE_PATH, FIGURE_TITLE, NUM_EPISODES, GOAL
import environment  # noqa: F401  (constants not used directly but kept for clarity)

# Colors indexed by cell-type code (0=free … 10=dyn_wind)
CELL_COLORS = ["#ECEFF1","#455A64","#64B5F6","#66BB6A","#FFC107",
               "#CE93D8","#FF7043","#B71C1C","#00E676","#78909C","#29B6F6"]
CMAP = ListedColormap(CELL_COLORS)
_QUIVER_UV = {0: (0, 1), 1: (0, -1), 2: (-1, 0), 3: (1, 0)}


class Visualizer:
    def __init__(self):
        os.makedirs(SAVE_PATH, exist_ok=True)
        self.fig = plt.figure(figsize=(22, 10), facecolor="#1a1a2e")
        gs = self.fig.add_gridspec(2, 4, hspace=0.45, wspace=0.38,
                                   left=0.04, right=0.98, top=0.92, bottom=0.07)
        self.ax_gq     = self.fig.add_subplot(gs[:, 0])   # Q-Learning grid
        self.ax_gb     = self.fig.add_subplot(gs[:, 1])   # Bellman grid
        self.ax_reward = self.fig.add_subplot(gs[0, 2])   # reward curves
        self.ax_bar    = self.fig.add_subplot(gs[1, 2])   # cumulative score bars
        self.ax_stats  = self.fig.add_subplot(gs[:, 3])   # text stats

        divider = make_axes_locatable(self.ax_gq)
        self.ax_cbar = divider.append_axes("right", size="5%", pad=0.05)

        for ax in [self.ax_gq, self.ax_gb, self.ax_reward,
                   self.ax_bar, self.ax_stats, self.ax_cbar]:
            ax.set_facecolor("#16213e")
        self.fig.suptitle(FIGURE_TITLE, color="white", fontsize=15, fontweight="bold")
        plt.ion()

    def _draw_grid(self, ax, env, agent, title):
        ax.clear()
        mat = env.get_grid_matrix()
        im = ax.imshow(mat, cmap=CMAP, vmin=0, vmax=10, aspect="equal",
                       interpolation="nearest")
        for x in range(GRID_SIZE + 1):
            ax.axhline(x - 0.5, color="#37474f", lw=0.4)
            ax.axvline(x - 0.5, color="#37474f", lw=0.4)
        if len(env.path) > 1:
            rows_p = [p[0] for p in env.path]
            cols_p = [p[1] for p in env.path]
            ax.plot(cols_p, rows_p, color="cyan", lw=1.5, alpha=0.7, zorder=3)
        # Policy arrows
        best = agent.get_best_actions()
        X, Y = np.meshgrid(np.arange(GRID_SIZE), np.arange(GRID_SIZE))
        U, Vq = np.zeros((GRID_SIZE, GRID_SIZE)), np.zeros((GRID_SIZE, GRID_SIZE))
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) not in env.buildings and (r, c) != GOAL:
                    U[r, c], Vq[r, c] = _QUIVER_UV[best[r, c]]
        ax.quiver(X, Y, U, Vq, color="white", scale=22, width=0.005,
                  headwidth=3, headlength=4, alpha=0.7, zorder=4)
        ax.set_title(title, color="white", fontsize=10, fontweight="bold")
        ax.tick_params(colors="white", labelsize=7)
        return im

    def _draw_rewards(self, rewards_q, rewards_b):
        ax = self.ax_reward
        ax.clear()
        eps = np.arange(1, len(rewards_q) + 1)
        ax.plot(eps, rewards_q, color="#00E5FF", lw=0.4, alpha=0.25)
        ax.plot(eps, rewards_b, color="#FF9800", lw=0.4, alpha=0.25)
        if len(rewards_q) >= 20:
            sm_q = np.convolve(rewards_q, np.ones(20) / 20, mode="valid")
            sm_b = np.convolve(rewards_b, np.ones(20) / 20, mode="valid")
            x = np.arange(20, len(rewards_q) + 1)
            ax.plot(x, sm_q, color="#00E5FF", lw=2, label="Q-Learning")
            ax.plot(x, sm_b, color="#FF9800", lw=2, label="Bellman (VI)")
        ax.set_xlim(1, NUM_EPISODES)
        ax.set_title("Reward per Episode", color="white", fontsize=10)
        ax.tick_params(colors="white", labelsize=8)
        [ax.spines[s].set_visible(False) for s in ["top", "right"]]
        [ax.spines[s].set_color("#444") for s in ["bottom", "left"]]
        ax.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8, edgecolor="#555")

    def _draw_bar(self, stats):
        ax = self.ax_bar
        ax.clear()
        vals   = [max(0, stats["cum_q"]), max(0, stats["cum_b"])]
        colors = ["#00E5FF", "#FF9800"]
        bars   = ax.bar(["Q-Learning", "Bellman (VI)"], vals, color=colors, width=0.4)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(vals + [1]) * 0.01,
                    f"{v:.0f}", ha="center", color="white", fontsize=9, fontweight="bold")
        ax.set_title("Cumulative Score", color="white", fontsize=10)
        ax.tick_params(colors="white", labelsize=8)
        [ax.spines[s].set_visible(False) for s in ["top", "right"]]
        [ax.spines[s].set_color("#444") for s in ["bottom", "left"]]

    def _draw_stats(self, stats):
        ax = self.ax_stats
        ax.clear()
        ax.axis("off")
        # (label, value, color)  — empty label = section header
        rows = [
            ("RACE STATUS", "", "#FFD700"),
            ("Episode", f"{stats['episode']} / {NUM_EPISODES}", "#00E5FF"),
            ("Active Events", f"{stats['n_events']}", "#FF6B6B"),
            ("", "", "white"),
            ("Q-LEARNING", "", "#00E5FF"),
            ("Goal Rate", f"{stats['rate_q']:.1%}", "#69F0AE"),
            ("Best Reward", f"{stats['best_q']:.0f}", "#CE93D8"),
            ("Epsilon", f"{stats['epsilon']:.4f}", "#FFF176"),
            ("", "", "white"),
            ("BELLMAN (VI)", "", "#FF9800"),
            ("Goal Rate", f"{stats['rate_b']:.1%}", "#69F0AE"),
            ("Best Reward", f"{stats['best_b']:.0f}", "#CE93D8"),
            ("", "", "white"),
            ("REWARDS", "", "#FFD700"),
            ("Goal / Bridge / Step", "+100 / +15 / -1", "#69F0AE"),
            ("Wind / Building / Pit", "-5 / -20 / -30", "#FF6B6B"),
        ]
        for i, (label, value, color) in enumerate(rows):
            y = 0.98 - i * 0.058
            if value:
                ax.text(0.03, y, label, color="#AAAAAA", fontsize=9, transform=ax.transAxes)
                ax.text(0.62, y, value, color=color, fontsize=9,
                        fontweight="bold", transform=ax.transAxes)
            else:
                ax.text(0.03, y, label, color=color, fontsize=10,
                        fontweight="bold", transform=ax.transAxes)

    def update(self, env_q, env_b, agent_q, agent_b, rewards_q, rewards_b, stats):
        im = self._draw_grid(self.ax_gq, env_q, agent_q, "Q-Learning Drone (blue)")
        self._draw_grid(self.ax_gb, env_b, agent_b, "Bellman (VI) Drone (orange)")
        self.ax_cbar.clear()
        cb = self.fig.colorbar(im, cax=self.ax_cbar)
        cb.ax.tick_params(colors="white", labelsize=6)
        self._draw_rewards(rewards_q, rewards_b)
        self._draw_bar(stats)
        self._draw_stats(stats)
        self.fig.canvas.draw_idle()
        plt.pause(0.001)

    def save(self, filename="race_final.png"):
        path = os.path.join(SAVE_PATH, filename)
        self.fig.savefig(path, dpi=150, bbox_inches="tight",
                         facecolor=self.fig.get_facecolor())
        print(f"Saved: {path}")
