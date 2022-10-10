import inspect
from functools import wraps


def trace_log(logger):
    def _decorator(func):
        """デコレーターを使用する関数を引数とする

        Args:
            func (function)

        Returns:
            wrapperの返り値
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """実際の処理を書くための関数

            Args:
                *args, **kwargs: funcの引数

            Returns:
                funcの返り値
            """
            filename = inspect.stack()[1].filename
            module_name = func.__module__
            func_name = func.__name__
            line_no = inspect.currentframe().f_back.f_lineno
            trace_data = f'{filename}:{module_name}.{func_name}:{line_no}'
            # loggerで使用するためにfuncに関する情報をdict化
            logger.debug(f'[Trace][Start] {trace_data}')
            try:
                # funcの実行
                return func(*args, **kwargs)
            except BaseException as ex:
                logger.error(f'[Trace][Exception] {trace_data}')
                logger.exception(ex, exc_info=True)
            finally:
                logger.debug(f'[Trace][End] {trace_data}')

        return wrapper

    return _decorator
