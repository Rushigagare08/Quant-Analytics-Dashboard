import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

def ticks_to_df(ticks):
    df = pd.DataFrame(ticks)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df

def resample_df(df, timeframe):
    if timeframe == "1s":
        return df.resample("1s").last().dropna()
    if timeframe == "1m":
        return df.resample("1min").last().dropna()
    if timeframe == "5m":
        return df.resample("5min").last().dropna()

def hedge_ratio(x, y):
    return np.cov(x, y)[0, 1] / np.var(x)

def spread_zscore(x, y, window=30):
    beta = hedge_ratio(x, y)
    spread = y - beta * x
    z = (spread - spread.rolling(window).mean()) / spread.rolling(window).std()
    return spread, z, beta

def rolling_corr(x, y, window=30):
    return x.rolling(window).corr(y)

def adf_test(series):
    return adfuller(series.dropna())[1]
