"""Interactive matplotlib dashboard: enter ticker + date range, see live results."""
import os
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import TextBox, Button
import torch
import config
from data_client import YFinanceDataClient
from preprocessor import prepare
from environment import TradingEnv
from agent import DQNAgent
from train import run_episode

_client = YFinanceDataClient()
_C = {"bg": "#1e1e2e", "ax": "#2a2a3e", "w": "white"}


def _style(ax):
    ax.set_facecolor(_C["ax"])
    for s in ax.spines.values():
        s.set_edgecolor("#555577")
    ax.tick_params(colors=_C["w"])
    ax.xaxis.label.set_color(_C["w"])
    ax.yaxis.label.set_color(_C["w"])
    ax.title.set_color(_C["w"])


def _candles(ax, df, ticker):
    ax.cla(); _style(ax); ax.set_title(f"{ticker} Candlesticks", color=_C["w"])
    o, h, l, c = df["Open"].values, df["High"].values, df["Low"].values, df["Close"].values
    for i in range(len(df)):
        col = "#55a868" if c[i] >= o[i] else "#c44e52"
        ax.plot([i, i], [l[i], h[i]], color=col, linewidth=0.8)
        ax.bar(i, abs(c[i]-o[i]), bottom=min(o[i],c[i]), width=0.6, color=col, linewidth=0)
    ax.set_ylabel("Price ($)", color=_C["w"])


def _portfolio(ax, test_env, close_series, ticker):
    ax.cla(); _style(ax)
    pv = np.array(test_env.portfolio_hist)
    bh = close_series.values[-len(pv):]
    bh = config.INITIAL_CAPITAL * bh / bh[0]
    ax.plot(pv, label="DQN Agent",  color="#4c72b0", linewidth=1.5)
    ax.plot(bh, label="Buy & Hold", color="#dd8452", linewidth=1.5, linestyle="--")
    ax.set_title("Portfolio vs Buy & Hold (test)", color=_C["w"])
    ax.set_ylabel("Value ($)", color=_C["w"])
    ax.legend(facecolor=_C["ax"], labelcolor=_C["w"]); ax.grid(alpha=0.2)


def _val_adv(ax_v, ax_a, agent, state):
    t = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(agent.device)
    with torch.no_grad():
        v, a = agent.policy_net.value_advantage(t)
    for ax in (ax_v, ax_a):
        ax.cla(); _style(ax)
    ax_v.bar(["V(s)"], [v.item()], color="#dd8452", width=0.4)
    ax_v.set_title("Value  V(s)", color=_C["w"])
    ax_a.bar(["Hold", "Buy", "Sell"], a.squeeze().cpu().numpy(),
             color=["#4c72b0", "#55a868", "#c44e52"])
    ax_a.axhline(0, color=_C["w"], linewidth=0.6, linestyle="--")
    ax_a.set_title("Advantage  A(s,a)", color=_C["w"])


def _stats(ax, env, ticker):
    ax.cla(); ax.axis("off")
    pv   = np.array(env.portfolio_hist)
    peak = np.maximum.accumulate(pv)
    dd   = ((pv - peak) / np.maximum(peak, 1e-9)).min() * 100
    text = (f"Ticker: {ticker}  |  Final: ${env.final_value:,.2f}  |  "
            f"Return: {env.total_return_pct:+.2f}%  |  "
            f"Trades: {env.total_trades}  |  Max Drawdown: {dd:.2f}%")
    ax.text(0.5, 0.5, text, ha="center", va="center", color=_C["w"],
            fontsize=11, transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#3a3a5e", edgecolor="#8888cc"))


def launch():
    fig = plt.figure(figsize=(18, 11))
    fig.patch.set_facecolor(_C["bg"])
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35, top=0.88, bottom=0.16)
    ax_c = fig.add_subplot(gs[0, :2])
    ax_p = fig.add_subplot(gs[1, :2])
    ax_v = fig.add_subplot(gs[0, 2])
    ax_a = fig.add_subplot(gs[1, 2])
    ax_s = fig.add_subplot(gs[2, :])
    for ax in (ax_c, ax_p, ax_v, ax_a, ax_s):
        _style(ax)
    fig.suptitle("Dueling DQN — Stock Trader Dashboard",
                 color=_C["w"], fontsize=14, fontweight="bold")

    tb_tick = TextBox(plt.axes([0.08, 0.05, 0.14, 0.04]), "Ticker ",
                      initial=config.DEFAULT_TICKER)
    tb_s    = TextBox(plt.axes([0.26, 0.05, 0.14, 0.04]), "Start  ",
                      initial=config.DEFAULT_START)
    tb_e    = TextBox(plt.axes([0.44, 0.05, 0.14, 0.04]), "End    ",
                      initial=config.DEFAULT_END)
    btn     = Button(plt.axes([0.62, 0.05, 0.12, 0.04]), "Run",
                     color="#4c72b0", hovercolor="#6699cc")
    st_ax   = plt.axes([0.78, 0.05, 0.18, 0.04])
    st_ax.axis("off")
    st_txt  = st_ax.text(0.0, 0.5, "Ready", color="#aaaacc", fontsize=9, va="center")

    def on_run(_):
        ticker = (tb_tick.text.strip().upper() or config.DEFAULT_TICKER)
        start  = tb_s.text.strip() or config.DEFAULT_START
        end    = tb_e.text.strip() or config.DEFAULT_END
        st_txt.set_text("Fetching…"); fig.canvas.draw_idle()
        try:
            df     = _client.fetch(ticker, start, end)
            splits = prepare(df)
            agent  = DQNAgent()
            mp     = os.path.join(config.MODEL_DIR, f"{ticker}_best.pt")
            if os.path.exists(mp):
                agent.load(mp); st_txt.set_text(f"Model loaded: {ticker}")
            else:
                st_txt.set_text("No model — random agent")
            env = TradingEnv(*splits["test"])
            run_episode(env, agent, train=False)
            _candles(ax_c, df.iloc[-120:], ticker)
            _portfolio(ax_p, env, df["Close"], ticker)
            _val_adv(ax_v, ax_a, agent, splits["test"][0][-1])
            _stats(ax_s, env, ticker)
        except Exception as exc:
            st_txt.set_text(f"Error: {exc}")
        fig.canvas.draw_idle()

    btn.on_clicked(on_run)
    on_run(None)
    plt.show()
