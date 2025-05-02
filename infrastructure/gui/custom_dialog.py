from tkinter.simpledialog import Dialog

import customtkinter as ctk

from constants.constants import CustomDialogParams, MainWindowParams


class CustomDialog(Dialog):
    """
    Кастомное диалоговое окно. Вызывается при неуспешном подключении к БД.
    Требует ввод ip адрес сервера БД.
    """

    def __init__(self, parent):
        self.db_ip_address = None
        super().__init__(parent)

    def body(self, master):
        self.title(CustomDialogParams.TITLE)
        self.iconbitmap(MainWindowParams.ICON_PATH)
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (325 / 2))
        y_cordinate = int((screen_height / 2) - (125 / 2))
        self.geometry(f"{325}x{125}+{x_cordinate}+{y_cordinate}")
        self.db_ip_address_label = ctk.CTkLabel(master, text=CustomDialogParams.LABLE)
        self.db_ip_address_label.pack(pady=(5, 0), anchor="w")
        self.db_ip_address_entry = ctk.CTkEntry(master)
        self.db_ip_address_entry.pack(pady=(0, 5), fill="x")

    def ok_pressed(self):
        self.db_ip_address = self.db_ip_address_entry.get()
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        self.ok_button = ctk.CTkButton(self, text=CustomDialogParams.BTN_OK, command=self.ok_pressed)
        self.ok_button.pack(padx=10, pady=0, side="left")
        cancel_button = ctk.CTkButton(self, text=CustomDialogParams.BTN_CANCEL, command=self.cancel_pressed)
        cancel_button.pack(padx=10, pady=10, side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())
