import logging.config
from cs.core.utils.config import AppConfig


class CsLogger:
    def __init__(self, config_file=''):
        self.config_file = config_file

    def get_logger(self, name, log_type='develop'):

        if not self.config_file:
            log_config = AppConfig.get_config_dict("logging_config.yml")
        else:
            log_config = AppConfig.get_config_dict(self.config_file)

        # 環境変数(environment)

        logging.config.dictConfig(log_config)
        logger: logging.Logger = logging.getLogger(log_type + "." + name)
        return logger
