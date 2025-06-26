from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from agent import get_analysis
from trader import trade_if_needed

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    analysis = get_analysis()
    result = {}

    if analysis["signal"] in ["BUY", "SELL"]:
        result = trade_if_needed(analysis["signal"])

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "result": result,
        "analysis": analysis
    })

def scheduled_job():
    analysis = get_analysis()
    if analysis["signal"] in ["BUY", "SELL"]:
        trade_if_needed(analysis["signal"])

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, "interval", minutes=1)
scheduler.start()

