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


class TaskLogFilter(logging.Filter): # filter for task monitor
    def filter(self, record):
        return "STEP_ID" and "TASK_ID" in record.getMessage()


db_task_monitor = logging.getLogger("TASK_MONITOR") # used heavily in tests to make sure task management working properly and task state is updated
db_task_monitor.addFilter(TaskLogFilter()) 


def create_conn():  # not implemented
    conn = sqlite3.connect(f'app/data/{settings.DB_NAME}.db')
    return conn


def update_task_state(task_id: str, task_state: dict, db: TTLCache):
    db.__setitem__(task_id, task_state)
    step_data = {"STEP_ID": uuid4().hex, "TASK_ID": task_id,
                 "STATUS": task_state['status']}
    db_task_monitor.info(json.dumps(step_data)) 
    # need to create immutable snapshot of task state at each step (to monitor) -- since task state is mutable in cache


class ScanManager:
    def __init__(
        self,
        db: TTLCache = TTLCache(maxsize=1024, ttl=timedelta(minutes=21), timer=datetime.now) 
        # https://cachetools.readthedocs.io/en/stable/#cachetools.TTLCache
        ):
        self.db = db

    def log_status(self, scan_func: Callable):
        def exec_scan(task, task_id):
            # initial task state
            task_state = dict(
                status=Status.Accepted.value,
                data=task,
                details="init"
            )
            # insert task state
            update_task_state(task_id, task_state, self.db)

            try:
                # running task state
                task_state["status"] = Status.Running.value
                task_state["details"] = "pre_process"
                # update task state
                update_task_state(task_id, task_state, self.db)
                # call the scan function (the decorated function)
                processed_task = scan_func(task)

                # completed task state
                task_state["status"] = Status.Completed.value
                task_state["details"] = "post_process"
                task_state["data"] = processed_task
                # update the task state
                update_task_state(task_id, task_state, self.db)

            except Exception as e:
                # failed task state
                task_state["status"] = Status.Error.value
                task_state["details"] = str(e)
                task_state["data"] = task
                # update task state
                update_task_state(task_id, task_state, self.db)

            return task_id

        return exec_scan

    def find_task_status(self, task_id: uuid4):
        try:
            # get the task state
            return self.db.__getitem__(task_id.hex)["status"]
        except KeyError:
            return Status.Not_found.value


scan_manager = ScanManager()
