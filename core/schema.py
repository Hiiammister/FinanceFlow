from core.db import get_conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('income','expense')),
        category TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0),
        note TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,                -- YYYY-MM
        category TEXT NOT NULL,
        budget_amount REAL NOT NULL CHECK(budget_amount >= 0),
        UNIQUE(month, category)
    )
    """)

    conn.commit()
    conn.close()
