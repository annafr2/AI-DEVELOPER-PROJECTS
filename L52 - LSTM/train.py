# train.py — training and evaluation loop for the LSTM filter

import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import config
from model import LSTMFilter


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _run_epoch(model, loader, criterion, optimizer, training: bool):
    model.train() if training else model.eval()
    total_loss = 0.0

    ctx = torch.enable_grad() if training else torch.no_grad()
    with ctx:
        for X_batch, y_batch in loader:
            X_batch = X_batch.to(DEVICE)
            y_batch = y_batch.to(DEVICE)

            pred = model(X_batch)
            loss = criterion(pred, y_batch)

            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            total_loss += loss.item() * len(y_batch)

    return total_loss / len(loader.dataset)


def train(model: LSTMFilter, train_loader: DataLoader, test_loader: DataLoader):
    """
    Full training loop.

    Returns
    -------
    history : dict with keys 'train_loss' and 'test_loss' (lists over epochs)
    """
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, patience=5, factor=0.5
    )

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    history = {"train_loss": [], "test_loss": []}
    best_loss = float("inf")

    for epoch in range(1, config.EPOCHS + 1):
        train_loss = _run_epoch(model, train_loader, criterion, optimizer, training=True)
        test_loss = _run_epoch(model, test_loader, criterion, optimizer=None, training=False)

        scheduler.step(test_loss)
        history["train_loss"].append(train_loss)
        history["test_loss"].append(test_loss)

        if test_loss < best_loss:
            best_loss = test_loss
            torch.save(model.state_dict(), config.MODEL_PATH)

        if epoch % 10 == 0 or epoch == 1:
            print(f"Epoch {epoch:3d}/{config.EPOCHS} | "
                  f"train MSE={train_loss:.6f} | test MSE={test_loss:.6f}")

    # Restore best weights
    model.load_state_dict(torch.load(config.MODEL_PATH, map_location=DEVICE))
    print(f"\nBest test MSE: {best_loss:.6f}")
    return history


def evaluate(model: LSTMFilter, test_loader: DataLoader):
    """Return all predictions and targets as numpy arrays."""
    model.eval()
    preds, targets = [], []
    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            pred = model(X_batch.to(DEVICE))
            preds.append(pred.cpu())
            targets.append(y_batch.cpu())

    preds = torch.cat(preds).squeeze().numpy()
    targets = torch.cat(targets).squeeze().numpy()
    return preds, targets
