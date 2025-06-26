from sentiment import analyze_sentiment
from news_fetcher import fetch_crypto_news
from trader import get_price
import random

def get_analysis():
    news = fetch_crypto_news()
    sentiment_score = analyze_sentiment(news)
    price = get_price()

    # این‌جا باید تحلیل تکنیکال دقیق‌تر اضافه شود
    if sentiment_score > 0.5:
        signal = "BUY"
    elif sentiment_score < -0.5:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "price": price,
        "signal": signal,
        "sentiment": sentiment_score,
        "news": news
    }
