import abc


class SQLDatabaseService:
    @abc.abstractmethod
    def execute(self, query):
        pass

    @abc.abstractmethod
    def execute_many(self, queries):
        pass
