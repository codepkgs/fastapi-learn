from functools import lru_cache

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
    enable_request_id: bool = True


# 全局配置
class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    middleware: MiddlewareSettings = MiddlewareSettings()

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter=".")


@lru_cache()
def get_settings():
    return Settings()
