from cs.core.logger import cslog
from cs.core.logger.cslog import CsLogger
from cs.core.logger.cslog import trace_log

logger = CsLogger().get_logger(__name__)

def zero_division():
    1/0


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