"""
visualize.py - All visualizations for the HCP card classifier.
Course: AI Developer Expert | Lesson 42

Outputs (saved to outputs/):
  - training_history.png      : accuracy & loss curves (both phases)
  - confusion_matrix.png      : 5×5 heatmap
  - sample_predictions.png    : 10 random test-set predictions
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from config import (HCP_CLASSES, CLASS_COLORS,
                    HISTORY_PLOT, CONFUSION_MATRIX_PLOT, SAMPLE_PREDICTIONS_PLOT)

os.makedirs("outputs", exist_ok=True)
LABELS = list(HCP_CLASSES.values())

# ── Training history ──────────────────────────────────────────────────────────

def plot_training_history(h1, h2=None):
    """Combine Phase-1 and Phase-2 histories and plot accuracy + loss."""
    acc  = h1.history["accuracy"]   + (h2.history["accuracy"]    if h2 else [])
    vacc = h1.history["val_accuracy"]+(h2.history["val_accuracy"] if h2 else [])
    loss = h1.history["loss"]       + (h2.history["loss"]         if h2 else [])
    vloss= h1.history["val_loss"]   + (h2.history["val_loss"]     if h2 else [])
    ep   = range(1, len(acc) + 1)
    split= len(h1.history["accuracy"])   # epoch where Phase 2 starts

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("ResNet-50 HCP Classifier — Training History",
                 fontsize=15, fontweight="bold", y=1.02)

    for ax, (train_m, val_m), title in [
        (ax1, (acc,  vacc),  "Accuracy"),
        (ax2, (loss, vloss), "Loss"),
    ]:
        ax.plot(ep, train_m, color="#4472C4", lw=2.5, label="Train")
        ax.plot(ep, val_m,   color="#ED7D31", lw=2.5, label="Validation")
        if h2:
            ax.axvline(split, color="#70AD47", lw=1.5,
                       linestyle="--", label="Fine-tune start")
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_xlabel("Epoch"); ax.legend(fontsize=11); ax.grid(alpha=0.3)
        ax.spines[["top","right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(HISTORY_PLOT, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {HISTORY_PLOT}")


# ── Confusion matrix ──────────────────────────────────────────────────────────

def plot_confusion_matrix(y_true, y_pred):
    """Styled 5×5 confusion-matrix heatmap."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=LABELS, yticklabels=LABELS,
                linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8},
                annot_kws={"size": 12})
    ax.set_title("Confusion Matrix — HCP Card Classification",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Predicted HCP Class", fontsize=11)
    ax.set_ylabel("True HCP Class",      fontsize=11)
    plt.xticks(rotation=25, ha="right"); plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PLOT, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {CONFUSION_MATRIX_PLOT}")


# ── Sample predictions ────────────────────────────────────────────────────────

def plot_sample_predictions(model, X_test, y_true, n=10):
    """Grid of n random test images with true vs predicted HCP labels."""
    idxs  = np.random.choice(len(X_test), n, replace=False)
    preds = np.argmax(model.predict(X_test[idxs], verbose=0), axis=1)
    cols  = 5
    rows  = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, 6 * rows))
    fig.suptitle("Sample Predictions — HCP Card Classification",
                 fontsize=15, fontweight="bold", y=1.01)

    for ax, idx, pred in zip(axes.flat, idxs, preds):
        true = int(y_true[idx])
        ok   = pred == true
        ax.imshow(X_test[idx])
        ax.set_title(
            f"True:  {LABELS[true]}\nPred:  {LABELS[pred]}",
            color="green" if ok else "red", fontsize=9, fontweight="bold"
        )
        for spine in ax.spines.values():
            spine.set_edgecolor("green" if ok else "red")
            spine.set_linewidth(3)
        ax.set_xticks([]); ax.set_yticks([])

    for ax in axes.flat[n:]:      # hide unused sub-plots
        ax.set_visible(False)

    plt.tight_layout()
    plt.savefig(SAMPLE_PREDICTIONS_PLOT, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {SAMPLE_PREDICTIONS_PLOT}")


# ── Classification report ─────────────────────────────────────────────────────

def print_report(y_true, y_pred):
    print("\n" + "=" * 55)
    print("  PER-CLASS CLASSIFICATION REPORT")
    print("=" * 55)
    print(classification_report(y_true, y_pred, target_names=LABELS))
