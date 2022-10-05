import logging

from logging import NullHandler

from google.auth.exceptions import DefaultCredentialsError
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging import Client

LOG_NAME = 'application'


class CsCloudLoggingHandler(logging.StreamHandler):
    _handler = None
    _name = None

    def __init__(
            self,
            *,
            name=LOG_NAME,
    ):
        _name = name
        try:
            # Cloud Logging用ハンドラを生成する
            self._handler = DefaultCloudLoggingHandler().__init__()
        except DefaultCredentialsError as ex:
            # NullHandlerを生成する
            print("cloud_logging error. Create NullHandler.")
            self._handler = NullHandler().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        self._handler.emit(record)


class DefaultCloudLoggingHandler(CloudLoggingHandler):
    def __init__(self):
        super(DefaultCloudLoggingHandler, self).__init__(client=Client(), name=LOG_NAME)
