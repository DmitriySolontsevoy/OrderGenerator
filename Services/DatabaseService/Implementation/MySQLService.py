from Services.DatabaseService.API.SQLDatabaseService import SQLDatabaseService
from Services.Connector.Implementation.MySQLConnector import MySQLConnector
from Services.Logger.Implementation.Logging import Logging
import time
import mysql.connector


class MySQLService(SQLDatabaseService):
    def __init__(self, conn, config):
        self.connector = conn
        self.config = config

    def select(self, query):
        try:
            cursor = self.connector.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error:
            Logging.error("Error while executing query")
        except Exception as err:
            Logging.error("Error")
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["SQL_RECONNECT_DELAY"])
                    self.connector = MySQLConnector()
                    self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                                   self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                    cursor = self.connector.connection.cursor()
                    cursor.execute(query)
                    result = cursor.fetchall()
                    cursor.close()
                    flag = True
                except Exception:
                    Logging.error("Couldn't work with connection! Is MySQL Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["SQL_RECONNECT_DELAY"]))

        return result

    def execute(self, query):
        try:
            cursor = self.connector.connection.cursor()
            cursor.execute(query)
            self.connector.connection.commit()
            cursor.close()
        except mysql.connector.Error:
            Logging.error("Error while executing query")
        except Exception as err:
            Logging.error("Error: {}".format(err.args.__str__()))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["SQL_RECONNECT_DELAY"])
                    self.connector = MySQLConnector()
                    self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                                   self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                    cursor = self.connector.connection.cursor()
                    cursor.execute(query)
                    self.connector.connection.commit()
                    cursor.close()
                    flag = True
                except Exception:
                    Logging.error("Couldn't work with connection! Is MySQL Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["SQL_RECONNECT_DELAY"]))

    def execute_many(self, queries):
        try:
            cursor = self.connector.connection.cursor()
            for item in queries:
                cursor.execute(item)
            self.connector.connection.commit()
            cursor.close()
        except mysql.connector.Error:
            Logging.error("Error while executing query")
        except Exception as err:
            Logging.error("Error")
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["SQL_RECONNECT_DELAY"])
                    self.connector = MySQLConnector()
                    self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                                   self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                    cursor = self.connector.connection.cursor()
                    for item in queries:
                        cursor.execute(item)
                    self.connector.connection.commit()
                    cursor.close()
                    flag = True
                except Exception:
                    Logging.error("Couldn't work with connection! Is MySQL Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["SQL_RECONNECT_DELAY"]))
