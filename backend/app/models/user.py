from typing import List, Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 关系定义 - 这些将在其他模型定义后添加
    health_records: Mapped[List["HealthRecord"]] = relationship("HealthRecord", back_populates="user")
    prescriptions: Mapped[List["Prescription"]] = relationship("Prescription", back_populates="user")
    challenge_records: Mapped[List["ChallengeRecord"]] = relationship("ChallengeRecord", back_populates="user")
    sent_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", foreign_keys="ChatMessage.sender_id", back_populates="sender")
    received_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", foreign_keys="ChatMessage.receiver_id", back_populates="receiver")
    challenges: Mapped[List["Challenge"]] = relationship("Challenge", secondary="challenge_participants", back_populates="participants") 