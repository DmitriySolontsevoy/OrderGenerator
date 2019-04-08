from Services.Logger.Implementation.TextFileLogger import TextFileLogger
from Services.Logger.Implementation.ConsoleLogger import ConsoleLogger
from Services.Logger.Implementation.Logging import Logging
from Services.ConfigLoader.Implementation.JSONConfigLoader import JSONConfigLoader
from Generators.RecordsBatchCreator import RecordsBatchCreator
from Services.MessageBrokerConsumer.Implementation.RabbitMQMessageConsumer import RabbitMQMessageConsumer
from Services.Connector.Implementation.RabbitMQConnector import RabbitMQConnector
from Services.MessageBrokerService.Implementation.RabbitMQService import RabbitMQService
from Reporters.Implementation.TextFileReporter import TextFileReporter
from Services.FileService.Implementation.TextFileService import TextFileService
from Configs.Constants.ConstantCollections import ConstantCollections
from Services.DatabaseService.Implementation.MySQLService import MySQLService
from Services.Connector.Implementation.MySQLConnector import MySQLConnector
from ReportData.ReportData import ReportData
from Utils.FormatConverter import FormatConverter
import datetime


class MainApp:
    def __init__(self, abspath):
        self.records = []
        self.config = None
        self.file_service = TextFileService(self.config)
        self.abspath = abspath + "/"
        self.broker_conn = RabbitMQConnector()
        self.consume_conn = RabbitMQConnector()

    def prep(self):
        parser = JSONConfigLoader(self.abspath + "Configs/Configurable/config.json")
        self.config = parser.parse()

        Logging.text_file_logger = TextFileLogger(self.abspath + self.config["LOG_FILE_PATH"],
                                                  self.config["TXT_LOG_LEVEL"])
        Logging.console_logger = ConsoleLogger(self.config["CONSOLE_LOG_LEVEL"])
        Logging.init(self.config["TEXT_LOGGING"], self.config["CONSOLE_LOGGING"])

        Logging.start()

        self.broker_conn.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                         self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                         self.config["RABBITMQ_PASS"])

        self.consume_conn.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                          self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                          self.config["RABBITMQ_PASS"])

    def exec(self):
        self.__generate_records()
        self.__post_to_rabbit()
        self.records = None
        self.__get_from_rabbit()

    def report(self):
        text_reporter = TextFileReporter(self.abspath + self.config["REPORT_FILE_PATH"], self.file_service)
        text_reporter.report()

    def free(self):
        self.file_service = None
        self.broker_conn.close_connection()
        self.consume_conn.close_connection()

    def __generate_records(self):
        creator = RecordsBatchCreator(self.config)

        for i in range(0, self.config["BATCHES_AMOUNT"]):
            batch = creator.batch_creation(i * self.config["BATCH_SIZE"])
            self.records.extend(batch)

    def __broker_setup(self):
        broker_service = RabbitMQService(self.broker_conn)
        broker_service.create_exchange("Main", "topic")
        broker_service.create_queue("New")
        broker_service.create_queue("ToProvide")
        broker_service.create_queue("Reject")
        broker_service.create_queue("PartialFilled")
        broker_service.create_queue("Filled")
        broker_service.bind("Main", "New", "New")
        broker_service.bind("Main", "ToProvide", "ToProvide")
        broker_service.bind("Main", "Reject", "Reject")
        broker_service.bind("Main", "PartialFilled", "PartialFilled")
        broker_service.bind("Main", "Filled", "Filled")

        return broker_service

    def __post_to_rabbit(self):
        service = self.__broker_setup()

        for item in self.records:
            start_time = datetime.datetime.now()

            proto = FormatConverter.convert_rec_to_proto(item)
            queue = list(ConstantCollections.STATUS_DICT.keys())[
                list(ConstantCollections.STATUS_DICT.values()).index(proto.status)]
            service.publish("Main", queue, proto.SerializeToString())

            finish_time = datetime.datetime.now()
            zone = proto.zone
            if zone == 1:
                ReportData.messaged_red.append((finish_time - start_time).total_seconds() * 1000)
            elif zone == 2:
                ReportData.messaged_green.append((finish_time - start_time).total_seconds() * 1000)
            else:
                ReportData.messaged_blue.append((finish_time - start_time).total_seconds() * 1000)

        service.publish("Main", "New", "exit")
        service.publish("Main", "ToProvide", "exit")
        service.publish("Main", "Reject", "exit")
        service.publish("Main", "PartialFilled", "exit")
        service.publish("Main", "Filled", "exit")

    def __get_from_rabbit(self):
        db_conn = MySQLConnector()
        db_conn.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
        db_service = MySQLService(db_conn, self.config)

        consumer = RabbitMQMessageConsumer(self.consume_conn, self.config, db_service)
        consumer.consume()
