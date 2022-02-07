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


def log_status(scan_func: Callable):

    current_time = datetime.datetime.now()

    def exec_scan(task, task_id):
        db_in_mem[task_id] = dict(
            status=Status.accepted.value,
            data=task,
            submit_time=current_time,
            details="init"
        )

        try:
            db_in_mem[task_id].update(
                status=Status.running.value,
                data=task,
                details="preprocess"
            )
            processed_task = scan_func(task)

            db_in_mem[task_id].update(
                status=Status.completed.value,
                data=processed_task,
                details="postprocess"
            )

        except Exception as e:
            db_in_mem[task_id].update(
                status=Status.error.value,
                data=task,
                details=str(e)
            )

        return task_id

    return exec_scan


def find_task_status(task_id: uuid4):
    try:
        return db_in_mem[task_id.hex]["status"]
    except KeyError:
        return Status.not_found.value
