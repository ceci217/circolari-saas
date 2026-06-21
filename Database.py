import sqlite3
import json

def init_db():
    conn = sqlite3.connect("data/circolari.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS circolari (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titolo TEXT,
        ente TEXT,
        json TEXT
    )
    """)

    conn.commit()
    conn.close()


def save(title, ente, json_data):
    conn = sqlite3.connect("data/circolari.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO circolari VALUES (NULL, ?, ?, ?)",
        (title, ente, json.dumps(json_data))
    )

    conn.commit()
    conn.close()
