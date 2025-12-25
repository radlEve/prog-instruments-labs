from loguru import logger


class Bank:

    name = 'International Bank'
    clients = []

    def update_db(self, client):
        self.clients.append(client)
        logger.debug("Database updated. Total clients: {}", len(self.clients))

    def authentication(self, name, account_number):
        for i in range(len(self.clients)):
            if name in self.clients[i].account.values() and account_number in self.clients[i].account.values():
                logger.success("Auth successful for user: {}", name)
                return self.clients[i]
        logger.error("Authentication failed for user: {}, account: {}",
                     name, account_number)
        return None
