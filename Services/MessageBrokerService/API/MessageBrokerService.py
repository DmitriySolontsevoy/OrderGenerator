import abc


class MessageBrokerService:
    connection = None

    @abc.abstractmethod
    def open_connection(self, host, port, vhost, user, password):
        pass

    def close_connection(self):
        self.connection.close()
