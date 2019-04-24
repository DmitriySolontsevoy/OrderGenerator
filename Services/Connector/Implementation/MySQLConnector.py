from Services.Logger.Implementation.Logging import Logging
from Services.Connector.API.Connector import Connector
import mysql.connector


class MySQLConnector(Connector):
    def __init__(self):
        self.connection = None

    def open_connection(self, host, schema, user, password):
        try:
            self.connection = mysql.connector.connect(host=host, database=schema, user=user, password=password)
            return True
        except mysql.connector.Error as err:
            Logging.error("Couldn't establish MySQL connection! Error: {}".format(err.args.__str__()))
            return False

    def close_connection(self, **kwargs):
        try:
            self.connection.close()
        except mysql.connector.Error as err:
            Logging.warn("Couldn't close MySQL connection! Error: {}".format(err.args.__str__()))

    def is_alive(self, **kwargs):
        try:
            return self.connection.is_connected()
        except:
            return False
