import logging.config
import os
import sys

from typing import Any, Dict

from cs.core.logger.filter import LogAttribute
from cs.core.utils.config import AppConfig

# ログファイル名
LOGGING_CONFIG_NAME: str = "logging_config.yml"

# 探査するディレクトリの階層するを指定する
SEARCH_LOGGING_CONFIG_FILE_DEPTH: int = 3

# デフォルトログタイプ
DEFAULT_LOG_TYPE = "develop"


class CsLogger:
    _instance = None
    _call_filepath = None

    def __new__(cls):
        """
            コンストラクタの可視性をPrivateにする
            インスタンス生成した場合（ __init__ )が呼ばれる場合 __new__ が先に呼ばれるため
            インスタンス生成を抑止する
        """
        raise NotImplementedError('Cannot Generate Instance By Constructor')

    @classmethod
    def __internal_new__(cls, file):
        """
            インスタンスを生成する
            初回インスタンス生成時は以下の振舞をする

            1. 初回インスタンス生成、呼び元のpyファイルの場所からloggerのコンフィグファイルを検索
            2. ログの設定ファイルが見つかった場合は、見つかった設定ファイル、見つからない場合が保持しているデフォルトの設定ファイルをロード
            3. インスタンスを生成する

        """
        cls._call_filepath = os.path.abspath(file)

        # ローカルファイルにlogging_config.ymlを捜査して取得する
        log_config_path = cls.__detect_file_config()
        if log_config_path is None:
            # 検出できなかった場合はライブラリのコンフィグをロードする
            sys.stdout.write('logger_config file could not be detected. load library default config.')
            log_config_path = AppConfig.get_config_dir(LOGGING_CONFIG_NAME)
            log_config = AppConfig.get_config_dict(log_config_path)
            sys.stdout.write('load library default config.({})'.format(log_config_path))
        else:
            sys.stdout.write('load application logger config.({})'.format(log_config_path))
            log_config = AppConfig.get_config_dict(log_config_path)

        logging.config.dictConfig(log_config)
        return super().__new__(cls)

    @classmethod
    def get_instance(cls, file):
        """
        CsLoggerインスタンスを取得する

        :return: インスタンス
        """
        if not cls._instance:
            cls._instance = cls.__internal_new__(file)
            return cls._instance
        else:
            return cls._instance

    @classmethod
    def clear_instance(cls):
        """
        インスタンス、設定情報を削除する
        :return: なし
        """
        cls._call_filepath = ''
        cls._instance = None

    @classmethod
    def add_field(cls, log_dict: Dict[str, Any]):
        """
        ログに追加フィールドを入れる
        :param log_dict: 追加したいフィールド（フィールド名、出力値）
        :return: void
        """
        for key, value in log_dict.items():
            LogAttribute.__setattr__(key, value)

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

    @classmethod
    def get_logger(cls, name, log_type=None):

        if log_type is not None:
            _log_type = log_type
        else:
            # 環境変数(ENVIRONMENT)からLoggerの切り替え
            env = os.environ.get('ENVIRONMENT')
            if env is not None:
                _log_type = env
            else:
                _log_type = DEFAULT_LOG_TYPE

        logger: logging.Logger = logging.getLogger(_log_type + "." + name)
        return logger
