# multi_coin_agent.py (mit dynamischer Coin Discovery & verbessertem Entscheidungs-Logging)

from sentiment import analyze_sentiment
from news_fetcher import fetch_crypto_news
from trader import get_price, trade_if_needed
from indicators import get_rsi, get_macd
from coin_discovery import get_top_usdt_symbols
import logging

# Logging konfigurieren
logging.basicConfig(
    filename="trade_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Dynamische Coin-Auswahl basierend auf Volumen
COINS = get_top_usdt_symbols(limit=25, min_volume_usdt=1000000)


def analyze_coin(symbol):
    try:
        news = fetch_crypto_news(symbol)
        sentiment_score = analyze_sentiment(news)
        price = get_price(symbol)
        rsi = get_rsi(symbol)
        macd_signal = get_macd(symbol)

        # Entscheidungs-Logging zur Analyse
        logging.info(f"→ Entscheidungsbasis für {symbol}: Sentiment={sentiment_score}, RSI={rsi}, MACD={macd_signal}")

        # Entscheidungslogik mit Sentiment, RSI und MACD
        if sentiment_score > 0 and rsi is not None and rsi < 50 and macd_signal == "BUY":
            signal = "BUY"
        elif sentiment_score < 0 and rsi is not None and rsi > 50 and macd_signal == "SELL":
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
        logging.info(f"{symbol} ➜ Preis: ${price:.2f}, Signal: {signal}")

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
    logging.info(f"Starte Analyse für {len(COINS)} Coins...")
    return [analyze_coin(symbol) for symbol in COINS]


if __name__ == "__main__":
    result = analyze_all()
    for entry in result:
        print(entry)
