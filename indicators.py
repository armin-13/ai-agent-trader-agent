import pandas as pd
import pandas_ta as ta
import yfinance as yf

def get_technical_indicators(symbol: str):
    df = yf.download(symbol, interval='1h', period='1d')  # استفاده از داده‌های واقعی

    if df.empty or len(df) < 50:
        return {"rsi": None, "macd": None, "signal": "HOLD"}

    df.ta.rsi(length=14, append=True)
    macd = ta.macd(df['Close'])
    df = pd.concat([df, macd], axis=1)

    rsi = df['RSI_14'].iloc[-1]
    macd_line = df['MACD_12_26_9'].iloc[-1]
    macd_signal = df['MACDs_12_26_9'].iloc[-1]

    signal = "HOLD"
    if rsi < 30 and macd_line > macd_signal:
        signal = "BUY"
    elif rsi > 70 and macd_line < macd_signal:
        signal = "SELL"

    return {"rsi": round(rsi, 2), "macd": round(macd_line, 4), "signal": signal}