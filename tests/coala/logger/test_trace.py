import pytest

from coala.logger.cs_logger import CsLogger
from logging import DEBUG, ERROR
from coala.logger.trace import trace_log


@pytest.fixture(autouse=True)
def init_mock(mocker):
    """
    Google認証の置き換えるfixturea
    :param mocker: mocker関数
    :return:
    """
    mocker.patch("google.auth.default", return_value=("dummy", "project_id"))


def test_trace_normal(caplog):
    """
    トレースログ出力試験
    :param caplog: loggerの出力内容をキャプチャする(正常系)
    :return:
    """
    logger_name = 'testLogger'
    logger = CsLogger.get_instance(__file__).get_logger(logger_name)
    logger.addHandler(caplog.handler)

    # トレースログの実行
    with caplog.at_level(DEBUG):
        @trace_log(logger)
        def trace_test_function():
            pass

        # テスト関数の実行
        trace_test_function()

    # 開始ログ（最初のログ）
    assert caplog.records[0].levelno == DEBUG
    assert caplog.records[0].message.find('[Trace][Start]') != -1

    # 終了ログ(最後のログ)
    assert caplog.records[len(caplog.records)-1].levelno == DEBUG
    assert caplog.records[len(caplog.records)-1].message.find('[Trace][End]') != -1

    # teardown
    CsLogger.get_instance(__file__).clear_instance()


def test_trace_exception(caplog):
    """
    トレースログ出力試験
    :param caplog: loggerの出力内容をキャプチャする(異常系)
    :return:
    """
    logger_name = 'testLogger'
    logger = CsLogger.get_instance(__file__).get_logger(logger_name)
    logger.addHandler(caplog.handler)

    # トレースログの実行
    with caplog.at_level(DEBUG):
        @trace_log(logger)
        def trace_test_function():
            zero_division()
            pass

        def zero_division():
            1 / 0

        # テスト関数の実行
        trace_test_function()

    # 開始ログ（最初のログ）
    assert caplog.records[0].levelno == DEBUG
    assert caplog.records[0].message.find('[Trace][Start]') != -1

    # スタックトレースログ(中間のログ)
    assert caplog.records[1].levelno == ERROR
    assert caplog.records[1].message.find('[Trace][Exception]') != -1

    # 終了ログ(最後のログ)
    assert caplog.records[len(caplog.records)-1].levelno == DEBUG
    assert caplog.records[len(caplog.records)-1].message.find('[Trace][End]') != -1

    # teardown
    CsLogger.get_instance(__file__).clear_instance()

