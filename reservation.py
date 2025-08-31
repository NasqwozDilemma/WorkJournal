from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import shutil

from constants.constants import DBParams, Reservation


def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _backups_path() -> Path:
    dir_path = _base_dir() / Reservation.BACKUPS_DIRNAME
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def _last_friday(ref: dt.datetime) -> dt.datetime:
    target = ref.replace(hour=Reservation.SAVE_HOUR, minute=0, second=0, microsecond=0)
    days_back = (target.weekday() - Reservation.FRIDAY) % Reservation.ONE_WEEK
    return target - dt.timedelta(days=days_back or 7) if target > ref else target - dt.timedelta(days=days_back)


def backup_once() -> tuple[bool, str]:
    backups_dir = _backups_path()
    now = dt.datetime.now()
    last_fr = _last_friday(now)
    stamp_last = last_fr.strftime("_%d_%m_%Y")
    stamp_now = now.strftime("_%d_%m_%Y")

    base = Reservation.DUMP_BASENAME.rsplit(".", 1)[0]
    dump_path = backups_dir / Reservation.DUMP_BASENAME
    zip_last = backups_dir / f"{base}{stamp_last}.zip"
    zip_now = backups_dir / f"{base}{stamp_now}.zip"

    zip_target = zip_last if not zip_last.exists() else zip_now

    mysqldump = shutil.which("mysqldump")
    if not mysqldump:
        return False, "mysqldump не найден в PATH"

    cmd = [
        str(mysqldump),
        f"--host={DBParams.HOST}",
        f"--port={DBParams.PORT}",
        f"--user={DBParams.USER}",
        "--databases",
        DBParams.DB_NAME,
        "--single-transaction",
        "--routines",
        "--events",
        "--default-character-set=utf8mb4",
        "--protocol=tcp",
    ]

    env = os.environ.copy()
    env["MYSQL_PWD"] = DBParams.PASSWORD

    try:
        with open(dump_path, "wb") as f:
            proc = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, env=env, check=False)
        if proc.returncode != 0:
            err = proc.stderr.decode(errors="ignore")
            return False, f"mysqldump exited {proc.returncode}: {err.strip() or 'no stderr'}"

        with ZipFile(zip_target, "w", compression=ZIP_DEFLATED, compresslevel=3) as zf:
            zf.write(dump_path, arcname=Reservation.DUMP_BASENAME)
    finally:
        if dump_path.exists():
            try:
                dump_path.unlink()
            except OSError:
                pass

    cutoff = dt.datetime.now().timestamp() - Reservation.RETENTION_DAYS * 86400
    for p in backups_dir.glob("*.zip"):
        try:
            if p.stat().st_ctime < cutoff:
                p.unlink()
        except OSError:
            pass

    return True, f"Бэкап создан: {zip_target}"
