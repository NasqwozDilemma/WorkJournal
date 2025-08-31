from __future__ import annotations

import datetime as dt
import logging
import threading

from constants.constants import Reservation
from reservation import _backups_path, _last_friday, backup_once


log = logging.getLogger("backup")
log.setLevel(logging.INFO)


class BackupScheduler:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None
        self._stopped = threading.Event()

    def start(self) -> None:
        """Старт планировщика. Делает catch-up за прошлую пятницу (если нужно) и ставит таймер на следующую."""
        with self._lock:
            if self._stopped.is_set():
                self._stopped.clear()
            self._catch_up_last_friday()
            self._schedule_next()

    def stop(self) -> None:
        """Остановка планировщика."""
        with self._lock:
            self._stopped.set()
            if self._timer:
                try:
                    self._timer.cancel()
                finally:
                    self._timer = None

    def _catch_up_last_friday(self) -> None:
        now = dt.datetime.now()
        last_fr = _last_friday(now)
        stamp = last_fr.strftime("_%d_%m_%Y")
        base = Reservation.DUMP_BASENAME.rsplit(".", 1)[0]
        zip_path = (_backups_path()) / f"{base}{stamp}.zip"
        if not zip_path.exists():
            ok, msg = backup_once()
            log.info("Catch-up backup: %s (%s)", "OK" if ok else "FAIL", msg)

    def _next_friday_17(self, ref: dt.datetime) -> dt.datetime:
        target = ref.replace(hour=Reservation.SAVE_HOUR, minute=0, second=0, microsecond=0)
        days_fwd = (Reservation.FRIDAY - target.weekday()) % Reservation.ONE_WEEK
        if days_fwd == 0 and target <= ref:
            days_fwd = Reservation.ONE_WEEK
        return target + dt.timedelta(days=days_fwd)

    def _schedule_next(self) -> None:
        if self._stopped.is_set():
            return
        now = dt.datetime.now()
        nxt = self._next_friday_17(now)
        delay = max(1.0, (nxt - now).total_seconds())
        log.info("Next DB backup at %s (in %.0f s)", nxt.strftime("%Y-%m-%d %H:%M:%S"), delay)

        def _run_and_reschedule():
            try:
                ok, msg = backup_once()
                log.info("Scheduled backup: %s (%s)", "OK" if ok else "FAIL", msg)
            finally:
                with self._lock:
                    if not self._stopped.is_set():
                        self._schedule_next()

        self._timer = threading.Timer(delay, _run_and_reschedule)
        self._timer.daemon = True
        self._timer.start()


backup_scheduler = BackupScheduler()
