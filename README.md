# Quant Analytics Dashboard – BTC–ETH Pair Trading

## Overview
This project implements a real-time quantitative analytics dashboard for BTC–ETH pair trading using live market data from Binance. The system ingests tick-level trade data, resamples it into time bars, computes statistical signals, and visualizes mean-reversion opportunities.

## Features
- Live BTC & ETH trade ingestion via Binance WebSocket
- Configurable resampling (1s, 1m, 5m)
- Hedge ratio estimation
- Spread and rolling Z-score computation
- Rolling correlation
- User-defined Z-score alerts
- Interactive Plotly charts
- CSV export of processed analytics

## Architecture
- **Data Ingestion:** Binance WebSocket (`@trade` stream)
- **Processing:** Pandas resampling and rolling analytics
- **Analytics:** Hedge ratio, spread, Z-score, correlation
- **Frontend:** Streamlit dashboard with real-time updates

## Data Storage
For low-latency analytics, ticks are buffered in memory. A SQLite schema is defined and can be enabled for persistent storage if required.

## Setup Instructions
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
