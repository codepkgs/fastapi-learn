from fastapi import FastAPI

from app.api.auth import router_auth
from app.core import get_settings
from app.core.lifespan import app_lifespan
from app.core.middleware import RequestLoggingMiddleware
from app.exceptions.handlers import register_all_api_exception_handlers

# 获取配置
settings = get_settings()

# 创建FastAPI实例
app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    version=settings.app.version,
    debug=settings.app.debug,
    # lifespan=app_lifespan,
)

# 注册异常处理
register_all_api_exception_handlers(app)

# 注册中间件
app.add_middleware(RequestLoggingMiddleware)

# 注册路由
app.include_router(router_auth)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
