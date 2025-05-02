import customtkinter as ctk

from constants.constants import CommandFrameParams


class CommandFrame(ctk.CTkFrame):
    """
    Кнопки добавления, редактирования и удаления записи(-ей).
    """

    def __init__(self, parent, data_manager):
        super().__init__(parent, fg_color="whitesmoke")

        self.pack(padx=20, pady=10, fill="x")
        self.parent = parent
        self.data_manager = data_manager

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.create_elements()

    def create_elements(self):
        insert_button = ctk.CTkButton(
            self, text=CommandFrameParams.COMMAND_INSERT_BUTTON, command=lambda: self.data_manager.insert_data()
        )
        insert_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        update_button = ctk.CTkButton(
            self, text=CommandFrameParams.COMMAND_UPDATE_BUTTON, command=lambda: self.data_manager.update_data()
        )
        update_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        delete_button = ctk.CTkButton(
            self, text=CommandFrameParams.COMMAND_DELETE_BUTTON, command=lambda: self.data_manager.delete_data()
        )
        delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
