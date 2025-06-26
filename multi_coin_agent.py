# multi_coin_agent.py (mit erweitertem Debug-Logging)

from sentiment import analyze_sentiment
from news_fetcher import fetch_crypto_news
from trader import get_price, trade_if_needed
from indicators import get_rsi, get_macd
import logging

# Konfiguriere Logging
logging.basicConfig(filename="trade_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Liste der Coins, die überwacht werden sollen
COINS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT"]

# Mindestvolumen in USDT
MIN_VOLUME = 5000000  # Beispielwert

def analyze_coin(symbol):
    try:
        news = fetch_crypto_news(symbol)
        sentiment_score = analyze_sentiment(news)
        price = get_price(symbol)
        rsi = get_rsi(symbol)
        macd_signal = get_macd(symbol)

        # Entscheidungslogik mit Sentiment, RSI und MACD
        if sentiment_score > 0.5 and rsi is not None and rsi < 30 and macd_signal == "BUY":
            signal = "BUY"
        elif sentiment_score < -0.5 and rsi is not None and rsi > 70 and macd_signal == "SELL":
            signal = "SELL"
        else:
            signal = "HOLD"

        analysis = {
            "symbol": symbol,
            "price": price,
            "signal": signal,
            "sentiment": sentiment_score,
            "rsi": rsi,
            "macd": macd_signal
        }

        # Debug-Logging
        logging.info(f"{symbol} ➜ Preis: ${price:.2f}, Sentiment: {sentiment_score}, RSI: {rsi}, MACD: {macd_signal}, Signal: {signal}")

        # Nur handeln, wenn BUY oder SELL
        result = {}
        if signal in ["BUY", "SELL"]:
            result = trade_if_needed(signal, symbol)
            logging.info(f"{symbol} ➜ Trade-Ergebnis: {result}")

        return analysis | {"trade": result}

    except Exception as e:
        logging.error(f"Fehler bei {symbol}: {str(e)}")
        return {"symbol": symbol, "error": str(e)}

def analyze_all():
    return [analyze_coin(symbol) for symbol in COINS]

if __name__ == "__main__":
    result = analyze_all()
    for entry in result:
        print(entry)