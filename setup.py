import os
import sys

from cx_Freeze import Executable, setup

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "config")
if not os.path.exists("db_backups"):
    os.makedirs("db_backups")
DB_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "db_backups")

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="WorkJournal.exe",
        icon="./config/work-journal.ico",
        copyright="Copyright (C) 2024 Dmitriy Pavlov",
    )
]

options = {
    "build_exe": {
        "packages": [
            "tkinter",
            "customtkinter",
            "re",
            "shutil",
            "datetime",
            "pymysql",
            "tkcalendar",
            "os",
            "threading",
            "configparser",
        ],
        "include_files": [CONFIG_DIRECTORY, DB_DIRECTORY],
        "excludes": [
            "logging",
            "unittest",
            "html",
            "http",
            "xml",
            "bz2",
            "concurrent",
            "distutils",
            "pydoc_data",
            "test",
            "wheel",
        ],
        "build_exe": "./build/WorkJournal",
        "include_msvcr": True,
        "zip_include_packages": ".",
    }
}

setup(
    name="WorkJournal",
    version="2025.05.02",
    description="WorkJournal",
    author="Dmitriy Pavlov",
    executables=executables,
    options=options,
)

# python setup.py build - create app
# python setup.py bdist_msi - create installer
