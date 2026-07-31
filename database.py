import sqlite3

DATABASE="bank.db"

def get_connection():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    return conn

def create_tables():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT UNIQUE,
        full_name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        pin TEXT,
        balance REAL DEFAULT 0
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT,
        transaction_type TEXT,
        amount REAL,
        balance_after REAL,
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

if __name__=="__main__":
    create_tables()
