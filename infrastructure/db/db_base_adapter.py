import configparser
import tkinter.messagebox as messagebox

import pymysql
import pymysql.cursors

from constants.constants import ConfigParameters, DBParams, ErrorsParams
from infrastructure.db.exceptions import DatabaseExecutionError


class BaseDBAdapter:
    """
    Базовый адаптер работы с БД:
        1) connect - подключение к БД при выполнении запроса
        2) execute - выполнение запроса
        3) executemany - выполнение множественного запроса
        4) commit - подтверждени транзакции
        5) roolback - откат транзакции
        6) close - закрытие транзакции
    """  # noqa: RUF002

    def __init__(self):
        super().__init__()
        self.conn = None

    def connect(self):
        config = configparser.ConfigParser()
        config.read(ConfigParameters.CONFIG_PATH)
        try:
            self.conn = pymysql.connect(
                host=config.get(ConfigParameters.DB_SECTION, ConfigParameters.HOST_KEY),
                port=DBParams.PORT,
                user=DBParams.USER,
                passwd=DBParams.PASSWORD,
                database=DBParams.DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
            )
            return self.conn
        except Exception as e:
            messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_DB_NO_CONN)
            raise DatabaseExecutionError(ErrorsParams.ERROR_DB_NO_CONN) from e

    def execute(self, cursor, sql):
        try:
            cursor.execute(sql)
        except Exception as e:
            messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_BAD_EXECUTE)
            raise DatabaseExecutionError(ErrorsParams.ERROR_BAD_EXECUTE) from e

    def executemany(self, cursor, sql, *args):
        try:
            cursor.executemany(sql, *args)
        except Exception as e:
            messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_BAD_EXECUTE)
            raise DatabaseExecutionError(ErrorsParams.ERROR_BAD_EXECUTE) from e

    def commit(self):
        if self.conn is not None:
            self.conn.commit()

    def rollback(self):
        if self.conn is not None:
            self.conn.rollback()

    def close(self, cursor):
        if self.conn is not None:
            cursor.close()
            self.conn.close()
