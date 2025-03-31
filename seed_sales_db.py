# seed_sales_db.py

import sqlite3
import csv
import os

DB_PATH = os.path.join("data", "app.db")
CSV_PATH = os.path.join("data", "sales.csv")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total INTEGER NOT NULL,
            refunds INTEGER NOT NULL
        );
    """)

    # Optional: Clear table first (to avoid duplicates if you run it again)
    cursor.execute("DELETE FROM sales")

    # Load from CSV
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [(row["date"], int(row["total"]), int(row["refunds"])) for row in reader]

    cursor.executemany("INSERT INTO sales (date, total, refunds) VALUES (?, ?, ?)", rows)

    conn.commit()
    conn.close()
    print(f"✅ Seeded {len(rows)} rows into {DB_PATH}")

if __name__ == "__main__":
    init_db()
