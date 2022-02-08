from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks
from pydantic.types import UUID4
from data.db import scan_manager
from core.process import scan_url
from data.types import InjestModel, InjestRequest, ScanStatusResponse

router = APIRouter()


@router.post("", response_model=InjestModel)
def injest(input_data: InjestRequest, background_tasks: BackgroundTasks):

    # using fastapi/starlette's background task manager... would use celery/redis
    # https://www.starlette.io/background/
    [background_tasks.add_task(scan_url, task=url, task_id=uuid4().hex)
     for url in input_data.urls]
    # accessing task ids from within background task (tasks) attribute to make sure submitted instead of generating ids outside
    return {"scan_ids": [t.kwargs.get("task_id") for t in background_tasks.tasks]}

@router.get("/{scan_id}", response_model=ScanStatusResponse)
def get_status(scan_id: UUID4): # using pydantic UUID4 to validate - if req is not uuid4 will receieve 422 out of the box
    return {"status": scan_manager.find_task_status(task_id=scan_id)}
