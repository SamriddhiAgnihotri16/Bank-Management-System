from database import connect_db


def create_account():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    balance = float(input("Initial Deposit: "))

    cursor.execute(
        "INSERT INTO accounts (name, phone, balance) VALUES (?, ?, ?)",
        (name, phone, balance)
    )

    account_no = cursor.lastrowid

    cursor.execute(
        "INSERT INTO transactions (account_no, transaction_type, amount) VALUES (?, ?, ?)",
        (account_no, "Deposit", balance)
    )

    conn.commit()
    conn.close()

    print("\n✅ Account Created Successfully!")
    print("Account Number:", account_no)


def deposit():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n========== DEPOSIT MONEY ==========")

    account_no = int(input("Enter Account Number: "))
    amount = float(input("Enter Amount: "))

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=?",
        (account_no,)
    )

    data = cursor.fetchone()

    if data is None:
        print("❌ Account Not Found")
        conn.close()
        return

    new_balance = data[0] + amount

    cursor.execute(
        "UPDATE accounts SET balance=? WHERE account_no=?",
        (new_balance, account_no)
    )

    cursor.execute(
        "INSERT INTO transactions(account_no, transaction_type, amount) VALUES (?, ?, ?)",
        (account_no, "Deposit", amount)
    )

    conn.commit()
    conn.close()

    print("✅ Deposit Successful")


def withdraw():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n========== WITHDRAW MONEY ==========")

    account_no = int(input("Enter Account Number: "))
    amount = float(input("Enter Amount: "))

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=?",
        (account_no,)
    )

    data = cursor.fetchone()

    if data is None:
        print("❌ Account Not Found")
        conn.close()
        return

    balance = data[0]

    if amount > balance:
        print("❌ Insufficient Balance")
        conn.close()
        return

    new_balance = balance - amount

    cursor.execute(
        "UPDATE accounts SET balance=? WHERE account_no=?",
        (new_balance, account_no)
    )

    cursor.execute(
        "INSERT INTO transactions(account_no, transaction_type, amount) VALUES (?, ?, ?)",
        (account_no, "Withdraw", amount)
    )

    conn.commit()
    conn.close()

    print("✅ Withdrawal Successful")


def check_balance():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n========== CHECK BALANCE ==========")

    account_no = int(input("Enter Account Number: "))

    cursor.execute(
        "SELECT * FROM accounts WHERE account_no=?",
        (account_no,)
    )

    data = cursor.fetchone()

    conn.close()

    if data is None:
        print("❌ Account Not Found")
    else:
        print("\n========== ACCOUNT DETAILS ==========")
        print("Account Number :", data[0])
        print("Name           :", data[1])
        print("Phone          :", data[2])
        print("Balance        :", data[3])