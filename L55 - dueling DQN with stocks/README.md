# L55 — Dueling DQN Stock Trader

An AI agent that learns to trade **SMH** (or any stock/ETF) by reading daily candlestick data.
It uses a **Dueling Deep Q-Network (DQN)** — the same kind of AI that learned to play Atari games — but trained to decide: **hold**, **buy**, or **sell**.

---

## What is a Dueling DQN?

A regular DQN just asks: *"How much reward do I get if I take action A right now?"*

A **Dueling DQN** splits that question into two separate answers:

| Stream | Question it answers |
|--------|---------------------|
| **Value V(s)** | *"How good is my current situation, no matter what I do?"* |
| **Advantage A(s,a)** | *"How much better is action A compared to the average action?"* |

Then it combines them: **Q(s,a) = V(s) + A(s,a) − mean(A)**

This is smarter because, on many trading days, *all* actions are equally bad (flat market).  
Separating V from A helps the AI learn faster and more stably.

---

## What does the agent see?

Every step the agent looks at the **last 30 trading days** through 10 numbers per day:

| Feature | Meaning |
|---------|---------|
| `log_return` | How much did the price change today? |
| `rsi_14` | Is the stock overbought or oversold? (0–100 scale) |
| `macd` + `macd_signal` + `macd_hist` | Momentum indicators |
| `bb_pct` | Where is today's price inside the Bollinger Band? |
| `vwap_dist` | Is price above or below its average weighted by volume? |
| `volume_norm` | How busy was trading today, compared to history? |
| `position` | Does the agent currently hold shares? |
| `unrealised_pnl` | If holding, how much profit/loss so far? |

---

## What does it learn to do?

The agent starts with **$10,000** and can make one decision per day:

- **Hold** — do nothing
- **Buy** — spend all cash to buy shares
- **Sell** — sell all shares for cash

A small **0.1% transaction cost** discourages excessive trading.  
The agent is rewarded only when it sells for a profit.

---

## Data source

Data comes from **Yahoo Finance** (free, no API key needed) via the `yfinance` library.
The project downloads daily Open/High/Low/Close/Volume bars and caches them locally
as fast Parquet files so you don't re-download on every run.

A **Gatekeeper** limits requests to 10/minute and 100/hour to be respectful of Yahoo's servers.

---

## Results — SMH (AI Infrastructure ETF)

### Candlestick Chart
> Daily price bars for SMH. Green = price went up that day. Red = went down.

*(Run the project to generate `outputs/SMH_candlesticks.png`)*

![Candlesticks](outputs/SMH_candlesticks.png)

---

### Value and Advantage Decomposition
> The Dueling DQN's two streams visualised for the last state in the test period.
> Left bar = how good the state is overall. Right bars = which action adds the most value.

![Value Advantage](outputs/SMH_value_advantage.png)

---

### Training Curves
> Left: total reward per episode. Middle: % return per episode on training data.
> Right: % return every 10 episodes on the validation set (unseen during training).

![Training Curves](outputs/SMH_training_curves.png)

---

### Portfolio vs Buy-and-Hold
> The blue line is the agent's portfolio value on the test set (data it never trained on).
> The orange dashed line is what you would have earned just buying and holding SMH.

![Portfolio](outputs/SMH_portfolio.png)

---

## Interactive Dashboard

When you run `python main.py`, an interactive window opens:

- Type any **ticker** (e.g. `NVDA`, `AAPL`, `QQQ`, `SMH`)
- Set a **start** and **end** date
- Click **Run** — the dashboard fetches data, loads the trained model, and draws all panels live

---

## File Structure

```
L55 - dueling DQN with stocks/
├── config.py          All settings (ticker, dates, network size, training params)
├── data_client.py     Download data from Yahoo Finance + local cache
├── preprocessor.py    Compute technical indicators, build 30-bar windows
├── environment.py     Trading simulation (buy/sell/hold + reward)
├── model.py           Dueling DQN neural network (PyTorch)
├── agent.py           Replay buffer, epsilon-greedy policy, learn step
├── train.py           Training loop — 300 episodes, save best model
├── visualize.py       Save PNG charts to outputs/
├── dashboard.py       Interactive matplotlib GUI
├── main.py            Run everything from the command line
├── requirements.txt   Python packages needed
└── outputs/           Auto-created folder for PNG results and saved models
```

---

## How to Run — Step by Step

### Step 1 — Install packages (once)

```bash
cd "L55 - dueling DQN with stocks"
pip install -r requirements.txt
```

### Step 2 — Full run (fetch data + train + dashboard)

```bash
python main.py
```

This will:
1. Download SMH daily data from Yahoo Finance (2020–2024)
2. Compute technical indicators and build windows
3. Train the Dueling DQN for 300 episodes (~5–15 minutes on CPU)
4. Save 4 PNG charts to `outputs/`
5. Open the interactive dashboard

### Step 3 — Try a different ticker

```bash
python main.py --ticker NVDA --start 2021-01-01 --end 2024-12-31
```

### Step 4 — Quick test (50 episodes, no window)

```bash
python main.py --episodes 50 --no-dashboard
```

### Step 5 — Skip training, just open the dashboard

```bash
python main.py --no-train
```
*(Requires a saved model in `outputs/models/SMH_best.pt`)*

### All options

| Flag | Default | Meaning |
|------|---------|---------|
| `--ticker` | `SMH` | Stock or ETF symbol |
| `--start` | `2020-01-01` | Start date |
| `--end` | `2024-12-31` | End date |
| `--episodes` | `300` | How many training episodes |
| `--no-train` | off | Skip training, load saved model |
| `--no-dashboard` | off | Train and save PNGs, then exit |

---

## What is SMH?

**SMH** is the VanEck Semiconductor ETF — a basket of the world's biggest chip companies
(NVIDIA, TSMC, Broadcom, ASML…). Because AI runs on chips, SMH is often called the
**AI infrastructure ETF**. It is highly volatile and technically interesting for RL experiments.
