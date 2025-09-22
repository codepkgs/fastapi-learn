from typing import Dict, Optional

from fastapi import status


class BaseAPIException(Exception):
    """API异常基类"""

    def __init__(
        self,
        code: str,
        message: str,
        detail: Optional[Dict] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.code = code  # 错误标识（如"USER_NOT_FOUND"）
        self.message = message  # 用户友好提示
        self.detail = detail  # 详细错误信息（可选）
        self.status_code = status_code  # HTTP状态码
        super().__init__(self.message)


# 400错误请求
class BadRequestError(BaseAPIException):
    """400错误请求"""

    def __init__(
        self,
        code: str = "BAD_REQUEST",  # 默认错误码
        message: str = "请求参数或业务逻辑错误",
        detail: Optional[Dict] = None,
    ):
        # 固定status_code为400
        super().__init__(code=code, message=message, detail=detail, status_code=400)
