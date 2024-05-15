import logging
import warnings


class Logger:
    """
    Logger class\n
    Author: Pedro Henrique Gonçalves Pires\n
    Date: 25/05/2023\n
    """
    def __init__(self, name: str, log_file: str):
        """
        Creates a logger with info level
        :param name: Name of the logger
        :param log_file: Name of the log file
        :return: Logger
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(message)s\n')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def log(self, message: str, to_print: bool = False, to_warn: bool = False):
        """
        Logs a message
        :param message: Message to log
        :param to_print: If the message should be printed
        :param to_warn: If the message should be warned
        :return: None
        """
        self.logger.info(message)

        if to_print:
            print(message)

        if to_warn:
            warnings.warn(message)

