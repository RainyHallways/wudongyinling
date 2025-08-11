from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ...core.database import get_async_db
from ...schemas.user import UserCreate, UserUpdate, UserPublic, PasswordChange
from ...core.security import get_current_active_user
from ...models.user import User
from ...schemas.base import DataResponse, ListResponse, PaginatedResponse
from ...services.user_service import UserService

router = APIRouter()
@router.get("/me", response_model=DataResponse[UserPublic])
async def get_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前登录用户信息
    """
    return DataResponse(data=current_user)

@router.put("/me", response_model=DataResponse[UserPublic])
async def update_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends()
):
    """
    更新当前登录用户信息
    """
    updated_user = await user_service.update_profile(
        db,
        user_id=current_user.id,
        user_in=user_update
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return DataResponse(data=updated_user)

@router.get("/", response_model=PaginatedResponse[UserPublic])
async def get_users(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    获取用户列表
    """
    users = await user_service.get_multi(db, skip=skip, limit=limit)
    total = await user_service.repository.count(db)
    
    return PaginatedResponse(
        data=users,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.get("/{user_id}", response_model=DataResponse[UserPublic])
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    通过ID获取用户信息
    """
    user = await user_service.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(data=user)

@router.put("/{user_id}", response_model=DataResponse[UserPublic])
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    更新用户信息
    """
    user = await user_service.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    updated_user = await user_service.update_profile(
        db, 
        user_id=user_id, 
        user_in=user_update
    )
    
    return DataResponse(data=updated_user)

@router.delete("/{user_id}", response_model=DataResponse)
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    删除用户
    """
    user = await user_service.delete(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(message="用户已删除")

@router.patch("/{user_id}/activate", response_model=DataResponse[UserPublic])
async def activate_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    激活用户
    """
    user = await user_service.activate_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(data=user, message="用户已激活")

@router.patch("/{user_id}/deactivate", response_model=DataResponse[UserPublic])
async def deactivate_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    停用用户
    """
    user = await user_service.deactivate_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(data=user, message="用户已停用")

@router.post("/", response_model=DataResponse[UserPublic])
async def create_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    创建新用户（管理员操作）
    """
    # 检查用户名是否已存在
    existing_user = await user_service.get_by_username(db, user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    existing_email = await user_service.get_by_email(db, user_create.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    try:
        user = await user_service.create(db, obj_in=user_create)
        return DataResponse(data=user, message="用户创建成功")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"创建用户失败: {str(e)}")

@router.patch("/{user_id}/change-password", response_model=DataResponse)
async def change_user_password(
    user_id: int,
    password_data: PasswordChange,
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    修改用户密码
    """
    try:
        success = await user_service.change_password(
            db, 
            user_id=user_id, 
            password_data=password_data
        )
        if success:
            return DataResponse(message="密码修改成功")
        else:
            raise HTTPException(status_code=400, detail="密码修改失败")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 