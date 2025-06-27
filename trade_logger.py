# trade_logger.py

import sqlite3
from datetime import datetime

# Initialisiere die Datenbank und Tabelle (wird einmal beim Start ausgeführt)
def init_db():
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            action TEXT,
            price REAL,
            sentiment REAL,
            rsi REAL,
            macd TEXT
        )
    """)
    conn.commit()
    conn.close()


# Speichert einen einzelnen Trade in der DB
def log_trade(symbol, action, price, sentiment, rsi, macd):
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trades (timestamp, symbol, action, price, sentiment, rsi, macd)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        symbol,
        action,
        price,
        sentiment,
        rsi,
        macd
    ))
    conn.commit()
    conn.close()


# Gibt die letzten N Trades zurück
def get_recent_trades(limit=10):
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT ?", (limit,))
    trades = cursor.fetchall()
    conn.close()
    return trades


if __name__ == "__main__":
    init_db()
    print("Letzte Trades:")
    for trade in get_recent_trades():
        print(trade)
