from sqlalchemy import Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum

from .base import Base

class RelationType(str, Enum):
    """关系类型枚举"""
    PARENT_CHILD = "parent_child"    # 父母-子女关系
    GUARDIAN = "guardian"            # 监护关系
    CARE_PROVIDER = "care_provider"  # 照护关系

class UserRelation(Base):
    """用户关系模型"""
    __tablename__ = "user_relations"

    elderly_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    child_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    relation_type: Mapped[RelationType] = mapped_column(SQLEnum(RelationType), default=RelationType.PARENT_CHILD)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # 关系定义
    elderly: Mapped["User"] = relationship("User", foreign_keys=[elderly_id], back_populates="children_relations")
    child: Mapped["User"] = relationship("User", foreign_keys=[child_id], back_populates="parent_relations") 