from Services.DatabaseService.API.RelationDatabaseService import RelationDatabaseService
from Services.Logger.Implementation.Logging import Logging
import mysql.connector


class MySQLService(RelationDatabaseService):
    def open_connection(self, host, schema, user, password):
        result = True

        try:
            self.connection = mysql.connector.connect(host=host, database=schema, user=user, password=password)
        except mysql.connector.Error as err:
            result = False

        return result

    def execute(self, query):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            pass

        cursor.close()

    def execute_many(self, queries):
        cursor = self.connection.cursor()

        try:
            for item in queries:
                cursor.execute(item)
            self.connection.commit()
        except mysql.connector.Error as err:
            pass

        cursor.close()
