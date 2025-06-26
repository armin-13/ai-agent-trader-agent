from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_pipeline(text[:512])[0]
    return 1 if result["label"] == "POSITIVE" else -1
