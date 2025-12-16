import sqlite3

def init_db():
    conn = sqlite3.connect("ticks.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            qty REAL
        )
    """)
    conn.commit()
    conn.close()
