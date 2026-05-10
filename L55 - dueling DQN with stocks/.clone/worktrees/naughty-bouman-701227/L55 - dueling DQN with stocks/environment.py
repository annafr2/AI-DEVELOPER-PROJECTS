"""Trading environment: wraps windowed data into a gym-like RL interface."""
import numpy as np
import config


class TradingEnv:
    """
    State  : (WINDOW_SIZE, FEATURES_COUNT) array — last 30 bars of features.
    Actions: 0=hold  1=buy  2=sell
    Reward : change in portfolio value, penalised for transaction costs.
    """

    def __init__(self, windows: np.ndarray, prices: np.ndarray):
        assert len(windows) == len(prices), "windows and prices must align"
        self.windows = windows
        self.prices  = prices
        self.n_steps = len(windows)
        self.reset()

    # ── Gym interface ─────────────────────────────────────────────────────────
    def reset(self):
        self.step_idx        = 0
        self.cash            = config.INITIAL_CAPITAL
        self.shares          = 0.0
        self.entry_price     = 0.0
        self.total_trades    = 0
        self.portfolio_hist  = [config.INITIAL_CAPITAL]
        return self._get_state()

    def step(self, action: int):
        price  = float(self.prices[self.step_idx])
        reward = 0.0
        info   = {"action": action, "price": price}

        if action == 1 and self.shares == 0:    # buy
            cost = price * (1 + config.TRANSACTION_COST_PCT)
            self.shares      = self.cash / cost
            self.cash        = 0.0
            self.entry_price = price
            self.total_trades += 1

        elif action == 2 and self.shares > 0:   # sell
            proceeds    = self.shares * price * (1 - config.TRANSACTION_COST_PCT)
            reward      = proceeds - self.shares * self.entry_price
            self.cash   = proceeds
            self.shares = 0.0
            self.total_trades += 1

        portfolio = self._portfolio_value(price)
        self.portfolio_hist.append(portfolio)

        self.step_idx += 1
        done  = self.step_idx >= self.n_steps
        state = None if done else self._get_state()
        info["portfolio"] = portfolio
        return state, reward, done, info

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _portfolio_value(self, price: float) -> float:
        return self.cash + self.shares * price

    def _get_state(self) -> np.ndarray:
        w = self.windows[self.step_idx].copy()
        price = float(self.prices[self.step_idx])
        pv    = self._portfolio_value(price)
        upnl  = (price - self.entry_price) / max(self.entry_price, 1e-9) if self.shares > 0 else 0.0
        # fill the two agent-state slots (columns 8, 9)
        w[:, 8] = float(self.shares > 0)   # 1 if holding, else 0
        w[:, 9] = upnl
        return w

    @property
    def final_value(self) -> float:
        return self.portfolio_hist[-1]

    @property
    def total_return_pct(self) -> float:
        return (self.final_value / config.INITIAL_CAPITAL - 1) * 100
