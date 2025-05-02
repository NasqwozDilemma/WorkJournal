from tkinter import CENTER, END, ttk

import customtkinter as ctk

from constants.constants import CommunicationWindowParams, DefaultLists, MainWindowParams, SQLRequests, TableHeaders


class CommunicationWindow(ctk.CTkToplevel):
    """
    Окно выбора оборудования.
    """

    def __init__(self, parent, db_adapter, field):
        super().__init__(parent)
        self.title("Выбор объекта")
        self.after(250, lambda: self.iconbitmap(MainWindowParams.ICON_PATH))
        x_cordinate = int(field.winfo_rootx())
        y_cordinate = int(field.winfo_rooty())
        self.geometry(
            f"{CommunicationWindowParams.WINDOW_WIDTH}"
            f"x{CommunicationWindowParams.WINDOW_HEIGHT}"
            f"+{x_cordinate + 150}+{y_cordinate - 100}"
        )
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close_communication_window)
        self.grab_set()

        self.parent = parent
        self.db_adapter = db_adapter
        self.field = field

        self.create_communication_treeview()
        self.create_elements()
        self.initialization_set_communication_db_data()

    def close_communication_window(self):
        self.destroy()

    def select_communication(self, e):
        self.selected = self.communication_treeview.selection()

    def create_communication_treeview(self):
        cols = (TableHeaders.COMMUNICATION,)
        self.communication_treeview = ttk.Treeview(self, show="", columns=cols)
        self.communication_treeview.pack(fill="both", expand=True)

        self.communication_treeview.column(
            TableHeaders.COMMUNICATION, width=150, minwidth=150, stretch=True, anchor=CENTER
        )

        for col in cols:
            self.communication_treeview.heading(col, text=col, anchor=CENTER)

        self.communication_treeview.tag_configure("oddrow", background="white")
        self.communication_treeview.tag_configure("evenrow", background="whitesmoke")

        treeScroll = ctk.CTkScrollbar(self.communication_treeview)
        treeScroll.pack(side="right", fill="y")
        treeScroll.configure(command=self.communication_treeview.yview)
        self.communication_treeview.configure(yscrollcommand=treeScroll.set)

        self.communication_treeview.bind("<<TreeviewSelect>>", lambda e: self.select_communication(e))

    def clear_field(self, field):
        field.delete("1.0", END)

    def get_selected_communication(self, field):
        try:
            if self.selected:
                self.clear_field(field)
                for index in self.selected:
                    values = self.communication_treeview.item(index, "values")
                    if values:
                        field.insert(END, values[0])
                    field.insert(END, "\n")
        except AttributeError:
            pass
        finally:
            self.close_communication_window()

    def create_elements(self):
        clear_button = ctk.CTkButton(
            self, text=CommunicationWindowParams.CLEAR_BUTTON, command=lambda field=self.field: self.clear_field(field)
        )
        clear_button.pack(padx=5, pady=(20, 5), fill="x")

        submit_button = ctk.CTkButton(
            self,
            text=CommunicationWindowParams.SUBMIT_BUTTON,
            command=lambda field=self.field: self.get_selected_communication(field),
        )
        submit_button.pack(padx=5, pady=(5, 10), side="left", fill="x")

        cancel_button = ctk.CTkButton(
            self, text=CommunicationWindowParams.CANCEL_BUTTON, command=lambda: self.close_communication_window()
        )
        cancel_button.pack(padx=5, pady=(5, 10), side="right", fill="x")

    def delete_all_communication_treerows(self):
        for row in self.communication_treeview.get_children():
            self.communication_treeview.delete(row)

    def parse_rows(self, communications):
        count = 0

        for communication in communications:
            row_tag = "evenrow" if count % 2 == 0 else "oddrow"
            self.communication_treeview.insert(
                parent="", index=END, iid=count, text="", values=(communication,), tags=(row_tag,)
            )
            count += 1

    def initialization_set_communication_db_data(self):
        self.delete_all_communication_treerows()
        conn = self.db_adapter.connect()
        cursor = conn.cursor()
        self.db_adapter.execute(cursor, SQLRequests.SQL_GET_COMMUNICATIONS)
        communications = cursor.fetchall()
        unique_communications = DefaultLists.COMMUNICATION_LIST.copy()
        for communication in communications:
            if communication[TableHeaders.COMMUNICATION_SQL]:
                temp_communications = communication[TableHeaders.COMMUNICATION_SQL].split("; ")
                for temp_communication in temp_communications:
                    if temp_communication not in unique_communications:
                        unique_communications.append(temp_communication)
        self.db_adapter.close(cursor)
        result_communications = sorted(unique_communications)
        self.parse_rows(result_communications)
