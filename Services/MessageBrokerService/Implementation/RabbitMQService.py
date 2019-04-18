from Services.MessageBrokerService.API.RoutedBrokerService import ExchangeQueueBrokerService
from Services.Logger.Implementation.Logging import Logging
import time


class RabbitMQService(ExchangeQueueBrokerService):
    def __init__(self, conn, config):
        self.connector = conn
        self.config = config

    def create_exchange(self, name, type="fanout"):
        try:
            self.connector.channel.exchange_declare(exchange=name, exchange_type=type, durable=True)
        except AttributeError:
            Logging.error("Couldn't work with connection! Is RabbitMQ Server running? Reconnecting after {} secs."
                          .format(self.config["RMQ_RECONNECT_DELAY"]))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                                   self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                                   self.config["RABBITMQ_PASS"])
                    self.connector.channel.exchange_declare(exchange=name, exchange_type=type, durable=True)
                    flag = True
                except AttributeError:
                    Logging.error("Couldn't work with connection! Is RabbitMQ Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["RMQ_RECONNECT_DELAY"]))
        except Exception as err:
            Logging.error("Couldn't create exchange. Error: {}")

    def create_queue(self, name):
        try:
            self.connector.channel.queue_declare(queue=name, durable=True)
        except AttributeError:
            Logging.error("Couldn't work with connection! Is RabbitMQ Server running? Reconnecting after {} secs."
                          .format(self.config["RMQ_RECONNECT_DELAY"]))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                                   self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                                   self.config["RABBITMQ_PASS"])
                    self.connector.channel.queue_declare(queue=name, durable=True)
                    flag = True
                except AttributeError:
                    Logging.error("Couldn't work with connection! Is RabbitMQ Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["RMQ_RECONNECT_DELAY"]))
        except Exception:
            Logging.error("Couldn't create queue")

    def bind(self, exchange, queue, routing_key):
        try:
            self.connector.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
        except AttributeError:
            Logging.error("Couldn't work with connection! Is RabbitMQ Server running? Reconnecting after {} secs."
                          .format(self.config["RMQ_RECONNECT_DELAY"]))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                                   self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                                   self.config["RABBITMQ_PASS"])
                    self.connector.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
                    flag = True
                except AttributeError:
                    Logging.error("Couldn't work with connection! Is RabbitMQ Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["RMQ_RECONNECT_DELAY"]))
        except Exception:
            Logging.error("Couldn't bind exchange to queue")

    def publish(self, exchange, routing_key, message):
        try:
            self.connector.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        except AttributeError:
            Logging.error("Couldn't work with connection! Is RabbitMQ Server running? Reconnecting after {} secs."
                          .format(self.config["RMQ_RECONNECT_DELAY"]))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                                   self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                                   self.config["RABBITMQ_PASS"])
                    self.connector.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
                    flag = True
                except AttributeError:
                    Logging.error("Couldn't work with connection! Is RabbitMQ Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["RMQ_RECONNECT_DELAY"]))
        except Exception:
            Logging.error("Couldn't publish a given message!")
