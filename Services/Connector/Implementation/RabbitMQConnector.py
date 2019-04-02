from Services.Logger.Implementation.Logging import Logging
from Services.Connector.API.Connector import Connector
import pika


class RabbitMQConnector(Connector):
    def __init__(self):
        self.connection = None
        self.channel = None

    def open_connection(self, host, port, virtual_host, user, password):
        try:
            credentials = pika.PlainCredentials(username=user, password=password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port,
                                                                                virtual_host=virtual_host,
                                                                                credentials=credentials))
            self.channel = self.connection.channel()
            return True
        except Exception as err:
            Logging.error("Couldn't establish RMQ connection!")
            return False

    def close_connection(self, **kwargs):
        try:
            self.connection.close()
        except Exception as err:
            Logging.warn("Couldn't close RMQ connection!")

    def is_alive(self, **kwargs):
        return self.connection.is_open
