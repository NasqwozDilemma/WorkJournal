from typing import ClassVar


class MainWindowParams:
    MAIN_WINDOW_NAME = "Технический журнал"
    ICON_PATH = "./config/work-journal.ico"
    MIN_WIDTH = 1800
    MIN_HEIGHT = 850


class DataFrameParams:
    DATA_FRAME_CLEAR_BUTTON_TEXT = "Очитска полей"


class CommandFrameParams:
    COMMAND_INSERT_BUTTON = "Добавить запись"
    COMMAND_UPDATE_BUTTON = "Редактировать запись"
    COMMAND_DELETE_BUTTON = "Удалить запись(-и)"


class MenuParams:
    MENU_BEGIN_LABEL = "От"
    MENU_END_LABEL = "До"
    MENU_TYPE_LABEL = "Тип записи"
    MENU_NAME_LABEL = "Название объекта"
    MENU_COMMUNICATION_LABEL = "Оборудование"
    MENU_AUTHOR_LABEL = "Автор записи"
    MENU_STATUS_LABEL = "Статус записи"
    MENU_FILTER_BUTTON = "Фильтрация"
    MENU_SEARCH_LABEL = "Значение для поиска"
    MENU_SEARCH_BUTTON = "Поиск"
    MENU_SEARCH_CHECK_LABEL = "Полное совпадение:"
    MENU_CLEAR_BUTTON = "Очитска полей"
    MENU_RESET_BUTTON = "Сбросить"


class DateWindowParams:
    MIN_WIDTH = 320
    MIN_HEIGHT = 330
    DATE_WINDOW_TEXT = "Дата и время"
    DATE_HOUR_LABEL = "Час"
    DATE_MINUTE_LABEL = "Минута"
    DATE_SUBMIT_BUTTON = "Ок"
    DATE_CANCEL_BUTTON = "Отмена"
    ZERO_VALUE_HOUR = "00"
    MIN_VALUE_HOUR = 1
    MAX_VALUE_HOUR = 24
    ZERO_VALUE_MINUTE = "00"
    MIN_VALUE_MINUTE = 1
    MAX_VALUE_MINUTE = 60
    DATE_REG = (
        r"([2][0]\d{2}).([0]\d|[1][0-2]).([0-2]\d|[3][0-1]) "
        r"([0-1]\d|[2][0-3]):([0-5]\d):([0-5]\d)"
    )


class ObjectWindowParams:
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 300
    SUBMIT_BUTTON = "Ок"
    CANCEL_BUTTON = "Отмена"
    CLEAR_BUTTON = "Очистить поле"


class CommunicationWindowParams:
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 300
    SUBMIT_BUTTON = "Ок"
    CANCEL_BUTTON = "Отмена"
    CLEAR_BUTTON = "Очистить поле"


class EmptyValues:
    EMPTY_STRING = ""
    ZERO = 0


class DBParams:
    HOST = "localhost"
    PORT = 3306
    USER = "worker"
    PASSWORD = "worker"
    DB_NAME = "workjournaldb"


