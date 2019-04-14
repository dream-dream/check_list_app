import os
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LoggingSet():
    def __init__(self):
        self.path = os.path.join(BASE_DIR, "flask_check_list/flask_logs")
        self.maxBytes = 1024 * 1024 * 100
        self.default_formatter = logging.Formatter(
            '%(levelname)s %(filename)s:%(lineno)d %(message)s')
        self.error_formatter = logging.Formatter(
            '[%(asctime)s] [%(filename)s:%(lineno)d\t] [%(levelname)s]  %(message)s '
        )

    def debug_log(self, log_level):
        logging.basicConfig(level=log_level)
        file_log_handler = RotatingFileHandler(
            os.path.join(self.path, "flask.log"),
            # maxBytes=1024 * 1024 * 100,
            maxBytes=self.maxBytes,
            backupCount=10
        )
        file_log_handler.setFormatter(self.default_formatter)
        logging.getLogger().addHandler(file_log_handler)

    def error_log(self, log_level):
        logging.basicConfig(level=log_level)
        file_error_handler = RotatingFileHandler(
            os.path.join(self.path, 'error.log'),
            maxBytes=self.maxBytes,
            backupCount=5
        )
        file_error_handler.setFormatter(self.error_formatter)
        logging.getLogger().addHandler(file_error_handler)


