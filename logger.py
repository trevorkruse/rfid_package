import logging
from termcolor import colored


class Logger:

    def __init__(self,log_name, file_path, level=logging.INFO):
        self.FORMAT = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.handler = logging.FileHandler(file_path)
        self.handler.setFormatter(self.FORMAT)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level)
        self.logger.addHandler(self.handler)

    def info(self, log):
        self.logger.info(colored(log, "green"))

    def warning(self, log):
        self.logger.warning(colored(log, "blue"))

    def error(self, log):
        self.logger.error(colored(log, "yellow"))

    def critical(self, log):
        self.logger.critical(colored(log, "red"))



