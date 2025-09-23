from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.lifespan import app_lifespan
from app.exceptions.handlers import register_all_api_exception_handlers
from app.middlewares.request_id import RequestIDMiddleware

settings = get_settings()


app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    version=settings.app.version,
    debug=settings.app.debug,
    # lifespan=app_lifespan,
)

register_all_api_exception_handlers(app)

if settings.middleware.enable_request_id:
    app.add_middleware(RequestIDMiddleware)


class UserLoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(user: UserLoginRequest):
    return {
        "username": user.username,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
