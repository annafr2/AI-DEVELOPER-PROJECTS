# CLAUDE.md — L55 Dueling DQN Stock Trader

## Project rules
- All code, prints, and comments in **English**
- Each Python file must stay under **150 lines**
- Output images go to `outputs/` as `.png`
- No emojis in code or docs

## File map
| File | Role |
|------|------|
| `config.py` | All constants and hyper-parameters — change settings here |
| `data_client.py` | Yahoo Finance fetch with gatekeeper + Parquet cache |
| `preprocessor.py` | Feature engineering + windowing + train/val/test split |
| `environment.py` | Gym-like trading env (hold/buy/sell, reward, PnL) |
| `model.py` | Dueling DQN network (Value stream + Advantage stream) |
| `agent.py` | Replay buffer, epsilon-greedy policy, Double-DQN update |
| `train.py` | Episode loop, validation, save best model |
| `visualize.py` | Candlesticks, V/A chart, training curves, portfolio PNG |
| `dashboard.py` | Interactive matplotlib dashboard (TextBox inputs, Button) |
| `main.py` | CLI entry point — glues all modules together |

## Key design decisions
- **Dueling DQN**: Q = V(s) + A(s,a) − mean(A). Faster convergence than plain DQN.
- **Double DQN update**: policy net selects action, target net evaluates — reduces overestimation.
- **3-tier data fallback**: Parquet cache → yfinance live → CSV. Gatekeeper limits 10 req/min.
- **All-in/all-out**: agent holds 100% cash or 100% equity (no partial sizing).

## How to extend
- **Add a feature**: edit `preprocessor.py:engineer_features()` and bump `FEATURES_COUNT` in `config.py`.
- **Add an action** (e.g. short): change `n_actions` everywhere it appears and update `environment.py:step()`.
- **Change the asset**: just pass `--ticker XXX` to `main.py`.
- **More episodes / bigger net**: edit `config.py` constants.

## Environment
- Python 3.10+, PyTorch CPU (venv_global)
- Run: `python main.py` (full pipeline + dashboard)
- No-GUI: `python main.py --no-dashboard`
- Fast test: `python main.py --episodes 50 --no-dashboard`
