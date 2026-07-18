import os
import csv
import json

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
XQUIK_EXPORT_PATH = os.getenv("XQUIK_EXPORT_PATH")

TEXT_FIELDS = ("text", "full_text", "tweet", "content", "headline")
SOURCE_FIELDS = ("source", "author", "author_username", "username")
TIME_FIELDS = ("published_at", "created_at", "timestamp", "date")


def _first_value(row, fields, default=""):
    for field in fields:
        value = row.get(field)
        if value:
            return str(value)
    return default


def _load_json_rows(path):
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read().strip()
    if not text:
        return []
    if path.endswith((".jsonl", ".ndjson")):
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "results", "tweets", "posts"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []


def _load_export_rows(path):
    if path.endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    return _load_json_rows(path)


def fetch_xquik_export(path, company, page_size=10):
    articles = []
    query = company.lower()
    for row in _load_export_rows(path):
        if not isinstance(row, dict):
            continue
        headline = _first_value(row, TEXT_FIELDS).strip()
        if not headline or (query and query not in headline.lower()):
            continue
        articles.append({
            "headline": headline,
            "source": _first_value(row, SOURCE_FIELDS, "Xquik export"),
            "published_at": _first_value(row, TIME_FIELDS)
        })
        if len(articles) >= page_size:
            break
    return articles

def fetch_headlines(company, page_size=10):
    if XQUIK_EXPORT_PATH:
        return fetch_xquik_export(XQUIK_EXPORT_PATH, company, page_size)
    if not API_KEY:
        print("NEWS_API_KEY is missing. Set it or use XQUIK_EXPORT_PATH.")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params, timeout=20)
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
