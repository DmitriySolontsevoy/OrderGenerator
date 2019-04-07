from Services.Logger.API.Logger import Logger
import datetime


class TextFileLogger(Logger):
    def __init__(self, path, level):
        self.path = path
        self.level = level
        self.file = None

    def start(self):
        self.file = open(self.path, "a")
        self.file.truncate(0)
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
        try:
            self.file.write("(At time: " +
                            datetime.datetime.today().strftime(
                                "%Y-%m-%d %H:%M:%S") + ") [" + level + "]: " + message + "\n")
        except OSError:
            TextFileLogger.__drop_app()
