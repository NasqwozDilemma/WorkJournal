from constants.constants import DeleteAskParams, ErrorsParams, SQLRequests, TableHeaders
from domain.models import Record
from domain.validators import validate_data
from interface_adapters.db_adapter.db_adapter import DBAdapter
from interface_adapters.gui_adapter.gui_adapter import GUIAdapter


class DataManager:
    """
    Класс отвечающий за выполнение CRUD-операций.
    """

    def __init__(self, parent, gui_adapter: GUIAdapter, db_adapter: DBAdapter):
        self.parent = parent
        self.db_adapter = db_adapter
        self.gui_adapter = gui_adapter

    def get_data(self):
        (
            record_date,
            record_type,
            record_name,
            record_communication,
            record_from,
            record_who,
            record_description,
            record_note,
            record_author,
            record_status,
        ) = self.gui_adapter.get_fields_data()

        validate_data(
            self.gui_adapter,
            record_date,
            record_type,
            record_name,
            record_communication,
            record_from,
            record_who,
            record_description,
            record_note,
            record_author,
        )

        return (
            record_date,
            record_type,
            record_name,
            record_communication,
            record_from,
            record_who,
            record_description,
            record_note,
            record_author,
            record_status,
        )

    def insert_data(self):
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_IDS)

        id_rows = cursor.fetchall()
        id_max = 0
        for id_row in id_rows:
            if int(id_row[TableHeaders.ID_SQL]) > id_max:
                id_max = int(id_row[TableHeaders.ID_SQL])
        id_max += 1

        (
            record_date,
            record_type,
            record_name,
            record_communication,
            record_from,
            record_who,
            record_description,
            record_note,
            record_author,
            record_status,
        ) = self.get_data()

        record = Record(
            id_=str(id_max),
            date=record_date,
            type_=record_type,
            name=record_name,
            communication=record_communication,
            from_=record_from,
            who=record_who,
            description=record_description,
            note=record_note,
            author=record_author,
            status=record_status,
        )

        try:
            self.db_adapter.insert(
                cursor,
                SQLRequests.SQL_INSERT,
                record,
            )
        except Exception:
            self.db_adapter.rollback()
            self.db_adapter.close(cursor)
        else:
            self.db_adapter.commit()
            self.db_adapter.close(cursor)

        self.parent.dataframe.clear_fields()

        self.parent.treeframe.update_gui()

    def update_data(self):
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        selected = self.parent.treeframe.treeview.focus()

        record_id = self.parent.treeframe.treeview.item(selected, "values")[TableHeaders.ID_IDX]

        (
            record_date,
            record_type,
            record_name,
            record_communication,
            record_from,
            record_who,
            record_description,
            record_note,
            record_author,
            record_status,
        ) = self.get_data()

        record = Record(
            id_=record_id,
            date=record_date,
            type_=record_type,
            name=record_name,
            communication=record_communication,
            from_=record_from,
            who=record_who,
            description=record_description,
            note=record_note,
            author=record_author,
            status=record_status,
        )

        try:
            self.db_adapter.update(
                cursor,
                SQLRequests.SQL_UPDATE,
                record,
            )
        except Exception:
            self.db_adapter.rollback()
            self.db_adapter.close(cursor)
        else:
            self.db_adapter.commit()
            self.db_adapter.close(cursor)

        self.parent.treeframe.update_gui()

    def delete_data(self):
        answer = self.gui_adapter.show_askyesno(DeleteAskParams.DELETE_WINDOW_NAME, DeleteAskParams.DELETE_MESSAGE)

        if answer:
            rows = self.parent.treeframe.treeview.selection()

            if rows == ():
                self.gui_adapter.show_error(message=ErrorsParams.ERROR_NOT_SELECTED_TO_DELETE)
                raise Exception("")

            ids_to_delete = []

            for row in rows:
                ids_to_delete.append(self.parent.treeframe.treeview.item(row, "values")[TableHeaders.ID_IDX])
                self.parent.treeframe.treeview.delete(row)

            conn = self.db_adapter.connect()

            cursor = conn.cursor()

            try:
                self.db_adapter.executemany(
                    cursor,
                    SQLRequests.SQL_DELETE,
                    [(record_id,) for record_id in ids_to_delete],
                )

                ids_to_delete = []
            except Exception:
                self.db_adapter.rollback()
                self.db_adapter.close(cursor)
            else:
                self.db_adapter.commit()
                self.db_adapter.close(cursor)

            self.parent.treeframe.update_gui()
