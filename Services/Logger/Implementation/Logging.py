class Logging:
    text_file_logger = None
    console_logger = None

    targets = []

    @staticmethod
    def init(txt_flag, console_flag):
        if txt_flag:
            Logging.targets.append(Logging.text_file_logger)
        if console_flag:
            Logging.targets.append(Logging.console_logger)

    @staticmethod
    def start():
        for logger in Logging.targets:
            logger.start()

    @staticmethod
    def debug(message):
        for logger in Logging.targets:
            logger.debug(message)

    @staticmethod
    def info(message):
        for logger in Logging.targets:
            logger.info(message)

    @staticmethod
    def warn(message):
        for logger in Logging.targets:
            logger.warn(message)

    @staticmethod
    def error(message):
        for logger in Logging.targets:
            logger.error(message)
