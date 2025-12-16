# app.py
import streamlit as st
import threading
import time
import plotly.graph_objects as go
import pandas as pd

from ws_client import poll_binance, tick_buffer
from analytics import *

# ---------------- PAGE SETUP ----------------
st.set_page_config(layout="wide")
st.title("Quant Analytics Dashboard — BTC–ETH Pair Trading")

# ---------------- START DATA (REST) ----------------
@st.cache_resource
def start_data():
    threading.Thread(target=poll_binance, args=("BTCUSDT",), daemon=True).start()
    threading.Thread(target=poll_binance, args=("ETHUSDT",), daemon=True).start()

start_data()

# ---------------- CONTROLS ----------------
timeframe = st.selectbox("Resample timeframe", ["1s", "1m", "5m"])
window = st.slider("Rolling window", 10, 100, 20)
alert_threshold = st.number_input("Alert if |Z| >", value=2.0)

placeholder = st.empty()

# ---------------- MAIN LOGIC ----------------
with placeholder.container():

    # Show init message ONLY before any data arrives
    if len(tick_buffer) == 0:
        st.info("Initializing live market data…")

    elif len(tick_buffer) < 200:
        st.info("Collecting sufficient market data…")

    else:
        # Thread-safe snapshot
        ticks_snapshot = tick_buffer[-5000:].copy()
        df = ticks_to_df(ticks_snapshot)

        # Split by symbol
        btc_df = df[df["symbol"] == "BTCUSDT"][["price"]]
        eth_df = df[df["symbol"] == "ETHUSDT"][["price"]]

        # Resample separately
        btc_resampled = resample_df(btc_df, timeframe)
        eth_resampled = resample_df(eth_df, timeframe)

        # Align on timestamps
        pair = pd.concat(
            [btc_resampled["price"], eth_resampled["price"]],
            axis=1,
            join="inner"
        )
        pair.columns = ["btc", "eth"]

        if len(pair) < window:
            st.info("Building rolling window for analytics…")

        else:
            # ---- Analytics ----
            spread, z, beta = spread_zscore(pair["btc"], pair["eth"], window)
            corr = rolling_corr(pair["btc"], pair["eth"], window)

            # ---- Metrics ----
            c1, c2, c3 = st.columns(3)
            c1.metric("Hedge Ratio (β)", round(beta, 4))
            c2.metric("Latest Z-Score", round(z.iloc[-1], 2))
            c3.metric("Rolling Correlation", round(corr.iloc[-1], 2))

            if abs(z.iloc[-1]) > alert_threshold:
                st.error("⚠️ Z-Score Alert Triggered")

            # ---- BTC Price Plot ----
            fig_price = go.Figure()
            fig_price.add_trace(
                go.Scatter(x=pair.index, y=pair["btc"], name="BTCUSDT")
            )
            fig_price.update_layout(title="BTC Price")
            st.plotly_chart(fig_price, width="stretch")

            # ---- Z-Score Plot ----
            fig_z = go.Figure()
            fig_z.add_trace(go.Scatter(x=z.index, y=z, name="Z-Score"))
            fig_z.add_hline(y=alert_threshold)
            fig_z.add_hline(y=-alert_threshold)
            fig_z.update_layout(title="BTC–ETH Spread Z-Score")
            st.plotly_chart(fig_z, width="stretch")

            # ---- CSV Export ----
            export_df = pair.copy()
            export_df["spread"] = spread
            export_df["zscore"] = z

            st.download_button(
                "Download CSV",
                export_df.to_csv(),
                "pair_analytics.csv",
                "text/csv"
            )

# ---------------- AUTO REFRESH ----------------
time.sleep(1)
st.rerun()
