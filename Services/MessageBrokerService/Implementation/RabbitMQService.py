from Services.MessageBrokerService.API.RoutedBrokerService import ExchangeQueueBrokerService
from Services.Logger.Implementation.Logging import Logging


class RabbitMQService(ExchangeQueueBrokerService):
    def __init__(self, conn):
        self.connector = conn

    def create_exchange(self, name, type="fanout"):
        try:
            self.connector.channel.exchange_declare(exchange=name, exchange_type=type)
        except Exception:
            Logging.error("Couldn't create exchange")

    def create_queue(self, name, ttl=0):
        try:
            arguments = {'x-message-ttl': ttl}
            self.connector.channel.queue_declare(queue=name, arguments=arguments)
        except Exception:
            Logging.error("Couldn't create queue")

    def bind(self, exchange, queue):
        try:
            self.connector.channel.queue_bind(exchange=exchange, queue=queue)
        except Exception:
            Logging.error("Couldn't bind exchange to queue")

    def publish(self, exchange, routing_key, message):
        try:
            self.connector.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        except Exception:
            Logging.error("Couldn't publish a given message!")
