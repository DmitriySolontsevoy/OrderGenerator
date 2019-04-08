from Services.DatabaseService.API.SQLDatabaseService import SQLDatabaseService
from Services.Connector.Implementation.MySQLConnector import MySQLConnector
from Services.Logger.Implementation.Logging import Logging

import time
import mysql.connector


class MySQLService(SQLDatabaseService):
    def __init__(self, conn, config):
        self.connector = conn
        self.config = config

    def __try_to_create_cursor(self):
        cursor = None

        try:
            cursor = self.connector.connection.cursor()
        except AttributeError:
            Logging.error("Couldn't work with connection! Is MySQL Server running? Reconnecting after {} secs."
                          .format(self.config["RECONNECT_DELAY"]))
            flag = False

            while not flag:
                try:
                    time.sleep(self.config["RECONNECT_DELAY"])
                    self.connector = MySQLConnector()
                    self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                                   self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                    cursor = self.connector.connection.cursor()
                    flag = True
                except AttributeError:
                    Logging.error("Couldn't work with connection! Is MySQL Server running?"
                                  "Reconnecting again after {} secs.".format(self.config["RECONNECT_DELAY"]))

        return cursor

    def execute(self, query):
        cursor = self.__try_to_create_cursor()

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            Logging.error("Error while executing query")

        try:
            self.connector.connection.commit()
        except mysql.connector.Error as err:
            Logging.error("Error while committing changes")

        cursor.close()

    def execute_many(self, queries):
        cursor = self.__try_to_create_cursor()

        try:
            for item in queries:
                cursor.execute(item)
        except mysql.connector.Error as err:
            Logging.error("Error while executing queries")

        try:
            self.connector.connection.commit()
        except mysql.connector.Error as err:
            Logging.error("Error while committing changes")

        cursor.close()
