import configparser
import os
import tkinter.messagebox as messagebox

import pymysql
import pymysql.cursors
from icecream import ic

from constants.constants import ConfigParameters, DBParams, ErrorsParams, SQLRequests
from domain.models import Record
from infrastructure.db.db_base_adapter import BaseDBAdapter
from infrastructure.db.exceptions import DatabaseExecutionError
from infrastructure.gui.custom_dialog import CustomDialog


class DBAdapter(BaseDBAdapter):
    """
    Адаптер работы с БД:
        1) get_rows - получение записей из БД
        2) initialization_connect - подключение к БД при инициализации
        3) initialization_reconnect - повторное подключение при неуспешном
            подключении
        4) insert - вставка данных
        5) update - обновление данных
    """  # noqa: RUF002

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.conn = None

    def get_rows(self, cursor):
        self.execute(cursor, SQLRequests.SQL_GET_ALL)
        return cursor.fetchall()

    def initialization_connect(self):
        config_file = ConfigParameters.CONFIG_PATH
        config_file_is_exist = os.path.isfile(config_file)
        config = configparser.ConfigParser()
        if not config_file_is_exist:
            config.set(ConfigParameters.DB_SECTION, ConfigParameters.HOST_KEY, DBParams.HOST)
            with open(ConfigParameters.CONFIG_PATH, "w") as configfile:
                config.write(configfile)
        config.read(ConfigParameters.CONFIG_PATH)
        ic("Параметры подключения:")
        ic(f"host: {config.get(ConfigParameters.DB_SECTION, ConfigParameters.HOST_KEY)}")
        ic(f"port: {DBParams.PORT}")
        ic(f"user: {DBParams.USER}")
        try:
            self.conn = pymysql.connect(
                host=config.get(ConfigParameters.DB_SECTION, ConfigParameters.HOST_KEY),
                port=DBParams.PORT,
                user=DBParams.USER,
                passwd=DBParams.PASSWORD,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
            )
        except Exception:
            dialog = CustomDialog(self.parent)
            address = dialog.db_ip_address
            if address:
                return self.initialization_reconnect(address)
            else:
                messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_DB_NO_CONN)
        else:
            return self.conn

    def initialization_reconnect(self, address):
        config = configparser.ConfigParser()
        config.read(ConfigParameters.CONFIG_PATH)
        config.set(ConfigParameters.DB_SECTION, ConfigParameters.HOST_KEY, address)
        with open(ConfigParameters.CONFIG_PATH, "w") as configfile:
            config.write(configfile)
        try:
            self.conn = pymysql.connect(
                host=address,
                port=DBParams.PORT,
                user=DBParams.USER,
                passwd=DBParams.PASSWORD,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
            )
        except Exception:
            dialog = CustomDialog(self.parent)
            address = dialog.db_ip_address
            if address:
                return self.initialization_reconnect(address)
            else:
                messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_DB_NO_CONN)
        else:
            return self.conn

    def insert(self, cursor, sql: str, record: Record = None):  # type: ignore
        try:
            if record:
                record_values = (
                    record.record_id,
                    record.record_date,
                    record.record_type,
                    record.record_name,
                    record.record_communication,
                    record.record_from,
                    record.record_who,
                    record.record_description,
                    record.record_note,
                    record.record_author,
                    record.record_status,
                )
                params = record_values
                cursor.execute(sql, params)
        except Exception as e:
            messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_BAD_EXECUTE)
            raise DatabaseExecutionError(ErrorsParams.ERROR_BAD_EXECUTE) from e

    def update(self, cursor, sql: str, record: Record = None):  # type: ignore
        try:
            if record:
                record_values = (
                    record.record_date,
                    record.record_type,
                    record.record_name,
                    record.record_communication,
                    record.record_from,
                    record.record_who,
                    record.record_description,
                    record.record_note,
                    record.record_author,
                    record.record_status,
                )
                params = (*record_values, record.record_id)
                cursor.execute(sql, params)
        except Exception as e:
            messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_BAD_EXECUTE)
            raise DatabaseExecutionError(ErrorsParams.ERROR_BAD_EXECUTE) from e
