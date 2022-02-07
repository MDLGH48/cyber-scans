from pydantic import BaseSettings, validator
from typing_extensions import Literal
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    PROJECT_NAME: str = "cyber-scans"
    API_PREFIX: str = ""
    API_PORT: Optional[int] = 8001
    RUN_ENV: Literal["dev", "deploy"] = "dev"
    APP_RELOAD: Optional[bool]
    DB_NAME:str = "scans"

    @validator("APP_RELOAD", pre=True)
    def get_app_reload(cls, v, values: Dict[str, Any]) -> bool:
        if v:
            return v
        else:
            run_env = values.get("RUN_ENV")
            return True if run_env == "dev" else False


settings = Settings(_env_file=".env")