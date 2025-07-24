from typing import Generic, TypeVar, Type, List, Optional, Dict, Any, Union
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from pydantic import BaseModel

from ..models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    通用Repository基类，提供通用的CRUD操作
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        初始化Repository
        
        Args:
            model: SQLAlchemy模型类
        """
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        通过ID获取单个对象
        
        Args:
            db: 数据库会话
            id: 对象ID
        
        Returns:
            找到的对象，如未找到返回None
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()
    
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
            filters: 过滤条件字典
            order_by: 排序字段
            order_desc: 是否降序排序
        
        Returns:
            对象列表
        """
        query = select(self.model)
        
        # 应用过滤条件
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        # 应用排序
        if order_by and hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            query = query.order_by(order_field.desc() if order_desc else order_field)
        
        # 应用分页
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建新对象
        
        Args:
            db: 数据库会话
            obj_in: 输入数据
        
        Returns:
            创建的对象
        """
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
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
            db_obj: 要更新的数据库对象
            obj_in: 更新数据
        
        Returns:
            更新后的对象
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def bulk_update(
        self, 
        db: AsyncSession, 
        *, 
        ids: List[int], 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> int:
        """
        批量更新对象
        
        Args:
            db: 数据库会话
            ids: 要更新的对象ID列表
            obj_in: 更新数据
        
        Returns:
            更新的记录数
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        stmt = (
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(**update_data)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount
    
    async def delete(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """
        删除对象
        
        Args:
            db: 数据库会话
            id: 对象ID
        
        Returns:
            删除的对象，如未找到返回None
        """
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
    
    async def bulk_delete(self, db: AsyncSession, *, ids: List[int]) -> int:
        """
        批量删除对象
        
        Args:
            db: 数据库会话
            ids: 对象ID列表
        
        Returns:
            删除的记录数
        """
        stmt = delete(self.model).where(self.model.id.in_(ids))
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount
    
    async def count(self, db: AsyncSession, *, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        计算符合条件的记录数
        
        Args:
            db: 数据库会话
            filters: 过滤条件
        
        Returns:
            记录数
        """
        query = select(func.count()).select_from(self.model)
        
        # 应用过滤条件
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        result = await db.execute(query)
        return result.scalar_one()
    
    async def exists(self, db: AsyncSession, id: int) -> bool:
        """
        判断指定ID的对象是否存在
        
        Args:
            db: 数据库会话
            id: 对象ID
        
        Returns:
            对象是否存在
        """
        query = select(func.count()).select_from(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one() > 0
    
    def build_query(
        self, 
        filters: Optional[Dict[str, Any]] = None, 
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> Select:
        """
        构建查询
        
        Args:
            filters: 过滤条件
            order_by: 排序字段
            order_desc: 是否降序排序
        
        Returns:
            查询对象
        """
        query = select(self.model)
        
        # 应用过滤条件
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        # 应用排序
        if order_by and hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            query = query.order_by(order_field.desc() if order_desc else order_field)
            
        return query 