from typing import Callable
from core.config import settings
import sqlite3
from uuid import uuid4
from .types import Status
from cachetools import cached, TTLCache
from datetime import datetime, timedelta
from core.config import settings
import logging
import json


class TaskLogFilter(logging.Filter):
    def filter(self, record):
        return "STEP_ID" and "TASK_ID" in record.getMessage()


db_task_monitor = logging.getLogger("TASK_MONITOR")
db_task_monitor.addFilter(TaskLogFilter())


def create_conn():  # not implemented
    conn = sqlite3.connect(f'app/data/{settings.DB_NAME}.db')
    return conn


def update_task_state(task_id: str, task_state: dict, db: TTLCache):
    db.__setitem__(task_id, task_state)
    step_data = {"STEP_ID": uuid4().hex, "TASK_ID": task_id,
                 "STATUS": task_state['status']}
    db_task_monitor.info(json.dumps(step_data))


class ScanManager:
    def __init__(self, db: TTLCache = TTLCache(maxsize=1024, ttl=timedelta(minutes=21), timer=datetime.now)):
        self.db = db

    def log_status(self, scan_func: Callable):
        def exec_scan(task, task_id):
            task_state = dict(
                status=Status.Accepted.value,
                data=task,
                details="init"
            )
            update_task_state(task_id, task_state, self.db)

            try:
                task_state["status"] = Status.Running.value
                task_state["details"] = "pre_process"
                update_task_state(task_id, task_state, self.db)

                processed_task = scan_func(task)

                task_state["status"] = Status.Completed.value
                task_state["details"] = "post_process"
                task_state["data"] = processed_task
                update_task_state(task_id, task_state, self.db)

            except Exception as e:
                task_state["status"] = Status.Error.value
                task_state["details"] = str(e)
                task_state["data"] = task
                update_task_state(task_id, task_state, self.db)

            return task_id

        return exec_scan

    def find_task_status(self, task_id: uuid4):
        try:
            return self.db.__getitem__(task_id.hex)["status"]
        except KeyError:
            return Status.Not_found.value


scan_manager = ScanManager()
