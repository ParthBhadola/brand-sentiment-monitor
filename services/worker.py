import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime
from dotenv import load_dotenv
from services.fetcher import fetch_headlines
from services.scorer import score_sentiment
from db import init_db, insert_headline, get_recent

load_dotenv()

def process_company(company):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Fetching headlines for {company}...")
    headlines = fetch_headlines(company, page_size=5)

    if not headlines:
        print(f"No headlines found for {company}")
        return 0

    existing = get_recent(company, limit=100)
    existing_headlines = {row[0] for row in existing}

    new_count = 0
    for article in headlines:
        if article["headline"] in existing_headlines:
            continue

        result = score_sentiment(article["headline"], company)
        insert_headline(
            company=company,
            headline=article["headline"],
            source=article["source"],
            published_at=article["published_at"],
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            scored_at=datetime.now().isoformat()
        )
        new_count += 1
        print(f"  [{result['sentiment']}] {article['headline'][:80]}...")

    print(f"  Stored {new_count} new headlines for {company}")
    return new_count