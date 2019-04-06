import abc


class ExchangeQueueBrokerService:
    @abc.abstractmethod
    def publish(self, exchange, routing_key, message):
        pass

    @abc.abstractmethod
    def create_exchange(self, name, type):
        pass

    @abc.abstractmethod
    def create_queue(self, name):
        pass

    @abc.abstractmethod
    def bind(self, exchange, queue, routing_key):
        pass
