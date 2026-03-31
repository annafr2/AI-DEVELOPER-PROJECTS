# visualize.py — real-time matplotlib dashboard for the drone RL agent

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from config import GRID_SIZE, SAVE_PATH, FIGURE_TITLE, NUM_EPISODES, START, GOAL
from environment import CELL_BUILDING, CELL_WIND, CELL_START, CELL_GOAL, CELL_PATH, CELL_DRONE

CELL_COLORS = ["#ECEFF1", "#455A64", "#64B5F6", "#66BB6A", "#FFC107", "#CE93D8", "#FF7043"]
CMAP = ListedColormap(CELL_COLORS)

# Action index -> (row_delta, col_delta) for quiver (U=col, V=-row because imshow y is flipped)
_QUIVER_UV = {0: (0, 1), 1: (0, -1), 2: (-1, 0), 3: (1, 0)}  # UP DOWN LEFT RIGHT


class Visualizer:
    def __init__(self):
        os.makedirs(SAVE_PATH, exist_ok=True)
        self.fig = plt.figure(figsize=(18, 9), facecolor="#1a1a2e")
        gs = self.fig.add_gridspec(2, 3, hspace=0.45, wspace=0.4,
                                   left=0.05, right=0.97, top=0.93, bottom=0.07)
        self.ax_grid = self.fig.add_subplot(gs[:, 0])
        self.ax_v = self.fig.add_subplot(gs[0, 1])
        self.ax_reward = self.fig.add_subplot(gs[1, 1])
        self.ax_stats = self.fig.add_subplot(gs[:, 2])

        # Pre-allocate a fixed colorbar axis so it never steals space from ax_v
        divider = make_axes_locatable(self.ax_v)
        self.ax_v_cbar = divider.append_axes("right", size="6%", pad=0.06)

        for ax in [self.ax_grid, self.ax_v, self.ax_reward, self.ax_stats, self.ax_v_cbar]:
            ax.set_facecolor("#16213e")
        self.fig.suptitle(FIGURE_TITLE, color="white", fontsize=15, fontweight="bold")
        plt.ion()

    def _draw_grid(self, env):
        ax = self.ax_grid
        ax.clear()
        mat = env.get_grid_matrix()
        ax.imshow(mat, cmap=CMAP, vmin=0, vmax=6, aspect="equal", interpolation="nearest")
        for x in range(GRID_SIZE + 1):
            ax.axhline(x - 0.5, color="#37474f", lw=0.5)
            ax.axvline(x - 0.5, color="#37474f", lw=0.5)
        if len(env.path) > 1:
            rows = [p[0] for p in env.path]
            cols = [p[1] for p in env.path]
            ax.plot(cols, rows, color="cyan", lw=1.5, alpha=0.7, zorder=3)
        legend_items = [
            mpatches.Patch(color=CELL_COLORS[CELL_BUILDING], label="Building (-20)"),
            mpatches.Patch(color=CELL_COLORS[CELL_WIND], label="Wind (-5)"),
            mpatches.Patch(color=CELL_COLORS[CELL_DRONE], label="Drone"),
            mpatches.Patch(color=CELL_COLORS[CELL_GOAL], label="Goal (+100)"),
            mpatches.Patch(color=CELL_COLORS[CELL_START], label="Start"),
        ]
        ax.legend(handles=legend_items, loc="upper right", fontsize=7,
                  facecolor="#1a1a2e", labelcolor="white", edgecolor="#555")
        ax.set_title("Environment", color="white", fontsize=11)
        ax.tick_params(colors="white", labelsize=8)

    def _draw_v(self, agent, env):
        ax = self.ax_v
        ax.clear()
        self.ax_v_cbar.clear()

        V = agent.get_v_values()
        im = ax.imshow(V, cmap="plasma", aspect="equal", interpolation="nearest",
                       vmin=V.min(), vmax=V.max())

        cb = self.fig.colorbar(im, cax=self.ax_v_cbar)
        cb.ax.tick_params(colors="white", labelsize=7)

        best = agent.get_best_actions()
        X, Y = np.meshgrid(np.arange(GRID_SIZE), np.arange(GRID_SIZE))
        U = np.zeros((GRID_SIZE, GRID_SIZE))
        Vq = np.zeros((GRID_SIZE, GRID_SIZE))
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) not in env.buildings and (r, c) != GOAL:
                    u, v = _QUIVER_UV[best[r, c]]
                    U[r, c] = u
                    Vq[r, c] = v
        ax.quiver(X, Y, U, Vq, color="white", scale=22, width=0.005,
                  headwidth=3, headlength=4, alpha=0.75, zorder=4)

        ax.set_title("V-Values + Best Policy", color="white", fontsize=10)
        ax.tick_params(colors="white", labelsize=8)
    def _draw_reward(self, reward_history):
        ax = self.ax_reward
        ax.clear()
        episodes = np.arange(1, len(reward_history) + 1)
        ax.plot(episodes, reward_history, color="#4fc3f7", lw=0.5, alpha=0.35, label="Raw")
        if len(reward_history) >= 20:
            sm = np.convolve(reward_history, np.ones(20) / 20, mode="valid")
            ax.plot(np.arange(20, len(reward_history) + 1), sm, color="#00e5ff", lw=2.0, label="Avg 20ep")
        ax.set_xlim(1, NUM_EPISODES)
        ax.set_title("Reward per Episode", color="white", fontsize=10)
        ax.tick_params(colors="white", labelsize=8)
        [ax.spines[s].set_visible(False) for s in ["top", "right"]]
        [ax.spines[s].set_color("#444") for s in ["bottom", "left"]]
        ax.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8, edgecolor="#555")

    def _draw_stats(self, stats):
        ax = self.ax_stats
        ax.clear()
        ax.axis("off")
        rows = [
            ("TRAINING", "", "#FFD700"),
            ("Episode", f"{stats['episode']} / {NUM_EPISODES}", "#00E5FF"),
            ("Epsilon (e)", f"{stats['epsilon']:.4f}", "#FF7043"),
            ("Goal Rate (50ep)", f"{stats['goal_rate']:.1%}", "#69F0AE"),
            ("Last Reward", f"{stats['last_reward']:.1f}", "#CE93D8"),
            ("Last Steps", f"{stats['last_steps']}", "#CE93D8"),
            ("Best Reward", f"{stats['best_reward']:.1f}", "#FFC107"),
            ("", "", "white"),
            ("SETTINGS", "", "#FFD700"),
            ("Grid", f"{GRID_SIZE} x {GRID_SIZE}", "white"),
            ("Start", f"{START}", "#66BB6A"),
            ("Goal", f"{GOAL}", "#FFC107"),
            ("", "", "white"),
            ("REWARDS", "", "#FFD700"),
            ("Goal reached", "+100", "#69F0AE"),
            ("Each step", "-1", "#FFF176"),
            ("Wind zone", "-5", "#64B5F6"),
            ("Hit building", "-20", "#FF6B6B"),
        ]
        for i, (label, value, color) in enumerate(rows):
            y = 0.97 - i * 0.054
            if value:
                ax.text(0.03, y, label, color="#AAAAAA", fontsize=9.5, transform=ax.transAxes)
                ax.text(0.62, y, value, color=color, fontsize=9.5,
                        fontweight="bold", transform=ax.transAxes)
            else:
                ax.text(0.03, y, label, color=color, fontsize=10.5,
                        fontweight="bold", transform=ax.transAxes)

    def update(self, env, agent, reward_history, stats):
        self._draw_grid(env)
        self._draw_v(agent, env)
        self._draw_reward(reward_history)
        self._draw_stats(stats)
        self.fig.canvas.draw_idle()
        plt.pause(0.001)

    def save(self, filename="drone_rl_final.png"):
        path = os.path.join(SAVE_PATH, filename)
        self.fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=self.fig.get_facecolor())
        print(f"Saved: {path}")
