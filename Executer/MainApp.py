from Services.Logger.Implementation.TextFileLogger import TextFileLogger
from Services.Logger.Implementation.ConsoleLogger import ConsoleLogger
from Services.Logger.Implementation.Logging import Logging
from Services.ConfigLoader.Implementation.JSONConfigLoader import JSONConfigLoader
from Generators.RecordsBatchCreator import RecordsBatchCreator
from Services.MessageBrokerConsumer.Implementation.RabbitMQMessageConsumer import RabbitMQMessageConsumer
from Services.Connector.Implementation.RabbitMQConnector import RabbitMQConnector
from Services.MessageBrokerService.Implementation.RabbitMQService import RabbitMQService
from Reporters.Implementation.TextFileReporter import TextFileReporter
from Reporters.Implementation.ConsoleReporter import ConsoleReporter
from Services.FileService.Implementation.TextFileService import TextFileService
from Configs.Constants.ConstantCollections import ConstantCollections
from Services.DatabaseService.Implementation.MySQLService import MySQLService
from Services.Connector.Implementation.MySQLConnector import MySQLConnector
from ReportData.ReportData import ReportData
from Utils.FormatConverter import FormatConverter
import datetime
import threading


class MainApp:
    def __init__(self, abspath):
        self.records = []
        self.config = None
        self.file_service = TextFileService(self.config)
        self.abspath = abspath + "/"
        self.broker_conn = RabbitMQConnector()
        self.consume_conn = RabbitMQConnector()
        self.console_reporter = None
        self.text_reporter = None
        self.stop_consume_event = None
        self.publisher = None

    def prep(self):
        parser = JSONConfigLoader(self.abspath + "Configs/Configurable/config.json")
        self.config = parser.parse()

        Logging.text_file_logger = TextFileLogger(self.abspath + self.config["LOG_FILE_PATH"],
                                                  self.config["TXT_LOG_LEVEL"])
        Logging.console_logger = ConsoleLogger(self.config["CONSOLE_LOG_LEVEL"])
        Logging.init(self.config["TEXT_LOGGING"], self.config["CONSOLE_LOGGING"])
        Logging.start()

        db_conn = MySQLConnector()
        db_conn.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
        db_report_service = MySQLService(db_conn, self.config)
        db_report_service.execute("TRUNCATE mytable")

        self.text_reporter = TextFileReporter(self.abspath + self.config["REPORT_FILE_PATH"],
                                              self.file_service, db_report_service)
        self.console_reporter = ConsoleReporter(db_report_service)

    def exec(self):
        self.__generate_records()
        self.stop_consume_event = threading.Event()
        self.publisher = self.__broker_setup()

        thread_publish = threading.Thread(target=self.__post_to_rabbit, args=(), name="Publisher")
        thread_publish.start()

        thread_consume = threading.Thread(target=self.__get_from_rabbit, args=(), name="Consumer")
        thread_consume.start()

        self.stop_consume_event.wait()
        self.publisher.publish("Main", "New", "timeout")

    def __input_listener(self):
        while True:
            request = input("Type 'status' to get a report\n>>> ")
            if request == "status":
                self.report()

    def report(self):
        self.console_reporter.report()

    def free(self):
        self.records = None
        self.file_service = None
        self.broker_conn.close_connection()
        self.consume_conn.close_connection()

    def __generate_records(self):
        creator = RecordsBatchCreator(self.config)

        for i in range(0, self.config["BATCHES_AMOUNT"]):
            batch = creator.batch_creation(i * self.config["BATCH_SIZE"])
            self.records.extend(batch)

    def __broker_setup(self):
        self.broker_conn.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                         self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                         self.config["RABBITMQ_PASS"])

        broker_service = RabbitMQService(self.broker_conn, self.config)
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
        for item in self.records:
            start_time = datetime.datetime.now()

            proto = FormatConverter.convert_rec_to_proto(item)
            queue = list(ConstantCollections.STATUS_DICT.keys())[
                list(ConstantCollections.STATUS_DICT.values()).index(proto.status)]
            self.publisher.publish("Main", queue, proto.SerializeToString())

            finish_time = datetime.datetime.now()
            zone = proto.zone
            if zone == 1:
                ReportData.messaged_red.append((finish_time - start_time).total_seconds() * 1000)
            elif zone == 2:
                ReportData.messaged_green.append((finish_time - start_time).total_seconds() * 1000)
            else:
                ReportData.messaged_blue.append((finish_time - start_time).total_seconds() * 1000)

    def __get_from_rabbit(self):
        self.consume_conn.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                          self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                          self.config["RABBITMQ_PASS"])
        db_conn = MySQLConnector()
        db_conn.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
        db_service = MySQLService(db_conn, self.config)

        consumer = RabbitMQMessageConsumer(self.consume_conn, self.config, db_service, self.stop_consume_event)
        consumer.consume()
