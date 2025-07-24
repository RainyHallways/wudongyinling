from typing import Generic, TypeVar, Type, List, Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.base import RepositoryBase, ModelType, CreateSchemaType, UpdateSchemaType

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    服务层基类，提供基本的业务逻辑操作
    """
    
    def __init__(self, repository: RepositoryBase):
        """
        初始化服务
        
        Args:
            repository: 数据访问层对象
        """
        self.repository = repository
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        通过ID获取单个对象
        
        Args:
            db: 数据库会话
            id: 对象ID
            
        Returns:
            找到的对象，如未找到返回None
        """
        return await self.repository.get(db, id)
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """
        获取多个对象
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            filters: 过滤条件
            order_by: 排序字段
            order_desc: 是否降序排序
            
        Returns:
            对象列表
        """
        return await self.repository.get_multi(
            db, 
            skip=skip, 
            limit=limit, 
            filters=filters, 
            order_by=order_by, 
            order_desc=order_desc
        )
    
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建对象
        
        Args:
            db: 数据库会话
            obj_in: 创建数据
            
        Returns:
            创建的对象
        """
        return await self.repository.create(db, obj_in=obj_in)
    
    async def update(
        self, 
        db: AsyncSession, 
        *, 
        db_obj: ModelType, 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新对象
        
        Args:
            db: 数据库会话
            db_obj: 数据库对象
            obj_in: 更新数据
            
        Returns:
            更新后的对象
        """
        return await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)
    
    async def delete(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """
        删除对象
        
        Args:
            db: 数据库会话
            id: 对象ID
            
        Returns:
            删除的对象，如未找到返回None
        """
        return await self.repository.delete(db, id=id)
    
    async def exists(self, db: AsyncSession, id: int) -> bool:
        """
        判断指定ID的对象是否存在
        
        Args:
            db: 数据库会话
            id: 对象ID
            
        Returns:
            对象是否存在
        """
        return await self.repository.exists(db, id) 