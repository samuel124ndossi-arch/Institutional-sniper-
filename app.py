import streamlit as st
import pandas as pd
from sniper_engine import InstitutionalSniperEngine

st.set_page_config(page_title="Institutional Sniper", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 10px; border-radius: 8px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Institutional Sniper Engine")
st.caption("Order Flow, CVD, & FVG Automated Scanner")

# Sidebar Controls
st.sidebar.header("Execution Parameters")
ticker = st.sidebar.selectbox("Select Asset", ["XAU/USD (Gold)", "NAS100", "US30"])
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1H", "4H"])
clean_ticker = "XAUUSD" if "XAU" in ticker else ("NAS100" if "NAS" in ticker else "US30")

engine = InstitutionalSniperEngine(ticker=clean_ticker)
analysis = engine.analyze_setup()

# Main Display Cards
st.subheader(f"Asset: {analysis['ticker']}")
col1, col2 = st.columns(2)
with col1:
    st.metric("Sniper Status", analysis['signal'])
with col2:
    st.metric("Confluence Score", f"{analysis['score']}/100")

st.divider()

# Trade Setup Levels (1:5 RR)
st.markdown("### 📊 Institutional Setup Levels")
t1, t2, t3 = st.columns(3)
t1.metric("Entry Price", analysis['entry'])
t2.metric("Stop Loss (SL)", analysis['sl'])
t3.metric("Take Profit (TP 1:5)", analysis['tp'])

st.divider()

# Market Confluence Breakdown
st.markdown("### 🔬 Confluence Matrix")
st.write(f"* **1H Macro Trend:** {analysis['macro_trend']}")
st.write(f"* **CVD Delta Flow:** {analysis['cvd_status']}")
st.write(f"* **Fair Value Gap (FVG):** {'Mitigated & Active 🟢' if analysis['fvg_active'] else 'None Detected ⚪'}")

# Live Chart Preview
st.markdown("### 📈 Price Action & Volume Profile")
chart_data = analysis['data'].set_index('timestamp')[['close']]
st.line_chart(chart_data)

if st.button("🔄 Refresh Market Feed"):
    st.rerun()
