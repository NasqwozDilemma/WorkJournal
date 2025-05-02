import tkinter as tk
from tkinter import END, BooleanVar, StringVar

import customtkinter as ctk

from constants.constants import DataFrameParams, DefaultLists, SQLRequests, TableHeaders
from domain.models import Record
from infrastructure.gui.communication_window import CommunicationWindow
from infrastructure.gui.date_window import DateWindow
from infrastructure.gui.object_window import ObjectWindow


class DataFrame(ctk.CTkFrame):
    """
    Поля для добавления, детального отображения и редактирования записей.
    """

    def __init__(self, parent, db_adapter):
        super().__init__(parent, fg_color="whitesmoke")
        self.pack(padx=20, pady=10, fill="x")
        self.parent = parent
        self.db_adapter = db_adapter

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        self.record_status = BooleanVar()

        self.create_elements()

    def get_type_values(self):
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_TYPES)
        types = cursor.fetchall()
        unique_types = DefaultLists.TYPES_LIST.copy()
        for type_ in types:
            if type_[TableHeaders.TYPE_SQL] not in unique_types:
                unique_types.append(type_[TableHeaders.TYPE_SQL])
        self.db_adapter.close(cursor)
        self.type_combobox.configure(values=sorted(unique_types))

    def get_author_values(self):
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_AUTHORS)
        authors = cursor.fetchall()
        unique_authors = DefaultLists.AUTHOR_LIST.copy()
        for author in authors:
            if author[TableHeaders.AUTHOR_SQL] not in unique_authors:
                unique_authors.append(author[TableHeaders.AUTHOR_SQL])
        self.db_adapter.close(cursor)
        self.author_combobox.configure(values=sorted(unique_authors))

    def copy_text(self, field):
        try:
            # Если у виджета есть метод tag_ranges – считаем, что это CTkTextbox
            if hasattr(field, "tag_ranges"):
                text = field.get("sel.first", "sel.last")
            else:
                text = field.selection_get()
            self.parent.parent.clipboard_clear()
            self.parent.parent.clipboard_append(text)
            self.parent.parent.update()
        except Exception:
            pass

    def paste_text(self, field):
        try:
            text = self.parent.parent.clipboard_get()
            # Если есть выделение, удаляем его, чтобы новый текст заменил старый
            if hasattr(field, "tag_ranges"):
                if field.tag_ranges("sel"):
                    field.delete("sel.first", "sel.last")
            else:
                # Для CTkEntry/CTkComboBox пытаемся получить индексы выделения
                try:
                    start = field.index("sel.first")
                    end = field.index("sel.last")
                    field.delete(start, end)
                except Exception:
                    pass
            field.insert("insert", text)
        except Exception:
            pass

    def cut_text(self, field):
        try:
            self.copy_text(field)
            if hasattr(field, "tag_ranges"):
                field.delete("sel.first", "sel.last")
            else:
                try:
                    start = field.index("sel.first")
                    end = field.index("sel.last")
                    field.delete(start, end)
                except Exception:
                    pass
        except Exception:
            pass

    def undo_text(self, field):
        try:
            field.edit_undo()
        except Exception:
            pass

    def bind_events(self, widget, field):
        widget.bind("<Control-Key>", lambda e: self.on_ctrl_key(e, field))

    def on_ctrl_key(self, event, field):
        if event.keycode == 67:  # Ctrl+C
            self.copy_text(field)
            return "break"
        elif event.keycode == 86:  # Ctrl+V
            self.paste_text(field)
            return "break"
        elif event.keycode == 88:  # Ctrl+X
            self.cut_text(field)
            return "break"
        elif event.keycode == 90:  # Ctrl+Z
            self.undo_text(field)
            return "break"

    def pick_date(self, e, field):
        self.date_window = DateWindow(field)

    def select_object(self, e, field):
        self.object_window = ObjectWindow(self, self.db_adapter, field)

    def select_communication(self, e, field):
        self.communication_window = CommunicationWindow(self, self.db_adapter, field)

    def clear_fields(self):
        self.date_entry.delete(0, END)
        self.type_combobox.set("")
        self.name_text.delete("1.0", END)
        self.communication_text.delete("1.0", END)
        self.from_entry.delete(0, END)
        self.who_entry.delete(0, END)
        self.description_text.delete("1.0", END)
        self.note_text.delete("1.0", END)
        self.author_combobox.set("")
        self.record_status.set(False)

    def unselect_row(self):
        if self.parent.treeframe.treeview.selection():
            self.parent.treeframe.treeview.selection_remove(self.parent.treeframe.treeview.selection())

    def clear_fields_and_unselect_row(self):
        self.unselect_row()
        self.clear_fields()

    def create_elements(self):
        self.date_label = ctk.CTkLabel(self, text=TableHeaders.DATE)
        self.date_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="s")
        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="n")
        self.date_entry.bind("<Button>", lambda e, field=self.date_entry: self.pick_date("<Button>", field))

        self.type_label = ctk.CTkLabel(self, text=TableHeaders.TYPE)
        self.type_label.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="s")
        self.type_variable = StringVar()
        self.type_combobox = ctk.CTkComboBox(self, variable=self.type_variable)
        self.type_combobox.grid(row=1, column=1, padx=10, pady=(0, 5), sticky="n")
        self.get_type_values()

        self.name_label = ctk.CTkLabel(self, text=TableHeaders.NAME)
        self.name_label.grid(row=0, column=2, padx=10, pady=(5, 0), sticky="s")
        self.name_text = ctk.CTkTextbox(self, wrap=tk.WORD, height=180, width=150)
        self.name_text.grid(row=1, column=2, rowspan=5, padx=10, pady=(0, 5), sticky="n")
        self.name_text.bind("<Button-3>", lambda e, field=self.name_text: self.select_object(e, field))
        self.bind_events(self.name_text, self.name_text)

        self.communication_label = ctk.CTkLabel(self, text=TableHeaders.COMMUNICATION)
        self.communication_label.grid(row=0, column=3, padx=10, pady=(5, 0), sticky="s")
        self.communication_text = ctk.CTkTextbox(self, wrap=tk.WORD, height=180, width=150)
        self.communication_text.grid(row=1, column=3, rowspan=5, padx=10, pady=(0, 5), sticky="n")
        self.communication_text.bind(
            "<Button-3>", lambda e, field=self.communication_text: self.select_communication(e, field)
        )
        self.bind_events(self.communication_text, self.communication_text)

        self.description_label = ctk.CTkLabel(self, text=TableHeaders.DESC)
        self.description_label.grid(row=0, column=4, padx=10, pady=(5, 0), sticky="s")
        self.description_text = ctk.CTkTextbox(self, wrap=tk.WORD, height=180, width=500, undo=True)
        self.description_text.grid(row=1, rowspan=5, column=4, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.description_text, self.description_text)

        self.note_label = ctk.CTkLabel(self, text=TableHeaders.NOTE)
        self.note_label.grid(row=0, column=5, padx=10, pady=(5, 0), sticky="s")
        self.note_text = ctk.CTkTextbox(self, wrap=tk.WORD, height=180, width=500, undo=True)
        self.note_text.grid(row=1, rowspan=5, column=5, padx=10, pady=(0, 20), sticky="n")
        self.bind_events(self.note_text, self.note_text)

        self.author_label = ctk.CTkLabel(self, text=TableHeaders.AUTHOR)
        self.author_label.grid(row=0, column=6, padx=10, pady=(5, 0), sticky="s")
        self.author_variable = StringVar()
        self.author_combobox = ctk.CTkComboBox(self, variable=self.author_variable)
        self.author_combobox.grid(row=1, column=6, padx=10, pady=(0, 5), sticky="n")
        self.get_author_values()

        self.from_label = ctk.CTkLabel(self, text=TableHeaders.FROM)
        self.from_label.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="s")
        self.from_entry = ctk.CTkEntry(self)
        self.from_entry.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="n")
        self.bind_events(self.from_entry, self.from_entry)

        self.who_label = ctk.CTkLabel(self, text=TableHeaders.WHO)
        self.who_label.grid(row=2, column=1, padx=10, pady=(5, 0), sticky="s")
        self.who_entry = ctk.CTkEntry(self)
        self.who_entry.grid(row=3, column=1, padx=10, pady=(0, 5), sticky="n")
        self.bind_events(self.who_entry, self.who_entry)

        # self.status_label = ctk.CTkLabel(self, text=TableHeaders.STATUS)
        # self.status_label.grid(row=2, column=5,
        #                        padx=10, pady=(5, 0), sticky='s')
        self.status_checkbutton = ctk.CTkCheckBox(
            self, variable=self.record_status, onvalue=True, offvalue=False, text=TableHeaders.STATUS
        )
        self.status_checkbutton.grid(row=3, column=6, padx=10, pady=(0, 5), sticky="n")

        clear_button = ctk.CTkButton(
            self, text=DataFrameParams.DATA_FRAME_CLEAR_BUTTON_TEXT, command=self.clear_fields_and_unselect_row
        )
        clear_button.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="n")

    def insert_data_in_fields(self, record: Record):
        self.clear_fields()
        self.date_entry.insert(0, record.record_date)
        self.type_combobox.set(record.record_type)
        self.name_text.insert(END, record.record_name)
        self.name_text.insert(END, "\n")
        self.communication_text.insert(END, record.record_communication)
        self.communication_text.insert(END, "\n")
        self.from_entry.insert(0, record.record_from)
        self.who_entry.insert(0, record.record_who)
        self.description_text.insert("1.0", record.record_description)
        self.note_text.insert("1.0", record.record_note)
        self.author_combobox.set(record.record_author)
        self.record_status.set(record.record_status)
