from datetime import datetime
from typing import Dict, Any, Optional, List

from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Prescription(Base):
    """康复处方模型"""
    __tablename__ = "prescriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    disease_type: Mapped[str] = mapped_column(String(50), nullable=False)
    training_plan: Mapped[str] = mapped_column(Text, nullable=False)
    schedule: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)  # 存储每周训练计划
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    doctor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # 关系定义
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="prescriptions")
    doctor: Mapped[Optional["User"]] = relationship("User", foreign_keys=[doctor_id])
    exercises: Mapped[List["PrescriptionExercise"]] = relationship("PrescriptionExercise", back_populates="prescription")

class PrescriptionExercise(Base):
    """处方中的具体训练项目"""
    __tablename__ = "prescription_exercises"
    
    prescription_id: Mapped[int] = mapped_column(ForeignKey("prescriptions.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)  # 以分钟为单位
    frequency: Mapped[str] = mapped_column(String(50), nullable=False)  # 如"每天一次"
    sets: Mapped[Optional[int]] = mapped_column(nullable=True)
    reps: Mapped[Optional[int]] = mapped_column(nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # 关系定义
    prescription: Mapped["Prescription"] = relationship("Prescription", back_populates="exercises") 