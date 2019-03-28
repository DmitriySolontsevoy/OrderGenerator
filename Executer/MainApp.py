from Services.Logger.Implementation.TextFileLogger import TextFileLogger
from Services.Logger.Implementation.Logging import Logging
from Services.ConfigLoader.Implementation.JSONConfigLoader import JSONConfigLoader
from Generators.RecordsBatchCreator import RecordsBatchCreator
from Services.FileService.Implementation.TextFileService import TextFileService
from Services.Connector.Implementation.MySQLConnector import *
from Services.MessageBrokerService.Implementation.RabbitMQService import RabbitMQService
from Services.DatabaseService.Implementation.MySQLService import MySQLService


class MainApp:
    def __init__(self):
        self.queries = None
        self.config = None

    def prep(self):
        parser = JSONConfigLoader("Configs/Configurable.json")
        self.config = parser.parse()
        Logging.text_file_logger = TextFileLogger(self.config["LOG_FILE_PATH"], 4)

    def exec(self):
        pass

    def report(self):
        pass

    def free(self):
        pass

    def __generate_records(self):
        pass

    def __post_to_rabbit(self):
        pass

    def __write_to_file(self):
        pass

    def __read_from_file(self):
        pass

    def __insert_to_db(self):
        pass

    def __return_number_of_batches(self):
        try:
            num_of_batches = (len(self.queries) // self.config.BATCH_SIZE) + 1
        except ZeroDivisionError:
            Logging.text_file_logger.error("Number of batches to generate was set to zero!")
            exit(self.config.ZERO_BATCHES_ERROR)

        return num_of_batches
