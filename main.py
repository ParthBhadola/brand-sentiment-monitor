import logging
import time
from fastapi import FastAPI
from db import init_db, get_recent, get_sentiment_counts, get_companies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Brand Sentiment Monitor API",
    description="Real-time brand sentiment monitoring using LLM scoring",
    version="1.0.0"
)

init_db()

@app.get("/")
def home():
    return {"message": "Brand Sentiment Monitor is running"}

@app.get("/health")
def health():
    companies = get_companies()
    return {
        "status": "healthy",
        "companies_tracked": len(companies),
        "companies": companies
    }

@app.get("/sentiment/{company}")
def get_sentiment(company: str, limit: int = 20):
    start = time.time()
    logger.info(f"Sentiment request for {company}")

    headlines = get_recent(company, limit=limit)
    counts = get_sentiment_counts(company)

    total = sum(counts.values())
    positive = counts.get("POSITIVE", 0)
    negative = counts.get("NEGATIVE", 0)
    neutral = counts.get("NEUTRAL", 0)

    if total > 0:
        score = round((positive - negative) / total * 100, 1)
    else:
        score = 0

    results = []
    for row in headlines:
        results.append({
            "headline": row[0],
            "source": row[1],
            "published_at": row[2],
            "sentiment": row[3],
            "confidence": row[4],
            "scored_at": row[5]
        })

    response_time = round((time.time() - start) * 1000, 2)

    return {
        "company": company,
        "sentiment_score": score,
        "total_headlines": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "headlines": results,
        "response_time_ms": response_time
    }

@app.get("/companies")
def companies():
    return {"companies": get_companies()}