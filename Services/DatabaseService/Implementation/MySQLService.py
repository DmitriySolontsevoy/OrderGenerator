from Services.DatabaseService.API.SQLDatabaseService import SQLDatabaseService
from Services.Logger.Implementation.Logging import Logging
import mysql.connector


class MySQLService(SQLDatabaseService):
    def __init__(self, conn):
        self.connector = conn

    def execute(self, query):
        try:
            cursor = self.connector.connection.cursor()
        except AttributeError:
            Logging.error("Couldn't work with connection! Is MySQL Server running?")

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
        try:
            cursor = self.connector.connection.cursor()
        except AttributeError:
            Logging.error("Couldn't work with connection! Is MySQL Server running?")

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
