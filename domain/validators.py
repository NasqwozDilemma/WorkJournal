import re

from constants.constants import DateWindowParams, ErrorsParams
from interface_adapters.gui_adapter.gui_adapter import GUIAdapter


def validate_data(
    gui_adapter: GUIAdapter,
    record_date,
    record_type,
    record_name,
    record_communication,
    record_from,
    record_who,
    record_description,
    record_note,
    record_author,
):
    if len(record_date) == 0:
        gui_adapter.show_error(message=ErrorsParams.ERROR_EMPTY_DATE)
        raise Exception("Empty date")
    pattern = re.compile(DateWindowParams.DATE_REG)
    if not re.fullmatch(pattern, record_date):
        gui_adapter.show_error(message=ErrorsParams.ERROR_DATE_FORMAT)
        raise Exception("Bad Date format")

    if len(record_type) == 0:
        gui_adapter.show_error(message=ErrorsParams.ERROR_EMPTY_TYPE)
        raise Exception("Empty type")
    if len(record_type) > 200:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_TYPE)
        raise Exception("MAX_LEN type")

    if len(record_name) == 0:
        gui_adapter.show_error(message=ErrorsParams.ERROR_EMPTY_NAME)
        raise Exception("Empty name")
    if len(record_name) > 200:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_NAME)
        raise Exception("MAX_LEN name")

    if len(record_communication) == 0:
        gui_adapter.show_error(message=ErrorsParams.ERROR_EMPTY_COMMUNICATION)
        raise Exception("Empty communication")
    if len(record_communication) > 200:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_COMMUNICATION)
        raise Exception("MAX_LEN communication")

    if len(record_from) > 200:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_FROM)
        raise Exception("MAX_LEN from")

    if len(record_who) > 200:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_WHO)
        raise Exception("MAX_LEN who")

    if len(record_description) == 0:
        gui_adapter.show_error(message=ErrorsParams.ERROR_EMPTY_DESC)
        raise Exception("Empty description")
    if len(record_description) > 5000:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_DESC)
        raise Exception("MAX_LEN description")

    if len(record_note) > 5000:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_NOTE)
        raise Exception("MAX_LEN note")

    if len(record_author) == 0:
        gui_adapter.show_error(message=ErrorsParams.ERROR_EMPTY_AUTHOR)
        raise Exception("Empty author")
    if len(record_author) > 200:
        gui_adapter.show_error(message=ErrorsParams.ERROR_LEN_AUTHOR)
        raise Exception("MAX_LEN author")
