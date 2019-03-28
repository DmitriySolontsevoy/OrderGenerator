from Services.MessageBrokerService.API.RoutedBrokerService import ExchangeQueueBrokerService
from Services.Logger.Implementation.Logging import Logging
import pika


class RabbitMQService(ExchangeQueueBrokerService):
    def __init__(self, conn):
        self.connection = conn
        self.channel = self.connection.channel()

    def create_exchange(self, name, type):
        self.channel.exchange_declare(exchange=name, exchange_type=type)

    def create_queue(self, name, ttl):
        arguments = {'x-message-ttl': ttl}
        self.channel.queue_declare(queue=name, arguments=arguments)

    def bind(self, exchange, queue, routing_key):
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

    def publish(self, exchange, routing_key, message):
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
