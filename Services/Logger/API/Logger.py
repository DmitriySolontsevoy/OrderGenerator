import abc


class Logger:
    level = None

    @staticmethod
    @abc.abstractmethod
    def start():
        pass

    @staticmethod
    @abc.abstractmethod
    def debug(message):
        pass

    @staticmethod
    @abc.abstractmethod
    def info(message):
        pass

    @staticmethod
    @abc.abstractmethod
    def warn(message):
        pass

    @staticmethod
    @abc.abstractmethod
    def error(message):
        pass

    @staticmethod
    @abc.abstractmethod
    def __drop_app():
        pass

    @staticmethod
    @abc.abstractmethod
    def __log(message):
        pass
