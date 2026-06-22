import sqlite3

def get_context(query):
    conn = sqlite3.connect("data/circolari.db")
    c = conn.cursor()

    c.execute("SELECT json FROM circolari")
    rows = c.fetchall()

    return "\n".join([r[0] for r in rows])
