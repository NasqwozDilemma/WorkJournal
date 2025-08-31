import logging
import os
import sys

from icecream import ic

from infrastructure.gui.main_window import App
from scheduler_backup import backup_scheduler


ic.disable()


def main():
    App()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)

    backup_scheduler.start()

    try:
        print(sys.version)
        main()
    except KeyboardInterrupt:
        pass
    finally:
        backup_scheduler.stop()
        os._exit(1)
