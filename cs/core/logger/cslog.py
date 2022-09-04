import logging
import logging.config
from enum import Enum
from pprint import pprint
import google.cloud.logging
import cs.core.utils.config
import yaml
import os

from cs.core.utils.config import AppConfig
from google.cloud.logging import Client
from google.cloud.logging.handlers import CloudLoggingHandler
from google.oauth2 import service_account


class CsLogger:
    def __init__(self, config_file=''):
        self.config_file = config_file

    def get_logger(self, name, log_type='default'):

        if not self.config_file:
            log_config = AppConfig.get_config_dict("logging_config.yml")
        else:
            log_config = AppConfig.get_config_dict(self.config_file)

        logging.config.dictConfig(log_config)
        logger = logging.getLogger(log_type + "." + name)
        return logger
