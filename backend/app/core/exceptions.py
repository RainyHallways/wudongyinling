from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Union
from .response import ErrorResponse

logger = logging.getLogger(__name__)


class BusinessException(Exception):
    """业务异常"""
    def __init__(self, message: str, code: int = 400, detail: str = None):
        self.message = message
        self.code = code
        self.detail = detail
        super().__init__(message)


class ValidationException(BusinessException):
    """验证异常"""
    def __init__(self, message: str = "数据验证失败", detail: str = None):
        super().__init__(message, code=422, detail=detail)


class NotFoundException(BusinessException):
    """资源不存在异常"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, code=404)


class UnauthorizedException(BusinessException):
    """未授权异常"""
    def __init__(self, message: str = "未授权访问"):
        super().__init__(message, code=401)


class ForbiddenException(BusinessException):
    """禁止访问异常"""
    def __init__(self, message: str = "禁止访问"):
        super().__init__(message, code=403)


# 异常处理器
async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    """业务异常处理器"""
    logger.warning(f"Business exception: {exc.message} - {exc.detail}")
    
    error_response = ErrorResponse(
        message=exc.message,
        code=exc.code,
        error_detail=exc.detail
    )
    
    return JSONResponse(
        status_code=exc.code,
        content=error_response.dict()
    )


async def http_exception_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]) -> JSONResponse:
    """HTTP异常处理器"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    # 根据状态码返回不同的错误响应
    if exc.status_code == 401:
        error_response = ErrorResponse.unauthorized(str(exc.detail))
    elif exc.status_code == 403:
        error_response = ErrorResponse.forbidden(str(exc.detail))
    elif exc.status_code == 404:
        error_response = ErrorResponse.not_found(str(exc.detail))
    elif exc.status_code == 422:
        error_response = ErrorResponse.validation_error(str(exc.detail))
    else:
        error_response = ErrorResponse(
            message=str(exc.detail),
            code=exc.status_code
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """请求验证异常处理器"""
    logger.warning(f"Validation exception: {exc.errors()}")
    
    # 提取验证错误信息
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_details.append(f"{field}: {message}")
    
    error_response = ErrorResponse.validation_error(
        message="请求参数验证失败",
        detail="; ".join(error_details)
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response.dict()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    logger.error(f"Unexpected exception: {type(exc).__name__}: {str(exc)}")
    
    error_response = ErrorResponse.internal_error("服务器内部错误")
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


# 注册异常处理器的函数
def register_exception_handlers(app):
    """注册所有异常处理器"""
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler) 