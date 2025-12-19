import sys
from loguru import logger

from client import Client
from bank import Bank


logger.add("bank_system.log", rotation="1 MB", compression="zip", level="DEBUG")

bank = Bank()
print()
print("Welcome to {}!".format(bank.name))
logger.info(f"System started")
print()
running = True
while running:
    print()
    print("""Choose an option:
    
    1. Open new bank account
    2. Open existing bank account
    3. Exit
    """)

    try:
        choice = int(input("1, 2 or 3: "))
    except ValueError:
        logger.error("Invalid input type (not a number)")
        continue

    if choice == 1:
        print()
        print("To create an account, please fill in the information below.")
        print()
        name = input("Name: ")
        try:
            deposit = int(input("Deposit amount: "))
            client = Client(name, deposit)
            bank.update_db(client)
            print(f"\nAccount created successfully! "
                  f"Your account number is: {client.account['account_number']}")
        except ValueError:
            logger.error("Invalid deposit amount")

    elif choice ==   2:
        print()
        print("To access your account, please enter your credentials below.")
        print()
        name = input("Name: ")
        try:
            account_number = int(input("Account number: "))
            current_client = bank.authentication(name, account_number)
            if current_client:
                print(f"\nWelcome {current_client.account['name']}!")
                acc_open = True
                while acc_open:
                    print(
                        "\nChoose an option:\n1. Withdraw\n2. Deposit\n3. Balance\n4. Exit")
                    try:
                        acc_choice = int(input("1, 2, 3 or 4: "))
                        if acc_choice == 1:
                            amt = int(input("Withdraw amount: "))
                            current_client.withdraw(amt)
                        elif acc_choice == 2:
                            amt = int(input("Deposit amount: "))
                            current_client.deposit(amt)
                        elif acc_choice == 3:
                            current_client.balance()
                        elif acc_choice == 4:
                            print("\nThank you for visiting!")
                            current_client = ''
                            acc_open = False
                            logger.info("User logged out")
                    except ValueError:
                        logger.error("Invalid input in account menu")
            else:
                print("\nAuthentication failed!\nReason: account not found.")
        except ValueError:
            logger.error("Invalid input for account number")

    elif choice == 3:
        print()
        print("Goodbye!")
        logger.info("System shutdown")
        running = False
