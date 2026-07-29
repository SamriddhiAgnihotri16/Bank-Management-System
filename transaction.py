from database import connect_db


def transaction_history():

    conn = connect_db()
    cursor = conn.cursor()

    print("\n========== TRANSACTION HISTORY ==========\n")

    account = int(input("Enter Account Number : "))

    cursor.execute(
        """
        SELECT account_no
        FROM accounts
        WHERE account_no=?
        """,
        (account,),
    )

    check = cursor.fetchone()

    if check is None:

        print("\nAccount Not Found")
        conn.close()
        return

    cursor.execute(
        """
        SELECT transaction_type,
               amount,
               transaction_date
        FROM transactions
        WHERE account_no=?
        ORDER BY transaction_date
        """,
        (account,),
    )

    records = cursor.fetchall()

    if len(records) == 0:

        print("\nNo Transactions Found")

    else:

        print("\n==============================================")
        print("TYPE\t\tAMOUNT\t\tDATE")
        print("==============================================")

        for row in records:
            print(f"{row[0]}\t\t₹{row[1]}\t\t{row[2]}")

    conn.close()