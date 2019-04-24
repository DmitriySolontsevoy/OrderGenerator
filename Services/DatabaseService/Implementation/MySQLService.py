from Services.DatabaseService.API.SQLDatabaseService import SQLDatabaseService
from Services.Connector.Implementation.MySQLConnector import MySQLConnector
from Services.Logger.Implementation.Logging import Logging
import time
import mysql.connector


class MySQLService(SQLDatabaseService):
    def __init__(self, conn, config):
        self.connector = conn
        self.current_cursor = None
        self.config = config

    def select(self, query):
        result = False
        try:
            self.current_cursor = self.connector.connection.cursor()
            self.current_cursor.execute(query)
            result = self.current_cursor.fetchall()
            self.current_cursor.close()
        except mysql.connector.ProgrammingError as err:
            Logging.error("Error while executing query. Error: {}".format(err.args.__str__()))
        except Exception as err:
            Logging.error("Error: {}".format(err.args.__str__()))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["SQL_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                                   self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                    self.current_cursor = self.connector.connection.cursor()
                    self.current_cursor.execute(query)
                    result = self.current_cursor.fetchall()
                    self.current_cursor.close()
                    flag = True
                except Exception:
                    Logging.error("Couldn't execute select statement! Is MySQL Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["SQL_RECONNECT_DELAY"]))

        return result

    def execute(self, query):
        try:
            self.current_cursor = self.connector.connection.cursor()
            self.current_cursor.execute(query)
            self.connector.connection.commit()
            self.current_cursor.close()
        except mysql.connector.ProgrammingError as err:
            Logging.error("Error while executing query. Error: {}".format(err.args.__str__()))
        except Exception as err:
            Logging.error("Error: {}".format(err.args.__str__()))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["SQL_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                                   self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                    self.current_cursor = self.connector.connection.cursor()
                    self.current_cursor.execute(query)
                    self.connector.connection.commit()
                    self.current_cursor.close()
                    flag = True
                except Exception:
                    Logging.error("Couldn't execute query! Is MySQL Server running? "
                                  "Reconnecting again after {} secs.".format(self.config["SQL_RECONNECT_DELAY"]))

    def execute_many(self, queries):
        try:
            self.current_cursor = self.connector.connection.cursor()
            for item in queries:
                self.current_cursor.execute(item)
            self.connector.connection.commit()
            self.current_cursor.close()
        except mysql.connector.ProgrammingError as err:
            Logging.error("Error while executing queries. Error: {}".format(err.args.__str__()))
        except Exception as err:
            Logging.error("Error: {}".format(err.args.__str__()))
            flag = False
            while not flag:
                try:
                    time.sleep(self.config["SQL_RECONNECT_DELAY"])
                    self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                                   self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                    self.current_cursor = self.connector.connection.cursor()
                    for item in queries:
                        self.current_cursor.execute(item)
                    self.connector.connection.commit()
                    self.current_cursor.close()
                    flag = True
                except Exception as err:
                    Logging.error("Couldn't execute queries: {}! Is MySQL Server running? "
                                  "Reconnecting again after {} secs.".format(err.args.__str__(),
                                                                             self.config["SQL_RECONNECT_DELAY"]))
