from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


# 应用配置
class AppSettings(BaseSettings):
    name: str = "FastAPI"
    description: str = "FastAPI Learn"
    version: str = "0.1.0"
    debug: bool = False


# Redis配置
class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    db: int = 0
    max_connections: int = 30


# 中间件配置
class MiddlewareSettings(BaseSettings):
    enable_request_logging: bool = False


# 日志配置
class LoggerSettings(BaseSettings):
    # 日志等级
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    # 日志文件存储路径
    log_dir: Path = Path("logs")
    # 日志轮转策略
    rotation: int = 1  # 日志轮转周期 1天
    retention: int = 30  # 日志保留周期 30天


# 全局配置
class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    middleware: MiddlewareSettings = MiddlewareSettings()
    logger: LoggerSettings = LoggerSettings()
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter=".")


@lru_cache()
def get_settings():
    return Settings()
