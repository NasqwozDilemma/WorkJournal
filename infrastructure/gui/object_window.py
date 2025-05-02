from tkinter import CENTER, END, ttk

import customtkinter as ctk

from constants.constants import DefaultLists, MainWindowParams, ObjectWindowParams, SQLRequests, TableHeaders


class ObjectWindow(ctk.CTkToplevel):
    """
    Окно выбора объекта.
    """

    def __init__(self, parent, db_adapter, field):
        super().__init__(parent)
        self.title("Выбор объекта")
        self.after(250, lambda: self.iconbitmap(MainWindowParams.ICON_PATH))
        x_cordinate = int(field.winfo_rootx())
        y_cordinate = int(field.winfo_rooty())
        self.geometry(
            f"{ObjectWindowParams.WINDOW_WIDTH}"
            f"x{ObjectWindowParams.WINDOW_HEIGHT}"
            f"+{x_cordinate + 150}+{y_cordinate - 100}"
        )
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close_object_window)
        self.grab_set()

        self.parent = parent
        self.db_adapter = db_adapter
        self.field = field

        self.create_object_treeview()
        self.create_elements()
        self.initialization_set_object_db_data()

    def close_object_window(self):
        self.destroy()

    def select_object(self, e):
        self.selected = self.object_treeview.selection()

    def create_object_treeview(self):
        cols = (TableHeaders.NAME,)
        self.object_treeview = ttk.Treeview(self, show="", columns=cols)
        self.object_treeview.pack(fill="both", expand=True)

        self.object_treeview.column(TableHeaders.NAME, width=150, minwidth=150, stretch=True, anchor=CENTER)

        for col in cols:
            self.object_treeview.heading(col, text=col, anchor=CENTER)

        self.object_treeview.tag_configure("oddrow", background="white")
        self.object_treeview.tag_configure("evenrow", background="whitesmoke")

        treeScroll = ctk.CTkScrollbar(self.object_treeview)
        treeScroll.pack(side="right", fill="y")
        treeScroll.configure(command=self.object_treeview.yview)
        self.object_treeview.configure(yscrollcommand=treeScroll.set)

        self.object_treeview.bind("<<TreeviewSelect>>", lambda e: self.select_object(e))

    def clear_field(self, field):
        field.delete("1.0", END)

    def get_selected_object(self, field):
        try:
            if self.selected:
                self.clear_field(field)
                for index in self.selected:
                    values = self.object_treeview.item(index, "values")
                    if values:
                        field.insert(END, values[0])
                    field.insert(END, "\n")
        except AttributeError:
            pass
        finally:
            self.close_object_window()

    def create_elements(self):
        clear_button = ctk.CTkButton(
            self, text=ObjectWindowParams.CLEAR_BUTTON, command=lambda field=self.field: self.clear_field(field)
        )
        clear_button.pack(padx=5, pady=(20, 5), fill="x")

        submit_button = ctk.CTkButton(
            self,
            text=ObjectWindowParams.SUBMIT_BUTTON,
            command=lambda field=self.field: self.get_selected_object(field),
        )
        submit_button.pack(padx=5, pady=(5, 10), side="left", fill="x")

        cancel_button = ctk.CTkButton(
            self, text=ObjectWindowParams.CANCEL_BUTTON, command=lambda: self.close_object_window()
        )
        cancel_button.pack(padx=5, pady=(5, 10), side="right", fill="x")

    def delete_all_object_treerows(self):
        for row in self.object_treeview.get_children():
            self.object_treeview.delete(row)

    def parse_rows(self, names):
        count = 0

        for name in names:
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            self.object_treeview.insert(parent="", index=END, iid=count, text="", values=(name,), tags=(row_tag,))
            count += 1

    def initialization_set_object_db_data(self):
        self.delete_all_object_treerows()
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_NAMES)
        names = cursor.fetchall()
        unique_names = DefaultLists.NAME_LIST.copy()
        for name in names:
            if name[TableHeaders.NAME_SQL]:
                temp_names = name[TableHeaders.NAME_SQL].split("; ")
                for temp_name in temp_names:
                    if temp_name not in unique_names:
                        unique_names.append(temp_name)
        self.db_adapter.close(cursor)
        result_names = sorted(unique_names)
        self.parse_rows(result_names)
