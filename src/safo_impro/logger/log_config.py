import logging
import logging.config
from os import path


class LogConfig:
    def __init__(self):
        pass

    def get_logger(self):
        logger_configuration = path.join(path.dirname(
            path.abspath(__file__)), 'logger.conf')

        logging.config.fileConfig(
            fname=logger_configuration, disable_existing_loggers=False)

        return logging.getLogger(__name__)
