from Services.DatabaseService.API.SQLDatabaseService import SQLDatabaseService
from Services.Logger.Implementation.Logging import Logging
import time
import mysql.connector


class MySQLService(SQLDatabaseService):
    def __init__(self, conn, config):
        self.connector = conn
        self.config = config

    def select(self, query):
        connected = self.connector.is_alive()
        if connected:
            try:
                cursor = self.connector.connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
            except (IndexError, AttributeError) as err:
                print("OOPS: {}".format(err.args.__str__()))
            except mysql.connector.Error as err:
                print("ERROR: {}".format(err.args.__str__()))
            except Exception as err:
                print("COOL: {}".format(err.args.__str__()))
        else:
            while not connected:
                Logging.error("Couldn't select data due to a closed connection! Retrying after {}s."
                              .format(self.config["SQL_RECONNECT_DELAY"]))
                time.sleep(self.config["SQL_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                               self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                connected = self.connector.is_alive()
            self.execute(query)

    def execute(self, query):
        connected = self.connector.is_alive()
        if connected:
            try:
                cursor = self.connector.connection.cursor()
                cursor.execute(query)
                self.connector.connection.commit()
                cursor.close()
            except (IndexError, AttributeError) as err:
                print("OOPS: {}".format(err.args.__str__()))
            except mysql.connector.Error as err:
                print("ERROR: {}".format(err.args.__str__()))
            except Exception as err:
                print("COOL: {}".format(err.args.__str__()))
        else:
            while not connected:
                Logging.error("Couldn't execute a query due to a closed connection! Retrying after {}s."
                              .format(self.config["SQL_RECONNECT_DELAY"]))
                time.sleep(self.config["SQL_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                               self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                connected = self.connector.is_alive()
            self.execute(query)

    def execute_many(self, queries):
        connected = self.connector.is_alive()
        if connected:
            try:
                cursor = self.connector.connection.cursor()
                for item in queries:
                    cursor.execute(item)
                self.connector.connection.commit()
                cursor.close()
            except (IndexError, AttributeError) as err:
                    print("OOPS: {}".format(err.args.__str__()))
            except mysql.connector.Error as err:
                    print("ERROR: {}".format(err.args.__str__()))
            except Exception as err:
                print("COOL: {}".format(err.args.__str__()))
        else:
            while not connected:
                Logging.error("Couldn't execute queries due to a closed connection! Retrying after {}s."
                              .format(self.config["SQL_RECONNECT_DELAY"]))
                time.sleep(self.config["SQL_RECONNECT_DELAY"])
                self.connector.open_connection(self.config["MYSQL_HOST"], self.config["MYSQL_DB_SCHEMA"],
                                               self.config["MYSQL_USER"], self.config["MYSQL_PASS"])
                connected = self.connector.is_alive()
            self.execute(queries)
