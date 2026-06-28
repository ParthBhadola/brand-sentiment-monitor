import sqlite3
import os

DB_PATH = "data/sentiment.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS headlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            headline TEXT,
            source TEXT,
            published_at TEXT,
            sentiment TEXT,
            confidence REAL,
            scored_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_headline(company, headline, source, published_at, sentiment, confidence, scored_at):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO headlines
        (company, headline, source, published_at, sentiment, confidence, scored_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (company, headline, source, published_at, sentiment, confidence, scored_at))
    conn.commit()
    conn.close()

def get_recent(company, limit=50):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT headline, source, published_at, sentiment, confidence, scored_at
        FROM headlines
        WHERE company = ?
        ORDER BY scored_at DESC
        LIMIT ?
    """, (company, limit)).fetchall()
    conn.close()
    return rows

def get_sentiment_counts(company):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT sentiment, COUNT(*) as count
        FROM headlines
        WHERE company = ?
        GROUP BY sentiment
    """, (company,)).fetchall()
    conn.close()
    return dict(rows)

def get_companies():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT DISTINCT company FROM headlines").fetchall()
    conn.close()
    return [r[0] for r in rows]