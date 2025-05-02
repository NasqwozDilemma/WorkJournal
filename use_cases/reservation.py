import os
import subprocess
import time
from datetime import datetime, timedelta
from zipfile import ZIP_DEFLATED, ZipFile

from constants.constants import DBParams, Reservation


def reservation():
    """
    Резрвирование БД с указанием даты. Через sql запрос делается экспорт
    БД в файл, файл архивируется с приписыванием даты резервирования
    к наименованию архива и удаляется, так как уже есть архив
    в директории бэкапов. Также архивы старше года автоматически
    удаляются. Резервирование происходит:
        1) каждую пятницу в 17:00, когда таймер == 0;
        2) при запуске программы, если отсутствует резервная копия
            от прошлый пятницы.
    """  # noqa: RUF002

    now = time.time()
    year = datetime.now().year
    month = datetime.now().month
    temp_date = datetime.now()
    while temp_date.weekday() != Reservation.FRIDAY:
        temp_date += timedelta(days=Reservation.ONE_DAY)
    day = temp_date.day
    hour = Reservation.SAVE_HOURS
    save_time = datetime(year, month, day, hour)
    str_save_time = save_time.strftime("_%d_%m_%Y")
    delta = timedelta(days=Reservation.ONE_WEEK)

    filename = Reservation.DB_BACKUP_FILE.split(".")[0:-1][0]
    extension = Reservation.DB_BACKUP_FILE.split(".")[-1]
    past_date = (save_time - delta).strftime("_%d_%m_%Y")

    zip_file = f"./db_backups/{filename}{past_date}.zip"
    zip_file_is_exist = os.path.isfile(zip_file)
    if not zip_file_is_exist:
        if not os.path.exists(Reservation.BACKUPS_PATH):
            os.makedirs(Reservation.BACKUPS_PATH)
        backup_command = (
            f"mysqldump -u{DBParams.USER} -h{DBParams.HOST} "
            f"-p{DBParams.PASSWORD} {DBParams.DB_NAME} > "
            f"{Reservation.DB_BACKUP_FILE}"
        )
        subprocess.run(backup_command, shell=True)
        with ZipFile(
            f"./db_backups/{filename}{past_date}.zip", "w", compression=ZIP_DEFLATED, compresslevel=3
        ) as db_zip:
            db_zip.write(f"./{filename}.{extension}")
        os.remove(Reservation.DB_BACKUP_FILE)

    for file in os.listdir(Reservation.BACKUPS_PATH):
        if file.split(".")[-1] == "zip":
            file = os.path.join(Reservation.BACKUPS_PATH, file)
            if os.stat(file).st_ctime < now - 365 * 86400:
                if os.path.isfile(file):
                    os.remove(file)

    while True:
        difference = save_time - datetime.now()
        if difference.seconds == 0:
            if not os.path.exists(Reservation.BACKUPS_PATH):
                os.makedirs(Reservation.BACKUPS_PATH)
            backup_command = (
                f"mysqldump -u{DBParams.USER} -h{DBParams.HOST} "
                f"-p{DBParams.PASSWORD} {DBParams.DB_NAME} > "
                f"{Reservation.DB_BACKUP_FILE}"
            )
            subprocess.run(backup_command, shell=True)
            with ZipFile(
                f"./db_backups/{filename}{str_save_time}.zip", "w", compression=ZIP_DEFLATED, compresslevel=3
            ) as db_zip:
                db_zip.write(f"./{filename}.{extension}")
            os.remove(Reservation.DB_BACKUP_FILE)
            save_time += delta
        time.sleep(1)
