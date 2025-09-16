import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# 应用配置
class AppSettings(BaseSettings):
    name: str = "FastAPI"
    description: str = "FastAPI Learn"
    version: str = "0.1.0"
    debug: bool = False


# 全局配置
class Settings(BaseSettings):
    app: AppSettings = AppSettings()

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter=".")


@lru_cache()
def get_settings():
    return Settings()
