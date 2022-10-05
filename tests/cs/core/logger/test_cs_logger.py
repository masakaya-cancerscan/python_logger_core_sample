import unittest

import pytest

from cs.core.logger.cs_logger import CsLogger


class CsLoggerTestCase(unittest.TestCase):

    def test_instance_new(self):
        """
        コンストラクタが隠蔽されているかのテスト
        :return:
        """
        with pytest.raises(NotImplementedError) as e:
            dummy = CsLogger()

        assert str(e.value) == "Cannot Generate Instance By Constructor"

    def test_getInstance(self):
        """
        同一インスタンスが取得できることを確認するテスト
        :return:
        """
        instance1 = CsLogger.get_instance()
        instance2 = CsLogger.get_instance()

        assert (instance1 == instance2) == True


if __name__ == '__main__':
    unittest.main()
