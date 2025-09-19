from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from app.db.redis import close_redis_pool, get_redis_client


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    """Redis 资源的独立 lifespan。"""
    app.state.redis = get_redis_client()

    # 启动时执行连通性检查
    try:
        app.state.redis.ping()
    except Exception:
        close_redis_pool()
        raise

    try:
        yield
    finally:
        close_redis_pool()


# 在这里集中登记需要启用的 lifespans，后续新增只需 append 到列表
LIFESPANS = [
    redis_lifespan,
]


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """组合多个 lifespan 的总入口"""
    async with AsyncExitStack() as stack:
        for lf in LIFESPANS:
            await stack.enter_async_context(lf(app))

        yield
    # 到这里，以上资源会按逆序自动清理
