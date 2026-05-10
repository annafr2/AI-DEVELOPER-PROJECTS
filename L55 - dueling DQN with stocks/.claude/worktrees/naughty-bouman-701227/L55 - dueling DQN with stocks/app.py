"""Streamlit dashboard — Dueling DQN Stock Trader."""
import os, sys
import numpy as np
import streamlit as st
import psutil, torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
from data_client import YFinanceDataClient
from preprocessor import prepare
from environment import TradingEnv
from agent import DQNAgent
from train import run_episode
from charts import candlestick, portfolio, value_advantage

st.set_page_config(page_title="Dueling DQN Trader", layout="wide", page_icon="📈")
st.markdown("""<style>
.stApp{background:#0d1117;color:#e6edf3}
div[data-testid="stMetric"]{background:#161b22;border-radius:8px;padding:10px}
.action{font-size:2.8rem;font-weight:900;text-align:center;padding:18px;border-radius:12px;margin:8px 0}
.BUY{background:#0d2818;color:#3fb950;border:2px solid #3fb950}
.SELL{background:#2d0f0f;color:#f85149;border:2px solid #f85149}
.HOLD{background:#1c1a0f;color:#d29922;border:2px solid #d29922}
.WAIT{background:#1c1f26;color:#8b949e;border:2px solid #30363d}
</style>""", unsafe_allow_html=True)

for k, v in [("df",None),("splits",None),("agent",None),("env",None),("pred",None)]:
    if k not in st.session_state: st.session_state[k] = v

# ── top bar ───────────────────────────────────────────────────────────────────
st.markdown("## Dueling DQN — AI Stock Trader")
c = st.columns([2,2,2,1,1,1,1,1])
ticker   = c[0].text_input("Ticker",   config.DEFAULT_TICKER).upper()
start    = c[1].text_input("Start",    config.DEFAULT_START)
end      = c[2].text_input("End",      config.DEFAULT_END)
eps      = c[3].number_input("Episodes", 10, 1000, 100, step=10)
do_data  = c[4].button("Prepare Data",  use_container_width=True)
do_train = c[5].button("Train Model",   use_container_width=True)
do_back  = c[6].button("Run Backtest",  use_container_width=True)
do_pred  = c[7].button("Predict Next",  use_container_width=True)
st.divider()
main, right = st.columns([3, 1])

# ── prepare data ──────────────────────────────────────────────────────────────
if do_data:
    with st.spinner(f"Downloading {ticker} from Yahoo Finance…"):
        try:
            df = YFinanceDataClient().fetch(ticker, start, end)
            st.session_state.df, st.session_state.splits = df, prepare(df)
            st.session_state.agent = st.session_state.env = st.session_state.pred = None
            st.success(f"{len(df)} trading days loaded for {ticker}")
        except Exception as e: st.error(str(e))

# ── train ─────────────────────────────────────────────────────────────────────
if do_train:
    if not st.session_state.splits: st.warning("Click Prepare Data first.")
    else:
        agent, best = DQNAgent(), -np.inf
        config.N_EPISODES = eps
        pb = st.progress(0, text="Training…")
        for ep in range(1, eps + 1):
            env = TradingEnv(*st.session_state.splits["train"])
            s = env.reset()
            for _ in range(config.MAX_STEPS_PER_EPISODE):
                a = agent.select_action(s)
                ns, r, done, _ = env.step(a)
                agent.store(s, a, r, ns if not done else np.zeros_like(s), done)
                agent.learn()
                if done: break
                s = ns
            agent.decay_epsilon()
            if ep % 10 == 0:
                ve = TradingEnv(*st.session_state.splits["val"])
                vs = ve.reset()
                for _ in range(config.MAX_STEPS_PER_EPISODE):
                    va = agent.select_action(vs); vns,_,vd,_ = ve.step(va)
                    if vd: break
                    vs = vns
                if ve.total_return_pct > best:
                    best = ve.total_return_pct
                    agent.save(os.path.join(config.MODEL_DIR, f"{ticker}_best.pt"))
            pb.progress(ep/eps, text=f"Episode {ep}/{eps} | eps={agent.epsilon:.3f} | best val={best:+.1f}%")
        st.session_state.agent = agent
        st.success(f"Training done! Best val return: {best:+.2f}%")

# ── backtest ──────────────────────────────────────────────────────────────────
if do_back:
    if not st.session_state.agent: st.warning("Train the model first.")
    else:
        env = TradingEnv(*st.session_state.splits["test"])
        run_episode(env, st.session_state.agent, train=False)
        st.session_state.env = env
        st.success(f"Backtest | Return {env.total_return_pct:+.2f}% | Trades {env.total_trades}")

# ── predict ───────────────────────────────────────────────────────────────────
if do_pred:
    if not st.session_state.agent: st.warning("Train the model first.")
    else:
        ls = st.session_state.splits["test"][0][-1]
        t  = torch.tensor(ls, dtype=torch.float32).unsqueeze(0).to(st.session_state.agent.device)
        with torch.no_grad():
            q = st.session_state.agent.policy_net(t).squeeze().cpu().numpy()
            v, a = st.session_state.agent.policy_net.value_advantage(t)
        st.session_state.pred = {"name":["HOLD","BUY","SELL"][int(q.argmax())],
                                  "q":q, "v":v.item(), "a":a.squeeze().cpu().numpy()}

# ── main charts ───────────────────────────────────────────────────────────────
with main:
    if st.session_state.df is not None:
        st.plotly_chart(candlestick(st.session_state.df.tail(180), ticker), use_container_width=True)
    if st.session_state.env is not None:
        st.plotly_chart(portfolio(st.session_state.env,
                                  st.session_state.splits["test"][1]), use_container_width=True)
    if st.session_state.df is None:
        st.info("Enter a ticker above and click **Prepare Data** to begin.")

# ── right panel ───────────────────────────────────────────────────────────────
with right:
    pred = st.session_state.pred
    name = pred["name"] if pred else "WAIT"
    st.markdown(f'<div class="action {name}">{name if pred else "WAITING"}</div>',
                unsafe_allow_html=True)
    if pred:
        conf = min(float(np.max(pred["q"]) - np.min(pred["q"])) / 5.0, 1.0)
        st.markdown(f"**Confidence:** {conf*100:.0f}%")
        st.progress(conf)
        st.plotly_chart(value_advantage(pred["v"], pred["a"]), use_container_width=True)

    st.markdown("**System Telemetry**")
    st.metric("CPU", f"{psutil.cpu_percent(0.1):.0f}%")
    st.metric("RAM", f"{psutil.Process().memory_info().rss/1e6:.0f} MB")
    if st.session_state.env:
        env  = st.session_state.env
        pv   = np.array(env.portfolio_hist)
        dd   = ((pv - np.maximum.accumulate(pv)) / np.maximum(np.maximum.accumulate(pv), 1e-9)).min() * 100
        st.markdown("**Performance**")
        st.metric("Return",       f"{env.total_return_pct:+.2f}%")
        st.metric("Final Value",  f"${env.final_value:,.0f}")
        st.metric("Trades",       env.total_trades)
        st.metric("Max Drawdown", f"{dd:.2f}%")
