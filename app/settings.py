from os import environ
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    API: str = "https://api.binance.com"

    ROOT_FOLDER: Path = Path(".")
    CACHE_DIR: str = ROOT_FOLDER / "cache_dir"

    API_KEY: str = Field(repr=False)
    SECRET_KEY: str = Field(repr=False)


settings = Settings(**environ)
