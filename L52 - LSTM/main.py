# main.py — orchestrate L52 LSTM Signal Filter

import os
import torch
import numpy as np

import config
import signals
import dataset
import model as model_module
import train as train_module
import visualize


def main():
    torch.manual_seed(config.SEED)
    np.random.seed(config.SEED)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    print(f"Target frequency to filter: {config.TARGET_FREQ_HZ} Hz\n")

    # ── 1. Generate signals ────────────────────────────────────────────────
    print("Generating signals...")
    t, clean_norm, noisy_norm, clean_mixed, noisy_mixed, amps, phases = signals.generate_signals()

    for i, freq in enumerate(config.FREQUENCIES):
        print(f"  {freq} Hz | amp={amps[i]:.3f} | phase={np.degrees(phases[i]):.1f} deg")

    # ── 2. Build dataset ───────────────────────────────────────────────────
    print("\nBuilding sliding-window dataset...")
    X, y = dataset.make_windows(noisy_mixed, clean_norm)
    train_loader, test_loader, splits = dataset.get_dataloaders(X, y)
    X_train, y_train, X_test, y_test = splits
    print(f"  Train samples : {len(y_train):,}")
    print(f"  Test samples  : {len(y_test):,}")

    # ── 3. Visualize signals ───────────────────────────────────────────────
    print("\nSaving signal visualizations...")
    visualize.plot_individual_signals(t, clean_norm, noisy_norm)
    visualize.plot_mixed_signals(t, clean_mixed, noisy_mixed)
    visualize.plot_spectrum(clean_mixed, noisy_mixed)

    # ── 4. Build and train model ───────────────────────────────────────────
    print("\nBuilding LSTM model...")
    model = model_module.build_model()
    n_params = model_module.count_parameters(model)
    print(f"  Trainable parameters: {n_params:,}")

    print(f"\nTraining for {config.EPOCHS} epochs...")
    history = train_module.train(model, train_loader, test_loader)

    # ── 5. Evaluate and visualize results ─────────────────────────────────
    print("\nEvaluating on test set...")
    preds, targets = train_module.evaluate(model, test_loader)
    mse = ((preds - targets) ** 2).mean()
    print(f"  Final test MSE : {mse:.6f}")
    print(f"  Final test RMSE: {mse ** 0.5:.6f}")

    visualize.plot_loss_curves(history)
    visualize.plot_predictions(t, clean_norm, preds, targets)

    print(f"\nAll outputs saved to: {config.OUTPUT_DIR}/")
    print("Done.")


if __name__ == "__main__":
    main()
