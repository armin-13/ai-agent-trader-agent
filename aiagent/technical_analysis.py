import pandas as pd
import pandas_ta as ta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['EMA20'] = ta.ema(df['close'], length=20)
    df['RSI'] = ta.rsi(df['close'], length=14)
    return df


def generate_signal(df: pd.DataFrame) -> str:
    last = df.iloc[-1]

    if last['RSI'] < 30 and last['close'] > last['EMA20']:
        return "BUY"
    elif last['RSI'] > 70 and last['close'] < last['EMA20']:
        return "SELL"
    else:
        return "HOLD"