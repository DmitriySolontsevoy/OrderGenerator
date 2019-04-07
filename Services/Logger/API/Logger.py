import abc
import sys


class Logger:
    level = None

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def debug(self, message):
        pass

    @abc.abstractmethod
    def info(self, message):
        pass

    @abc.abstractmethod
    def warn(self, message):
        pass

    @abc.abstractmethod
    def error(self, message):
        pass

    @abc.abstractmethod
    def __log(self, level, message):
        pass

    @staticmethod
    def __drop_app():
        # syslog.syslog("Can't write logs! Closing generator")
        sys.exit()
