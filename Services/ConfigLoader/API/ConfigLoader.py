import abc


class ConfigLoader:
    @abc.abstractmethod
    def parse(self):
        pass

    @abc.abstractmethod
    def __verify(self):
        pass
