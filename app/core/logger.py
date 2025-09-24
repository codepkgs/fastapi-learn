import sys

from loguru import logger

from app.core.config import Settings


def init_log_handlers(settings: Settings):
    """初始化日志处理器（控制台 + 文件 + 错误日志单独输出）"""
    # 1. 移除默认处理器
    logger.remove()

    # 2. 创建日志目录
    settings.logger.log_dir.mkdir(parents=True, exist_ok=True)

    # 3. 通用日志格式
    log_format = (
        "{{"
        '"time": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
        '"level": "{level}", '
        '"request_id": "{extra[request_id]}", '
        '"client_ip": "{extra[client_ip]}", '
        '"http_x_forwarded_for": "{extra[http_x_forwarded_for]}", '
        '"request_method": "{extra[request_method]}", '
        '"request_url": "{extra[request_url]}", '
        '"request_path": "{extra[request_path]}", '
        '"request_length": "{extra[request_length]}", '
        '"module": "{module}", '
        '"function": "{function}", '
        '"line": {line}, '
        '"message": "{message}"'
        "}}"
    )

    # 4. 控制台输出
    logger.add(
        sink=sys.stdout,
        format=log_format,
        level=settings.logger.level,
        enqueue=True,  # 异步写入，避免阻塞
        backtrace=True,  # 错误时显示堆栈回溯
    )

    # 5. 应用主日志文件输出
    logger.add(
        sink=str(settings.logger.log_dir / "app.log"),
        format=log_format,
        level=settings.logger.level,
        rotation=f"{settings.logger.rotation} days",
        retention=f"{settings.logger.retention} days",
        compression="gz",
        enqueue=True,
        backtrace=True,
    )

    # 6. 错误日志单独输出（仅 ERROR 及以上级别）
    logger.add(
        sink=str(settings.logger.log_dir / "error.log"),
        format=log_format,
        level="ERROR",  # 只记录 ERROR/CRITICAL
        rotation=f"{settings.logger.rotation} days",
        retention=f"{settings.logger.retention} days",
        compression="gz",
        enqueue=True,
        backtrace=True,
    )
