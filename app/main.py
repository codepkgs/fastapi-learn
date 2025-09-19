from typing import Any, Optional

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, EmailStr, Field

from app.core.config import get_settings
from app.core.lifespan import app_lifespan

settings = get_settings()


app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    version=settings.app.version,
    debug=settings.app.debug,
    lifespan=app_lifespan,
)


class User(BaseModel):
    username: str
    password: str = Field(
        ..., min_length=8, max_length=16, description="密码长度为8-16位"
    )
    address: Optional[str] = "北京"
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    username: str
    address: str
    email: Optional[EmailStr] = None


class RespModel(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None


@app.post("/user", response_model=RespModel, response_model_include={"code", "message"})
async def create_user(user: User):
    return RespModel(code=200, message="success", data=UserOut(**user.model_dump()))


def sync_task():
    import time

    time.sleep(10)
    print("sync_task done")


@app.post("/sync", response_model=RespModel)
async def sync(tasks: BackgroundTasks):
    tasks.add_task(sync_task)
    return RespModel(code=200, message="数据同步中,请稍后刷新", data=None)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
