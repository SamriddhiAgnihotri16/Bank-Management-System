from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import random
from contextlib import closing

app = Flask(__name__)
app.secret_key = "bank_secret_key_123"

DATABASE = "bank.db"


def get_connection():
    conn = sqlite3.connect(DATABASE, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT UNIQUE,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            pin TEXT NOT NULL,
            balance REAL DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            transaction_type TEXT,
            amount REAL,
            balance_after REAL,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()


create_tables()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()
        pin = request.form["pin"].strip()
        balance = float(request.form["balance"])

        account_number = str(random.randint(10000000, 99999999))

        with closing(get_connection()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE email=?",
                (email,)
            )

            if cursor.fetchone():
                flash("Email already registered!")
                return redirect(url_for("register"))

            while True:

                cursor.execute(
                    "SELECT * FROM users WHERE account_number=?",
                    (account_number,)
                )

                if cursor.fetchone() is None:
                    break

                account_number = str(random.randint(10000000, 99999999))

            cursor.execute("""
            INSERT INTO users
            (account_number, full_name, email, phone, pin, balance)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                account_number,
                full_name,
                email,
                phone,
                pin,
                balance
            ))

            conn.commit()

        return render_template(
            "account_created.html",
            account_number=account_number
        )

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        account_number = request.form["account_number"].strip()
        pin = request.form["pin"].strip()

        with closing(get_connection()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE account_number=? AND pin=?",
                (account_number, pin)
            )

            user = cursor.fetchone()

        if user:
            session["account_number"] = user["account_number"]
            return redirect(url_for("dashboard"))

        flash("Invalid Account Number or PIN")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "account_number" not in session:
        return redirect(url_for("login"))

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE account_number=?",
            (session["account_number"],)
        )

        user = cursor.fetchone()

    return render_template("dashboard.html", user=user)


@app.route("/deposit", methods=["GET", "POST"])
def deposit():

    if "account_number" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = float(request.form["amount"])

        if amount <= 0:
            flash("Enter a valid amount.")
            return redirect(url_for("deposit"))

        with closing(get_connection()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance FROM users WHERE account_number=?",
                (session["account_number"],)
            )

            balance = cursor.fetchone()["balance"]

            new_balance = balance + amount

            cursor.execute(
                "UPDATE users SET balance=? WHERE account_number=?",
                (new_balance, session["account_number"])
            )

            cursor.execute("""
                INSERT INTO transactions
                (account_number, transaction_type, amount, balance_after)
                VALUES(?,?,?,?)
            """, (
                session["account_number"],
                "Deposit",
                amount,
                new_balance
            ))

            conn.commit()

        flash("Amount deposited successfully.")
        return redirect(url_for("dashboard"))

    return render_template("deposit.html")


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():

    if "account_number" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = float(request.form["amount"])

        with closing(get_connection()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance FROM users WHERE account_number=?",
                (session["account_number"],)
            )

            balance = cursor.fetchone()["balance"]

            if amount > balance:

                flash("Insufficient Balance")
                return redirect(url_for("withdraw"))

            new_balance = balance - amount

            cursor.execute(
                "UPDATE users SET balance=? WHERE account_number=?",
                (new_balance, session["account_number"])
            )

            cursor.execute("""
                INSERT INTO transactions
                (account_number, transaction_type, amount, balance_after)
                VALUES(?,?,?,?)
            """, (
                session["account_number"],
                "Withdraw",
                amount,
                new_balance
            ))

            conn.commit()

        flash("Withdrawal successful.")
        return redirect(url_for("dashboard"))

    return render_template("withdraw.html")
@app.route("/transactions")
def transactions():

    if "account_number" not in session:
        return redirect(url_for("login"))

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM transactions
            WHERE account_number=?
            ORDER BY date_time DESC
        """, (session["account_number"],))

        transaction_list = cursor.fetchall()

    return render_template(
        "transactions.html",
        transactions=transaction_list
    )


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    return "<h2>404 - Page Not Found</h2>", 404


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )