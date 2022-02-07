from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.router import api_router
from core.config import settings
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    uvicorn.run("main:app", port=settings.API_PORT, reload=settings.APP_RELOAD)
