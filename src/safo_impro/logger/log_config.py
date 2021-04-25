import logging
import logging.config


class LogConfig:
    def __init__(self):
        pass

    def get_logger(self):
        logging.config.fileConfig(fname='safo_impro/logger/logger.conf', disable_existing_loggers=False)
        return logging.getLogger(__name__)
