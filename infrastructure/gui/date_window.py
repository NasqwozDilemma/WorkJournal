from datetime import datetime
from tkinter import CENTER, END, StringVar, ttk
from tkinter.font import Font

import customtkinter as ctk
from tkcalendar import Calendar

from constants.constants import DateWindowParams, MainWindowParams


class DateWindow(ctk.CTkToplevel):
    """
    Окно для указания даты и времени.
    """

    def __init__(self, field):
        super().__init__()

        self.title(DateWindowParams.DATE_WINDOW_TEXT)
        self.after(250, lambda: self.iconbitmap(MainWindowParams.ICON_PATH))
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close_date_window)
        self.grab_set()

        field_x = field.winfo_rootx()
        field_y = field.winfo_rooty()
        field_width = field.winfo_width()
        field_height = field.winfo_height()

        x = field_x + field_width
        y = field_y - field_height

        self.geometry(f"{DateWindowParams.MIN_WIDTH}x{DateWindowParams.MIN_HEIGHT}+{x}+{y}")

        self.string_var_hours = StringVar(self)
        self.string_var_hours.set(f"{datetime.now().hour:0>2}")
        self.string_var_minutes = StringVar(self)
        self.string_var_minutes.set(f"{datetime.now().minute:0>2}")

        self.calc = Calendar(self, selectmode="day", date_pattern="y.mm.dd")
        self.calc.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        values_hours = [DateWindowParams.ZERO_VALUE_HOUR]

        for i in range(DateWindowParams.MIN_VALUE_HOUR, DateWindowParams.MAX_VALUE_HOUR):
            if len(str(i)) == 1:
                values_hours.append(f"0{str(i)}")
            else:
                values_hours.append(str(i))
            i += 1

        values_hours = tuple(values_hours)

        hour_label = ctk.CTkLabel(self, text=DateWindowParams.DATE_HOUR_LABEL)
        hour_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="n")
        self.hour_spinbox = ttk.Spinbox(
            self,
            values=values_hours,
            justify=CENTER,
            width=15,
            wrap=True,
            textvariable=self.string_var_hours,
            font=Font(size=11),
        )
        self.hour_spinbox.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="n")

        values_minutes = [DateWindowParams.ZERO_VALUE_MINUTE]

        for i in range(DateWindowParams.MIN_VALUE_MINUTE, DateWindowParams.MAX_VALUE_MINUTE):
            if len(str(i)) == 1:
                values_minutes.append(f"0{str(i)}")
            else:
                values_minutes.append(str(i))
            i += 1

        values_minutes = tuple(values_minutes)

        minute_label = ctk.CTkLabel(self, text=DateWindowParams.DATE_MINUTE_LABEL)
        minute_label.grid(row=1, column=1, padx=10, pady=(5, 0), sticky="n")
        self.minute_spinbox = ttk.Spinbox(
            self,
            values=values_minutes,
            justify=CENTER,
            width=15,
            wrap=True,
            textvariable=self.string_var_minutes,
            font=Font(size=11),
        )
        self.minute_spinbox.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="n")

        submit_button = ttk.Button(
            self, text=DateWindowParams.DATE_SUBMIT_BUTTON, command=lambda: self.menu_grab_date(field)
        )
        submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        cancel_button = ttk.Button(
            self, text=DateWindowParams.DATE_CANCEL_BUTTON, command=lambda: self.menu_delete_date(field)
        )
        cancel_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    def menu_grab_date(self, field):
        field.delete(0, END)
        field.insert(0, f"{self.calc.get_date()} {self.hour_spinbox.get()}:{self.minute_spinbox.get()}:00")
        self.close_date_window()

    def menu_delete_date(self, field):
        field.delete(0, END)
        self.close_date_window()

    def close_date_window(self):
        self.destroy()
