import inspect
import logging.config
import os

from cs.core.utils.config import AppConfig
from functools import wraps

# ログファイル名
LOGGING_CONFIG_NAME: str = "logging_config.yml"

# 探査するディレクトリの階層するを指定する
SEARCH_LOGGING_CONFIG_FILE_DEPTH: int = 3


class CsLogger:

    """
    コンストラクタ

    :arg
        config_file: logの設定ファイルをファイルパスを渡す（デフォルト：未指定（自動的にコンフィグファイルをロードする））
    """

    def __init__(self, config_file=''):
        self.config_file = config_file
        self.call_filepath = inspect.currentframe().f_back.f_code.co_filename

    """
    ローカルファイルに配置されたlogging_config.ymlを捜査して取得する

    :arg
        name: 取得するlogger名（基本的には get_logger(__name__))で良い
        log_type: 設定ファイルにて定義したlogger名を指定（デフォルト：develop ）
    :return
        logger Python標準のlogger
    """

    def get_logger(self, name, log_type='develop'):

        if not self.config_file:
            # ローカルファイルにlogging_config.ymlを捜査して取得する
            log_config_path = self._detect_file_config()
            if log_config_path is None:
                # 検出できなかった場合はライブラリのコンフィグをロードする
                print('logger_config file could not be detected. load library default config.')
                log_config_path = AppConfig.get_config_dir(LOGGING_CONFIG_NAME)
                log_config = AppConfig.get_config_dict(log_config_path)
                print('load library default config.({})'.format(log_config_path))
            else:
                log_config = AppConfig.get_config_dict(log_config_path)
        else:
            log_config = AppConfig.get_config_dict(self.config_file)

        # 環境変数(ENVIRONMENT)からLoggerの切り替え
        env = os.environ.get('ENVIRONMENT')
        if env is not None:
            log_type = env

        logging.config.dictConfig(log_config)
        logger: logging.Logger = logging.getLogger(log_type + "." + name)
        return logger

    """
    ローカルファイルに配置されたlogging_config.ymlを捜査して取得する
    
    :arg
        depth: 捜査を階層（default:3階層までさかのぼってファイル検索を行う）
        path: 設定ファイルのパス
        
    :return
        str 設定ファイルのパス
    """

    def _detect_file_config(self, depth=SEARCH_LOGGING_CONFIG_FILE_DEPTH, path='') -> str:
        # no detect
        if depth == 0:
            return ''

        if path == '':
            search_dir = os.path.dirname(os.path.abspath(self.call_filepath))
            find_path = os.path.join(search_dir, LOGGING_CONFIG_NAME)
            if os.path.exists(find_path):
                print('detect logger_config file.')
                return find_path
            else:
                parent_dir_path = os.path.dirname(search_dir)
                self._detect_file_config(depth=depth - 1, path=parent_dir_path)
        else:
            find_path = os.path.join(path, LOGGING_CONFIG_NAME)
            if os.path.exists(find_path):
                # detect config file
                print('detect logger_config file.')
                return find_path
            else:
                parent_dir_path = os.path.dirname(path)
                self._detect_file_config(depth=depth - 1, path=parent_dir_path)


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
                logging.debug(f'[TRACE][End] {trace_data}')

        return wrapper

    return _decorator
