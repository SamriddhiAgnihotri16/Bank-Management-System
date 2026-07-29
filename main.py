from database import create_tables
from account import create_account, deposit, withdraw, check_balance
from transaction import transaction_history


def menu():
    while True:
        print("\n====================================")
        print("     BANK MANAGEMENT SYSTEM")
        print("====================================")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            deposit()

        elif choice == "3":
            withdraw()

        elif choice == "4":
            check_balance()

        elif choice == "5":
            transaction_history()

        elif choice == "6":
            print("\nThank You For Using Bank Management System")
            break

        else:
            print("\nInvalid Choice")


if __name__ == "__main__":
    print("Starting Bank Management System...")
    create_tables()
    menu()