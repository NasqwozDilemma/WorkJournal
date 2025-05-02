import tkinter as tk
from tkinter import END, BooleanVar, StringVar, ttk

import customtkinter as ctk

from constants.constants import DefaultLists, MenuParams, SQLRequests, StatusValues, TableHeaders
from infrastructure.gui.communication_window import CommunicationWindow
from infrastructure.gui.date_window import DateWindow
from infrastructure.gui.object_window import ObjectWindow


class MenuFrame(ctk.CTkFrame):
    """
    Вызываемое меню для фильтрации и поиска записей.
    """

    def __init__(self, parent, db_adapter):
        super().__init__(parent, fg_color="transparent")
        self.pack(padx=(20, 10), fill="x", expand=False)
        self.parent = parent
        self.db_adapter = db_adapter

        self.menu_search_status = BooleanVar()

        self.hidden = True

    def create_elements(self):
        self.menu_button = ctk.CTkButton(self, text="≡", command=self.show_hide_menu)
        self.menu_button.pack(padx=(0, 10), pady=5, side="left")

    def create_menu(self):
        self.toogle_menu = ctk.CTkFrame(self.parent, fg_color="transparent", border_width=1, height=575, width=600)

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.create_menu_elements()

    def show_hide_menu(self):
        if self.hidden is True:
            self.toogle_menu.place(x=20, y=38, bordermode="outside")
            self.menu_button.configure(text="X", command=self.show_hide_menu)
        else:
            self.toogle_menu.place_forget()
            self.menu_button.configure(text="≡", command=self.show_hide_menu)
        self.hidden = not self.hidden

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark":
            self.parent.configure(fg_color="dimgray")
            self.parent.dataframe.configure(fg_color="gray")
            self.parent.commandframe.configure(fg_color="gray")
        else:
            self.parent.configure(fg_color="white")
            self.parent.dataframe.configure(fg_color="whitesmoke")
            self.parent.commandframe.configure(fg_color="whitesmoke")

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def get_menu_type_values(self):
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_TYPES)
        types = cursor.fetchall()
        unique_types = DefaultLists.TYPES_LIST.copy()
        for type_ in types:
            if type_[TableHeaders.TYPE_SQL] not in unique_types:
                unique_types.append(type_[TableHeaders.TYPE_SQL])
        self.db_adapter.close(cursor)
        self.menu_type_combobox.configure(values=sorted(unique_types))

    def get_menu_author_values(self):
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_AUTHORS)
        authors = cursor.fetchall()
        unique_authors = DefaultLists.AUTHOR_LIST.copy()
        for author in authors:
            if author[TableHeaders.AUTHOR_SQL] not in unique_authors:
                unique_authors.append(author[TableHeaders.AUTHOR_SQL])
        self.db_adapter.close(cursor)
        self.menu_author_combobox.configure(values=sorted(unique_authors))

    def get_menu_status_values(self):
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_STATUS)
        statuses = cursor.fetchall()
        unique_stat = DefaultLists.STATUS_LIST.copy()
        for status in statuses:
            if status[TableHeaders.STATUS_SQL] == StatusValues.BOOL_FALSE:
                if StatusValues.COMPLETE_STRING not in unique_stat:
                    unique_stat.append(StatusValues.COMPLETE_STRING)
            else:
                if StatusValues.NOT_COMPLETE_STRING not in unique_stat:
                    unique_stat.append(StatusValues.NOT_COMPLETE_STRING)
        self.db_adapter.close(cursor)
        self.menu_status_combobox.configure(values=sorted(unique_stat))

    def menu_pick_date(self, e, field):
        self.date_window = DateWindow(field)

    def select_object(self, e, field):
        self.object_window = ObjectWindow(self, self.db_adapter, field)

    def select_communication(self, e, field):
        self.communication_window = CommunicationWindow(self, self.db_adapter, field)

    def menu_clear_fields(self):
        self.menu_begin_date_entry.delete(0, END)
        self.menu_end_date_entry.delete(0, END)
        self.menu_type_combobox.set("")
        self.menu_name_text.delete("1.0", END)
        self.menu_communication_text.delete("1.0", END)
        self.menu_author_combobox.set("")
        self.menu_status_combobox.set("")
        self.menu_search_entry.delete(0, END)
        self.menu_search_status.set(False)

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

    def create_menu_elements(self):
        self.menu_begin_date_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_BEGIN_LABEL)
        self.menu_begin_date_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="n")
        self.menu_begin_date_entry = ctk.CTkEntry(self.toogle_menu)
        self.menu_begin_date_entry.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="n")
        self.menu_begin_date_entry.bind(
            "<Button>", lambda e, field=self.menu_begin_date_entry: self.menu_pick_date("<Button>", field)
        )
        self.menu_begin_date_entry.bind("<Return>", self.parent.treeframe.treeview_date_filter)

        self.menu_end_date_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_END_LABEL)
        self.menu_end_date_label.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="n")
        self.menu_end_date_entry = ctk.CTkEntry(self.toogle_menu)
        self.menu_end_date_entry.grid(row=1, column=1, padx=10, pady=(0, 5), sticky="n")
        self.menu_end_date_entry.bind(
            "<Button>", lambda e, field=self.menu_end_date_entry: self.menu_pick_date("<Button>", field)
        )
        self.menu_end_date_entry.bind("<Return>", self.parent.treeframe.treeview_date_filter)

        self.menu_type_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_TYPE_LABEL)
        self.menu_type_label.grid(row=0, column=2, padx=10, pady=(5, 0), sticky="n")
        self.menu_type_variable = StringVar()
        self.menu_type_combobox = ctk.CTkComboBox(self.toogle_menu, variable=self.menu_type_variable)
        self.menu_type_combobox.grid(row=1, column=2, padx=10, pady=(0, 5), sticky="n")
        self.menu_type_combobox.bind("<Return>", self.parent.treeframe.treeview_date_filter)
        self.get_menu_type_values()

        self.menu_name_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_NAME_LABEL)
        self.menu_name_label.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="n")
        self.menu_name_text = ctk.CTkTextbox(
            self.toogle_menu, wrap=tk.WORD, height=95, width=140, border_width=1, border_color="black"
        )
        self.menu_name_text.grid(row=3, column=0, rowspan=5, padx=10, pady=(0, 5), sticky="n")
        self.menu_name_text.bind("<Button-3>", lambda e, field=self.menu_name_text: self.select_object(e, field))
        self.bind_events(self.menu_name_text, self.menu_name_text)

        self.menu_communication_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_COMMUNICATION_LABEL)
        self.menu_communication_label.grid(row=2, column=1, padx=10, pady=(5, 0), sticky="n")
        self.menu_communication_text = ctk.CTkTextbox(
            self.toogle_menu, wrap=tk.WORD, height=95, width=140, border_width=1, border_color="black"
        )
        self.menu_communication_text.grid(row=3, column=1, rowspan=5, padx=10, pady=(0, 5), sticky="n")
        self.menu_communication_text.bind(
            "<Button-3>", lambda e, field=self.menu_communication_text: self.select_communication(e, field)
        )
        self.bind_events(self.menu_communication_text, self.menu_communication_text)

        self.menu_author_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_AUTHOR_LABEL)
        self.menu_author_label.grid(row=2, column=2, padx=10, pady=(5, 0), sticky="n")
        self.menu_author_variable = StringVar()
        self.menu_author_combobox = ctk.CTkComboBox(self.toogle_menu, variable=self.menu_author_variable)
        self.menu_author_combobox.grid(row=3, column=2, padx=10, pady=(0, 5), sticky="n")
        self.menu_author_combobox.bind("<Return>", self.parent.treeframe.treeview_date_filter)
        self.get_menu_author_values()

        self.menu_status_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_STATUS_LABEL)
        self.menu_status_label.grid(row=4, column=2, padx=10, pady=(5, 0), sticky="n")
        self.menu_status_variable = StringVar()
        self.menu_status_combobox = ctk.CTkComboBox(self.toogle_menu, variable=self.menu_status_variable)
        self.menu_status_combobox.grid(row=5, column=2, padx=10, pady=(0, 5), sticky="n")
        self.menu_status_combobox.bind("<Return>", self.parent.treeframe.treeview_date_filter)
        self.get_menu_status_values()

        filter_button = ctk.CTkButton(
            self.toogle_menu,
            text=MenuParams.MENU_FILTER_BUTTON,
            command=lambda: self.parent.treeframe.treeview_date_filter("<Return>"),
        )
        filter_button.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        middle_separator = ttk.Separator(self.toogle_menu)
        middle_separator.grid(row=7, column=0, columnspan=3, padx=(20, 10), pady=10, sticky="ew")

        self.menu_search_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_SEARCH_LABEL)
        self.menu_search_label.grid(row=8, column=0, padx=10, pady=(5, 0), sticky="n")
        self.menu_search_entry = ctk.CTkEntry(self.toogle_menu, width=300)
        self.menu_search_entry.grid(row=9, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="n")
        self.menu_search_entry.bind("<Return>", self.parent.treeframe.treeview_search)
        self.bind_events(self.menu_search_entry, self.menu_search_entry)

        search_button = ctk.CTkButton(
            self.toogle_menu,
            text=MenuParams.MENU_SEARCH_BUTTON,
            command=lambda: self.parent.treeframe.treeview_search("<Return>"),
        )
        search_button.grid(row=9, column=2, padx=10, pady=(0, 5), sticky="nsew")

        self.search_checkbutton_label = ctk.CTkLabel(self.toogle_menu, text=MenuParams.MENU_SEARCH_CHECK_LABEL)
        self.search_checkbutton_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="ns")
        self.search_checkbutton = ctk.CTkCheckBox(
            self.toogle_menu, variable=self.menu_search_status, onvalue=True, offvalue=False, text=""
        )
        self.search_checkbutton.grid(row=10, column=1, padx=10, pady=(10, 0), sticky="ns")

        down_separator = ttk.Separator(self.toogle_menu)
        down_separator.grid(row=11, column=0, columnspan=3, padx=(20, 10), pady=10, sticky="ew")

        clear_window_button = ctk.CTkButton(
            self.toogle_menu, text=MenuParams.MENU_CLEAR_BUTTON, command=lambda: self.menu_clear_fields()
        )
        clear_window_button.grid(row=12, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        reset_button = ctk.CTkButton(
            self.toogle_menu, text=MenuParams.MENU_RESET_BUTTON, command=self.parent.treeframe.treeview_reset
        )
        reset_button.grid(row=13, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.appearance_mode_label = ctk.CTkLabel(self.toogle_menu, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=14, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.toogle_menu, values=["Light", "Dark"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=15, column=0, padx=10, pady=(10, 20))

        self.scaling_label = ctk.CTkLabel(self.toogle_menu, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=14, column=2, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.toogle_menu, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(row=15, column=2, padx=10, pady=(10, 20))
        self.scaling_optionemenu.set("100%")
