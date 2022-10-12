import logging


class LogAttribute:
    """
    ログ出力したい属性設定する
    :param key: 登録するキー
    :param value: 登録する値
    """
    @staticmethod
    def __setattr__(key, value):
        setattr(LogAttribute, key, value)

    """
    ログ出力したい属性取得する
    :param key: 登録したキー
    """
    @staticmethod
    def __getattr__(key):
        return getattr(LogAttribute, key)


class LogAttributeFilter(logging.Filter):
    """
    ログに任意の項目を追加するFilter
    LogAttributeに登録されているKey-value情報からログに新しいフィールドを追加する。
    :param record: ログレコード
    :return bool
    """
    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in LogAttribute.__dict__.items():
            if not key.startswith('_'):
                setattr(record, key, value)
        return True
