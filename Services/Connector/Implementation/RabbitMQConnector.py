from Services.Logger.Implementation.Logging import Logging
from Services.Connector.API.Connector import Connector
import pika


class RabbitMQConnector(Connector):
    def __init__(self):
        self.connection = None

    def open_connection(self, host, port, vhost, user, password):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, vhost=vhost,
                                                                                user=user, password=password))
        except Exception as err:
            pass

    def close_connection(self, **kwargs):
        try:
            self.connection.close()
        except Exception as err:
            pass

    def is_alive(self, **kwargs):
        return self.connection.is_open
