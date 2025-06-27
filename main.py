# main.py (kombiniert mit Dashboard, Live Binance API und robuster Analyse)

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from multi_coin_agent import analyze_all
from trade_dashboard import app as trade_dashboard_app
import logging
import requests
import pandas as pd

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# FastAPI Setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Route: Dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    logging.info("Dashboard-Anfrage erhalten")
    try:
        results = analyze_all()
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "results": results
        })
    except Exception as e:
        logging.error(f"Fehler im Dashboard: {e}")
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "results": [],
            "error": str(e)
        })

# Geplante Hintergrundanalyse (z. B. jede Minute)
def scheduled_job():
    logging.info("Geplante Analyse gestartet")
    try:
        analyze_all()
    except Exception as e:
        logging.error(f"Fehler bei geplanter Analyse: {e}")

# Starte Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, "interval", minutes=1)
scheduler.start()

logging.info("AI Trading Agent gestartet")

# --- REST API für Binance-Daten ---

def get_tradeable_symbols(base_currency="USDT"):
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url, timeout=10)
        data = response.json()
        return [s['symbol'] for s in data['symbols'] if s['status'] == 'TRADING' and s['quoteAsset'] == base_currency]
    except Exception as e:
        logging.error(f"Fehler beim Abrufen handelbarer Symbole: {e}")
        return []

def get_latest_prices(symbols):
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        response = requests.get(url, timeout=10)
        prices_data = response.json()
        return {item['symbol']: float(item['price']) for item in prices_data if item['symbol'] in symbols}
    except Exception as e:
        logging.error(f"Fehler beim Abrufen von Preisen: {e}")
        return {}

@app.get("/symbols")
def api_get_symbols(base: str = "USDT"):
    return {"base": base, "symbols": get_tradeable_symbols(base)}

@app.get("/prices")
def api_get_prices(base: str = "USDT"):
    symbols = get_tradeable_symbols(base)
    return get_latest_prices(symbols)

@app.get("/ohlcv")
def api_get_ohlcv(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 100):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        response = requests.get(url, timeout=10)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        return df[["timestamp", "close"]].tail(50).to_dict(orient="records")
    except Exception as e:
        logging.error(f"Fehler beim Abrufen von OHLCV-Daten: {e}")
        return {"error": str(e)}
