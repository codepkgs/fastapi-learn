from functools import lru_cache

from redis import ConnectionPool, Redis

from app.core.config import get_settings


@lru_cache
def get_redis_pool() -> ConnectionPool:
    """获取 Redis 连接池（缓存单例）"""
    settings = get_settings()
    return ConnectionPool(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
        db=settings.redis.db,
        max_connections=settings.redis.max_connections,
        decode_responses=True,
        encoding="utf-8",
    )


@lru_cache
def get_redis_client() -> Redis:
    """获取 Redis 客户端（缓存单例）"""
    return Redis(connection_pool=get_redis_pool())


def close_redis_pool() -> None:
    """关闭 Redis 连接池并清理缓存"""
    pool = get_redis_pool()
    # 断开底层连接
    pool.disconnect()
    # 清除缓存的单例，确保下次可重新初始化
    get_redis_client.cache_clear()
    get_redis_pool.cache_clear()
