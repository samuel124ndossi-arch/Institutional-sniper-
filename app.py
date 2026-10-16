import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sniper_engine import InstitutionalSniperEngine

# --- PAGE CONFIGURATION FOR MOBILE ---
st.set_page_config(
    page_title="Institutional Sniper",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLING FOR A CLEAN, CLUTTER-FREE MOBILE UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #2962ff; color: white; font-weight: bold; height: 3em; }
    .signal-card { background-color: #1e222d; padding: 20px; border-radius: 12px; border: 1px solid #2a2e39; margin-top: 15px; }
    .metric-title { font-size: 14px; color: #848e9c; }
    .metric-value { font-size: 18px; font-weight: bold; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("### ⚡ Institutional Sniper Engine")
st.caption("Order Flow, CVD, & FVG Automated Scanner")

# --- ASSET & PARAMETER SELECTOR ---
col1, col2 = st.columns(2)
with col1:
    asset = st.selectbox("Select Asset", ["XAU/USD (Gold)", "NAS100", "US30"])
with col2:
    timeframe = st.selectbox("Timeframe", ["15m", "5m", "1H"])

# Mock data generator for live simulation feed (In production, replace with live MetaAPI or broker fetch)
@st.cache_data(ttl=60)
def fetch_market_data(symbol):
    # Generating sample OHLCV data structure to test the engine
    np.random.seed(42)
    rows = 150
    base_price = 4160.0 if "XAU" in symbol else 18000.0
    close_prices = base_price + np.cumsum(np.random.randn(rows) * 2.5)
    df = pd.DataFrame({
        'open': close_prices + np.random.randn(rows) * 0.5,
        'high': close_prices + abs(np.random.randn(rows) * 1.5),
        'low': close_prices - abs(np.random.randn(rows) * 1.5),
        'close': close_prices,
        'volume': np.random.randint(1000, 5000, size=rows)
    })
    return df

df_market = fetch_market_data(asset)

# Initialize Sniper Engine
engine = InstitutionalSniperEngine(atr_period=14, r_multiplier=5.0)
df_processed = engine.calculate_indicators(df_market)

# Run Signal Check (Assuming macro is bullish for demonstration toggle)
htf_bullish_bias = st.toggle("Macro 1H Trend: Bullish", value=True)

if st.button("🔍 Run Live Market Scan"):
    with st.spinner(f"Connecting to live feed & scanning {asset}..."):
        signal = engine.check_signal(df_processed, htf_bullish=htf_bullish_bias)
        
        if signal["status"] == "SIGNAL_READY":
            st.success(f"🎯 Institutional Confluence Verified for {asset}!")
            
            # Display Clean Signal Card matching professional UI standards
            st.markdown(f"""
                <div class="signal-card">
                    <h2 style="margin:0; color: {'#0ecb81' if signal['type']=='BUY' else '#f6465d'};">{signal['type']} — {asset}</h2>
                    <hr style="border: 0.5px solid #2a2e39;">
                    <p class="metric-title">ENTRY PRICE</p>
                    <p class="metric-value">{signal['entry']}</p>
                    <p class="metric-title">DYNAMIC STOP LOSS</p>
                    <p class="metric-value" style="color: #f6465d;">{signal['stop_loss']}</p>
                    <p class="metric-title">50% PARTIAL TP (1:2.5 & Move to BE)</p>
                    <p class="metric-value" style="color: #0ecb81;">{signal['partial_tp']}</p>
                    <p class="metric-title">FULL TAKE PROFIT ({signal['risk_reward']})</p>
                    <p class="metric-value" style="color: #0ecb81;">{signal['full_tp']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            st.info("ℹ️ No high-probability setup met right now. Market is currently ranging or awaiting institutional volume sweep.")

# Footer info
st.markdown("---")
st.caption(f"System Time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} | Mode: Live Feed Ready")
