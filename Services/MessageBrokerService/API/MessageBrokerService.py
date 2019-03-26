from Services.Logger.Implementation.Logging import Logging
import abc


class MessageBrokerService:
    connection = None

    @abc.abstractmethod
    def open_connection(self, host, port, vhost, user, password):
        pass

    def close_connection(self):
        try:
            self.connection.close
        except Exception as err:
            Logging.text_file_logger.error("Couldn't close connection to RMQ. Error: " + err.__str__())
