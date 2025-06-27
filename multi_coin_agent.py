# multi_coin_agent.py (fix: import korrigiert + robust)

from sentiment import analyze_sentiment
from news_fetcher import fetch_crypto_news
from trader import get_price, trade_if_needed
from aiagent.technical_analysis import calculate_indicators, generate_signal
from coin_discovery import get_top_usdt_symbols
from aiagent.binance_data import get_ohlcv
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

        # Berechne technische Indikatoren
        df = get_ohlcv(symbol)
        df = calculate_indicators(df)
        signal = generate_signal(df)

        logging.info(f"→ Entscheidungsbasis für {symbol}: Sentiment={sentiment_score}, Signal={signal}")

        analysis = {
            "symbol": symbol,
            "price": price,
            "signal": signal,
            "sentiment": sentiment_score
        }

        logging.info(f"{symbol} ➜ Preis: ${price:.2f}, Signal: {signal}")

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
    results = []
    for symbol in COINS:
        try:
            results.append(analyze_coin(symbol))
        except Exception as e:
            logging.error(f"{symbol} ➜ Analysefehler: {str(e)}")
            results.append({"symbol": symbol, "error": str(e)})
    return results


if __name__ == "__main__":
    result = analyze_all()
    for entry in result:
        print(entry)
