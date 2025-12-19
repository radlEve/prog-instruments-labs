from loguru import logger


class Bank:
    def __init__(self):
        self.name = 'International Bank'
        self.clients = []

    def update_db(self, client):
        self.clients.append(client)
        logger.debug(f"Database updated. Total clients: {len(self.clients)}")

    def authentication(self, name, account_number):
        for client in self.clients:
            if client.account['name'] == name and client.account[
                'account_number'] == account_number:
                logger.success(f"Auth successful for user: {name}")
                return client

        logger.error(
            f"Authentication failed for user: {name}, account: {account_number}")
        return None
