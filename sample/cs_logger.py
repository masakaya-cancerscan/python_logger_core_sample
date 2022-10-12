from coala.logger.cs_logger import CsLogger
from coala.logger.trace import trace_log

cs_logger = CsLogger.get_instance(__file__)
cs_logger.add_field({"user_id": "USER_HOGE", "trace_id": "123456"})
logger = cs_logger.get_logger(__name__)

def zero_division():
    1 / 0


@trace_log(logger)
def main():
    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

    # コンソールは出力されないが、Google Cloud Loggingには自動的に出力される
    custom_dict = {
        'custom1': "test1"
    }
    logger.info('custom value', extra=custom_dict)
    zero_division()


if __name__ == '__main__':
    main()
