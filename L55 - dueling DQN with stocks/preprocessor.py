"""Feature engineering: raw OHLCV → 10-feature windows, train/val/test split."""
import numpy as np
import pandas as pd
import pandas_ta as ta

import config


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add 8 technical indicators to the OHLCV frame."""
    out = df.copy()

    # 1. Log return
    out["log_return"] = np.log(out["Close"] / out["Close"].shift(1))

    # 2. RSI-14
    out["rsi_14"] = ta.rsi(out["Close"], length=14)

    # 3-5. MACD (12/26/9)
    macd_df = ta.macd(out["Close"], fast=12, slow=26, signal=9)
    out["macd"]        = macd_df.iloc[:, 0]
    out["macd_signal"] = macd_df.iloc[:, 2]
    out["macd_hist"]   = macd_df.iloc[:, 1]

    # 6. Bollinger %B (20-period)
    bb_df = ta.bbands(out["Close"], length=20)
    bb_lower = bb_df.iloc[:, 0]
    bb_upper = bb_df.iloc[:, 2]
    denom = (bb_upper - bb_lower).replace(0, np.nan)
    out["bb_pct"] = (out["Close"] - bb_lower) / denom

    # 7. VWAP distance (daily approximation)
    vwap = (out["Close"] * out["Volume"]).cumsum() / out["Volume"].cumsum()
    out["vwap_dist"] = (out["Close"] - vwap) / vwap

    # 8. Volume (min-max normalised over the entire series)
    v_min, v_max = out["Volume"].min(), out["Volume"].max()
    out["volume_norm"] = (out["Volume"] - v_min) / max(v_max - v_min, 1e-9)

    # 9-10. Agent-state slots (filled at runtime by the environment)
    out["position"]       = 0.0
    out["unrealised_pnl"] = 0.0

    feature_cols = [
        "log_return", "rsi_14", "macd", "macd_signal", "macd_hist",
        "bb_pct", "vwap_dist", "volume_norm", "position", "unrealised_pnl",
    ]
    out = out.dropna()
    return out[feature_cols], out.index


def build_windows(features: pd.DataFrame) -> np.ndarray:
    """Slide a window of WINDOW_SIZE over the feature matrix → (N, W, F)."""
    arr = features.values.astype(np.float32)
    W, F = config.WINDOW_SIZE, config.FEATURES_COUNT
    N = len(arr) - W
    windows = np.stack([arr[i: i + W] for i in range(N)])   # (N, W, F)
    return windows


def split_data(windows: np.ndarray, prices: np.ndarray):
    """Return (train, val, test) tuples of (windows, prices)."""
    n = len(windows)
    n_train = int(n * config.TRAIN_FRAC)
    n_val   = int(n * config.VAL_FRAC)

    slices = {
        "train": (windows[:n_train],             prices[:n_train]),
        "val":   (windows[n_train:n_train+n_val], prices[n_train:n_train+n_val]),
        "test":  (windows[n_train+n_val:],        prices[n_train+n_val:]),
    }
    for k, (w, p) in slices.items():
        print(f"  {k:5s}: {len(w):>5d} windows")
    return slices


def prepare(df: pd.DataFrame):
    """Full pipeline: OHLCV → split dict ready for the trading env."""
    features, idx = engineer_features(df)
    windows = build_windows(features)
    # prices aligned to the *last* bar of each window
    close_prices = df["Close"].reindex(idx).values[config.WINDOW_SIZE:]
    return split_data(windows, close_prices.astype(np.float32))
