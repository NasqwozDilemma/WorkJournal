from typing import Optional


class DatabaseExecutionError(Exception):
    """Кастомное исключение для ошибок базы данных."""
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception
