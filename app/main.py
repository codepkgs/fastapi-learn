from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

# settings = get_settings()
from app.core import settings

# from app.core.config import get_settings
from app.core.lifespan import app_lifespan
from app.core.middleware import (
    RequestLoggingMiddleware,
)
from app.exceptions.handlers import register_all_api_exception_handlers

app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    version=settings.app.version,
    debug=settings.app.debug,
    # lifespan=app_lifespan,
)

register_all_api_exception_handlers(app)

# 添加中间件
app.add_middleware(RequestLoggingMiddleware)


class UserLoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(user: UserLoginRequest):
    logger.info(f"User {user.username} is logging in")
    return {
        "username": user.username,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
