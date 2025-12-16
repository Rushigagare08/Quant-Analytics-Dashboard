# ws_client.py
import time
import requests
from datetime import datetime

tick_buffer = []

def poll_binance(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/trades"
    params = {"symbol": symbol, "limit": 5}

    while True:
        try:
            r = requests.get(url, params=params, timeout=5)
            trades = r.json()

            for t in trades:
                tick_buffer.append({
                    "timestamp": datetime.fromtimestamp(t["time"] / 1000),
                    "symbol": symbol,
                    "price": float(t["price"]),
                    "qty": float(t["qty"])
                })

            if len(tick_buffer) > 20000:
                tick_buffer[:] = tick_buffer[-20000:]

            time.sleep(1)

        except Exception as e:
            print("REST error:", e)
            time.sleep(2)
