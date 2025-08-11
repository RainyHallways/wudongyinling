from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ...core.config import settings
from ...core.database import get_async_db
from ...schemas.user import UserCreate, TokenResponse, UserLogin
from ...schemas.base import DataResponse
from ...core.security import get_current_active_user
from ...models.user import User
from ...services.auth_service import AuthService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

@router.post("/login", response_model=DataResponse[TokenResponse])
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_async_db),
    auth_service: AuthService = Depends()
):
    """
    用户登录
    """
    token_response = await auth_service.login(
        db, 
        username=login_data.username, 
        password=login_data.password
    )
    
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return DataResponse(
        code=0,
        message="登录成功",
        data=token_response
    )

@router.post("/logout", response_model=DataResponse)
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    用户登出（前端删除 token 即可，后端保留接口以保持一致的调用方式）
    """
    return DataResponse(message="登出成功")

@router.post("/register", response_model=DataResponse)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_async_db),
    auth_service: AuthService = Depends()
):
    """
    用户注册
    """
    try:
        user = await auth_service.register(db, user_in=user_in)
        return DataResponse(message="注册成功")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 