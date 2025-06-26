# main.py (verbessert)

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from multi_coin_agent import analyze_all
import logging

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
