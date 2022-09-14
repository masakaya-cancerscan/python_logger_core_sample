import inspect
import logging.config
import os

from cs.core.utils.config import AppConfig
from functools import wraps

# ログファイル名
LOGGING_CONFIG_NAME: str = "logging_config.yml"

# 探査するディレクトリの階層するを指定する
SEARCH_LOGGING_CONFIG_FILE_DEPTH: int = 3


class CsLogger():
    _instance = None
    _call_filepath = None
    _log_type = None

    def __new__(cls):
        """
            コンストラクタの可視性をPrivateにする
            インスタンス生成した場合（ __init__ )が呼ばれる場合 __new__ が先に呼ばれるため
            インスタンス生成を抑止する
        """
        raise NotImplementedError('Cannot Generate Instance By Constructor')

    @classmethod
    def __internal_new__(cls):
        """
            インスタンスを生成する
            初回インスタンス生成時は以下の振舞をする

            1. 初回インスタンス生成、呼び元のpyファイルの場所からloggerのコンフィグファイルを検索
            2. ログの設定ファイルが見つかった場合は、見つかった設定ファイル、見つからない場合が保持しているデフォルトの設定ファイルをロード
            3. 環境変数を読み込み
            4. インスタンスを生成する

        """
        cls._call_filepath = inspect.currentframe().f_back.f_code.co_filename

        # ローカルファイルにlogging_config.ymlを捜査して取得する
        log_config_path = cls.__detect_file_config()
        if log_config_path is None:
            # 検出できなかった場合はライブラリのコンフィグをロードする
            print('logger_config file could not be detected. load library default config.')
            log_config_path = AppConfig.get_config_dir(LOGGING_CONFIG_NAME)
            log_config = AppConfig.get_config_dict(log_config_path)
            print('load library default config.({})'.format(log_config_path))
        else:
            print('load application logger config.({})'.format(log_config_path))
            log_config = AppConfig.get_config_dict(log_config_path)

        # 環境変数(ENVIRONMENT)からLoggerの切り替え
        env = os.environ.get('ENVIRONMENT')
        if env is not None:
            cls._log_type = env

        logging.config.dictConfig(log_config)
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        """
        CsLoggerインスタンスを取得する

        :return: インスタンス
        """
        if not cls._instance:
            cls._instance = cls.__internal_new__()
            return cls._instance

    @classmethod
    def clear_instance(cls):
        """
        インスタンス、設定情報を削除する
        :return: なし
        """
        cls._call_filepath = None
        cls._log_type = None
        del cls._instance


    @classmethod
    def __detect_file_config(cls, depth=SEARCH_LOGGING_CONFIG_FILE_DEPTH, path='') -> str:
        """
        ローカルファイルに配置されたlogging_config.ymlを捜査して取得する

        :arg
            depth: 捜査を階層（default:3階層までさかのぼってファイル検索を行う）
            path: 設定ファイルのパス

        :return
            str 設定ファイルのパス
        """

        # no detect
        if depth == 0:
            return ''

        if path == '':
            search_dir = os.path.dirname(os.path.abspath(cls._call_filepath))
            find_path = os.path.join(search_dir, LOGGING_CONFIG_NAME)
            if os.path.exists(find_path):
                return find_path
            else:
                parent_dir_path = os.path.dirname(search_dir)
                cls.__detect_file_config(depth=depth - 1, path=parent_dir_path)
        else:
            find_path = os.path.join(path, LOGGING_CONFIG_NAME)
            if os.path.exists(find_path):
                # detect config file
                return find_path
            else:
                parent_dir_path = os.path.dirname(path)
                cls.__detect_file_config(depth=depth - 1, path=parent_dir_path)

    def get_logger(self, name, log_type='develop'):

        if self._log_type is not None:
            log_type = self._log_type

        logger: logging.Logger = logging.getLogger(log_type + "." + name)
        return logger


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
