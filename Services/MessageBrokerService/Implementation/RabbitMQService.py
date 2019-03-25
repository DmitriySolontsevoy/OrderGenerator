from Services.MessageBrokerService.API.ExchangeQueueBrokerService import ExchangeQueueBrokerService
import pika


class RabbitMQService(ExchangeQueueBrokerService):
    def __init__(self):
        self.channel = None

    def open_connection(self, host, port, vhost, user, password):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, vhost=vhost,
                                                                            user=user, password=password))
        self.channel = self.connection.channel()

    def create_exchange(self, name, type):
        self.channel.exchange_declare(exchange=name, exchange_type=type)

    def create_queue(self, name):
        self.channel.queue_declare(queue=name)

    def bind(self, exchange, queue, key):
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=key)

    def publish(self, exchange, key, message):
        self.channel.basic_publish(exchange=exchange, routing_key=key, body=message)
