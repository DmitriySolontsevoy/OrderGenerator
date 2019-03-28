import abc


class Connector:
    @abc.abstractmethod
    def open_connection(self, **kwargs):
        pass

    @abc.abstractmethod
    def close_connection(self, **kwargs):
        pass

    @abc.abstractmethod
    def is_alive(self, **kwargs):
        pass
