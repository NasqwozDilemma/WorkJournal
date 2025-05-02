import customtkinter as ctk

from infrastructure.gui.command_frame import CommandFrame
from infrastructure.gui.data_frame import DataFrame
from infrastructure.gui.menu_frame import MenuFrame
from infrastructure.gui.tree_frame import TreeFrame
from interface_adapters.db_adapter.db_adapter import DBAdapter
from interface_adapters.gui_adapter.gui_adapter import GUIAdapter
from use_cases.record_management import DataManager


class MainFrame(ctk.CTkFrame):
    """
    Основной фрейм.
    """

    def __init__(self, parent, gui_adapter: GUIAdapter, db_adapter: DBAdapter):
        super().__init__(parent, fg_color="white")
        self.pack(fill="both", expand=True)
        self.parent = parent
        self.gui_adapter = gui_adapter
        self.db_adapter = db_adapter

        self.menuframe = MenuFrame(self, self.db_adapter)
        self.treeframe = TreeFrame(self, self.db_adapter)
        self.dataframe = DataFrame(self, self.db_adapter)
        self.data_manager = DataManager(self, self.gui_adapter, self.db_adapter)
        self.commandframe = CommandFrame(self, self.data_manager)
        self.menuframe.create_elements()
        self.menuframe.create_menu()