class SQLRequests:
    SQL_CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS workjournaldb"
    SQL_USE_DB = "USE workjournaldb"
    SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS `work` (
        `ID` int NOT NULL AUTO_INCREMENT,
        `Date` datetime NOT NULL,
        `Type` varchar(200) NOT NULL,
        `Name` varchar(200) NOT NULL,
        `Communication` varchar(200) NOT NULL,
        `Sender_from` varchar(200) DEFAULT NULL,
        `Sender_who` varchar(200) DEFAULT NULL,
        `Description` varchar(5000) NOT NULL,
        `Note` varchar(5000) DEFAULT NULL,
        `Author` varchar(200) NOT NULL,
        `Status` tinyint DEFAULT '0',
        PRIMARY KEY (`ID`),
        UNIQUE KEY `ID_UNIQUE` (`ID`)
        ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4
        COLLATE=utf8mb4_0900_ai_ci;"""
    SQL_GET_ALL = "SELECT * FROM work ORDER BY Date, ID"
    SQL_GET_IDS = "SELECT ID FROM work"
    SQL_GET_TYPES = "SELECT Type FROM work"
    SQL_GET_NAMES = "SELECT Name FROM work"
    SQL_GET_COMMUNICATIONS = "SELECT Communication FROM work"
    SQL_GET_AUTHORS = "SELECT Author FROM work"
    SQL_GET_STATUS = "SELECT Status FROM work"
    SQL_INSERT = "INSERT INTO work VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    SQL_UPDATE = """UPDATE work SET Date=%s, Type=%s, Name=%s, Communication=%s, Sender_from=%s,
        Sender_who=%s, Description=%s, Note=%s, Author=%s, Status=%s
        WHERE ID=%s"""
    SQL_DELETE = "DELETE FROM work WHERE ID = %s"


class TableHeaders:
    ID = "№"
    DATE = "Дата записи"
    TYPE = "Тип записи"
    NAME = "Название объекта"
    COMMUNICATION = "Оборудование"
    FROM = "Откуда"
    WHO = "От кого"
    DESC = "Описание"
    NOTE = "Примечание"
    AUTHOR = "Автор записи"
    STATUS = "Статус записи"
    ID_SQL = "ID"
    DATE_SQL = "Date"
    TYPE_SQL = "Type"
    NAME_SQL = "Name"
    COMMUNICATION_SQL = "Communication"
    FROM_SQL = "Sender_from"
    WHO_SQL = "Sender_who"
    DESC_SQL = "Description"
    NOTE_SQL = "Note"
    AUTHOR_SQL = "Author"
    STATUS_SQL = "Status"
    ID_IDX = 0
    DATE_IDX = 1
    TYPE_IDX = 2
    NAME_IDX = 3
    COMMUNICATION_IDX = 4
    FROM_IDX = 5
    WHO_IDX = 6
    DESC_IDX = 7
    NOTE_IDX = 8
    AUTHOR_IDX = 9
    STATUS_IDX = 10


class StatusValues:
    COMPLETE_STRING = "Выполнено"
    NOT_COMPLETE_STRING = "Не выполнено"
    BOOL_TRUE = 1
    BOOL_FALSE = 0


class DeleteAskParams:
    DELETE_WINDOW_NAME = "Осторожно!"
    DELETE_MESSAGE = "Это действие удалит ВСЕ ВЫДЕЛЕННЫЕ данные.\nВы уверены?"


class ErrorsParams:
    ERROR_WINDOW_NAME = "Ошибка"
    ERROR_DB_NO_CONN = "Не удалось подключиться к БД."
    ERROR_ENTER_DB_IP = "Введите IP адрес БД"
    ERROR_BAD_EXECUTE = "Запрос не выполнен."
    ERROR_EMPTY_DATE = "Вставьте дату записи."
    ERROR_EMPTY_TYPE = "Вставьте тип записи."
    ERROR_EMPTY_NAME = "Вставьте название объекта."
    ERROR_EMPTY_COMMUNICATION = "Вставьте название оборудования."
    ERROR_EMPTY_DESC = "Вставьте описание записи."
    ERROR_EMPTY_AUTHOR = "Вставьте автора записи."
    ERROR_LEN_TYPE = f'Превышено ограничение по длине в поле "{TableHeaders.TYPE}".'
    ERROR_LEN_NAME = f'Превышено ограничение по длине в поле "{TableHeaders.NAME}".'
    ERROR_LEN_COMMUNICATION = f'Превышено ограничение по длине в поле "{TableHeaders.COMMUNICATION}".'
    ERROR_LEN_FROM = f'Превышено ограничение по длине в поле "{TableHeaders.FROM}".'
    ERROR_LEN_WHO = f'Превышено ограничение по длине в поле "{TableHeaders.WHO}".'
    ERROR_LEN_DESC = f'Превышено ограничение по длине в поле "{TableHeaders.DESC}".'
    ERROR_LEN_NOTE = f'Превышено ограничение по длине в поле "{TableHeaders.NOTE}".'
    ERROR_LEN_AUTHOR = f'Превышено ограничение по длине в поле "{TableHeaders.AUTHOR}".'
    ERROR_NOT_SELECTED_TO_DELETE = "Выберите строки для удаления."
    ERROR_SELECTED_DATE_PERIOD = "Выбран неправильный временной промежуток."
    ERROR_DATE_FORMAT = "Указана неверная дата."
    ERROR_BEGIN_DATE_FORMAT = "Указана неверная начальная дата."
    ERROR_END_DATE_FORMAT = "Указана неверная конечная дата."


class Reservation:
    FRIDAY = 4
    ONE_DAY = 1
    ONE_WEEK = 7
    SAVE_HOURS = 17
    BACKUPS_PATH = "./db_backups/"
    DB_BACKUP_FILE = "workjournaldb_work.sql"


class DateTimeValues:
    TABLE_FORMAT = "%Y.%m.%d %H:%M:%S"


class DefaultLists:
    """
    Класс дефолтных значений для полей записи.

    TYPES_LIST - тип события;
    NAME_LIST - название объекта (адрес);
    COMMUNICATION_LIST - наименование оборудования;
    AUTHOR_LIST - автор записи;
    STATUS_LIST - статус события.
    """

    TYPES_LIST: ClassVar[list[str]] = [
        "Авария",
        "Информация",
        "Конфигурирование оборудования",
        "Монтажные работы",
        "Согласование исходных данных",
        "Указание"
    ]
    NAME_LIST: ClassVar[list[str]] = []
    COMMUNICATION_LIST: ClassVar[list[str]] = []
    AUTHOR_LIST: ClassVar[list[str]] = []
    STATUS_LIST: ClassVar[list[str]] = ["Выполнено", "Не выполнено"]


class ConfigParameters:
    CONFIG_PATH = "./config/config.ini"
    DB_SECTION = "DB_Params"
    HOST_KEY = "Host"


class CustomDialogParams:
    TITLE = "Подключение к БД"
    LABLE = "Введите адрес БД:"
    BTN_OK = "ОК"
    BTN_CANCEL = "Отмена"
