from Services.MessageBrokerConsumer.API.MessageConsumer import MessageConsumer
from Services.Logger.Implementation.Logging import Logging
from Proto.OrderRecord_pb2 import OrderRecord
from Utils.FormatConverter import FormatConverter
from ReportData.ReportData import ReportData
from google.protobuf.message import DecodeError
import datetime
import threading
import time


class RabbitMQMessageConsumer(MessageConsumer):
    def __init__(self, conn, config, db_service, stop_consume_event):
        self.connector = conn
        self.channel = None
        self.config = config
        self.db_service = db_service
        self.last_call_time = datetime.datetime.now()
        self.current_queries_batch = []
        self.stop_consume_event = stop_consume_event

    def __callback(self, channel, method, header, body):
        connected = self.connector.is_alive()
        if connected:
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

            channel.basic_ack(delivery_tag=method.delivery_tag)
            self.last_call_time = datetime.datetime.now()
        else:
            while not connected:
                Logging.error("Couldn't consume a message consuming due to a closed connection! Retrying after {}s."
                              .format(self.config["RMQ_RECONNECT_DELAY"]))
                time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                               self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                               self.config["RABBITMQ_PASS"])
                connected = self.connector.is_alive()
            self.__callback(channel, method, header, body)

    def consume(self):
        thread_timer = threading.Thread(target=self.__timer, args=(), name="Timer")
        thread_timer.daemon = True
        thread_timer.start()

        connected = self.connector.is_alive()
        if connected:
            self.__prep()
        else:
            while not connected:
                Logging.error("Couldn't init consuming due to a closed connection! Retrying after {}s."
                              .format(self.config["RMQ_RECONNECT_DELAY"]))
                time.sleep(self.config["RMQ_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                               self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                               self.config["RABBITMQ_PASS"])
                connected = self.connector.is_alive()
            self.__prep()

    def __prep(self):
        self.channel = self.connector.connection.channel()
        self.channel.basic_consume("New", self.__callback)
        self.channel.basic_consume("ToProvide", self.__callback)
        self.channel.basic_consume("Reject", self.__callback)
        self.channel.basic_consume("PartialFilled", self.__callback)
        self.channel.basic_consume("Filled", self.__callback)
        self.channel.start_consuming()

    def __timer(self):
        cycle = True
        while cycle:
            if (datetime.datetime.now() - self.last_call_time).total_seconds() >= 1:
                self.db_service.execute_many(self.current_queries_batch)
                self.current_queries_batch = []
                self.stop_consume_event.set()
                cycle = False
