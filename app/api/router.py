
from fastapi import APIRouter

from api.routes import scans

api_router = APIRouter()

api_router.include_router(scans.router, prefix="/scans", tags=["scans"])