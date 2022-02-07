import datetime
from typing import Callable
from core.config import settings
import sqlite3
from uuid import uuid4
from pydantic.types import UUID4
from enum import Enum

db_in_mem = {}


def create_conn():  # not implemented
    conn = sqlite3.connect(f'app/data/{settings.DB_NAME}.db')
    return conn


class Status(Enum):
    accepted = "Accepted"
    running = "Running"
    completed = "Complete"
    error = "Error"
    not_found = "Not-Found"

class ScanManager:
    def __init__(self, db={}):
        self.db = db

    def log_status(self, scan_func: Callable):
        current_time = datetime.datetime.now()
        def exec_scan(task, task_id):
            self.db[task_id] = dict(
                status=Status.accepted.value,
                data=task,
                submit_time=current_time,
                details="init"
            )

            try:
                self.db[task_id].update(
                    status=Status.running.value,
                    data=task,
                    details="preprocess"
                )
                processed_task = scan_func(task)

                self.db[task_id].update(
                    status=Status.completed.value,
                    data=processed_task,
                    details="postprocess"
                )

            except Exception as e:
                self.db[task_id].update(
                    status=Status.error.value,
                    data=task,
                    details=str(e)
                )

            return task_id

        return exec_scan


    def find_task_status(self, task_id: uuid4):
        try:
            return self.db[task_id.hex]["status"]
        except KeyError:
            return Status.not_found.value

scan_manager = ScanManager()