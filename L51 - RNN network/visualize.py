import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
from config import OUTPUTS_DIR, PLOT_BG, ACCENT, COLORS

plt.rcParams.update({
    "text.color": "white", "axes.labelcolor": "white",
    "xtick.color": "white", "ytick.color": "white",
    "axes.edgecolor": "#444444", "axes.spines.top": False, "axes.spines.right": False,
})

LEGEND_STYLE = dict(facecolor="#1a1a2e", labelcolor="white", edgecolor="#444")


def _save(fig, name):
    path = os.path.join(OUTPUTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PLOT_BG)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def _styled_ax(ax):
    ax.set_facecolor("#1a1a2e")
    ax.tick_params(colors="white")
    return ax


def plot_training(history, title, color, filename):
    """3-panel training dashboard: loss, accuracy, perplexity over epochs."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor=PLOT_BG)
    fig.suptitle(title, fontsize=15, color=ACCENT, fontweight="bold", y=1.02)
    epochs = range(1, len(history["train_loss"]) + 1)
    metrics = [("loss", "Loss"), ("acc", "Accuracy"), ("ppl", "Perplexity (lower = better)")]

    for ax, (m, ylabel) in zip(axes, metrics):
        _styled_ax(ax)
        ax.plot(epochs, history[f"train_{m}"], color=color, lw=2.5, label="Train")
        ax.plot(epochs, history[f"val_{m}"], color=color, lw=2.5, ls="--", label="Val", alpha=0.7)
        ax.set_title(ylabel, color="white", fontsize=12)
        ax.set_xlabel("Epoch")
        ax.legend(**LEGEND_STYLE)

    plt.tight_layout()
    return _save(fig, filename)


def plot_comparison(results, filename="experiment_comparison.png"):
    """Short vs Long: perplexity and accuracy curves together."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor=PLOT_BG)
    fig.suptitle("Short vs Long: The Vanishing Gradient Effect",
                 fontsize=15, color=ACCENT, fontweight="bold")
    exp_colors = [COLORS[0], COLORS[2]]

    for ax in axes:
        _styled_ax(ax)

    for i, (name, history) in enumerate(results.items()):
        c = exp_colors[i]
        epochs = range(1, len(history["val_ppl"]) + 1)
        label = f"{name}  (final PPL: {history['val_ppl'][-1]:.1f})"
        axes[0].plot(epochs, history["val_ppl"], color=c, lw=3, label=label)
        axes[1].plot(epochs, history["val_acc"], color=c, lw=3, label=label)

    axes[0].set_title("Validation Perplexity", color="white", fontsize=13)
    axes[0].set_ylabel("Perplexity")
    axes[0].set_xlabel("Epoch")
    axes[0].legend(**LEGEND_STYLE, fontsize=10)
    axes[1].set_title("Validation Accuracy", color="white", fontsize=13)
    axes[1].set_ylabel("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].legend(**LEGEND_STYLE, fontsize=10)
    plt.tight_layout()
    return _save(fig, filename)


def plot_sweep(sweep_results, filename="parameter_sweep.png"):
    """Heatmap grid: hidden_size x seq_len for each layer count. The WOW factor."""
    hs, sl, layers = [64, 128, 256], [5, 10, 20], [1, 2, 3]
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=PLOT_BG)
    fig.suptitle("Parameter Map: What Makes RNN Better?\n(cell value = final validation perplexity, green = smart)",
                 fontsize=13, color=ACCENT, fontweight="bold")

    for i, nl in enumerate(layers):
        matrix = np.array([[
            sweep_results.get(f"h{h}_l{nl}_s{s}", {}).get("final_val_ppl", 999)
            for s in sl] for h in hs], dtype=float)
        _styled_ax(axes[i])
        im = axes[i].imshow(matrix, cmap="RdYlGn_r", aspect="auto", vmin=50, vmax=600)
        axes[i].set_xticks(range(len(sl)))
        axes[i].set_xticklabels([f"seq={s}" for s in sl])
        axes[i].set_yticks(range(len(hs)))
        axes[i].set_yticklabels([f"hidden={h}" for h in hs])
        axes[i].set_title(f"{nl} RNN Layer(s)", color="white", fontsize=13)
        for hi in range(len(hs)):
            for si in range(len(sl)):
                axes[i].text(si, hi, f"{matrix[hi, si]:.0f}",
                             ha="center", va="center", fontsize=11, color="black", fontweight="bold")
        fig.colorbar(im, ax=axes[i], label="Perplexity")

    plt.tight_layout()
    return _save(fig, filename)


def plot_generation(generated, filename="generation_results.png"):
    """Display RNN-generated sentences in a visually appealing layout."""
    fig, ax = plt.subplots(figsize=(16, 10), facecolor=PLOT_BG)
    ax.set_facecolor(PLOT_BG)
    ax.axis("off")
    ax.text(0.5, 0.97, "Experiment 3: What Does the RNN Dream?", ha="center", va="top",
            transform=ax.transAxes, fontsize=18, color=ACCENT, fontweight="bold")
    ax.text(0.5, 0.91, "Seed word  →  RNN generates the next 20 words",
            ha="center", va="top", transform=ax.transAxes, fontsize=12, color="#aaaaaa")

    y = 0.82
    for i, (seed, text) in enumerate(generated.items()):
        c = COLORS[i % len(COLORS)]
        ax.text(0.03, y, f'"{seed}"', transform=ax.transAxes, fontsize=14, color=c, fontweight="bold")
        words = text.split()
        line1 = " ".join(words[:15])
        line2 = " ".join(words[15:]) if len(words) > 15 else ""
        ax.text(0.14, y, line1, transform=ax.transAxes, fontsize=11, color="white", style="italic")
        if line2:
            ax.text(0.14, y - 0.045, line2, transform=ax.transAxes, fontsize=11, color="#cccccc", style="italic")
        y -= 0.12

    return _save(fig, filename)
