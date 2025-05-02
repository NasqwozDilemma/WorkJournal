import re
import tkinter.messagebox as messagebox
from datetime import datetime
from tkinter import CENTER, END, W, ttk

import customtkinter as ctk

from constants.constants import (
    DateTimeValues,
    DateWindowParams,
    EmptyValues,
    ErrorsParams,
    SQLRequests,
    StatusValues,
    TableHeaders,
)
from domain.models import Record


class TreeFrame(ctk.CTkFrame):
    """
    Таблица, отображающая записи. Также присутствует сортировка по нажатию
    на название колонки таблицы.
    """

    def __init__(self, parent, db_adapter):
        super().__init__(parent)
        self.pack(padx=(20, 10), pady=(0, 10), fill="both", expand=True)
        self.treeScroll_y = ctk.CTkScrollbar(self)
        self.treeScroll_y.pack(side="right", fill="y")
        self.treeScroll_x = ctk.CTkScrollbar(self, orientation="horizontal")
        self.treeScroll_x.pack(side="bottom", fill="x")
        self.parent = parent
        self.db_adapter = db_adapter

        self.create_treeview()
        self.initialization_set_db_data()
        self.treeview.yview_moveto(1)

    def create_treeview(self):
        cols = (
            TableHeaders.ID,
            TableHeaders.DATE,
            TableHeaders.TYPE,
            TableHeaders.NAME,
            TableHeaders.COMMUNICATION,
            TableHeaders.FROM,
            TableHeaders.WHO,
            TableHeaders.DESC,
            TableHeaders.NOTE,
            TableHeaders.AUTHOR,
            TableHeaders.STATUS,
        )
        self.treeview = ttk.Treeview(
            self,
            show="headings",
            yscrollcommand=self.treeScroll_y.set,
            xscrollcommand=self.treeScroll_x.set,
            columns=cols,
        )
        self.treeview.pack(fill="both", expand=True)

        self.treeview.column(TableHeaders.ID, width=25, minwidth=25, stretch=False, anchor=W)
        self.treeview.column(TableHeaders.DATE, width=125, minwidth=125, stretch=False, anchor=W)
        self.treeview.column(TableHeaders.TYPE, width=125, minwidth=125, stretch=False, anchor=CENTER)
        self.treeview.column(TableHeaders.NAME, width=150, minwidth=150, stretch=False, anchor=CENTER)
        self.treeview.column(TableHeaders.COMMUNICATION, width=150, minwidth=150, stretch=False, anchor=CENTER)
        self.treeview.column(TableHeaders.FROM, width=125, minwidth=125, stretch=False, anchor=CENTER)
        self.treeview.column(TableHeaders.WHO, width=125, minwidth=125, stretch=False, anchor=CENTER)
        self.treeview.column(TableHeaders.DESC, width=400, minwidth=400, stretch=True, anchor=W)
        self.treeview.column(TableHeaders.NOTE, width=200, minwidth=200, stretch=True, anchor=W)
        self.treeview.column(TableHeaders.AUTHOR, width=100, minwidth=100, stretch=False, anchor=CENTER)
        self.treeview.column(TableHeaders.STATUS, width=100, minwidth=100, stretch=False, anchor=CENTER)

        for col in cols:
            self.treeview.heading(
                col, text=col, anchor=CENTER, command=lambda _col=col: self.treeview_sort_column(_col, False)
            )

        self.treeview.tag_configure("oddrow", background="white")
        self.treeview.tag_configure("evenrow", background="whitesmoke")
        self.treeview.tag_configure("red_font", foreground="red")
        self.treeview.tag_configure("normal_font", foreground="black")

        self.treeScroll_y.configure(command=self.treeview.yview)
        self.treeScroll_x.configure(command=self.treeview.xview)

        self.treeview.bind("<<TreeviewSelect>>", lambda e: self.select_data(e))

    def initialization_set_db_data(self):
        self.delete_all_treerows()
        conn = self.db_adapter.initialization_connect()
        cursor = conn.cursor()
        try:
            self.db_adapter.execute(cursor, SQLRequests.SQL_CREATE_SCHEMA)
            self.db_adapter.execute(cursor, SQLRequests.SQL_USE_DB)
            self.db_adapter.execute(cursor, SQLRequests.SQL_CREATE_TABLE)
            self.parse_rows(self.db_adapter.get_rows(cursor))
        except Exception:
            self.db_adapter.rollback()
            self.db_adapter.close(cursor)
        else:
            self.db_adapter.commit()
            self.db_adapter.close(cursor)

    def set_db_data(self):
        self.delete_all_treerows()
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.parse_rows(self.db_adapter.get_rows(cursor))
        self.db_adapter.close(cursor)
        self.treeview.yview_moveto(1)

    def delete_all_treerows(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

    def parse_rows(self, rows):
        count = 0

        for row in rows:
            if row[TableHeaders.STATUS_SQL] == StatusValues.BOOL_TRUE:
                row[TableHeaders.STATUS_SQL] = StatusValues.COMPLETE_STRING
            else:
                row[TableHeaders.STATUS_SQL] = StatusValues.NOT_COMPLETE_STRING

            if row[TableHeaders.STATUS_SQL] == StatusValues.NOT_COMPLETE_STRING:
                font_tag = "red_font"
            else:
                font_tag = "normal_font"

            row_tag = "evenrow" if count % 2 == 0 else "oddrow"

            self.treeview.insert(
                parent="",
                index=END,
                iid=count,
                text="",
                values=(
                    row[TableHeaders.ID_SQL],
                    row[TableHeaders.DATE_SQL].strftime(DateTimeValues.TABLE_FORMAT),
                    row[TableHeaders.TYPE_SQL],
                    row[TableHeaders.NAME_SQL],
                    row[TableHeaders.COMMUNICATION_SQL],
                    row[TableHeaders.FROM_SQL],
                    row[TableHeaders.WHO_SQL],
                    row[TableHeaders.DESC_SQL],
                    row[TableHeaders.NOTE_SQL],
                    row[TableHeaders.AUTHOR_SQL],
                    row[TableHeaders.STATUS_SQL],
                ),
                tags=(row_tag, font_tag),
            )
            count += 1

    def select_data(self, e):
        self.parent.dataframe.clear_fields()
        selected = self.treeview.selection()
        if selected:
            values = self.treeview.item(selected[0], "values")
            if values[TableHeaders.STATUS_IDX] == (StatusValues.COMPLETE_STRING):
                select_record_status = True
            else:
                select_record_status = False
            record = Record(
                id_=values[TableHeaders.ID_IDX],
                date=values[TableHeaders.DATE_IDX],
                type_=values[TableHeaders.TYPE_IDX],
                name="\n".join(values[TableHeaders.NAME_IDX].split("; ")),
                communication="\n".join(values[TableHeaders.COMMUNICATION_IDX].split("; ")),
                from_=values[TableHeaders.FROM_IDX],
                who=values[TableHeaders.WHO_IDX],
                description=values[TableHeaders.DESC_IDX],
                note=values[TableHeaders.NOTE_IDX],
                author=values[TableHeaders.AUTHOR_IDX],
                status=select_record_status,
            )

            self.parent.dataframe.insert_data_in_fields(record)

    def update_gui(self):
        self.treeview.delete(*self.treeview.get_children())

        self.set_db_data()

        self.treeview.yview_moveto(1)

        self.parent.dataframe.get_type_values()
        self.parent.dataframe.get_author_values()

        self.parent.menuframe.get_menu_type_values()
        self.parent.menuframe.get_menu_author_values()
        self.parent.menuframe.get_menu_status_values()

    def treeview_sort_column(self, col, reverse):
        if col == TableHeaders.ID:
            link_row = [(int(self.treeview.set(row, col)), row) for row in self.treeview.get_children("")]
        else:
            link_row = [(self.treeview.set(row, col), row) for row in self.treeview.get_children("")]
        sorted_link_row = sorted(link_row, reverse=reverse)

        for index, (_, row) in enumerate(sorted_link_row):
            self.treeview.move(row, "", index)

        self.treeview.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def treeview_reset(self):
        self.delete_all_treerows()
        self.set_db_data()

    def treeview_date_filter(self, e):
        self.delete_all_treerows()
        self.set_db_data()
        rows = []

        string_begin_date = self.parent.menuframe.menu_begin_date_entry.get()
        string_end_date = self.parent.menuframe.menu_end_date_entry.get()

        if string_begin_date > string_end_date:
            messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_SELECTED_DATE_PERIOD)
            raise Exception("")

        global count
        count = 0

        if len(string_begin_date) != 0 and len(string_end_date) != 0:
            pattern = re.compile(DateWindowParams.DATE_REG)
            if not re.fullmatch(pattern, string_begin_date):
                messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_BEGIN_DATE_FORMAT)
                raise Exception("")
            if not re.fullmatch(pattern, string_end_date):
                messagebox.showerror(ErrorsParams.ERROR_WINDOW_NAME, ErrorsParams.ERROR_END_DATE_FORMAT)
                raise Exception("")

            begin_date = datetime.strptime(string_begin_date, DateTimeValues.TABLE_FORMAT)
            end_date = datetime.strptime(string_end_date, DateTimeValues.TABLE_FORMAT)
            for row_index in self.treeview.get_children():
                record_date = datetime.strptime(
                    self.treeview.item(row_index)["values"][TableHeaders.DATE_IDX], DateTimeValues.TABLE_FORMAT
                )
                if record_date >= begin_date and record_date <= end_date:
                    rows.append(self.treeview.item(row_index)["values"])

            self.delete_all_treerows()

            for row in rows:
                if row[TableHeaders.STATUS_IDX] == StatusValues.NOT_COMPLETE_STRING:
                    font_tag = "red_font"
                else:
                    font_tag = "normal_font"

                row_tag = "evenrow" if count % 2 == 0 else "oddrow"

                self.treeview.insert(
                    parent="",
                    index=END,
                    iid=count,
                    text="",
                    values=(
                        row[TableHeaders.ID_IDX],
                        row[TableHeaders.DATE_IDX],
                        row[TableHeaders.TYPE_IDX],
                        row[TableHeaders.NAME_IDX],
                        row[TableHeaders.COMMUNICATION_IDX],
                        row[TableHeaders.FROM_IDX],
                        row[TableHeaders.WHO_IDX],
                        row[TableHeaders.DESC_IDX],
                        row[TableHeaders.NOTE_IDX],
                        row[TableHeaders.AUTHOR_IDX],
                        row[TableHeaders.STATUS_IDX],
                    ),
                    tags=(row_tag, font_tag),
                )
                count += 1

            self.treeview_type_filter()
        else:
            self.treeview_type_filter()

    def treeview_type_filter(self):
        rows = []

        string_type = self.parent.menuframe.menu_type_combobox.get()

        if len(string_type) != 0:
            for row_index in self.treeview.get_children():
                record_type = str(self.treeview.item(row_index)["values"][TableHeaders.TYPE_IDX])
                if record_type == string_type:
                    rows.append(self.treeview.item(row_index)["values"])

            global count

            self.delete_all_treerows()

            for row in rows:
                if row[TableHeaders.STATUS_IDX] == StatusValues.NOT_COMPLETE_STRING:
                    font_tag = "red_font"
                else:
                    font_tag = "normal_font"

                row_tag = "evenrow" if count % 2 == 0 else "oddrow"

                self.treeview.insert(
                    parent="",
                    index=END,
                    iid=count,
                    text="",
                    values=(
                        row[TableHeaders.ID_IDX],
                        row[TableHeaders.DATE_IDX],
                        row[TableHeaders.TYPE_IDX],
                        row[TableHeaders.NAME_IDX],
                        row[TableHeaders.COMMUNICATION_IDX],
                        row[TableHeaders.FROM_IDX],
                        row[TableHeaders.WHO_IDX],
                        row[TableHeaders.DESC_IDX],
                        row[TableHeaders.NOTE_IDX],
                        row[TableHeaders.AUTHOR_IDX],
                        row[TableHeaders.STATUS_IDX],
                    ),
                    tags=(row_tag, font_tag),
                )
                count += 1

            self.treeview_name_filter()
        else:
            self.treeview_name_filter()

    def treeview_name_filter(self):
        rows = []
        string_name = self.parent.menuframe.menu_name_text.get("1.0", "end-1c").strip()
        print(string_name)
        if string_name:
            search_terms = [term.strip() for term in string_name.split("\n") if term.strip()]
            print(search_terms)
            for row_index in self.treeview.get_children():
                record_name = str(self.treeview.item(row_index)["values"][TableHeaders.NAME_IDX])
                if all(term.casefold() in record_name.casefold() for term in search_terms):
                    rows.append(self.treeview.item(row_index)["values"])
            global count
            self.delete_all_treerows()
            for row in rows:
                font_tag = (
                    "red_font" if row[TableHeaders.STATUS_IDX] == StatusValues.NOT_COMPLETE_STRING else "normal_font"
                )
                row_tag = "evenrow" if count % 2 == 0 else "oddrow"
                self.treeview.insert(
                    parent="",
                    index=END,
                    iid=count,
                    text="",
                    values=(
                        row[TableHeaders.ID_IDX],
                        row[TableHeaders.DATE_IDX],
                        row[TableHeaders.TYPE_IDX],
                        row[TableHeaders.NAME_IDX],
                        row[TableHeaders.COMMUNICATION_IDX],
                        row[TableHeaders.FROM_IDX],
                        row[TableHeaders.WHO_IDX],
                        row[TableHeaders.DESC_IDX],
                        row[TableHeaders.NOTE_IDX],
                        row[TableHeaders.AUTHOR_IDX],
                        row[TableHeaders.STATUS_IDX],
                    ),
                    tags=(row_tag, font_tag),
                )
                count += 1
            self.treeview_communication_filter()
        else:
            self.treeview_communication_filter()

    def treeview_communication_filter(self):
        rows = []
        string_communication = self.parent.menuframe.menu_communication_text.get("1.0", "end-1c").strip()
        if string_communication:
            search_terms = [term.strip() for term in string_communication.split("\n") if term.strip()]
            for row_index in self.treeview.get_children():
                record_communication = str(self.treeview.item(row_index)["values"][TableHeaders.COMMUNICATION_IDX])
                if all(term.casefold() in record_communication.casefold() for term in search_terms):
                    rows.append(self.treeview.item(row_index)["values"])
            global count
            self.delete_all_treerows()
            for row in rows:
                font_tag = (
                    "red_font" if row[TableHeaders.STATUS_IDX] == StatusValues.NOT_COMPLETE_STRING else "normal_font"
                )
                row_tag = "evenrow" if count % 2 == 0 else "oddrow"
                self.treeview.insert(
                    parent="",
                    index=END,
                    iid=count,
                    text="",
                    values=(
                        row[TableHeaders.ID_IDX],
                        row[TableHeaders.DATE_IDX],
                        row[TableHeaders.TYPE_IDX],
                        row[TableHeaders.NAME_IDX],
                        row[TableHeaders.COMMUNICATION_IDX],
                        row[TableHeaders.FROM_IDX],
                        row[TableHeaders.WHO_IDX],
                        row[TableHeaders.DESC_IDX],
                        row[TableHeaders.NOTE_IDX],
                        row[TableHeaders.AUTHOR_IDX],
                        row[TableHeaders.STATUS_IDX],
                    ),
                    tags=(row_tag, font_tag),
                )
                count += 1
            self.treeview_author_filter()
        else:
            self.treeview_author_filter()

    def treeview_author_filter(self):
        rows = []

        string_author = self.parent.menuframe.menu_author_combobox.get()

        if len(string_author) != 0:
            for row_index in self.treeview.get_children():
                record_author = str(self.treeview.item(row_index)["values"][TableHeaders.AUTHOR_IDX])
                if record_author == string_author:
                    rows.append(self.treeview.item(row_index)["values"])

            global count

            self.delete_all_treerows()

            for row in rows:
                if row[TableHeaders.STATUS_IDX] == StatusValues.NOT_COMPLETE_STRING:
                    font_tag = "red_font"
                else:
                    font_tag = "normal_font"

                row_tag = "evenrow" if count % 2 == 0 else "oddrow"

                self.treeview.insert(
                    parent="",
                    index=END,
                    iid=count,
                    text="",
                    values=(
                        row[TableHeaders.ID_IDX],
                        row[TableHeaders.DATE_IDX],
                        row[TableHeaders.TYPE_IDX],
                        row[TableHeaders.NAME_IDX],
                        row[TableHeaders.COMMUNICATION_IDX],
                        row[TableHeaders.FROM_IDX],
                        row[TableHeaders.WHO_IDX],
                        row[TableHeaders.DESC_IDX],
                        row[TableHeaders.NOTE_IDX],
                        row[TableHeaders.AUTHOR_IDX],
                        row[TableHeaders.STATUS_IDX],
                    ),
                    tags=(row_tag, font_tag),
                )
                count += 1

            self.treeview_status_filter()
        else:
            self.treeview_status_filter()

    def treeview_status_filter(self):
        rows = []

        string_status = self.parent.menuframe.menu_status_combobox.get()

        if len(string_status) != 0:
            for row_index in self.treeview.get_children():
                record_status = self.treeview.item(row_index)["values"][TableHeaders.STATUS_IDX]
                if record_status == string_status:
                    rows.append(self.treeview.item(row_index)["values"])

            global count

            self.delete_all_treerows()

            for row in rows:
                if row[TableHeaders.STATUS_IDX] == StatusValues.NOT_COMPLETE_STRING:
                    font_tag = "red_font"
                else:
                    font_tag = "normal_font"

                row_tag = "evenrow" if count % 2 == 0 else "oddrow"

                self.treeview.insert(
                    parent="",
                    index=END,
                    iid=count,
                    text="",
                    values=(
                        row[TableHeaders.ID_IDX],
                        row[TableHeaders.DATE_IDX],
                        row[TableHeaders.TYPE_IDX],
                        row[TableHeaders.NAME_IDX],
                        row[TableHeaders.COMMUNICATION_IDX],
                        row[TableHeaders.FROM_IDX],
                        row[TableHeaders.WHO_IDX],
                        row[TableHeaders.DESC_IDX],
                        row[TableHeaders.NOTE_IDX],
                        row[TableHeaders.AUTHOR_IDX],
                        row[TableHeaders.STATUS_IDX],
                    ),
                    tags=(row_tag, font_tag),
                )
                count += 1

    def treeview_search(self, e):
        rows = []

        search_string = self.parent.menuframe.menu_search_entry.get()

        if len(search_string) != 0:
            if self.parent.menuframe.menu_search_status.get() is False:
                for row_index in self.treeview.get_children():
                    record_from = str(self.treeview.item(row_index)["values"][TableHeaders.FROM_IDX])
                    from_matches = re.finditer(search_string.casefold(), record_from.casefold())
                    from_indices = [match.start() for match in from_matches]
                    if len(from_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])

                    record_who = str(self.treeview.item(row_index)["values"][TableHeaders.WHO_IDX])
                    who_matches = re.finditer(search_string.casefold(), record_who.casefold())
                    who_indices = [match.start() for match in who_matches]
                    if len(who_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])

                    record_description = str(self.treeview.item(row_index)["values"][TableHeaders.DESC_IDX])
                    description_matches = re.finditer(search_string.casefold(), record_description.casefold())
                    description_indices = [match.start() for match in description_matches]
                    if len(description_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])

                    record_note = str(self.treeview.item(row_index)["values"][TableHeaders.NOTE_IDX])
                    note_matches = re.finditer(search_string.casefold(), record_note.casefold())
                    note_indices = [match.start() for match in note_matches]
                    if len(note_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])
            else:
                for row_index in self.treeview.get_children():
                    record_from = str(self.treeview.item(row_index)["values"][TableHeaders.FROM_IDX])
                    from_matches = re.finditer(search_string, record_from)
                    from_indices = [match.start() for match in from_matches]
                    if len(from_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])

                    record_who = str(self.treeview.item(row_index)["values"][TableHeaders.WHO_IDX])
                    who_matches = re.finditer(search_string, record_who)
                    who_indices = [match.start() for match in who_matches]
                    if len(who_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])

                    record_description = str(self.treeview.item(row_index)["values"][TableHeaders.DESC_IDX])
                    description_matches = re.finditer(search_string, record_description)
                    description_indices = [match.start() for match in description_matches]
                    if len(description_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])

                    record_note = str(self.treeview.item(row_index)["values"][TableHeaders.NOTE_IDX])
                    note_matches = re.finditer(search_string, record_note)
                    note_indices = [match.start() for match in note_matches]
                    if len(note_indices) != 0:
                        rows.append(self.treeview.item(row_index)["values"])

            count = 0

            self.delete_all_treerows()

            for row in rows:
                if row[TableHeaders.FROM_IDX] is None:
                    row[TableHeaders.FROM_IDX] = EmptyValues.EMPTY_STRING
                if row[TableHeaders.WHO_IDX] is None:
                    row[TableHeaders.WHO_IDX] = EmptyValues.EMPTY_STRING

                if row[TableHeaders.STATUS_IDX] == StatusValues.NOT_COMPLETE_STRING:
                    font_tag = "red_font"
                else:
                    font_tag = "normal_font"

                row_tag = "evenrow" if count % 2 == 0 else "oddrow"

                self.treeview.insert(
                    parent="",
                    index=END,
                    iid=count,
                    text="",
                    values=(
                        row[TableHeaders.ID_IDX],
                        row[TableHeaders.DATE_IDX],
                        row[TableHeaders.TYPE_IDX],
                        row[TableHeaders.NAME_IDX],
                        row[TableHeaders.COMMUNICATION_IDX],
                        row[TableHeaders.FROM_IDX],
                        row[TableHeaders.WHO_IDX],
                        row[TableHeaders.DESC_IDX],
                        row[TableHeaders.NOTE_IDX],
                        row[TableHeaders.AUTHOR_IDX],
                        row[TableHeaders.STATUS_IDX],
                    ),
                    tags=(row_tag, font_tag),
                )
                count += 1
        else:
            self.set_db_data()
