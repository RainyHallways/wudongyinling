from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class HealthRecord(Base):
    """健康记录模型"""
    __tablename__ = "health_records"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    blood_pressure: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 格式: "120/80"
    heart_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    blood_sugar: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 体重(kg)
    height: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 身高(cm)
    bmi: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # BMI指数
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # 备注信息
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    # 关系定义
    user: Mapped["User"] = relationship("User", back_populates="health_records") 