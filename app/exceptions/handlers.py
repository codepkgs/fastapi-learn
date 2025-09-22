from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import BaseAPIException


# 注册API异常处理器
def register_api_exception_handler(app: FastAPI):
    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(request: Request, exc: BaseAPIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "detail": exc.detail,
            },
        )


# 注册所有API异常处理器
def register_all_api_exception_handlers(app: FastAPI):
    register_api_exception_handler(app)
