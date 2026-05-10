# PRD — L55: Dueling DQN Stock Trader

## Overview
An AI agent that learns to trade a single stock or ETF by watching daily price bars.
It uses a **Dueling DQN** neural network — a modern upgrade of the classic DQN —
to decide whether to **hold**, **buy**, or **sell** at each step.

The default asset is **SMH** (VanEck Semiconductor ETF — AI infrastructure basket).

---

## Goals
| # | Goal |
|---|------|
| 1 | Fetch real OHLCV data from Yahoo Finance (no API key needed) |
| 2 | Engineer 8 technical features per bar (RSI, MACD, Bollinger %B, VWAP, …) |
| 3 | Train a Dueling DQN with separate Value and Advantage neural streams |
| 4 | Visualise candlesticks, V/A decomposition, training curves, portfolio vs buy-and-hold |
| 5 | Provide an interactive dashboard where the user types any ticker + date range |

---

## Users
Students following the AI Developer Expert course (lesson 55).
No prior trading knowledge required.

---

## Data Source
- **Library**: `yfinance` (Yahoo Finance, no key)
- **Granularity**: daily bars — Open, High, Low, Close, Volume
- **Cache**: Parquet files in `data/raw/` (snappy compressed)
- **Rate limit**: 10 req/min, 100 req/hour, max 2 concurrent, burst 5/10s

---

## Feature Engineering (preprocessor.py)
| Column | Description |
|--------|-------------|
| `log_return` | log(Close_t / Close_{t-1}) — daily return |
| `rsi_14` | Relative Strength Index, 14-period |
| `macd` | MACD line (12/26 EMA difference) |
| `macd_signal` | 9-period EMA of MACD |
| `macd_hist` | MACD histogram |
| `bb_pct` | Bollinger %B (where price sits in the band) |
| `vwap_dist` | Distance of Close from cumulative VWAP |
| `volume_norm` | Volume scaled 0–1 over the full series |
| `position` | 1 if agent holds shares, 0 otherwise (runtime) |
| `unrealised_pnl` | % gain/loss on open position (runtime) |

Window size: **30 bars**.  
Split: **70% train / 15% val / 15% test**.

---

## Model Architecture — Dueling DQN
```
Input (30 × 10) → Flatten → Linear(300,128) → ReLU → Linear(128,128) → ReLU
                                     ↓
              ┌──────────────────────┴──────────────────────┐
        Value Stream                                 Advantage Stream
     Linear(128,64) → ReLU                       Linear(128,64) → ReLU
     Linear(64, 1)  → V(s)                       Linear(64, 3)  → A(s,a)
              └──────────────────────┬──────────────────────┘
                      Q(s,a) = V(s) + A(s,a) − mean(A)
```
**Why Dueling?** The network learns *how good a state is* (V) independently from *which action is best* (A). This makes learning faster and more stable, especially when many actions have similar value.

---

## Trading Environment (environment.py)
- **Actions**: 0 = hold, 1 = buy (all-in), 2 = sell (all-out)
- **Reward**: realised PnL on sell; 0 on hold/buy
- **Transaction cost**: 0.1 % per trade
- **Starting capital**: $10,000

---

## Training (train.py)
| Hyper-parameter | Value |
|-----------------|-------|
| Episodes | 300 |
| Batch size | 64 |
| Replay buffer | 50,000 |
| Learning rate | 1e-4 |
| Gamma (discount) | 0.99 |
| Epsilon start/end | 1.0 → 0.05 |
| Target net sync | every 200 steps |

Best model saved to `outputs/models/{ticker}_best.pt`.

---

## Outputs
| File | Content |
|------|---------|
| `outputs/{ticker}_candlesticks.png` | Full OHLCV candlestick chart |
| `outputs/{ticker}_value_advantage.png` | V(s) bar + A(s,a) bars for last test state |
| `outputs/{ticker}_training_curves.png` | Episode reward, train return, val return |
| `outputs/{ticker}_portfolio.png` | DQN portfolio vs Buy-and-Hold on test set |

---

## Non-Goals
- Live / paper trading execution
- Multi-asset portfolio management
- Intraday (sub-daily) data
- Hyper-parameter search / AutoML
