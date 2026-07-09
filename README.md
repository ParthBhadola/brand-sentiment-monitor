# Pulse - Real-Time Brand Sentiment Monitor

Track how the news feels about Indian brands in real time.
Headlines are fetched automatically, scored by an LLM and displayed on a live dashboard.

---

## What it does

- Fetches live news headlines for Indian companies every 30 minutes
- Scores each headline as Positive, Negative or Neutral using Groq LLaMA
- Stores all results in SQLite with confidence scores and timestamps
- Displays a live Streamlit dashboard that auto-refreshes
- Serves sentiment data via a FastAPI REST API

---

## System Architecture
News API

↓

services/fetcher.py - fetch latest headlines per company

↓

services/scorer.py - LLM scores each headline (Positive/Negative/Neutral)

↓

db.py - store results in SQLite

↓

FastAPI - serve sentiment data as REST API

↓

Streamlit - live dashboard auto-refreshing every 30 seconds

---

## Companies Tracked

Zomato · Swiggy · Paytm · Razorpay · PhonePe

---

## Tech Stack

| Layer | Tool |
|---|---|
| News data | NewsAPI |
| Sentiment scoring | Groq LLaMA 3.3 70B |
| Database | SQLite |
| Pipeline scheduling | Python schedule |
| Backend API | FastAPI |
| Frontend | Streamlit |

---

## Project Structure
brand-sentiment-monitor/

services/

fetcher.py      - fetch headlines from NewsAPI

scorer.py       - LLM-based sentiment scoring

worker.py       - continuous pipeline runner

db.py               - SQLite database operations

main.py             - FastAPI REST API

app.py              - Streamlit live dashboard

data/               - SQLite database (gitignored)

logs/               - pipeline logs (gitignored)

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/ParthBhadola/brand-sentiment-monitor.git
cd brand-sentiment-monitor
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add API keys to .env**
```dotenv
NEWS_API_KEY=<newsapi key>
GROQ_API_KEY=<groq key>
```

To score a reviewed Xquik or TweetClaw export instead of NewsAPI headlines,
set `XQUIK_EXPORT_PATH` to a CSV, JSON, JSONL, or NDJSON file:

```dotenv
XQUIK_EXPORT_PATH=./exports/xquik-posts.csv
```

The importer reads common text fields such as `text`, `full_text`, `tweet`,
`content`, or `headline`, then maps public author/source and timestamp fields
into the same scoring pipeline.

References:

- Xquik docs: <https://docs.xquik.com>
- TweetClaw repository: <https://github.com/Xquik-dev/tweetclaw>

**4. Run the pipeline**
```bash
python services/worker.py
```

**5. Run the dashboard**
```bash
streamlit run app.py
```

**6. Run the API**
```bash
uvicorn main:app --reload
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| / | GET | Health check |
| /health | GET | System status and companies tracked |
| /sentiment/{company} | GET | Sentiment data for a company |
| /companies | GET | List all tracked companies |

---

## Key Technical Decisions

**Why LLM scoring over traditional sentiment analysis?**
Traditional tools like VADER or TextBlob do keyword matching.
They cannot understand context - "Zomato loses market share to Swiggy"
would score neutral because no negative keywords exist.
LLaMA understands the business implication and scores it negative correctly.

**Why SQLite over PostgreSQL?**
SQLite is zero-configuration, file-based and sufficient for
a single-node monitoring system. For production scale with
multiple workers, PostgreSQL would be the right choice.

**Why schedule over Celery?**
Celery requires a message broker like Redis or RabbitMQ.
For a 30-minute polling interval, Python schedule is simpler
and has zero infrastructure overhead. Celery would be chosen
for sub-minute scheduling or distributed workers.
