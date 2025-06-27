import pandas as pd
import requests

def get_ohlcv(symbol: str, interval: str = "1m", limit: int = 100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "_1", "_2", "_3", "_4", "_5", "_6"
    ])
    df["close"] = df["close"].astype(float)
    return df[["timestamp", "close"]]
