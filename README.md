# AI Crypto Trading Agent 💹🤖

This project is an **AI-powered crypto trading agent** that:
- Fetches live news headlines
- Performs sentiment analysis
- Applies basic trading logic
- Sends buy/sell signals
- Places market orders automatically on Binance **Testnet**
- Displays everything on a **FastAPI dashboard**

## ⚙️ Features

- 🔄 Runs every minute with APScheduler
- 📈 Uses Binance Testnet (safe for experimentation)
- 📰 Fetches latest BTC-related news from CryptoPanic
- 🤖 Analyzes market sentiment using HuggingFace Transformers
- 🧠 Generates trade signals (BUY / SELL / HOLD)
- 💸 Automatically places trades with adjustable risk
- 📊 Dashboard built with FastAPI + Jinja2 templates

## 🚀 How to Run

1. Clone this repo:

```bash
git clone https://github.com/armin-13/ai-agent-trader-agent.git
cd ai-agent-trader-agent
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Set your Binance Testnet API keys in `trader.py`

```python
API_KEY = "your_testnet_api_key"
API_SECRET = "your_testnet_api_secret"
```

4. Run the agent:

```bash
uvicorn main:app --reload
```

5. Open your browser:

```
http://localhost:8000
```

## 🧪 Testnet

Use [https://testnet.binance.vision/](https://testnet.binance.vision/) to get free BTC/USDT and create test API keys.

## 📦 Requirements

- fastapi
- uvicorn
- python-binance
- requests
- transformers
- torch
- apscheduler
- jinja2

## 📌 Notes

This is an MVP (minimum viable product) — you can extend it by:
- Adding technical indicators (RSI, MACD)
- More advanced risk management
- Multi-coin support
- Database logging
