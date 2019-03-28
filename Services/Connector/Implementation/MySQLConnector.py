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
            return False

    def close_connection(self, **kwargs):
        try:
            self.connection.close()
        except mysql.connector.Error as err:
            pass

    def is_alive(self, **kwargs):
        return self.connection.open
