from Services.Logger.Implementation.TextFileLogger import TextFileLogger
from Services.Logger.Implementation.Logging import Logging


class MainApp:
    def __init__(self):
        self.queries = None
        self.config = None

    def prep(self):
        Logging.text_file_logger = TextFileLogger("LOG.txt", 4)

    def launch(self):
        pass

    def report(self):
        pass

    def free(self):
        pass

    def __generate_records(self):
        pass

    def __post_to_rabbit(self):
        pass

    def __write_to_file(self):
        pass

    def __read_from_file(self):
        pass

    def __insert_to_db(self):
        pass

    def __return_number_of_batches(self):
        try:
            num_of_batches = (len(self.queries) // self.config.BATCH_SIZE) + 1
        except ZeroDivisionError:
            TextFileLogger.error("Number of batches to generate was set to zero!")
            exit(self.config.ZERO_BATCHES_ERROR)

        return num_of_batches
