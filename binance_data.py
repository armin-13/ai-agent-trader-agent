# main.py (kombiniert mit Dashboard & Live Binance API)

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from multi_coin_agent import analyze_all
from trade_dashboard import app as trade_dashboard_app  # Falls als Sub-App eingebunden
import logging
import requests

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

# --- Erweiterung: REST API für Live-Symbole und Preise von Binance ---

def get_tradeable_symbols(base_currency="USDT"):
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()

    symbols = []
    for s in data['symbols']:
        if s['status'] == 'TRADING' and s['quoteAsset'] == base_currency:
            symbols.append(s['symbol'])

    return symbols


def get_latest_prices(symbols):
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    prices_data = response.json()

    price_dict = {}
    for item in prices_data:
        if item['symbol'] in symbols:
            price_dict[item['symbol']] = float(item['price'])

    return price_dict


@app.get("/symbols")
def api_get_symbols(base: str = "USDT"):
    symbols = get_tradeable_symbols(base)
    return {"base": base, "symbols": symbols}


@app.get("/prices")
def api_get_prices(base: str = "USDT"):
    symbols = get_tradeable_symbols(base)
    prices = get_latest_prices(symbols)
    return prices
