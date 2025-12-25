from random import randint
from loguru import logger


class Client:

    # {account_number: xxxxx, name: "xxxxxx", holdings: xxxx}

    def __init__(self, name, deposit):
        self.account = {}    #т.к. аккаунт должен быть у каждого свой
        self.account['account_number'] = randint(10000, 99999)
        self.account['name'] = name
        self.account['holdings'] = deposit
        logger.info("Created client {} with account {}", name,
                    self.account['account_number'])

    def withdraw(self, amount):
        if self.account['holdings'] >= amount:
            self.account['holdings'] -= amount
            logger.info("Account {}: Withdrawn {}. New balance: {}",
                        self.account['account_number'], amount,
                        self.account['holdings'])
            self.balance()
        else:
            logger.warning(
                "Account {}: Failed to withdraw {}. Insufficient funds.",
                self.account['account_number'], amount)
            self.balance()

    def deposit(self, amount):
        self.account['holdings'] += amount
        logger.info("Account {}: Deposit {}. New balance: {}",
                    self.account['account_number'], amount,
                    self.account['holdings'])
        self.balance()

    def balance(self):
        logger.info("Account {}: Current balance is {}",
                    self.account['account_number'], self.account['holdings'])
