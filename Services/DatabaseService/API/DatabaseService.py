from Services.Logger.Implementation.Logging import Logging
import abc
import mysql.connector


class DatabaseService:
    connection = None

    @abc.abstractmethod
    def open_connection(self, host, schema, user, password):
        pass

    def close_connection(self):
        try:
            self.connection.close
        except mysql.connector.Error as err:
            pass
