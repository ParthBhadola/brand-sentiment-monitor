import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def fetch_headlines(company, page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print(f"API error: {data.get('message')}")
        return []

    articles = []
    for article in data.get("articles", []):
        if article.get("title") and article["title"] != "[Removed]":
            articles.append({
                "headline": article["title"],
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": article.get("publishedAt", "")
            })
    return articles

if __name__ == "__main__":
    results = fetch_headlines("Zomato")
    print(f"Fetched {len(results)} headlines\n")
    for r in results:
        print(f"[{r['source']}] {r['headline']}")