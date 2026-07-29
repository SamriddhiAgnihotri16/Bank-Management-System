import sqlite3

DATABASE_NAME = "bank.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        account_no INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        balance REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_no INTEGER,
        transaction_type TEXT,
        amount REAL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(account_no) REFERENCES accounts(account_no)
    )
    """)

    conn.commit()
    conn.close()