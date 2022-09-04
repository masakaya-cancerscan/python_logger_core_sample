from cs.core.logger import cslog
from cs.core.logger.cslog import CsLogger

l = CsLogger()
logger1 = l.get_logger(log_name=__name__)

logger = cslog.get_logger()

if __name__ == '__main__':
    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

    # logger1.debug('debug message')
    # logger1.info('info message')
    # logger1.warning('warn message')
    # logger1.error('error message')
    # logger1.critical('critical message')
