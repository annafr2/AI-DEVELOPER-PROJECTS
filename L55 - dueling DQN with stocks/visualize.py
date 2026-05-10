"""Save all output PNGs: candlesticks, V/A streams, training curves, portfolio."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mplfinance as mpf

import config


def _savefig(name: str):
    path = os.path.join(config.OUTPUT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


def plot_candlesticks(df: pd.DataFrame, ticker: str):
    """Candlestick chart of the full OHLCV data."""
    style = mpf.make_mpf_style(base_mpf_style="charles", rc={"font.size": 9})
    fig, axes = mpf.plot(
        df[["Open", "High", "Low", "Close", "Volume"]],
        type="candle", style=style, volume=True,
        title=f"{ticker} — Daily Candlestick",
        figsize=(14, 7), returnfig=True,
    )
    path = os.path.join(config.OUTPUT_DIR, f"{ticker}_candlesticks.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_value_advantage(agent, sample_state: np.ndarray, ticker: str):
    """Bar chart of V(s) and A(s,a) for a sample state."""
    import torch
    t = torch.tensor(sample_state, dtype=torch.float32).unsqueeze(0).to(agent.device)
    with torch.no_grad():
        value, advantage = agent.policy_net.value_advantage(t)

    v = value.item()
    a = advantage.squeeze().cpu().numpy()
    actions = ["Hold", "Buy", "Sell"]
    colors  = ["#4c72b0", "#55a868", "#c44e52"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle(f"{ticker} — Dueling DQN: Value & Advantage Decomposition", fontsize=12)

    axes[0].bar(["V(s)"], [v], color="#dd8452", width=0.4)
    axes[0].set_title("Value Stream  V(s)")
    axes[0].set_ylabel("Score")

    axes[1].bar(actions, a, color=colors)
    axes[1].axhline(0, color="black", linewidth=0.8, linestyle="--")
    axes[1].set_title("Advantage Stream  A(s,a)")
    axes[1].set_ylabel("Advantage")

    _savefig(f"{ticker}_value_advantage.png")


def plot_training_curves(ep_rewards: list, ep_returns: list, val_returns: list, ticker: str):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle(f"{ticker} — Training Curves", fontsize=12)

    axes[0].plot(ep_rewards, color="#4c72b0", linewidth=0.8)
    axes[0].set_title("Episode Reward")
    axes[0].set_xlabel("Episode")

    axes[1].plot(ep_returns, color="#55a868", linewidth=0.8)
    axes[1].axhline(0, color="black", linewidth=0.6, linestyle="--")
    axes[1].set_title("Train Return (%)")
    axes[1].set_xlabel("Episode")

    axes[2].plot(range(10, len(val_returns) * 10 + 1, 10), val_returns, color="#c44e52", linewidth=1.2)
    axes[2].axhline(0, color="black", linewidth=0.6, linestyle="--")
    axes[2].set_title("Val Return (%) every 10 ep")
    axes[2].set_xlabel("Episode")

    plt.tight_layout()
    _savefig(f"{ticker}_training_curves.png")


def plot_portfolio(test_env, df_close: pd.Series, ticker: str):
    """Portfolio value vs buy-and-hold on the test period."""
    pv  = np.array(test_env.portfolio_hist)
    bh  = df_close.values[-len(pv):]
    bh  = config.INITIAL_CAPITAL * bh / bh[0]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(pv, label="DQN Agent",    color="#4c72b0", linewidth=1.5)
    ax.plot(bh, label="Buy & Hold",   color="#dd8452", linewidth=1.5, linestyle="--")
    ax.set_title(f"{ticker} — Test Portfolio vs Buy & Hold")
    ax.set_xlabel("Step")
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    _savefig(f"{ticker}_portfolio.png")
