from data.db import create_conn, db_in_mem, log_status
import requests
import time
    
@log_status
def scan_url(task):
    time.sleep(40.0)
    return str(requests.get(task).content)

    
 

