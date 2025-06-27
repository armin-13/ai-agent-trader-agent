# technical_analysis.py (ohne pandas_ta, nur mit pandas + numpy)

import pandas as pd
import numpy as np

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df

def calculate_macd(df, fast=12, slow=26, signal=9):
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    macd_hist = macd_line - signal_line
    df['MACD'] = macd_line
    df['MACD_signal'] = signal_line
    df['MACD_hist'] = macd_hist
    return df

def calculate_indicators(df):
    df = calculate_rsi(df)
    df = calculate_macd(df)
    return df

def generate_signal(df):
    latest = df.iloc[-1]
    rsi = latest.get("RSI")
    macd = latest.get("MACD")
    macd_signal = latest.get("MACD_signal")

    if rsi is not None and macd is not None and macd_signal is not None:
        if rsi < 30 and macd > macd_signal:
            return "BUY"
        elif rsi > 70 and macd < macd_signal:
            return "SELL"
    return "HOLD"
