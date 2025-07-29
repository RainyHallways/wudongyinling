from typing import Any, Optional, Union, List
from pydantic import BaseModel


class BaseResponse(BaseModel):
    """基础响应模型"""
    code: int = 200
    message: str = "success"
    timestamp: Optional[str] = None
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            from datetime import datetime
            data['timestamp'] = datetime.now().isoformat()
        super().__init__(**data)


class DataResponse(BaseResponse):
    """数据响应模型"""
    data: Any = None
    
    @classmethod
    def success(cls, data: Any = None, message: str = "操作成功"):
        return cls(code=200, message=message, data=data)
    
    @classmethod
    def error(cls, message: str = "操作失败", code: int = 400, data: Any = None):
        return cls(code=code, message=message, data=data)


class PaginatedResponse(BaseResponse):
    """分页响应模型"""
    data: dict
    
    def __init__(self, items: List[Any], total: int, page: int = 1, page_size: int = 10, **kwargs):
        data = {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
        super().__init__(data=data, **kwargs)
    
    @classmethod
    def success(cls, items: List[Any], total: int, page: int = 1, page_size: int = 10, message: str = "获取成功"):
        return cls(items=items, total=total, page=page, page_size=page_size, code=200, message=message)


class ErrorResponse(BaseResponse):
    """错误响应模型"""
    error: Optional[dict] = None
    
    def __init__(self, message: str, code: int = 400, error_detail: Optional[str] = None, **kwargs):
        error_data = None
        if error_detail:
            error_data = {
                "detail": error_detail,
                "type": "validation_error" if code == 422 else "business_error"
            }
        super().__init__(code=code, message=message, error=error_data, **kwargs)
    
    @classmethod
    def validation_error(cls, message: str = "数据验证失败", detail: Optional[str] = None):
        return cls(message=message, code=422, error_detail=detail)
    
    @classmethod
    def not_found(cls, message: str = "资源不存在"):
        return cls(message=message, code=404)
    
    @classmethod
    def unauthorized(cls, message: str = "未授权访问"):
        return cls(message=message, code=401)
    
    @classmethod
    def forbidden(cls, message: str = "禁止访问"):
        return cls(message=message, code=403)
    
    @classmethod
    def internal_error(cls, message: str = "服务器内部错误"):
        return cls(message=message, code=500)


# 便捷响应函数
def success_response(data: Any = None, message: str = "操作成功") -> DataResponse:
    """成功响应"""
    return DataResponse.success(data=data, message=message)


def error_response(message: str = "操作失败", code: int = 400, data: Any = None) -> DataResponse:
    """错误响应"""
    return DataResponse.error(message=message, code=code, data=data)


def paginated_response(
    items: List[Any], 
    total: int, 
    page: int = 1, 
    page_size: int = 10, 
    message: str = "获取成功"
) -> PaginatedResponse:
    """分页响应"""
    return PaginatedResponse.success(
        items=items, 
        total=total, 
        page=page, 
        page_size=page_size, 
        message=message
    ) 