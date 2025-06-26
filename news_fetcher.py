# news_fetcher.py (verbessert mit Google News & CryptoPanic kombiniert)

import requests
import feedparser
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Optional: eigener CryptoPanic-Token statt "demo"
CRYPTOPANIC_TOKEN = "demo"


def fetch_crypto_news(symbol="BTC"):
    try:
        # CryptoPanic API
        cp_url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_TOKEN}&currencies={symbol}"
        response = requests.get(cp_url, timeout=10)
        data = response.json()
        cp_headlines = [item["title"] for item in data.get("results", [])[:5]]
    except Exception as e:
        logging.warning(f"CryptoPanic fehlgeschlagen ({symbol}): {e}")
        cp_headlines = []

    try:
        # Google News RSS
        rss_url = f"https://news.google.com/rss/search?q={symbol}+cryptocurrency"
        feed = feedparser.parse(rss_url)
        gnews_headlines = [entry.title for entry in feed.entries[:5]]
    except Exception as e:
        logging.warning(f"Google News fehlgeschlagen ({symbol}): {e}")
        gnews_headlines = []

    combined = cp_headlines + gnews_headlines
    if not combined:
        return f"{symbol} price stable. No major news."
    return " ".join(combined)
