# trade_dashboard.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from trade_logger import get_recent_trades, init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

init_db()

@app.get("/trades", response_class=HTMLResponse)
async def show_trades(request: Request):
    trades = get_recent_trades(limit=50)
    return templates.TemplateResponse("trades.html", {
        "request": request,
        "trades": trades
    })
