from datetime import datetime
from typing import Optional, List
from pydantic import EmailStr, Field, validator

from .base import BaseSchema

class UserBase(BaseSchema):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="电子邮箱")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")

class UserCreate(UserBase):
    """创建用户的请求模型"""
    password: str = Field(..., min_length=8, description="密码")
    
    @validator('password')
    def password_complexity(cls, v):
        """验证密码复杂度"""
        if len(v) < 8:
            raise ValueError('密码长度至少为8位')
        # 可以添加更多密码复杂度验证逻辑
        return v

class UserUpdate(BaseSchema):
    """更新用户的请求模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="电子邮箱")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    password: Optional[str] = Field(None, min_length=8, description="密码")
    is_active: Optional[bool] = Field(None, description="是否激活")

class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: int = Field(..., description="用户ID")
    hashed_password: str = Field(..., description="哈希密码")
    is_active: bool = Field(True, description="是否激活")
    is_admin: bool = Field(False, description="是否管理员")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class UserPublic(UserBase):
    """返回给客户端的用户模型"""
    id: int = Field(..., description="用户ID")
    is_active: bool = Field(..., description="是否激活")
    is_admin: bool = Field(..., description="是否管理员")
    created_at: datetime = Field(..., description="创建时间")

class UserLogin(BaseSchema):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class TokenResponse(BaseSchema):
    """登录响应模型"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    user: UserPublic = Field(..., description="用户信息") 