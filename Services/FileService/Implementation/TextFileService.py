from Services.Logger.Implementation.Logging import Logging
from Services.FileService.API.FileService import FileService


class TextFileService(FileService):
    def __init__(self, config):
        self.config = config

    # Try to open file by given path
    def open_file(self, path, mode):
        Logging.info("Attempting to open file: " + path)

        try:
            return open(path, mode)
        except OSError:
            Logging.error("Couldn't open file. Closing!")
            exit(self.config["QUERY_FILE_WRITING_ERROR"])

    # Read a single line from file
    def read_line(self, file):
        try:
            return file.readline()
        except OSError:
            Logging.error("Couldn't read a line from file!")

    # Read every line from file
    def read_all(self, file):
        try:
            return file.readlines()
        except OSError:
            Logging.error("Couldn't read from file!")

    # Write a single line to file
    def write_line(self, file, line):
        try:
            file.write(line + '\n')
        except OSError:
            Logging.error("Couldn't write a line from file!")

    # Write list of lines to file
    def write_all(self, file, lines):
        try:
            for item in lines:
                file.write(item + '\n')
        except OSError:
            Logging.error("Couldn't write to file!")
