from datetime import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """所有数据库模型的基类"""
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """自动生成表名为类名的小写"""
        return cls.__name__.lower()
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """将模型实例转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
