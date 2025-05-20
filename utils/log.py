# utils/log.py

import logging
import os

os.makedirs('./logs', exist_ok=True)

class Logger:
    """
    Logger class for handling logging in the application.
    """
    def __init__(self):
        self.error_handler = logging.FileHandler('./logs/error.log', 'a', 'utf-8')
        self.error_handler.setLevel(logging.ERROR)
        self.error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.warning_handler = logging.FileHandler('./logs/warning.log', 'a', 'utf-8')
        self.warning_handler.setLevel(logging.WARNING)
        self.warning_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.info_handler = logging.FileHandler('./logs/info.log', 'a', 'utf-8')
        self.info_handler.setLevel(logging.INFO)
        self.info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.debug_handler = logging.FileHandler('./logs/debug.log', 'a', 'utf-8')
        self.debug_handler.setLevel(logging.DEBUG)
        self.debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.info_handler)
        self.logger.addHandler(self.warning_handler)
        self.logger.addHandler(self.error_handler)
        self.logger.addHandler(self.debug_handler)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info("Logger initialized.")
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)