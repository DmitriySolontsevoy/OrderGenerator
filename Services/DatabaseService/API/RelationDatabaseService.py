from Services.DatabaseService.API.DatabaseService import DatabaseService
import abc


class RelationDatabaseService(DatabaseService):
    @abc.abstractmethod
    def execute(self, query):
        pass

    @abc.abstractmethod
    def execute_many(self, queries):
        pass
