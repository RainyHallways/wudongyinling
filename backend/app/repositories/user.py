from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import RepositoryBase
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

class UserRepository(RepositoryBase[User, UserCreate, UserUpdate]):
    """
    用户数据访问层
    """
    
    def __init__(self):
        super().__init__(User)
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        通过电子邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 电子邮箱
            
        Returns:
            用户对象，如未找到返回None
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        通过用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            用户对象，如未找到返回None
        """
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()
    
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
        query = select(User).where(User.is_active == True).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
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
        query = select(User).where(User.is_admin == True).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def authenticate(
        self, 
        db: AsyncSession, 
        *, 
        username: str, 
        password: str
    ) -> Optional[User]:
        """
        验证用户
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            验证成功返回用户对象，否则返回None
        """
        user = await self.get_by_username(db, username)
        if not user:
            return None
        
        if not user.verify_password(password):
            return None
            
        return user
    
    async def is_active(self, user: User) -> bool:
        """
        判断用户是否活跃
        
        Args:
            user: 用户对象
            
        Returns:
            用户是否活跃
        """
        return user.is_active
    
    async def is_admin(self, user: User) -> bool:
        """
        判断用户是否是管理员
        
        Args:
            user: 用户对象
            
        Returns:
            用户是否是管理员
        """
        return user.is_admin 