import argparse
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from config import NEWS_API_KEY
from database import init_db, insert_news

def fetch_newsapi(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()

    news = []
    for article in response.get("articles", []):
        news.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "published": article["publishedAt"],
            "url": article["url"]
        })
    return news

def scrape_bbc():
    url = "https://www.bbc.com/news"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    news = []
    for h3 in soup.select("h3")[:10]:
        news.append({
            "title": h3.get_text(),
            "source": "BBC",
            "published": "N/A",
            "url": url
        })
    return news

def save_json(data):
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def export_data(data, filetype):
    df = pd.DataFrame(data)
    if filetype == "csv":
        df.to_csv("news.csv", index=False)
    elif filetype == "excel":
        df.to_excel("news.xlsx", index=False)

def main():
    parser = argparse.ArgumentParser(description="News Aggregator CLI")
    parser.add_argument("--keyword", help="Search keyword")
    parser.add_argument("--source", choices=["newsapi", "bbc"], help="News source")
    parser.add_argument("--export", choices=["csv", "excel"], help="Export format")

    args = parser.parse_args()
    init_db()

    all_news = []

    if args.source == "newsapi" and args.keyword:
        all_news.extend(fetch_newsapi(args.keyword))

    if args.source == "bbc":
        all_news.extend(scrape_bbc())

    insert_news(all_news)
    save_json(all_news)

    if args.export:
        export_data(all_news, args.export)

    print(f"✅ {len(all_news)} news articles processed successfully")


if __name__ == "__main__":
    main()
