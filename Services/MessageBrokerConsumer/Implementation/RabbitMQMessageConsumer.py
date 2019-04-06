from Services.MessageBrokerConsumer.API.MessageConsumer import MessageConsumer
from Services.Logger.Implementation.Logging import Logging
from Proto.OrderRecord_pb2 import OrderRecord


class RabbitMQMessageConsumer(MessageConsumer):
    def __init__(self, conn):
        self.connector = conn

    @staticmethod
    def __callback(channel, method, header, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        if body == "quit":
            channel.basic_cancel(consumer_tag="hello-consumer")
            channel.stop_consuming()
        else:
            obj = OrderRecord()
            obj.ParseFromString(body)
            Logging.info("Message received: {}".format(obj))
        return

    def consume(self):
        channel = self.connector.connection.channel()

        channel.basic_consume("New", self.__callback)
        channel.basic_consume("ToProvide", self.__callback)
        channel.basic_consume("Reject", self.__callback)
        channel.basic_consume("PartialFilled", self.__callback)
        channel.basic_consume("Filled", self.__callback)

        channel.start_consuming()
