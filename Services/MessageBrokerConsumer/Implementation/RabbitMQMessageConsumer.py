from Services.MessageBrokerConsumer.API.MessageConsumer import MessageConsumer
from Services.Logger.Implementation.Logging import Logging
from Proto.OrderRecord_pb2 import OrderRecord
from Utils.FormatConverter import FormatConverter
from ReportData.ReportData import ReportData
from google.protobuf.message import DecodeError
import datetime
import threading


class RabbitMQMessageConsumer(MessageConsumer):
    def __init__(self, conn, config, db_service):
        self.connector = conn
        self.channel = None
        self.config = config
        self.db_service = db_service
        self.last_call_time = datetime.datetime.now()
        self.current_queries_batch = []

    def __callback(self, channel, method, header, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)

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

        self.last_call_time = datetime.datetime.now()

    def consume(self):
        thread = threading.Thread(target=self.__timer, args=())
        thread.daemon = True
        thread.start()

        self.channel = self.connector.connection.channel()
        self.channel.basic_consume("New", self.__callback)
        self.channel.basic_consume("ToProvide", self.__callback)
        self.channel.basic_consume("Reject", self.__callback)
        self.channel.basic_consume("PartialFilled", self.__callback)
        self.channel.basic_consume("Filled", self.__callback)
        self.channel.start_consuming()

    def __timer(self):
        while True:
            if (datetime.datetime.now() - self.last_call_time).total_seconds() >= 10:
                self.db_service.execute_many(self.current_queries_batch)
                self.current_queries_batch = []
                self.channel.basic_cancel(consumer_tag="hello-consumer")
                self.channel.stop_consuming()
