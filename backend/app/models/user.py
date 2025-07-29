from typing import List, Optional
from enum import Enum

from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class UserRole(str, Enum):
    """用户角色枚举"""
    ELDERLY = "elderly"     # 老年人
    CHILD = "child"         # 子女
    VOLUNTEER = "volunteer" # 志愿者
    TEACHER = "teacher"     # 教师
    DOCTOR = "doctor"       # 医生
    ADMIN = "admin"         # 管理员

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)  # 保持向后兼容
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.ELDERLY, server_default='ELDERLY')
    unique_id: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    
    # 关系定义 - 这些将在其他模型定义后添加
    health_records: Mapped[List["HealthRecord"]] = relationship("HealthRecord", back_populates="user")
    prescriptions: Mapped[List["Prescription"]] = relationship("Prescription", foreign_keys="Prescription.user_id", back_populates="user")
    doctor_prescriptions: Mapped[List["Prescription"]] = relationship("Prescription", foreign_keys="Prescription.doctor_id", back_populates="doctor")
    
    # 用户关系
    children_relations: Mapped[List["UserRelation"]] = relationship("UserRelation", foreign_keys="UserRelation.elderly_id", back_populates="elderly")
    parent_relations: Mapped[List["UserRelation"]] = relationship("UserRelation", foreign_keys="UserRelation.child_id", back_populates="child")
    
    # 社交关系
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")
    post_comments: Mapped[List["PostComment"]] = relationship("PostComment", back_populates="user")
    post_likes: Mapped[List["PostLike"]] = relationship("PostLike", back_populates="user")
    enrollments: Mapped[List["CourseEnrollment"]] = relationship("CourseEnrollment", back_populates="user")
    challenge_records: Mapped[List["ChallengeRecord"]] = relationship("ChallengeRecord", back_populates="user")
    sent_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", foreign_keys="ChatMessage.sender_id", back_populates="sender")
    received_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", foreign_keys="ChatMessage.receiver_id", back_populates="receiver")
    challenges: Mapped[List["Challenge"]] = relationship("Challenge", secondary="challenge_participants", back_populates="participants") 