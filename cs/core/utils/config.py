# coding:utf-8
import os
import socket

import yaml


class AppConfig:

    @staticmethod
    def get_base_dir():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def get_config_dir(filename):
        base_dir = AppConfig.get_base_dir()
        config_file = os.path.join(base_dir, filename)
        return config_file

    @staticmethod
    def get_config_dict(file_path):
        with open(os.path.join(file_path), 'r', encoding='UTF-8') as f:
            config = f.read()
        return yaml.safe_load(config)

    @staticmethod
    def get_config_properties(filename, key):
        """
        設定ファイルからキーに紐づく値を取得する
        """
        dict = AppConfig.get_config_dict(filename)
        return dict[key]
