from Services.Logger.API.Logger import Logger
import datetime


class ConsoleLogger(Logger):
    def __init__(self, level):
        self.level = level

    def start(self):
        self.__log("START", "Application started")

    def debug(self, message):
        if self.level > 3:
            self.__log("DEBUG", message)

    def info(self, message):
        if self.level > 2:
            self.__log("INFO", message)

    def warn(self, message):
        if self.level > 1:
            self.__log("WARN", message)

    def error(self, message):
        if self.level > 0:
            self.__log("ERROR", message)

    def __log(self, level, message):
        print("(At time: " + datetime.datetime.today().strftime(
              "%Y-%m-%d %H:%M:%S") + ") [" + level + "]: " + message)
