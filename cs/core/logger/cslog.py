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

    def get_logger(self, log_type='develop', log_name=''):

        if not self.config_file:
            log_config = AppConfig.get_config_dict("logging_config.yml")
        else:
            log_config = AppConfig.get_config_dict(self.config_file)

        # set google cloud logging

        logging.config.dictConfig(log_config)
        logger = logging.getLogger(log_type + "." + log_name)
        return logger



def get_logger():
    client = google.cloud.logging.Client()
    credentials = service_account.Credentials.from_service_account_file(AppConfig.get_config_dir('service_account.json'))
    logging_client = Client(project='loggersample', credentials=credentials)
    handler = CloudLoggingHandler(logging_client, name='DEFAULT_LOGGER')

    # logging.config.dictConfig(yaml.safe_load(open("config.yml").read()))
    # logging.config.dictConfig(AppConfig.get_config_dict("logging_config.yml"))
    logger = logging.getLogger('develop')
    logger.addHandler(handler)
    return logger
