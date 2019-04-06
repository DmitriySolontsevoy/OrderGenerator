import abc


class MessageConsumer:
    @staticmethod
    @abc.abstractmethod
    def __callback(ch, method, properties, body):
        pass

    @abc.abstractmethod
    def consume(self):
        pass
