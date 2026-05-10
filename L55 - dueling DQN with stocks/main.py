"""Entry point: fetch data, train Dueling DQN, save visuals, launch dashboard."""
import argparse
import os

import config
from data_client import YFinanceDataClient
from preprocessor import prepare
from agent import DQNAgent
from train import train, evaluate_test
import visualize


def parse_args():
    p = argparse.ArgumentParser(description="Dueling DQN Stock Trader — L55")
    p.add_argument("--ticker", default=config.DEFAULT_TICKER,
                   help="Ticker symbol, e.g. SMH, AAPL, NVDA")
    p.add_argument("--start",  default=config.DEFAULT_START,
                   help="Start date YYYY-MM-DD")
    p.add_argument("--end",    default=config.DEFAULT_END,
                   help="End date YYYY-MM-DD")
    p.add_argument("--no-train",   action="store_true",
                   help="Skip training — load saved model and go straight to dashboard")
    p.add_argument("--no-dashboard", action="store_true",
                   help="Train and save visuals, then exit (no GUI)")
    p.add_argument("--episodes", type=int, default=config.N_EPISODES,
                   help="Override number of training episodes")
    return p.parse_args()


def main():
    args = parse_args()
    config.N_EPISODES = args.episodes

    ticker = args.ticker.upper()
    print(f"\n{'='*60}")
    print(f" L55 — Dueling DQN Stock Trader")
    print(f" Ticker: {ticker}  |  {args.start} → {args.end}")
    print(f"{'='*60}\n")

    # ── 1. Fetch & engineer features ──────────────────────────────────────────
    client  = YFinanceDataClient()
    print(f"Fetching {ticker} data from Yahoo Finance…")
    df      = client.fetch(ticker, args.start, args.end)
    print(f"  {len(df)} trading days loaded\n")

    print("Engineering features & building windows…")
    splits  = prepare(df)

    # ── 2. Train (or load) ────────────────────────────────────────────────────
    model_path = os.path.join(config.MODEL_DIR, f"{ticker}_best.pt")

    if args.no_train and os.path.exists(model_path):
        print(f"Loading saved model: {model_path}")
        agent = DQNAgent()
        agent.load(model_path)
        ep_rewards, ep_returns, val_returns = [], [], []
    else:
        agent, ep_rewards, ep_returns, val_returns, model_path = train(splits, ticker)

    # ── 3. Evaluate on test set ───────────────────────────────────────────────
    test_env = evaluate_test(splits, agent)

    # ── 4. Save visualizations ────────────────────────────────────────────────
    print("\nGenerating output PNGs…")
    visualize.plot_candlesticks(df, ticker)
    last_state = splits["test"][0][-1]
    visualize.plot_value_advantage(agent, last_state, ticker)
    if ep_rewards:
        visualize.plot_training_curves(ep_rewards, ep_returns, val_returns, ticker)
    visualize.plot_portfolio(test_env, df["Close"], ticker)
    print(f"All PNGs saved to {config.OUTPUT_DIR}\n")

    # ── 5. Dashboard ──────────────────────────────────────────────────────────
    if not args.no_dashboard:
        print("Launching interactive dashboard…")
        from dashboard import launch
        launch()


if __name__ == "__main__":
    main()
