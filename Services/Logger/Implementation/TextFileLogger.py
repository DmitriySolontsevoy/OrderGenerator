from Services.Logger.API.Logger import Logger
import datetime


class TextFileLogger(Logger):
    def __init__(self, path, level):
        self.path = path
        self.level = level

    def start(self):
        self.__log("START", "Application started", "w")

    def debug(self, message):
        if self.level > 3:
            self.__log("DEBUG", message, "a")

    def info(self, message):
        if self.level > 2:
            self.__log("INFO", message, "a")

    def warn(self, message):
        if self.level > 1:
            self.__log("WARN", message, "a")

    def error(self, message):
        if self.level > 0:
            self.__log("ERROR", message, "a")

    def __log(self, level, message, mode):
        try:
            with open(self.path, mode) as out:
                out.write("(At time: " +
                          datetime.datetime.today().strftime(
                              "%Y-%m-%d %H:%M:%S") + ") [" + level + "]: " + message + "\n")
        except OSError:
            TextFileLogger.__drop_app()
