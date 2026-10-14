"""
MACRO EDGE AI - Streamlit Dashboard
Professional fundamental forex & gold pre-news forecasting tool.
Entry point: app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from config import COLORS, MARKET_NAMES, DEMO_MODE_LABEL, RISK_PARAMS
from data_sources import DataSources
from macro_engine import MacroEngine

st.set_page_config(
    page_title="MACRO EDGE AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {COLORS['bg']}; color: {COLORS['text']}; }}
    .metric-card {{ background-color: {COLORS['card']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['green']}; }}
    h1, h2, h3 {{ color: {COLORS['gold']}; }}
    .demo-banner {{ background-color: #7C2D12; color: white; padding: 0.5rem; border-radius: 4px; text-align: center; }}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def get_engine():
    return MacroEngine(DataSources())

engine = get_engine()
ds = engine.ds

st.title("MACRO EDGE AI")
st.markdown("**Fundamental Forex & Gold Forecasting Desk** — Pre-news scenarios, post-release analysis, and risk tools.")
st.caption("Educational tool only. Not financial advice. No guaranteed predictions or profits.")

if ds.demo_mode:
    st.markdown(f'<div class="demo-banner">{DEMO_MODE_LABEL}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Controls")
    selected_market = st.selectbox("Market", list(MARKET_NAMES.values()))
    account_size = st.number_input("Account Size ($)", value=float(RISK_PARAMS["default_account_size"]), min_value=100.0)
    risk_pct = st.slider("Risk % per idea", 0.1, 5.0, RISK_PARAMS["max_risk_per_trade_pct"], 0.1)
    stop_pips = st.number_input("Stop (pips)", value=20, min_value=5)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Market Snapshot", "Economic Calendar", "Pre-News Scenarios", "Post-News Analysis", "Risk & History"
])

with tab1:
    st.subheader("Live / Latest Market Prices")
    snapshot = ds.get_market_snapshot()
    cols = st.columns(4)
    for i, (name, info) in enumerate(snapshot.items()):
        with cols[i % 4]:
            price = info["price"]
            meta = info["meta"]
            st.metric(name, f"{price:.4f}" if price and "JPY" not in name and "XAU" not in name else f"{price:.2f}" if price else "N/A")
            if meta.get("warning"):
                st.caption(f"⚠️ {meta['warning']}")
            st.caption(f"Source: {meta['source']} | {meta['fetched_at'][:16]}")

    st.subheader(f"{selected_market} Recent Price")
    ticker = [k for k, v in MARKET_NAMES.items() if v == selected_market][0]
    df, meta = ds.get_price_data(ticker, period="5d", interval="1h")
    if not df.empty:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
            name=selected_market
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLORS["bg"],
            plot_bgcolor=COLORS["card"],
            height=400,
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        if meta.get("is_demo"):
            st.warning("Chart uses DEMO sample data.")

with tab2:
    st.subheader("High-Impact Economic Calendar (DEMO structure)")
    events = ds.get_upcoming_events()
    st.dataframe(events, use_container_width=True, hide_index=True)
    st.info("For production, integrate a real calendar API (e.g. Trading Economics, Forex Factory via approved method, or official statistical agency feeds). Current view uses scheduled event types with DEMO placeholders.")

with tab3:
    st.subheader("Pre-News Scenarios")
    event_choice = st.selectbox("Select event type", [e["event"] for e in ds.get_upcoming_events().to_dict("records")])
    scenarios = engine.pre_news_scenarios(event_choice)
    st.json(scenarios)
    st.markdown("**Methodology note:** Scenarios derived from typical historical market reactions to data surprises. Always consider broader context (Fed policy path, positioning, correlated releases).")

with tab4:
    st.subheader("Post-News Analysis")
    st.markdown("Enter actual vs consensus (use real values from official sources when available).")
    col1, col2, col3 = st.columns(3)
    with col1:
        actual = st.number_input("Actual", value=0.0, format="%.3f")
    with col2:
        consensus = st.number_input("Consensus", value=0.0, format="%.3f")
    with col3:
        previous = st.number_input("Previous", value=0.0, format="%.3f")
    if st.button("Analyze Surprise"):
        analysis = engine.post_news_analysis(event_choice, actual, consensus, previous)
        st.json(analysis)

    st.subheader("Historical Series Trend (illustrative)")
    series_code = st.selectbox("FRED series example", ["CPIAUCSL", "PAYEMS", "UNRATE", "FEDFUNDS"])
    model_out = engine.simple_surprise_model(series_code)
    st.json(model_out)

with tab5:
    st.subheader("Risk Calculator")
    risk_out = engine.risk_calculator(account_size, risk_pct, stop_pips, selected_market)
    st.json(risk_out)
    st.warning(risk_out["event_warning"])

    st.subheader("Session Forecast / Analysis History")
    hist = engine.get_forecast_history()
    if not hist.empty:
        st.dataframe(hist, use_container_width=True)
    else:
        st.info("No analyses recorded this session yet.")
    st.caption(engine.performance_note())

st.markdown("---")
st.caption(f"MACRO EDGE AI • Data fetched at {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} • Transparent methodology • Demo mode active if no FRED key")
