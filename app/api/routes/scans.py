from typing import Any, Dict, List
from typing_extensions import Literal
from uuid import uuid4
from fastapi import Depends, APIRouter, Request, Path, BackgroundTasks
from pydantic.types import UUID4
from pydantic import BaseModel, AnyHttpUrl
from data.db import Status, find_task_status
from core.process import scan_url


class InjestRequest(BaseModel):
    urls: List[AnyHttpUrl]


class InjestModel(BaseModel):
    scan_ids: List[UUID4]


class ScanStatusResponse(BaseModel):
    status: Literal[tuple([v.value for v in Status.__members__.values()])]


router = APIRouter()


@router.post("", response_model=InjestModel)
def injest(input_data: InjestRequest, background_tasks: BackgroundTasks):
    [background_tasks.add_task(scan_url, task=url, task_id=uuid4().hex)
     for url in input_data.urls]

    return {"scan_ids": [t.kwargs.get("task_id") for t in background_tasks.tasks]}


@router.get("/{scan_id}", response_model=ScanStatusResponse)
def get_status(scan_id: UUID4):
    return {"status": find_task_status(task_id=scan_id)}
