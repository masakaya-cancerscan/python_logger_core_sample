from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging import Client

LOG_NAME = 'application'


class CsCloudLoggingHandler(CloudLoggingHandler):
    def __init__(self):
        super(CsCloudLoggingHandler, self).__init__(client=Client(), name=LOG_NAME)
