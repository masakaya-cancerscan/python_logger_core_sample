from cs.core.logger import cslog
from cs.core.logger.cslog import CsLogger

logger = CsLogger().get_logger(__name__)

def zero_division():
    1/0

if __name__ == '__main__':
    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

    # コンソールは出力されないが、Google Cloud Loggingには自動的に出力される
    custom_dict = {
        'custom1':"test1"
    }
    logger.info('custom value',extra=custom_dict)

    try:
        zero_division()
    except Exception as ex:
        logger.error(ex, exc_info=True)
