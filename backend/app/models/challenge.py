from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

# 用户-挑战关联表
challenge_participants = Table(
    'challenge_participants',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('challenge_id', Integer, ForeignKey('challenges.id'), primary_key=True),
    Column('joined_at', DateTime(timezone=True), nullable=False)
)

class Challenge(Base):
    """挑战活动模型"""
    __tablename__ = "challenges"

    title: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reward_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # 关系定义
    participants: Mapped[List["User"]] = relationship(
        "User", 
        secondary=challenge_participants, 
        back_populates="challenges"
    )
    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id])
    records: Mapped[List["ChallengeRecord"]] = relationship("ChallengeRecord", back_populates="challenge")

class ChallengeRecord(Base):
    """挑战记录模型，记录用户参与挑战的情况"""
    __tablename__ = "challenge_records"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"), nullable=False)
    check_in_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 活动时长(分钟)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # 完成证明(图片/视频)
    
    # 关系定义
    user: Mapped["User"] = relationship("User", back_populates="challenge_records")
    challenge: Mapped["Challenge"] = relationship("Challenge", back_populates="records") 