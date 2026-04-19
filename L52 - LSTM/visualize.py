# visualize.py — all 5 output visualizations for the LSTM signal filter project

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config

os.makedirs(config.OUTPUT_DIR, exist_ok=True)
COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]


# ── 1. Individual signals ────────────────────────────────────────────────────

def plot_individual_signals(t, clean_signals, noisy_signals):
    """4-panel plot: clean vs noisy for each frequency (first 1 second)."""
    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    fig.suptitle("Clean vs Noisy — Individual Sinusoids (first 1 s)", fontsize=14)
    mask = t < 1.0

    for i, (freq, ax) in enumerate(zip(config.FREQUENCIES, axes)):
        ax.plot(t[mask], clean_signals[i][mask], color=COLORS[i], lw=1.5, label="clean")
        ax.plot(t[mask], noisy_signals[i][mask], color=COLORS[i], lw=0.6,
                alpha=0.5, ls="--", label="noisy")
        ax.set_ylabel(f"{freq} Hz", fontsize=10)
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Time (s)")
    plt.tight_layout()
    plt.savefig(f"{config.OUTPUT_DIR}/01_individual_signals.png", dpi=150)
    plt.close()


# ── 2. Mixed signals ─────────────────────────────────────────────────────────

def plot_mixed_signals(t, clean_mixed, noisy_mixed):
    """Clean vs noisy for the combined signal (full 10 s)."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
    fig.suptitle("Mixed Signal — Clean vs Noisy (full 10 s)", fontsize=14)

    axes[0].plot(t, clean_mixed, color="#1f77b4", lw=0.8, label="clean mixed")
    axes[0].set_ylabel("Amplitude")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, noisy_mixed, color="#ff7f0e", lw=0.8, alpha=0.7, label="noisy mixed")
    axes[1].set_ylabel("Amplitude")
    axes[1].set_xlabel("Time (s)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{config.OUTPUT_DIR}/02_mixed_signals.png", dpi=150)
    plt.close()


# ── 3. Frequency spectrum (FFT) ──────────────────────────────────────────────

def plot_spectrum(clean_mixed, noisy_mixed):
    """FFT magnitude of clean and noisy mixed signals."""
    N, fs = config.N_SAMPLES, config.SAMPLE_RATE
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)
    clean_fft = np.abs(np.fft.rfft(clean_mixed)) / N
    noisy_fft = np.abs(np.fft.rfft(noisy_mixed)) / N

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.semilogy(freqs, clean_fft, color="#1f77b4", lw=1.5, label="clean")
    ax.semilogy(freqs, noisy_fft, color="#ff7f0e", lw=0.8, alpha=0.7, label="noisy")
    for f in config.FREQUENCIES:
        ax.axvline(f, color="red", ls=":", lw=0.8, alpha=0.6)
    ax.set_xlim(0, 15)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (log)")
    ax.set_title("Frequency Spectrum — Clean vs Noisy Mixed Signal")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{config.OUTPUT_DIR}/03_spectrum.png", dpi=150)
    plt.close()


# ── 4. Training loss curves ──────────────────────────────────────────────────

def plot_loss_curves(history: dict):
    """Train and test MSE loss over epochs."""
    fig, ax = plt.subplots(figsize=(10, 5))
    epochs = range(1, len(history["train_loss"]) + 1)
    ax.plot(epochs, history["train_loss"], label="Train MSE", color="#1f77b4")
    ax.plot(epochs, history["test_loss"], label="Test MSE", color="#ff7f0e", ls="--")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MSE Loss")
    ax.set_title("LSTM Filter — Training & Test Loss")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{config.OUTPUT_DIR}/04_loss_curves.png", dpi=150)
    plt.close()


# ── 5. Predictions vs ground truth ───────────────────────────────────────────

def plot_predictions(t, clean_signals, preds, targets):
    """Model predictions vs clean target on first 500 test samples."""
    n = min(500, len(preds))
    target_idx = config.FREQUENCIES.index(config.TARGET_FREQ_HZ)
    split = int((config.N_SAMPLES - config.WINDOW_SIZE) * config.TRAIN_RATIO)
    t_test = t[split + config.WINDOW_SIZE: split + config.WINDOW_SIZE + n]

    fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True)
    fig.suptitle(f"LSTM Filter Output — Target: {config.TARGET_FREQ_HZ} Hz", fontsize=14)

    axes[0].plot(t_test, targets[:n], color="#2ca02c", lw=1.5, label="clean target")
    axes[0].plot(t_test, preds[:n], color="#d62728", lw=1.0, ls="--", label="LSTM prediction")
    axes[0].set_ylabel("Amplitude")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    residual = targets[:n] - preds[:n]
    axes[1].plot(t_test, residual, color="#9467bd", lw=0.8)
    axes[1].axhline(0, color="black", lw=0.8, ls="--")
    axes[1].set_ylabel("Residual")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_title("Prediction Error (clean - predicted)")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{config.OUTPUT_DIR}/05_predictions.png", dpi=150)
    plt.close()
