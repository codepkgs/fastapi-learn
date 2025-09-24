import uuid

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


# 请求日志中间件 - 包含请求ID
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    @staticmethod
    def get_client_ip(request: Request) -> str:
        """
        1. 从 X-Forwarded-For 或 X-Real-IP 头获取真实 IP
        2. 非代理场景，直接获取客户端 IP
        """
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            # XFF中的第一个IP是客户端的真实IP
            return x_forwarded_for.split(",")[0].strip()

        # 从 X-Real-IP 头获取真实 IP
        x_real_ip = request.headers.get("X-Real-IP")
        if x_real_ip:
            return x_real_ip

        # 非代理场景，直接获取客户端 IP
        client = request.client
        return client.host if client else "-"

    @staticmethod
    def get_http_x_forwarded_for(request: Request) -> str:
        """
        从 X-Forwarded-For 头获取真实 IP
        """
        return request.headers.get("X-Forwarded-For", "-")

    @staticmethod
    def get_request_length(request: Request) -> int:
        """
        获取请求长度
        """
        content_length_str = request.headers.get("Content-Length", "0")
        try:
            request_length = int(content_length_str)
        except ValueError:
            request_length = 0
        return request_length

    # 记录请求日志
    async def dispatch(self, request: Request, call_next):
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # 获取客户端IP
        client_ip = self.get_client_ip(request)

        # 获取X-Forwarded-For
        http_x_forwarded_for = self.get_http_x_forwarded_for(request)

        # 获取请求长度
        request_length = self.get_request_length(request)

        # 初始化上下文 - 每个请求默认携带的字段
        context = {
            "request_id": request_id,
            "client_ip": client_ip,
            "http_x_forwarded_for": http_x_forwarded_for,
            "request_method": request.method,
            "request_path": str(request.url.path),
            "request_url": str(request.url),
            "request_length": request_length,
        }

        with logger.contextualize(**context):
            # 处理请求
            try:
                response = await call_next(request)
            except Exception as e:
                # 记录未捕获异常
                logger.error(f"请求处理异常: {str(e)}", exc_info=True)
                raise  # 交给全局异常处理器处理

            # 响应头返回 RequestID（便于客户端关联）
            response.headers["X-Request-ID"] = request_id
            return response
