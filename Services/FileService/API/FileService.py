import abc


class FileService:
    @abc.abstractmethod
    def open_file(self, path, mode):
        pass

    @abc.abstractmethod
    def read_line(self, file):
        pass

    @abc.abstractmethod
    def read_all(self, file):
        pass

    @abc.abstractmethod
    def write_line(self, file, line):
        pass

    @abc.abstractmethod
    def write_all(self, file, lines):
        pass
