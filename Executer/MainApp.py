from Services.Logger.Implementation.TextFileLogger import TextFileLogger
from Services.Logger.Implementation.ConsoleLogger import ConsoleLogger
from Services.Logger.Implementation.Logging import Logging
from Services.ConfigLoader.Implementation.JSONConfigLoader import JSONConfigLoader
from Generators.RecordsBatchCreator import RecordsBatchCreator
from Services.FileService.Implementation.TextFileService import TextFileService
from Services.Connector.Implementation.MySQLConnector import MySQLConnector
from Services.Connector.Implementation.RabbitMQConnector import RabbitMQConnector
from Services.MessageBrokerService.Implementation.RabbitMQService import RabbitMQService
from Services.DatabaseService.Implementation.MySQLService import MySQLService
from Reporters.Implementation.ConsoleReporter import ConsoleReporter
from Reporters.Implementation.TextFileReporter import TextFileReporter
from ReportData.ReportData import ReportData
from Proto.OrderRecord_pb2 import OrderRecord
from Utils.FormatConverter import FormatConverter
import datetime


class MainApp:
    def __init__(self, abspath):
        self.records = []
        self.config = None
        self.abspath = abspath + "/"
        self.file_service = TextFileService(self.config)
        self.broker_conn = RabbitMQConnector()
        self.db_conn = MySQLConnector()

    def prep(self):
        parser = JSONConfigLoader(self.abspath + "Configs/Configurable/config.json")
        self.config = parser.parse()

        Logging.text_file_logger = TextFileLogger(self.abspath + self.config["LOG_FILE_PATH"],
                                                  self.config["TXT_LOG_LEVEL"])
        Logging.console_logger = ConsoleLogger(self.config["CONSOLE_LOG_LEVEL"])
        Logging.init(self.config["TEXT_LOGGING"], self.config["CONSOLE_LOGGING"])

    def exec(self):
        self.__generate_records()
        self.__post_to_rabbit()
        self.__write_to_file()

        self.records = self.__read_from_file()

        self.__insert_to_db()

    def report(self):
        text_reporter = TextFileReporter(self.abspath + self.config["REPORT_FILE_PATH"], self.file_service)
        text_reporter.report()
        console_reporter = ConsoleReporter()
        console_reporter.report()

    def free(self):
        self.file_service = None
        self.broker_conn.close_connection()
        self.db_conn.close_connection()

    def __generate_records(self):
        creator = RecordsBatchCreator(self.config)

        for i in range(0, self.config["BATCHES_AMOUNT"]):
            batch = creator.batch_creation(i * self.config["BATCH_SIZE"])
            self.records.extend(batch)

    def __rec_to_proto(self):
        protos = []

        for item in self.records:
            proto = OrderRecord()
            proto.id = item.order.get_id()
            proto.cur_pair = item.order.get_cur_pair()
            proto.direction = item.order.get_direction()
            proto.status = item.get_status()
            proto.datetime = item.get_datetime()
            proto.init_px = item.order.get_init_px()
            proto.init_volume = item.order.get_init_volume()
            proto.fill_px = item.get_fill_px()
            proto.fill_volume = item.get_fill_volume()
            proto.desc = item.order.get_desc()
            proto.tags = item.order.get_tags()
            proto.zone = item.order.get_zone()
            protos.append(proto)

        return protos

    def __post_to_rabbit(self):
        self.broker_conn.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                         self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                         self.config["RABBITMQ_PASS"])

        broker_service = RabbitMQService(self.broker_conn)

        broker_service.create_exchange("Main", "topic")

        broker_service.create_queue("New")
        broker_service.create_queue("ToProvide")
        broker_service.create_queue("Reject")
        broker_service.create_queue("PartialFilled")
        broker_service.create_queue("Filled")

        broker_service.bind("Main", "New")
        broker_service.bind("Main", "ToProvide")
        broker_service.bind("Main", "Reject")
        broker_service.bind("Main", "PartialFilled")
        broker_service.bind("Main", "Filled")

        protos = self.__rec_to_proto()

        for item in protos:
            start_time = datetime.datetime.now()
            queue = item.status
            broker_service.publish("Main", queue, item.SerializeToString())
            finish_time = datetime.datetime.now()
            zone = item.zone
            if zone == 1:
                ReportData.messaged_red.append((finish_time - start_time).total_seconds() * 1000)
            elif zone == 2:
                ReportData.messaged_green.append((finish_time - start_time).total_seconds() * 1000)
            else:
                ReportData.messaged_blue.append((finish_time - start_time).total_seconds() * 1000)

    def __write_to_file(self):
        file = self.file_service.open_file(self.abspath + self.config["RECORD_FILE_PATH"], "w")

        lines = []

        for item in self.records:
            start_time = datetime.datetime.now()
            lines.append(FormatConverter.convert_rec_to_txt(item))
            finish_time = datetime.datetime.now()
            zone = item.order.get_zone()
            if int(zone) == 1:
                ReportData.written_red.append((finish_time - start_time).total_seconds() * 1000)
            elif int(zone) == 2:
                ReportData.written_green.append((finish_time - start_time).total_seconds() * 1000)
            else:
                ReportData.written_blue.append((finish_time - start_time).total_seconds() * 1000)

        self.file_service.write_all(file, lines)

        file.close()

    def __read_from_file(self):
        file = self.file_service.open_file(self.abspath + self.config["RECORD_FILE_PATH"], "r")
        lines = self.file_service.read_all(file)

        records = []

        for item in lines:
            start_time = datetime.datetime.now()
            rec = FormatConverter.convert_txt_to_rec(item)
            records.append(rec)
            finish_time = datetime.datetime.now()
            zone = rec.order.get_zone()
            if int(zone) == 1:
                ReportData.read_red.append((finish_time - start_time).total_seconds() * 1000)
            elif int(zone) == 2:
                ReportData.read_green.append((finish_time - start_time).total_seconds() * 1000)
            else:
                ReportData.read_blue.append((finish_time - start_time).total_seconds() * 1000)

        file.close()
        return records

    def __insert_to_db(self):
        self.db_conn.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                     self.config["MYSQL_USER"], self.config["MYSQL_PASS"])

        db_service = MySQLService(self.db_conn)

        queries = []

        for item in self.records:
            start_time = datetime.datetime.now()
            queries.append(FormatConverter.convert_rec_to_sql_query(item))
            finish_time = datetime.datetime.now()
            zone = item.order.get_zone()
            if int(zone) == 1:
                ReportData.inserted_red.append((finish_time - start_time).total_seconds() * 1000)
            elif int(zone) == 2:
                ReportData.inserted_green.append((finish_time - start_time).total_seconds() * 1000)
            else:
                ReportData.inserted_blue.append((finish_time - start_time).total_seconds() * 1000)

        db_service.execute_many(queries)
