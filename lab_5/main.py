import sys
from loguru import logger

from client import Client
from bank import Bank

logger.remove()
logger.add(sys.stderr, format="<level>{message}</level>", level="INFO")
logger.add("bank_system.log", rotation="1 MB", compression="zip", level="DEBUG",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

bank = Bank()
logger.info("Welcome to {}!", bank.name)
logger.info(f"System started")

running = True
while running:
    logger.info("\nChoose an option:\n1. Open new bank account\n2. Open existing bank account\n3. Exit")

    try:
        choice = int(input("1, 2 or 3: "))
    except ValueError:
        logger.error("Invalid input type (not a number)")
        continue

    if choice == 1:
        logger.info("To create an account, please fill in the information below.")
        name = input("Name: ")
        try:
            deposit = int(input("Deposit amount: "))
            client = Client(name, deposit)
            bank.update_db(client)
            logger.success("Account created successfully! Your account number is: {}", client.account['account_number'])
        except ValueError:
            logger.error("Invalid deposit amount")

    elif choice ==   2:
        logger.info("To access your account, please enter your credentials below.")
        name = input("Name: ")
        try:
            account_number = int(input("Account number: "))
            current_client = bank.authentication(name, account_number)
            if current_client:
                logger.info("Welcome {}!", current_client.account['name'])
                acc_open = True
                while acc_open:
                    logger.info("\nChoose an option:\n1. Withdraw\n2. Deposit\n3. Balance\n4. Exit")
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
                            logger.info("Thank you for visiting!")
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
        logger.info("Goodbye!")
        logger.info("System shutdown")
        running = False
