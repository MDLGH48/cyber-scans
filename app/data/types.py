from typing import Any, Dict, List
from typing_extensions import Literal
from pydantic import BaseModel, AnyHttpUrl, Field
from enum import Enum
from pydantic.types import UUID4

class Status(Enum):
    Accepted = "Accepted"
    Running = "Running"
    Completed = "Complete"
    Error = "Error"
    Not_found = "Not-Found"

class InjestRequest(BaseModel):
    urls: List[AnyHttpUrl] = Field(..., example=["https://www.google.com"])


class InjestModel(BaseModel):
    scan_ids: List[UUID4]


class ScanStatusResponse(BaseModel):
    status: Literal[tuple([v.value for v in Status.__members__.values()])]