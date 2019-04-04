from Services.ConfigLoader.API.ConfigLoader import ConfigLoader
from Services.Logger.Implementation.Logging import Logging
from Configs.Constants.ConfigDefaults import ConfigDefaults
import json


class JSONConfigLoader(ConfigLoader):
    def __init__(self, path):
        self.path = path
        self.config = None

    def parse(self):
        try:
            with open(self.path) as json_file:
                self.config = json.load(json_file)
        except OSError:
            Logging.error("Couldn't parse JSON file")

        self.__verify()
        return self.config

    def __verify(self):
        self.__verify_mysql()
        self.__verify_rmq()
        self.__verify_errors()
        self.__verify_wait_time()
        self.__verify_paths()
        self.__verify_generator_initials()
        self.__verify_generator_settings()
        self.__verify_zones()
        self.__verify_decimal_places()
        self.__verify_beginning_time()
        self.__verify_batch_settings()
        self.__verify_logger_settings()

    def __verify_mysql(self):
        if type(self.config["MYSQL_HOST"]) != str or self.config["MYSQL_HOST"] == "":
            self.config["MYSQL_HOST"] = ConfigDefaults.MYSQL_HOST
        if type(self.config["MYSQL_DB_SCHEMA"]) != str or self.config["MYSQL_DB_SCHEMA"] == "":
            self.config["MYSQL_DB_SCHEMA"] = ConfigDefaults.MYSQL_DB_SCHEMA
        if type(self.config["MYSQL_USER"]) != str or self.config["MYSQL_USER"] == "":
            self.config["MYSQL_USER"] = ConfigDefaults.MYSQL_USER
        if type(self.config["MYSQL_PASS"]) != str or self.config["MYSQL_PASS"] == "":
            self.config["MYSQL_PASS"] = ConfigDefaults.MYSQL_PASS

    def __verify_rmq(self):
        if type(self.config["RABBITMQ_HOST"]) != str or self.config["RABBITMQ_HOST"] == "":
            self.config["RABBITMQ_HOST"] = ConfigDefaults.RABBITMQ_HOST
        if type(self.config["RABBITMQ_PORT"]) != int or self.config["RABBITMQ_PORT"] == 0:
            self.config["RABBITMQ_PORT"] = ConfigDefaults.RABBITMQ_PORT
        if type(self.config["RABBITMQ_VHOST"]) != str or self.config["RABBITMQ_VHOST"] == "":
            self.config["RABBITMQ_VHOST"] = ConfigDefaults.RABBITMQ_VHOST
        if type(self.config["RABBITMQ_USER"]) != str or self.config["RABBITMQ_USER"] == "":
            self.config["RABBITMQ_USER"] = ConfigDefaults.RABBITMQ_USER
        if type(self.config["RABBITMQ_PASS"]) != str or self.config["RABBITMQ_PASS"] == "":
            self.config["RABBITMQ_PASS"] = ConfigDefaults.RABBITMQ_PASS

    def __verify_errors(self):
        if type(self.config["LOG_FILE_WRITING_ERROR"]) != int:
            self.config["LOG_FILE_WRITING_ERROR"] = ConfigDefaults.LOG_FILE_WRITING_ERROR
        if type(self.config["QUERY_FILE_READING_ERROR"]) != int:
            self.config["QUERY_FILE_READING_ERROR"] = ConfigDefaults.QUERY_FILE_READING_ERROR
        if type(self.config["QUERY_FILE_WRITING_ERROR"]) != int:
            self.config["QUERY_FILE_WRITING_ERROR"] = ConfigDefaults.QUERY_FILE_WRITING_ERROR
        if type(self.config["MEMORY_ERROR"]) != "class 'int'":
            self.config["MEMORY_ERROR"] = ConfigDefaults.MEMORY_ERROR

    def __verify_wait_time(self):
        if type(self.config["WAIT_AFTER"]) != int:
            self.config["WAIT_AFTER"] = ConfigDefaults.WAIT_AFTER
        if type(self.config["WAIT_BEFORE"]) != int:
            self.config["WAIT_BEFORE"] = ConfigDefaults.WAIT_BEFORE

    def __verify_paths(self):
        if type(self.config["RECORD_FILE_PATH"]) != str or self.config["RECORD_FILE_PATH"] == "":
            self.config["RECORD_FILE_PATH"] = ConfigDefaults.RECORD_FILE_PATH
        if type(self.config["REPORT_FILE_PATH"]) != str or self.config["REPORT_FILE_PATH"] == "":
            self.config["REPORT_FILE_PATH"] = ConfigDefaults.REPORT_FILE_PATH
        if type(self.config["LOG_FILE_PATH"]) != str or self.config["LOG_FILE_PATH"] == "":
            self.config["LOG_FILE_PATH"] = ConfigDefaults.LOG_FILE_PATH

    def __verify_generator_initials(self):
        if type(self.config["FIRST_ID_PART"]) != int:
            self.config["FIRST_ID_PART"] = ConfigDefaults.FIRST_ID_PART
        if type(self.config["SECOND_ID_PART"]) != int:
            self.config["SECOND_ID_PART"] = ConfigDefaults.SECOND_ID_PART
        if type(self.config["THIRD_ID_PART"]) != int:
            self.config["THIRD_ID_PART"] = ConfigDefaults.THIRD_ID_PART
        if type(self.config["FOURTH_ID_PART"]) != int:
            self.config["FOURTH_ID_PART"] = ConfigDefaults.FOURTH_ID_PART
        if type(self.config["FIRST_PAIR"]) != int:
            self.config["FIRST_PAIR"] = ConfigDefaults.FIRST_PAIR
        if type(self.config["FIRST_DESC"]) != int:
            self.config["FIRST_DESC"] = ConfigDefaults.FIRST_DESC
        if type(self.config["FIRST_TAG"]) != int:
            self.config["FIRST_TAG"] = ConfigDefaults.FIRST_TAG
        if type(self.config["SECOND_TAG"]) != int:
            self.config["SECOND_TAG"] = ConfigDefaults.SECOND_TAG
        if type(self.config["THIRD_TAG"]) != int:
            self.config["THIRD_TAG"] = ConfigDefaults.THIRD_TAG
        if type(self.config["FOURTH_TAG"]) != int:
            self.config["FOURTH_TAG"] = ConfigDefaults.FOURTH_TAG
        if type(self.config["FIFTH_TAG"]) != int:
            self.config["FIFTH_TAG"] = ConfigDefaults.FIFTH_TAG

    def __verify_generator_settings(self):
        if type(self.config["ID_DIV"]) != int:
            self.config["ID_DIV"] = ConfigDefaults.ID_DIV
        if type(self.config["ID_OFFSET"]) != int:
            self.config["ID_OFFSET"] = ConfigDefaults.ID_OFFSET
        if type(self.config["ID_MULT"]) != int:
            self.config["ID_MULT"] = ConfigDefaults.ID_MULT
        if type(self.config["CURPAIR_DIV"]) != int:
            self.config["CURPAIR_DIV"] = ConfigDefaults.CURPAIR_DIV
        if type(self.config["CURPAIR_OFFSET"]) != int:
            self.config["CURPAIR_OFFSET"] = ConfigDefaults.CURPAIR_OFFSET
        if type(self.config["CURPAIR_MULT"]) != int:
            self.config["CURPAIR_MULT"] = ConfigDefaults.CURPAIR_MULT
        if type(self.config["DESC_DIV"]) != int:
            self.config["DESC_DIV"] = ConfigDefaults.DESC_DIV
        if type(self.config["DESC_OFFSET"]) != int:
            self.config["DESC_OFFSET"] = ConfigDefaults.DESC_OFFSET
        if type(self.config["DESC_MULT"]) != int:
            self.config["DESC_MULT"] = ConfigDefaults.DESC_MULT
        if type(self.config["TAGS_DIV"]) != int:
            self.config["TAGS_DIV"] = ConfigDefaults.TAGS_DIV
        if type(self.config["TAGS_OFFSET"]) != int:
            self.config["TAGS_OFFSET"] = ConfigDefaults.TAGS_OFFSET
        if type(self.config["TAGS_MULT"]) != int:
            self.config["TAGS_MULT"] = ConfigDefaults.TAGS_MULT
        if type(self.config["INIT_MARGIN"]) != int:
            self.config["INIT_MARGIN"] = ConfigDefaults.INIT_MARGIN
        if type(self.config["FILL_MARGIN"]) != int:
            self.config["FILL_MARGIN"] = ConfigDefaults.FILL_MARGIN
        if type(self.config["INIT_LESS"]) != int:
            self.config["INIT_LESS"] = ConfigDefaults.INIT_LESS
        if type(self.config["INIT_MORE"]) != int:
            self.config["INIT_MORE"] = ConfigDefaults.INIT_MORE
        if type(self.config["FILL_LESS"]) != int:
            self.config["FILL_LESS"] = ConfigDefaults.FILL_LESS
        if type(self.config["FILL_MORE"]) != int:
            self.config["FILL_MORE"] = ConfigDefaults.FILL_MORE

    def __verify_decimal_places(self):
        if type(self.config["PLACES_FOR_VOLUME"]) != int or self.config["PLACES_FOR_VOLUME"] < 0:
            self.config["PLACES_FOR_VOLUME"] = ConfigDefaults.PLACES_FOR_VOLUME
        if type(self.config["PLACES_FOR_PRICE"]) != int or self.config["PLACES_FOR_PRICE"] < 0:
            self.config["PLACES_FOR_PRICE"] = ConfigDefaults.PLACES_FOR_PRICE

    def __verify_beginning_time(self):
        if type(self.config["BEGINNING_OF_TIME"]) != int:
            self.config["BEGINNING_OF_TIME"] = ConfigDefaults.BEGINNING_OF_TIME

    def __verify_zones(self):
        if type(self.config["RED"]) != float:
            self.config["RED"] = ConfigDefaults.RED
        if type(self.config["GREEN"]) != float:
            self.config["GREEN"] = ConfigDefaults.GREEN

    def __verify_batch_settings(self):
        if type(self.config["BATCH_SIZE"]) != int or self.config["BATCH_SIZE"] < 1:
            self.config["BATCH_SIZE"] = ConfigDefaults.BATCH_SIZE
        if type(self.config["BATCHES_AMOUNT"]) != int or self.config["BATCHES_AMOUNT"] < 1:
            self.config["BATCHES_AMOUNT"] = ConfigDefaults.BATCHES_AMOUNT

    def __verify_logger_settings(self):
        if type(self.config["TEXT_LOGGING"]) != int or not (-1 < self.config["TEXT_LOGGING"] < 2):
            self.config["TEXT_LOGGING"] = ConfigDefaults.TEXT_LOGGING
        if type(self.config["TXT_LOG_LEVEL"]) != int:
            self.config["TXT_LOG_LEVEL"] = ConfigDefaults.TXT_LOG_LEVEL
        if type(self.config["CONSOLE_LOGGING"]) != int or not (-1 < self.config["CONSOLE_LOGGING"] < 2):
            self.config["CONSOLE_LOGGING"] = ConfigDefaults.CONSOLE_LOGGING
        if type(self.config["CONSOLE_LOG_LEVEL"]) != int:
            self.config["CONSOLE_LOG_LEVEL"] = ConfigDefaults.CONSOLE_LOG_LEVEL
