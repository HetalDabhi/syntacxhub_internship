import sqlite3

def init_db():
    conn = sqlite3.connect("news.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            title TEXT UNIQUE,
            source TEXT,
            published TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_news(data):
    conn = sqlite3.connect("news.db")
    cur = conn.cursor()

    for item in data:
        try:
            cur.execute(
                "INSERT INTO news VALUES (?, ?, ?, ?)",
                (item["title"], item["source"], item["published"], item["url"])
            )
        except sqlite3.IntegrityError:
            pass  

    conn.commit()
    conn.close()
