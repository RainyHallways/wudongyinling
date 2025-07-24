from typing import List, Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession

from .base_service import BaseService
from ..models.user import User
from ..repositories import user_repository
from ..schemas.user import UserCreate, UserUpdate

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """
    用户服务，处理用户管理相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化用户服务
        """
        super().__init__(user_repository)
    
    async def get_by_email(
        self, 
        db: AsyncSession, 
        email: str
    ) -> Optional[User]:
        """
        通过电子邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 电子邮箱
            
        Returns:
            用户对象，如未找到返回None
        """
        return await self.repository.get_by_email(db, email)
    
    async def get_by_username(
        self, 
        db: AsyncSession, 
        username: str
    ) -> Optional[User]:
        """
        通过用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            用户对象，如未找到返回None
        """
        return await self.repository.get_by_username(db, username)
    
    async def get_active_users(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        获取活跃用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            活跃用户列表
        """
        return await self.repository.get_active_users(db, skip, limit)
    
    async def get_admin_users(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        获取管理员用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            管理员用户列表
        """
        return await self.repository.get_admin_users(db, skip, limit)
    
    async def update_profile(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        user_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Optional[User]:
        """
        更新用户资料
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            user_in: 更新数据
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        return await self.repository.update(db, db_obj=user, obj_in=user_in)
    
    async def activate_user(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int
    ) -> Optional[User]:
        """
        激活用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        update_data = {"is_active": True}
        return await self.repository.update(db, db_obj=user, obj_in=update_data)
    
    async def deactivate_user(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int
    ) -> Optional[User]:
        """
        停用用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        update_data = {"is_active": False}
        return await self.repository.update(db, db_obj=user, obj_in=update_data)
    
    async def set_admin_status(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        is_admin: bool
    ) -> Optional[User]:
        """
        设置用户管理员状态
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            is_admin: 是否为管理员
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        update_data = {"is_admin": is_admin}
        return await self.repository.update(db, db_obj=user, obj_in=update_data)
    
    async def is_active(
        self, 
        db: AsyncSession, 
        *, 
        user: User
    ) -> bool:
        """
        检查用户是否活跃
        
        Args:
            db: 数据库会话
            user: 用户对象
            
        Returns:
            用户是否活跃
        """
        return await self.repository.is_active(user)
    
    async def is_admin(
        self, 
        db: AsyncSession, 
        *, 
        user: User
    ) -> bool:
        """
        检查用户是否是管理员
        
        Args:
            db: 数据库会话
            user: 用户对象
            
        Returns:
            用户是否是管理员
        """
        return await self.repository.is_admin(user) 