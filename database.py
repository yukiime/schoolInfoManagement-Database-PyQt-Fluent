import os
import configparser

import pymysql

# 数据库连接信息从 config.ini 读取（参考 config.example.ini），
# 也可以用环境变量 DB_HOST / DB_USER / DB_PASSWORD / DB_NAME 覆盖，
# 避免把真实密码写进代码库
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")


def _load_db_config():
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "school_info_db",
    }
    parser = configparser.ConfigParser()
    if parser.read(CONFIG_FILE, encoding="utf-8") and parser.has_section("mysql"):
        for key in config:
            if parser.has_option("mysql", key):
                config[key] = parser.get("mysql", key)

    env_map = {
        "host": "DB_HOST",
        "user": "DB_USER",
        "password": "DB_PASSWORD",
        "database": "DB_NAME",
    }
    for key, env_name in env_map.items():
        if os.environ.get(env_name):
            config[key] = os.environ[env_name]
    return config


class DatabaseConnection:
    def __init__(self):
        self.db = None

    def connect(self):
        self.db = pymysql.connect(**_load_db_config())

    def disconnect(self):
        if self.db:
            self.db.close()

    def execute_query(self, query, values=None):
        cursor = self.db.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        self.db.commit()
        return result

    def execute_query_needColName(self, query, values=None):
        cursor = self.db.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        col = cursor.description
        cursor.close()
        self.db.commit()
        return result, col

    def callproc_query(self, query, values=("", "")):
        cursor = self.db.cursor()
        cursor.callproc(query, args=values)

        result = cursor.fetchall()
        col = cursor.description

        cursor.close()
        return result, col
