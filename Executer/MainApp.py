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
from Proto.OrderRecord_pb2 import OrderRecord
from Utils.FormatConverter import FormatConverter


class MainApp:
    def __init__(self):
        self.records = []
        self.config = None
        self.file_service = TextFileService(self.config)
        self.broker_conn = RabbitMQConnector()
        self.db_conn = MySQLConnector()

    def prep(self):
        parser = JSONConfigLoader("Configs/Configurable/config.json")
        self.config = parser.parse()

        Logging.text_file_logger = TextFileLogger(self.config["LOG_FILE_PATH"], self.config["TXT_LOG_LEVEL"])
        Logging.console_logger = ConsoleLogger(self.config["CONSOLE_LOG_LEVEL"])
        Logging.init(self.config["TEXT_LOGGING"], self.config["CONSOLE_LOGGING"])

    def exec(self):
        self.__generate_records()
        self.__post_to_rabbit()
        self.__write_to_file()

        self.records = self.__read_from_file()

        self.__insert_to_db()

    def report(self):
        pass

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

            protos.append(proto)

        return protos

    def __post_to_rabbit(self):
        self.broker_conn.open_connection(self.config["RABBITMQ_HOST"], self.config["RABBITMQ_PORT"],
                                         self.config["RABBITMQ_VHOST"], self.config["RABBITMQ_USER"],
                                         self.config["RABBITMQ_PASS"])

        broker_service = RabbitMQService(self.broker_conn)

        broker_service.create_exchange("Main", "topic")

        broker_service.create_queue("New")
        broker_service.create_queue("ToProvider")
        broker_service.create_queue("Reject")
        broker_service.create_queue("PartialFilled")
        broker_service.create_queue("Filled")

        broker_service.bind("Main", "New")
        broker_service.bind("Main", "ToProvider")
        broker_service.bind("Main", "Reject")
        broker_service.bind("Main", "PartialFilled")
        broker_service.bind("Main", "Filled")

        protos = self.__rec_to_proto()

        for item in protos:
            queue = item.status
            broker_service.publish(queue, queue, item.SerializeToString())

    def __write_to_file(self):
        file = self.file_service.open_file(self.config["QUERY_FILE_PATH"], "a")

        lines = []

        for item in self.records:
            lines.append(FormatConverter.convert_rec_to_txt(item))

        self.file_service.write_all(file, lines)

        file.close()

    def __read_from_file(self):
        file = self.file_service.open_file(self.config["QUERY_FILE_PATH"], "r")
        lines = self.file_service.read_all(file)

        records = []

        for item in lines:
            records.append(FormatConverter.convert_txt_to_rec(item))

        file.close()
        return records

    def __insert_to_db(self):
        self.db_conn.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                     self.config["MYSQL_USER"], self.config["MYSQL_PASS"])

        db_service = MySQLService(self.db_conn)

        queries = []

        for item in self.records:
            queries.append(FormatConverter.convert_rec_to_sql_query(item))

        db_service.execute_many(queries)

    def __return_number_of_batches(self):
        try:
            num_of_batches = (len(self.records) // self.config["BATCH_SIZE"]) + 1
        except ZeroDivisionError:
            Logging.error("Number of batches to generate was set to zero!")
            exit(self.config["ZERO_BATCHES_ERROR"])

        return num_of_batches
