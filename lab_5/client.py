from random import randint
from loguru import logger


class Client:

    # {account_number: xxxxx, name: "xxxxxx", holdings: xxxx}

    def __init__(self, name, deposit):
        self.account = {}    #т.к. аккаунт должен быть у каждого свой
        self.account['account_number'] = randint(10000, 99999)
        self.account['name'] = name
        self.account['holdings'] = deposit
        logger.info(f"Created client {name}"
                    f" with account {self.account['account_number']}")

    def withdraw(self, amount):
        if self.account['holdings'] >= amount:
            self.account['holdings'] -= amount
            print()
            print("The sum of {} has been withdrawn from your account balance.".format(amount))
            logger.info(f"Account {self.account['account_number']}: "
                        f"Withdrawn {amount}. New balance: {self.account['holdings']}")
            self.balance()
        else:
            print()
            print("Not enough funds!")
            logger.warning(f"Account {self.account['account_number']}: "
                           "Failed to withdraw {amount}. Insufficient funds.")
            self.balance()

    def deposit(self, amount):
        self.account['holdings'] += amount
        print()
        print("The sum of {} has been added to your account balance.".format(amount))
        logger.info(f"Account {self.account['account_number']}: "
                    f"Deposit {amount}. New balance: {self.account['holdings']}")
        self.balance()

    def balance(self):
        print()
        print("Your current account balance is: {} ".format(self.account['holdings']))
        logger.debug(f"Account {self.account['account_number']}: "
                     "Balance check requested")
