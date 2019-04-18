from Services.MessageBrokerConsumer.API.MessageConsumer import MessageConsumer
from Services.Logger.Implementation.Logging import Logging
from Proto.OrderRecord_pb2 import OrderRecord
from Utils.FormatConverter import FormatConverter
from ReportData.ReportData import ReportData
from google.protobuf.message import DecodeError
from pika import exceptions
import datetime
import threading
import time


class RabbitMQMessageConsumer(MessageConsumer):
    def __init__(self, conn, config, db_service):
        self.connector = conn
        self.channel = None
        self.config = config
        self.db_service = db_service
        self.last_call_time = datetime.datetime.now()
        self.current_queries_batch = []

    def __callback(self, channel, method, header, body):
        try:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            self.last_call_time = datetime.datetime.now()
        except (exceptions.ChannelWrongStateError, exceptions.StreamLostError,
                exceptions.ConnectionWrongStateError):
            Logging.error("Couldn't work with connection! Is RabbitMQ Server running? Reconnecting after {} secs."
                          .format(self.config["RMQ_RECONNECT_DELAY"]))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                                   self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                                   self.config["RABBITMQ_PASS"])
                    channel = self.connector.connection.channel()
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    self.last_call_time = datetime.datetime.now()
                    flag = True
                except (exceptions.ChannelWrongStateError, exceptions.StreamLostError,
                        exceptions.ConnectionWrongStateError):
                    Logging.error("Couldn't work with connection! Is RabbitMQ Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["RMQ_RECONNECT_DELAY"]))

        obj = OrderRecord()
        try:
            obj.ParseFromString(body)
            Logging.info("Message received: {}".format(obj))
            ReportData.received_from_rabbit += 1
        except DecodeError as err:
            Logging.error("Couldn't parse proto message. Error: {}".format(err.__str__()))

        if len(self.current_queries_batch) < self.config["SQL_BATCH_SIZE"]:
            rec = FormatConverter.convert_proto_to_rec(obj)
            self.current_queries_batch.append(FormatConverter.convert_rec_to_sql_query(rec))
        else:
            self.db_service.execute_many(self.current_queries_batch)
            self.current_queries_batch = []
            rec = FormatConverter.convert_proto_to_rec(obj)
            self.current_queries_batch.append(FormatConverter.convert_rec_to_sql_query(rec))

    def consume(self):
        try:
            self.channel = self.connector.connection.channel()
            self.channel.basic_consume("New", self.__callback)
            self.channel.basic_consume("ToProvide", self.__callback)
            self.channel.basic_consume("Reject", self.__callback)
            self.channel.basic_consume("PartialFilled", self.__callback)
            self.channel.basic_consume("Filled", self.__callback)
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
                    self.channel = self.connector.connection.channel()
                    self.channel.basic_consume("New", self.__callback)
                    self.channel.basic_consume("ToProvide", self.__callback)
                    self.channel.basic_consume("Reject", self.__callback)
                    self.channel.basic_consume("PartialFilled", self.__callback)
                    self.channel.basic_consume("Filled", self.__callback)
                    flag = True
                except AttributeError:
                    Logging.error("Couldn't work with connection! Is RabbitMQ Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["RMQ_RECONNECT_DELAY"]))

        thread_consumer = threading.Thread(target=self.channel.start_consuming, args=(), name="Consumer")
        thread_consumer.start()

        thread_timer = threading.Thread(target=self.__timer, args=(), name="Timer")
        thread_timer.daemon = True
        thread_timer.start()

        thread_consumer.join()

    def __timer(self):
        cycle = True
        while cycle:
            if (datetime.datetime.now() - self.last_call_time).total_seconds() >= 1:
                Logging.warn("Inserting last batch (not full)")
                self.db_service.execute_many(self.current_queries_batch)
                self.current_queries_batch = []
                try:
                    self.channel.basic_cancel(consumer_tag="hello-consumer")
                    self.channel.stop_consuming()
                except:
                    pass
                cycle = False
