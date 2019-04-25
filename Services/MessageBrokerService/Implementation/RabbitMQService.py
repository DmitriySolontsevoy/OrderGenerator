from Services.MessageBrokerService.API.RoutedBrokerService import ExchangeQueueBrokerService
from Services.Logger.Implementation.Logging import Logging
import time


class RabbitMQService(ExchangeQueueBrokerService):
    def __init__(self, conn, config):
        self.connector = conn
        self.config = config

    def create_exchange(self, name, type="topic"):
        connected = self.connector.is_alive()
        if connected:
            self.connector.channel.exchange_declare(exchange=name, exchange_type=type, durable=True)
        else:
            while not connected:
                Logging.error("Couldn't create exchange due to a closed connection! Retrying after {}s."
                              .format(self.config["RMQ_RECONNECT_DELAY"]))
                time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                               self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                               self.config["RABBITMQ_PASS"])
                connected = self.connector.is_alive()
            self.create_exchange(name, type)

    def create_queue(self, name):
        connected = self.connector.is_alive()
        if connected:
            self.connector.channel.queue_declare(queue=name, durable=True)
        else:
            while not connected:
                Logging.error("Couldn't create queue due to a closed connection! Retrying after {}s."
                              .format(self.config["RMQ_RECONNECT_DELAY"]))
                time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                               self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                               self.config["RABBITMQ_PASS"])
                connected = self.connector.is_alive()
            self.create_queue(name)

    def bind(self, exchange, queue, routing_key):
        connected = self.connector.is_alive()
        if connected:
            self.connector.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
        else:
            while not connected:
                Logging.error("Couldn't bind exchange to a queue due to a closed connection! Retrying after {}s."
                              .format(self.config["RMQ_RECONNECT_DELAY"]))
                time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                               self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                               self.config["RABBITMQ_PASS"])
                connected = self.connector.is_alive()
            self.bind(exchange, queue, routing_key)

    def publish(self, exchange, routing_key, message):
        connected = self.connector.is_alive()
        if connected:
            self.connector.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        else:
            while not connected:
                Logging.error("Couldn't publish a message to a queue due to a closed connection! Retrying after {}s."
                              .format(self.config["RMQ_RECONNECT_DELAY"]))
                time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                               self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                               self.config["RABBITMQ_PASS"])
                connected = self.connector.is_alive()
            self.publish(exchange, routing_key, message)
