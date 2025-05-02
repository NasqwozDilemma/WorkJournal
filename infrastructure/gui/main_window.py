from threading import Thread
from tkinter import ttk

import customtkinter as ctk

from constants.constants import MainWindowParams
from infrastructure.gui.main_frame import MainFrame
from interface_adapters.db_adapter.db_adapter import DBAdapter
from interface_adapters.gui_adapter.gui_adapter import GUIAdapter
from use_cases.reservation import reservation


class WindowSettings:
    """
    Передача настроек главного окна в конструктор окна.
    """

    min_width_window = MainWindowParams.MIN_WIDTH
    min_height_window = MainWindowParams.MIN_HEIGHT
    window_icon = MainWindowParams.ICON_PATH
    can_resize_width = True
    can_resize_height = True


class WindowFactory:
    """
    Конструктор окна.
    """

    @staticmethod
    def create_window(window_settings, window_name):
        window = ctk.CTk()
        window.title(window_name)

        if window_settings.min_width_window is not None and window_settings.min_height_window is not None:
            window.minsize(window_settings.min_width_window, window_settings.min_height_window)
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (window_settings.min_width_window / 2))
            y_cordinate = int((screen_height / 2) - (window_settings.min_height_window / 2))
            window.geometry(
                f"{window_settings.min_width_window}x{window_settings.min_height_window}+{x_cordinate}+{y_cordinate}"
            )

        if window_settings.window_icon is not None:
            window.iconbitmap(window_settings.window_icon)

        window.resizable(window_settings.can_resize_width, window_settings.can_resize_height)
        return window

    @staticmethod
    def destroy(window):
        window.destroy()


class App:
    """
    Главное окно.
    """

    def __init__(self):
        window_settings = WindowSettings()
        app = WindowFactory.create_window(window_settings, MainWindowParams.MAIN_WINDOW_NAME)

        ctk.set_appearance_mode("Light")
        # Modes: 'System' (standard), 'Dark', 'Light'
        ctk.set_default_color_theme("dark-blue")
        # Themes: 'blue' (standard), 'green', 'dark-blue'

        bg_color = app._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = app._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        # selected_color = app._apply_appearance_mode(
        #     ctk.ThemeManager.theme['CTkButton']['fg_color'])

        ttk.Style().configure("Treeview", rowheight=30)
        ttk.Style().configure(
            "Treeview",
            background=bg_color,
            foreground=text_color,
            fieldbackground=bg_color,
            borderwidth=0,
        )
        # ttk.Style().map(
        #     'Treeview', background=[('selected', bg_color)],
        #     foreground=[('selected', selected_color)])

        self.gui_adapter = GUIAdapter(self)
        self.db_adapter = DBAdapter(app)
        self.frame = MainFrame(app, self.gui_adapter, self.db_adapter)

        reserv = Thread(target=reservation)
        reserv.start()
        app.mainloop()
