from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Job Tracker 2026"
    debug: bool = False
    db_conn_str: str


@lru_cache
def get_settings():
    return Settings()
