import logging
import os
import shutil

import pytest

from coala.logger.cs_logger import CsLogger
from coala.logger.handler import CsCloudLoggingHandler
from logging import DEBUG, INFO, ERROR, WARNING, CRITICAL


@pytest.fixture(autouse=True)
def init_mock(mocker):
    """
    Google認証の置き換えるfixturea
    :param mocker: mocker関数
    :return:
    """
    mocker.patch("google.auth.default", return_value=("dummy", "project_id"))


def test_instance_new():
    """
    コンストラクタが隠蔽されているかのテスト
    :return:
    """
    with pytest.raises(NotImplementedError) as e:
        dummy = CsLogger()

    assert str(e.value) == "Cannot Generate Instance By Constructor"


def test_getInstance():
    """
    同一インスタンスが取得できることを確認するテスト
    :return:
    """
    instance1 = CsLogger.get_instance(__file__)
    instance2 = CsLogger.get_instance(__file__)

    assert (instance1 == instance2) == True

    # teardown
    # singletonオブジェクトなので片方だけでよい
    instance1.clear_instance()


def test_not_detect_config(capsys):
    """
    コンフィグファイルが検出できなかった場合の動作
    :param capsys:sys.stdout.writeの内容を取得する
    :return:
    """
    testee = CsLogger.get_instance(__file__)
    captured = capsys.readouterr()
    assert "logger_config file could not be detected. load library default config." in captured.out
    assert "load library default config." in captured.out

    # teardown
    testee.clear_instance()


def test_detect_config(capsys):
    """
    コンフィグファイルが検出した場合の動作
    :param capsys: sys.stdout.writeの内容を取得する
    :return:
    """
    # テスト用の設定ファイルを配置する
    test_config_file_original = os.path.join(os.path.dirname(__file__), "logging_config.yml.sample")
    test_config_file = os.path.join(os.path.dirname(test_config_file_original), "logging_config.yml")
    shutil.copyfile(test_config_file_original, test_config_file)
    testee = CsLogger.get_instance(__file__)
    captured = capsys.readouterr()
    assert "load application logger config." in captured.out
    # remove sample file.
    os.remove(test_config_file)

    # teardown
    testee.clear_instance()


def test_detect_config_specify(capsys):
    """
    コンフィグファイルをパス指定で取得する場合の動作
    :param capsys:sys.stdout.writeの内容を取得する
    :return:
    """
    # テスト用の設定ファイルを配置する
    test_config_file_original = os.path.join(os.path.dirname(__file__), "logging_config.yml.sample")
    test_config_file = os.path.join('/tmp', 'logging_config.yml')
    shutil.copyfile(test_config_file_original, test_config_file)
    testee = CsLogger.get_instance(test_config_file)
    captured = capsys.readouterr()
    assert "load application logger config." in captured.out
    # remove sample file.
    os.remove(test_config_file)

    # teardown
    testee.clear_instance()


@pytest.mark.parametrize(
    "input_value, expected_prefix ",
    [
        (None, 'develop'),
        ('develop', 'develop'),
        ('staging', 'staging'),
        ('production', 'production')
    ]
)
def test_switch_loggers(input_value, expected_prefix):
    testee = CsLogger.get_instance(__file__)
    logger = testee.get_logger(__name__, log_type=input_value)
    expected = expected_prefix + "." + __name__
    assert logger.name == expected

    CsLogger.get_instance(__file__).clear_instance()


def test_switch_loggers_with_environment(monkeypatch):
    expected_prefix = 'staging'
    monkeypatch.setenv('ENVIRONMENT', expected_prefix)
    expected = expected_prefix + "." + __name__
    logger = CsLogger.get_instance(__file__).get_logger(__name__)
    assert logger.name == expected

    CsLogger.get_instance(__file__).clear_instance()


def test_created_handler():
    """
    ログ作成時のハンドラー生成の試験
    :return:
    """
    logger = CsLogger.get_instance(__file__).get_logger(__name__)

    streamHandler = []
    cloudLoggingsHandler = []
    assert len(logger.parent.handlers) == 2
    for handler in logger.parent.handlers:
        if type(handler) == logging.StreamHandler:
            streamHandler.append(handler)
        elif type(handler) == CsCloudLoggingHandler:
            cloudLoggingsHandler.append(handler)

    assert len(streamHandler) == 1, 'StreamHandler is not one'
    assert len(cloudLoggingsHandler) == 1, 'CloudLoggingsHandler is not one'

    # teardown
    CsLogger.get_instance(__file__).clear_instance()


def test_logging(caplog):
    """
    ログ出力試験
    :param caplog: loggerの出力内容をキャプチャする
    :return:
    """
    test_config_file_original = os.path.join(os.path.dirname(__file__), "logging_config.yml.sample")
    test_config_file = os.path.join('/tmp', 'logging_config.yml')
    shutil.copyfile(test_config_file_original, test_config_file)

    logger_name = 'testLogger'
    logger = CsLogger.get_instance(__file__).get_logger(logger_name)
    logger.addHandler(caplog.handler)
    with caplog.at_level(DEBUG):
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')

    expected_logger_name = 'develop' + "." + logger_name
    assert [(expected_logger_name, DEBUG, 'debug message'),
            (expected_logger_name, INFO, 'info message'),
            (expected_logger_name, WARNING, 'warn message'),
            (expected_logger_name, ERROR, 'error message'),
            (expected_logger_name, CRITICAL, 'critical message')] == caplog.record_tuples

    # teardown
    os.remove(test_config_file)
    CsLogger.get_instance(__file__).clear_instance()


def test_logging_custom_field(caplog):
    """
    ログ出力試験(カスタムフィールド)
    :param caplog: loggerの出力内容をキャプチャする(正常系)
    :return:
    """
    logger_name = 'testLogger'
    cs_logger = CsLogger.get_instance(__file__)
    cs_logger.add_field({"user_id": "USER_HOGE", "trace_id": "123456"})
    logger = cs_logger.get_logger(logger_name)
    logger.addHandler(caplog.handler)

    # トレースログの実行
    with caplog.at_level(DEBUG):
        def trace_test_function():
            logger.debug("debug message")
            pass

        # テスト関数の実行
        trace_test_function()

    assert caplog.records[0].levelno == DEBUG
    assert "debug message" in caplog.records[0].message
    # カスタムフィールドが出力されていること
    assert "USER_HOGE" in caplog.records[0].user_id

    # teardown
    CsLogger.get_instance(__file__).clear_instance()
