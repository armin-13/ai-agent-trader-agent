# trader.py (erweitert mit Logging, Absicherung, Risiko-Kalkulation & Doku)

from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("trade_log.txt"),
        logging.StreamHandler()
    ]
)

# Umgebungsvariablen laden
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Binance-Client initialisieren
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Kapital-Management
initial_capital_usdt = float(os.getenv("INITIAL_USDT", 100))
risk_percentage = float(os.getenv("RISK_PERCENTAGE", 0.05))  # z. B. 5 %
MIN_NOTIONAL = 10


def get_price(symbol):
    """Liefert den aktuellen Marktpreis für ein gegebenes Symbol."""
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        price = float(ticker['price'])
        logging.info(f"{symbol} ➜ aktueller Preis: ${price:.2f}")
        return price
    except Exception as e:
        logging.error(f"Fehler beim Abrufen des Preises für {symbol}: {e}")
        return None


def place_order(symbol="BTCUSDT", side="BUY"):
    """Führt eine Market Order auf dem Testnet aus."""
    try:
        price = get_price(symbol)
        if price is None:
            return {"status": "error", "message": "Price fetch failed"}

        amount_in_usdt = initial_capital_usdt * risk_percentage

        if amount_in_usdt < MIN_NOTIONAL:
            msg = f"Order übersprungen: ${amount_in_usdt:.2f} ist unter MIN_NOTIONAL (${MIN_NOTIONAL})"
            logging.warning(msg)
            return {"status": "skipped", "reason": msg}

        logging.info(f"[⚙️] {side} {symbol} für ${amount_in_usdt:.2f}")

        if side == "BUY":
            order = client.order_market_buy(symbol=symbol, quoteOrderQty=amount_in_usdt)
        else:
            order = client.order_market_sell(symbol=symbol, quoteOrderQty=amount_in_usdt)

        logging.info(f"[✅] Order ausgeführt: ID {order['orderId']} | {symbol} | {side}")
        return {"status": "filled", "order": order}

    except BinanceAPIException as e:
        logging.error(f"[❌] Binance API-Fehler: {e.message}")
        return {"status": "error", "message": e.message}
    except Exception as e:
        logging.error(f"[‼️] Allgemeiner Fehler: {str(e)}")
        return {"status": "error", "message": str(e)}


def trade_if_needed(signal: str, symbol: str):
    """Führt je nach Signal eine Kauf- oder Verkaufsorder aus."""
    logging.info(f"Trade-Entscheidung für {symbol}: {signal}")
    if signal == "BUY":
        return place_order(symbol, "BUY")
    elif signal == "SELL":
        return place_order(symbol, "SELL")
    else:
        logging.info(f"Kein Trade ausgeführt für {symbol} (Signal: HOLD)")
        return {"status": "no_action", "message": "Signal war HOLD"}
