import os
import sys
from icecream import ic

from infrastructure.gui.main_window import App

ic.disable()


def main():
    App()


if __name__ == "__main__":
    print(sys.version)
    main()
    os._exit(1)
