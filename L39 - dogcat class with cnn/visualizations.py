"""
visualizations.py
=========================================================
  All plotting and visualization functions.
  Creates 5 PNG files in OUT_DIR:
    01_training_curves.png
    02_timing.png
    03_accuracy_comparison.png
    04_sample_predictions.png
    05_architecture.png
=========================================================
"""

import os
import torch
import matplotlib.pyplot as plt
import numpy as np

from config import EPOCHS, OUT_DIR


# ─────────────────────────────────────────────
#  COLOR PALETTE
# ─────────────────────────────────────────────
COLORS = {
    "cnn_train": "#2196F3",   # blue
    "cnn_test":  "#1976D2",   # dark blue
    "fc_train":  "#FF5722",   # orange
    "fc_test":   "#E64A19",   # dark orange
}

DARK_BG   = "#1a1a2e"
PANEL_BG  = "#16213e"
LEGEND_BG = "#0f3460"


def _dark_fig(fig, axes_list):
    """Apply dark background to figure and axes."""
    fig.patch.set_facecolor(DARK_BG)
    for ax in axes_list:
        ax.set_facecolor(PANEL_BG)
        for spine in ax.spines.values():
            spine.set_edgecolor("#444")


def plot_training_curves(cnn_history, fc_history):
    """Figure 1: Loss & Accuracy curves for both models."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    _dark_fig(fig, axes)
    epochs = range(1, EPOCHS + 1)

    # Loss
    ax = axes[0]
    ax.plot(epochs, cnn_history["train_loss"], color=COLORS["cnn_train"],
            linewidth=2.5, label="CNN Train",  marker="o", markersize=4)
    ax.plot(epochs, cnn_history["test_loss"],  color=COLORS["cnn_test"],
            linewidth=2.5, label="CNN Test",   linestyle="--", marker="s", markersize=4)
    ax.plot(epochs, fc_history["train_loss"],  color=COLORS["fc_train"],
            linewidth=2.5, label="FC Train",   marker="o", markersize=4)
    ax.plot(epochs, fc_history["test_loss"],   color=COLORS["fc_test"],
            linewidth=2.5, label="FC Test",    linestyle="--", marker="s", markersize=4)
    ax.set_title("Training & Test Loss", color="white", fontsize=14, fontweight="bold", pad=10)
    ax.set_xlabel("Epoch", color="#aaa"); ax.set_ylabel("Loss (lower = better)", color="#aaa")
    ax.tick_params(colors="#aaa"); ax.legend(facecolor=LEGEND_BG, labelcolor="white", fontsize=9)
    ax.grid(alpha=0.2, color="#555")

    # Accuracy
    ax = axes[1]
    ax.plot(epochs, [a*100 for a in cnn_history["train_acc"]], color=COLORS["cnn_train"],
            linewidth=2.5, label="CNN Train",  marker="o", markersize=4)
    ax.plot(epochs, [a*100 for a in cnn_history["test_acc"]],  color=COLORS["cnn_test"],
            linewidth=2.5, label="CNN Test",   linestyle="--", marker="s", markersize=4)
    ax.plot(epochs, [a*100 for a in fc_history["train_acc"]],  color=COLORS["fc_train"],
            linewidth=2.5, label="FC Train",   marker="o", markersize=4)
    ax.plot(epochs, [a*100 for a in fc_history["test_acc"]],   color=COLORS["fc_test"],
            linewidth=2.5, label="FC Test",    linestyle="--", marker="s", markersize=4)
    ax.set_title("Training & Test Accuracy", color="white", fontsize=14, fontweight="bold", pad=10)
    ax.set_xlabel("Epoch", color="#aaa"); ax.set_ylabel("Accuracy %  (higher = better)", color="#aaa")
    ax.set_ylim(40, 105); ax.tick_params(colors="#aaa")
    ax.legend(facecolor=LEGEND_BG, labelcolor="white", fontsize=9); ax.grid(alpha=0.2, color="#555")

    plt.suptitle("Dogs vs Cats — CNN vs Fully Connected Network",
                 color="white", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, "01_training_curves.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print(f"   💾 Saved: {path}")
    return path


def plot_timing(cnn_history, fc_history):
    """Figure 2: Epoch time and total training time comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    _dark_fig(fig, axes)
    epochs = range(1, EPOCHS + 1)

    ax = axes[0]
    ax.bar(epochs, cnn_history["epoch_times"], color="#2196F3", alpha=0.8, label="CNN")
    ax.bar(epochs, fc_history["epoch_times"],  color="#FF5722", alpha=0.6, label="FC")
    ax.set_title("Time per Epoch (seconds)", color="white", fontsize=13, fontweight="bold")
    ax.set_xlabel("Epoch", color="#aaa"); ax.set_ylabel("Seconds", color="#aaa")
    ax.tick_params(colors="#aaa"); ax.legend(facecolor=LEGEND_BG, labelcolor="white")
    ax.grid(alpha=0.2, color="#555", axis="y")

    ax = axes[1]
    names = ["CNN", "Fully Connected"]
    times = [cnn_history["total_time"], fc_history["total_time"]]
    bars = ax.bar(names, times, color=["#2196F3", "#FF5722"], width=0.5, alpha=0.85)
    for bar, t in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{t:.1f}s", ha="center", va="bottom", color="white", fontsize=12)
    ax.set_title("Total Training Time", color="white", fontsize=13, fontweight="bold")
    ax.set_ylabel("Seconds", color="#aaa"); ax.tick_params(colors="#aaa")
    ax.grid(alpha=0.2, color="#555", axis="y")

    plt.suptitle("Training Speed Comparison", color="white", fontsize=15, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(OUT_DIR, "02_timing.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print(f"   💾 Saved: {path}")
    return path


def plot_accuracy_comparison(cnn_history, fc_history):
    """Figure 3: Final accuracy bar chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(DARK_BG); ax.set_facecolor(PANEL_BG)
    for spine in ax.spines.values(): spine.set_edgecolor("#444")

    categories = ["Train Acc", "Test Acc"]
    cnn_vals = [max(cnn_history["train_acc"])*100, max(cnn_history["test_acc"])*100]
    fc_vals  = [max(fc_history["train_acc"])*100,  max(fc_history["test_acc"])*100]
    x = np.arange(len(categories)); w = 0.3

    bars1 = ax.bar(x - w/2, cnn_vals, w, label="CNN",            color="#2196F3", alpha=0.9)
    bars2 = ax.bar(x + w/2, fc_vals,  w, label="Fully Connected", color="#FF5722", alpha=0.9)

    for bar in bars1 + bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{bar.get_height():.1f}%", ha="center", va="bottom",
                color="white", fontsize=11, fontweight="bold")

    ax.axhline(50, color="#FFD700", linestyle="--", alpha=0.7, linewidth=1.5, label="Random guess (50%)")
    ax.set_xticks(x); ax.set_xticklabels(categories, color="#aaa", fontsize=12)
    ax.set_ylabel("Accuracy %", color="#aaa", fontsize=12); ax.set_ylim(0, 110)
    ax.set_title("CNN vs Fully Connected — Final Accuracy",
                 color="white", fontsize=15, fontweight="bold", pad=15)
    ax.tick_params(colors="#aaa"); ax.legend(facecolor=LEGEND_BG, labelcolor="white", fontsize=10)
    ax.grid(alpha=0.2, color="#555", axis="y")

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "03_accuracy_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print(f"   💾 Saved: {path}")
    return path


def plot_sample_predictions(train_loader, model_cnn, device):
    """Figure 4: Grid of 16 sample images with CNN predictions."""
    MEAN = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    STD  = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)

    images_batch, labels_batch = next(iter(train_loader))
    model_cnn.eval()
    with torch.no_grad():
        preds_cnn = model_cnn(images_batch.to(device)).argmax(1).cpu()
    class_names = ["Cat 🐱", "Dog 🐶"]

    n = min(16, len(images_batch))
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    fig.patch.set_facecolor(DARK_BG)
    for i in range(n):
        ax = axes[i // 4][i % 4]
        img = (images_batch[i] * STD + MEAN).clamp(0, 1).permute(1, 2, 0).numpy()
        ax.imshow(img)
        true_label = class_names[labels_batch[i].item()]
        pred_label = class_names[preds_cnn[i].item()]
        correct    = labels_batch[i].item() == preds_cnn[i].item()
        ax.set_title(f"True: {true_label}\nPred: {pred_label}",
                     color="lime" if correct else "red",
                     fontsize=8, fontweight="bold")
        ax.axis("off")
    plt.suptitle("Sample Predictions (Green = Correct, Red = Wrong)",
                 color="white", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(OUT_DIR, "04_sample_predictions.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print(f"   💾 Saved: {path}")
    return path


def plot_architecture():
    """Figure 5: Network architecture diagram for CNN and FC."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor(DARK_BG)

    def draw_network(ax, title, layers):
        ax.set_facecolor(PANEL_BG)
        ax.set_title(title, color="white", fontsize=14, fontweight="bold", pad=15)
        ax.axis("off")
        x_positions = np.linspace(0.05, 0.95, len(layers))
        max_height = max(l[1] for l in layers)

        for i, ((name, size, color), x) in enumerate(zip(layers, x_positions)):
            bar_height = 0.1 + 0.7 * (size / max_height)
            rect = plt.Rectangle((x - 0.04, 0.5 - bar_height/2),
                                  0.08, bar_height,
                                  color=color, alpha=0.85, linewidth=1.5,
                                  edgecolor="white", zorder=3)
            ax.add_patch(rect)
            ax.text(x, 0.5 + bar_height/2 + 0.04, name,
                    ha="center", va="bottom", color="white",
                    fontsize=8, fontweight="bold", zorder=4)
            ax.text(x, 0.5 - bar_height/2 - 0.04, str(size),
                    ha="center", va="top", color="#aaa", fontsize=7)
            if i < len(layers) - 1:
                x_next = x_positions[i + 1]
                ax.annotate("", xy=(x_next - 0.04, 0.5), xytext=(x + 0.04, 0.5),
                            arrowprops=dict(arrowstyle="->", color="white", lw=1.5, alpha=0.7))
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    cnn_layers = [
        ("Input\n3×64×64", 12288, "#37474f"),
        ("Conv1\n32 filters", 3200, "#1565C0"),
        ("Conv2\n64 filters", 1600, "#1976D2"),
        ("Conv3\n128 filters", 800,  "#2196F3"),
        ("Flatten\n8192", 8192,  "#0288D1"),
        ("FC 512", 512,   "#039BE5"),
        ("FC 128", 128,   "#26C6DA"),
        ("Output\n2 classes", 2,    "#4CAF50"),
    ]
    fc_layers = [
        ("Input\n3×64×64", 12288, "#37474f"),
        ("Flatten\n12288", 12288, "#BF360C"),
        ("FC 512",  512,  "#D84315"),
        ("FC 256",  256,  "#E64A19"),
        ("FC 128",  128,  "#FF5722"),
        ("FC 64",   64,   "#FF7043"),
        ("Output\n2 classes", 2, "#4CAF50"),
    ]

    draw_network(axes[0], "🧠 CNN Architecture", cnn_layers)
    draw_network(axes[1], "🔗 Fully Connected (FC)", fc_layers)

    plt.suptitle("Network Architecture Comparison", color="white",
                 fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, "05_architecture.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print(f"   💾 Saved: {path}")
    return path


def make_visualizations(cnn_history, fc_history, train_loader, model_cnn, model_fc, device):
    """Create all 5 visualizations and save as PNG files."""
    path1 = plot_training_curves(cnn_history, fc_history)
    path2 = plot_timing(cnn_history, fc_history)
    path3 = plot_accuracy_comparison(cnn_history, fc_history)
    path4 = plot_sample_predictions(train_loader, model_cnn, device)
    path5 = plot_architecture()
    print(f"\n✨ All visualizations saved in '{OUT_DIR}/'")
    return path1, path2, path3, path4, path5
