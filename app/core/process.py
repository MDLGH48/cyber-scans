from data.db import scan_manager
import requests
import time

SLEEP_TIME_SEC = 10.0
@scan_manager.log_status
def scan_url(task):
    time.sleep(SLEEP_TIME_SEC)
    return requests.get(task).headers