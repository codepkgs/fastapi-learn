from fastapi import Request
import uuid


async def request_id_middleware(request: Request, call_next):
    # 生成请求ID
    request_id = str(uuid.uuid4())

    # 存储到request.state供后续使用
    request.state.request_id = request_id

    # 调用下一个中间件
    response = await call_next(request)

    # 将请求ID添加到响应头
    response.headers["X-Request-ID"] = request_id

    return response
