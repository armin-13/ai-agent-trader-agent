# main.py (inkl. Signal-Multi-API und Dashboard)

from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from multi_coin_agent import analyze_all
from trade_dashboard import app as trade_dashboard_app
import logging
import pandas as pd
from aiagent.binance_data import get_ohlcv
from aiagent.technical_analysis import calculate_indicators, generate_signal

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

# --- REST API: Platzhalter für Symbol-/Preisdaten ---
@app.get("/symbols")
def get_symbols():
    return {"symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"]}


@app.get("/prices")
def get_prices():
    return {
        "BTCUSDT": 64000.0,
        "ETHUSDT": 3400.0,
        "SOLUSDT": 145.25
    }

# --- REST API: Technische Signal-Ausgabe für ein Symbol ---
@app.get("/signal")
def signal(symbol: str = "BTCUSDT"):
    try:
        df = get_ohlcv(symbol)
        df = calculate_indicators(df)
        signal = generate_signal(df)
        return {"symbol": symbol, "signal": signal}
    except Exception as e:
        logging.error(f"Fehler bei Signalscan für {symbol}: {e}")
        return {"symbol": symbol, "error": str(e)}

# --- NEU: Multi-Symbol Signal API ---
@app.get("/signals")
def signals(symbols: list[str] = Query(default=["BTCUSDT", "ETHUSDT", "SOLUSDT"])):
    response = []
    for symbol in symbols:
        try:
            df = get_ohlcv(symbol)
            df = calculate_indicators(df)
            signal = generate_signal(df)
            response.append({"symbol": symbol, "signal": signal})
        except Exception as e:
            response.append({"symbol": symbol, "error": str(e)})
    return response
