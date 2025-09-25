from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


# 成功响应
class SuccessResponse(BaseModel):
    code: str = "SUCCESS"
    message: str = Field(..., description="成功提示")
    data: Union[Dict, List, Any] = Field(..., description="业务数据")
    # request_id: str = Field(..., description="请求唯一ID")


# 错误响应
class ErrorResponse(BaseModel):
    code: str = Field(..., description="错误码(如PARAM_VALIDATION_ERROR)")
    message: str = Field(..., description="错误提示")
    detail: Optional[Dict] = Field(None, description="详细信息(如错误字段)")
    # request_id: str = Field(..., description="请求唯一ID")
