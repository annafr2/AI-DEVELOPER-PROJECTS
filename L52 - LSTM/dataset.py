# dataset.py — sliding-window dataset for LSTM signal filtering

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import config


class SignalDataset(Dataset):
    """
    Each sample:
      X : context window of WINDOW_SIZE noisy mixed samples  → shape (WINDOW_SIZE, 1)
      y : next clean value of the target frequency            → shape (1,)
    """

    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)  # (N, W, 1)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(-1)  # (N, 1)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def make_windows(noisy_mixed: np.ndarray, clean_signals: np.ndarray):
    """
    Build sliding-window dataset.

    Parameters
    ----------
    noisy_mixed   : shape (N,) — input signal (noisy sum)
    clean_signals : shape (4, N) — individual clean sinusoids

    Returns
    -------
    X : shape (M, WINDOW_SIZE) — each row is a context window from noisy_mixed
    y : shape (M,)            — clean value of TARGET_FREQ at position (start + WINDOW_SIZE)
    """
    W = config.WINDOW_SIZE
    N = len(noisy_mixed)

    # Find index of target frequency
    target_idx = config.FREQUENCIES.index(config.TARGET_FREQ_HZ)
    target_clean = clean_signals[target_idx]  # shape (N,)

    num_windows = N - W
    X = np.zeros((num_windows, W), dtype=np.float32)
    y = np.zeros(num_windows, dtype=np.float32)

    for i in range(num_windows):
        X[i] = noisy_mixed[i: i + W]
        y[i] = target_clean[i + W]  # predict next clean value

    return X, y


def get_dataloaders(X: np.ndarray, y: np.ndarray):
    """
    Split into train/test and return DataLoaders.

    Returns
    -------
    train_loader, test_loader, (X_train, y_train, X_test, y_test)
    """
    split = int(len(y) * config.TRAIN_RATIO)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    train_ds = SignalDataset(X_train, y_train)
    test_ds = SignalDataset(X_test, y_test)

    train_loader = DataLoader(train_ds, batch_size=config.BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=config.BATCH_SIZE, shuffle=False)

    return train_loader, test_loader, (X_train, y_train, X_test, y_test)
