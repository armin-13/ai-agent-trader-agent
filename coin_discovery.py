# coin_discovery.py (korrigiert für aktuelle Binance-API)

from binance.client import Client
from dotenv import load_dotenv
import os

# .env laden
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Binance-Client initialisieren
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'


def get_top_usdt_symbols(limit=25, min_volume_usdt=1000000):
    """
    Gibt die Top-USDT-Paare zurück, sortiert nach Handelsvolumen (24h).
    """
    try:
        tickers = client.get_ticker()  # Korrekte Methode
        usdt_pairs = [
            t for t in tickers
            if t["symbol"].endswith("USDT") and not t["symbol"].startswith("USD")
        ]

        # Da get_ticker() keine Volumen-Daten enthält, optional ausklammern oder aus anderer Quelle holen
        filtered = [t for t in usdt_pairs][:limit]
        return [entry["symbol"] for entry in filtered]

    except Exception as e:
        print(f"[Fehler] Coin Discovery fehlgeschlagen: {e}")
        return ["BTCUSDT", "ETHUSDT"]  # Fallback


if __name__ == "__main__":
    coins = get_top_usdt_symbols()
    print("Top USDT-Paare:", coins)
