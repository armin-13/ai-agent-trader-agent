# indicators.py (verbessert mit Fehlerbehandlung & Logging)

import pandas as pd
import ta
from binance.client import Client
from dotenv import load_dotenv
import os
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Umgebungsvariablen laden
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Binance Client konfigurieren
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'


def get_ohlcv(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, limit=100):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["close"] = pd.to_numeric(df["close"])
        return df
    except Exception as e:
        logging.error(f"Fehler beim Abrufen von OHLCV-Daten für {symbol}: {e}")
        return pd.DataFrame()


def get_rsi(symbol):
    df = get_ohlcv(symbol)
    if df.empty:
        return None
    try:
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
        rsi_value = df["rsi"].iloc[-1]
        return round(rsi_value, 2)
    except Exception as e:
        logging.error(f"Fehler beim Berechnen des RSI für {symbol}: {e}")
        return None


def get_macd(symbol):
    df = get_ohlcv(symbol)
    if df.empty:
        return "HOLD"
    try:
        macd = ta.trend.MACD(df["close"], window_slow=26, window_fast=12, window_sign=9)
        macd_diff = macd.macd_diff().iloc[-1]
        if macd_diff > 0:
            return "BUY"
        elif macd_diff < 0:
            return "SELL"
        else:
            return "HOLD"
    except Exception as e:
        logging.error(f"Fehler beim Berechnen des MACD für {symbol}: {e}")
        return "HOLD"