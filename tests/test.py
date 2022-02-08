import time
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.process import SLEEP_TIME_SEC
import logging
import json
client = TestClient(app)


def test_single_good_injest():
    request = {
        "urls": [
            "https://www.google.com"
        ]
    }
    response = client.post("/scans", json=request)

    assert response.status_code == 200


def test_multiple_good_injest():
    request = {
        "urls": [
            "https://www.google.com",
            "https://www.example.com",
            "https://www.amazon.com",
        ]
    }
    response = client.post("/scans", json=request)

    assert response.status_code == 200
    assert len(response.json()["scan_ids"]) == len(request["urls"])


def test_scan_id():
    request = {
        "urls": [
            "https://www.google.com",
            "https://www.example.com",
            "https://www.amazon.com",
        ]
    }
    response = client.post("/scans", json=request)
    scan_ids = response.json()["scan_ids"]
    for id_ in scan_ids:
        good_id_response = client.get(f"/scans/{id_}")
        assert good_id_response.status_code == 200
        assert good_id_response.json()["status"] != "Not-Found"

    bad_uuid = None
    while not bad_uuid:
        uuid_gen = uuid4().hex
        if uuid_gen not in scan_ids:
            bad_uuid = uuid_gen
    bad_id_response = client.get(f"/scans/{bad_uuid}")
    assert bad_id_response.status_code == 200
    assert bad_id_response.json()["status"] == "Not-Found"


def test_task_manager(caplog):
    caplog.set_level(logging.INFO, logger="TASK_MONITOR")
    scans_to_submit = {
        "urls": ["https://www.google.com", "http://blahblahblah.io.blah.whatever"]}
    scan_ids = client.post("/scans", json=scans_to_submit).json()["scan_ids"]
    time.sleep(SLEEP_TIME_SEC)
    statuses = [json.loads(record.message)["STATUS"]
                for record in caplog.records]
    assert statuses.count("Accepted") == 2
    assert statuses.count("Running") == 2
    assert statuses.count("Complete") == 1
    assert statuses.count("Error") == 1
