"""Plotly chart builders for the Streamlit dashboard."""
import numpy as np
import plotly.graph_objects as go
import config

_DARK = dict(template="plotly_dark", paper_bgcolor="#0d1117", plot_bgcolor="#161b22")


def candlestick(df, ticker: str) -> go.Figure:
    fig = go.Figure(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"],
        increasing_line_color="#3fb950", decreasing_line_color="#f85149", name=ticker,
    ))
    fig.update_layout(**_DARK, title=f"{ticker} — Last 180 Days",
                      xaxis_rangeslider_visible=False, height=380,
                      margin=dict(l=10, r=10, t=40, b=10))
    return fig


def portfolio(env, test_prices: np.ndarray) -> go.Figure:
    pv  = np.array(env.portfolio_hist)
    bh  = np.concatenate([[config.INITIAL_CAPITAL],
                           config.INITIAL_CAPITAL * test_prices / test_prices[0]])[:len(pv)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=pv, name="DQN Agent",  line=dict(color="#58a6ff", width=2)))
    fig.add_trace(go.Scatter(y=bh, name="Buy & Hold", line=dict(color="#f0883e", width=2, dash="dash")))
    fig.update_layout(**_DARK, title="Portfolio vs Buy & Hold (test)", height=280,
                      margin=dict(l=10, r=10, t=40, b=10))
    return fig


def value_advantage(v: float, a: np.ndarray) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["V(s)"], y=[v], marker_color="#f0883e", name="Value"))
    fig.add_trace(go.Bar(x=["Hold", "Buy", "Sell"], y=a.tolist(),
                         marker_color=["#8b949e", "#3fb950", "#f85149"], name="Advantage"))
    fig.update_layout(**_DARK, title="Value & Advantage", height=220,
                      margin=dict(l=5, r=5, t=30, b=5), showlegend=False)
    return fig
