from random import randint
from loguru import logger


class Client:
    def __init__(self, name, deposit):
        self.account = {}
        self.account['account_number'] = randint(10000, 99999)
        self.account['name'] = name
        self.account['holdings'] = deposit
        logger.info(
            f"Created client {name} with account {self.account['account_number']}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if self.account['holdings'] >= amount:
            self.account['holdings'] -= amount
            logger.info(
                f"Account {self.account['account_number']}: Withdrawn {amount}. New balance: {self.account['holdings']}")
            return self.account['holdings']
        else:
            logger.warning(
                f"Account {self.account['account_number']}: Failed to withdraw {amount}. Insufficient funds.")
            raise ValueError("Not enough funds")

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.account['holdings'] += amount
        logger.info(
            f"Account {self.account['account_number']}: Deposit {amount}. New balance: {self.account['holdings']}")
        return self.account['holdings']

    def transfer(self, other_client, amount):
        if not isinstance(other_client, Client):
            raise TypeError("Target must be a Client object")

        self.withdraw(amount)
        other_client.deposit(amount)
        logger.info(
            f"Transferred {amount} from {self.account['account_number']} to {other_client.account['account_number']}")
        return True

    def get_balance(self):
        logger.debug(
            f"Account {self.account['account_number']}: Balance check requested")
        return self.account['holdings']
