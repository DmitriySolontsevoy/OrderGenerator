from Services.MessageBrokerService.API.MessageBrokerService import MessageBrokerService
import abc


class ExchangeQueueBrokerService(MessageBrokerService):
    @abc.abstractmethod
    def publish(self, exchange, key, message):
        pass

    @abc.abstractmethod
    def create_exchange(self, name, type):
        pass

    @abc.abstractmethod
    def create_queue(self, name):
        pass

    @abc.abstractmethod
    def bind(self, exchange, queue, key):
        pass
