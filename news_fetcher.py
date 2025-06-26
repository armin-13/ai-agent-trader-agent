import requests

def fetch_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=demo&currencies=BTC"
    try:
        response = requests.get(url)
        data = response.json()
        headlines = [item["title"] for item in data["results"][:5]]
        return " ".join(headlines)
    except:
        return "Bitcoin price stable. Market waiting for next move."
