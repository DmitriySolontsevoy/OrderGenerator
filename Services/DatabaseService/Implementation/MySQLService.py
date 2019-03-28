from Services.DatabaseService.API.SQLDatabaseService import SQLDatabaseService
from Services.Logger.Implementation.Logging import Logging
import mysql.connector


class MySQLService(SQLDatabaseService):
    def __init__(self, conn):
        self.connection = conn

    def execute(self, query):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            pass

        try:
            self.connection.commit()
        except mysql.connector.Error as err:
            pass

        cursor.close()

    def execute_many(self, queries):
        cursor = self.connection.cursor()

        try:
            for item in queries:
                cursor.execute(item)
        except mysql.connector.Error as err:
            pass

        try:
            self.connection.commit()
        except mysql.connector.Error as err:
            pass

        cursor.close()
