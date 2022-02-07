from data.db import create_conn, db_in_mem, scan_manager
import requests
import time
    
@scan_manager.log_status
def scan_url(task):
    time.sleep(40.0)
    return str(requests.get(task).content)
 

