from Services.MessageBrokerConsumer.API.MessageConsumer import MessageConsumer
from Services.Logger.Implementation.Logging import Logging
from Proto.OrderRecord_pb2 import OrderRecord
from Utils.FormatConverter import FormatConverter
from ReportData.ReportData import ReportData
from google.protobuf.message import DecodeError
import datetime


class RabbitMQMessageConsumer(MessageConsumer):
    def __init__(self, conn, config, db_service):
        self.connector = conn
        self.config = config
        self.db_service = db_service
        self.abort_votes = 0

    def __callback(self, channel, method, header, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        if body.__str__() == "b'exit'":
            self.abort_votes += 1
        else:
            obj = OrderRecord()
            try:
                obj.ParseFromString(body)
                Logging.info("Message received: {}".format(obj))
            except DecodeError as err:
                Logging.error("Couldn't parse proto message. Error: {}".format(err.__str__()))

            self.__insert(FormatConverter.convert_proto_to_rec(obj))

        if self.abort_votes >= 5:
            channel.basic_cancel(consumer_tag="hello-consumer")
            channel.stop_consuming()
            self.db_service.connector.close_connection()

    def consume(self):
        self.db_service.execute("TRUNCATE mytable")
        channel = self.connector.connection.channel()
        channel.basic_consume("New", self.__callback)
        channel.basic_consume("ToProvide", self.__callback)
        channel.basic_consume("Reject", self.__callback)
        channel.basic_consume("PartialFilled", self.__callback)
        channel.basic_consume("Filled", self.__callback)
        channel.start_consuming()

    def __insert(self, record):
        start_time = datetime.datetime.now()
        self.db_service.execute(FormatConverter.convert_rec_to_sql_query(record))
        finish_time = datetime.datetime.now()
        zone = record.order.get_zone()
        if int(zone) == 1:
            ReportData.inserted_red.append((finish_time - start_time).total_seconds() * 1000)
        elif int(zone) == 2:
            ReportData.inserted_green.append((finish_time - start_time).total_seconds() * 1000)
        else:
            ReportData.inserted_blue.append((finish_time - start_time).total_seconds() * 1000)
