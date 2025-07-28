from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import String, Text, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class DifficultyLevel(str, PyEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Course(Base):
    """课程模型"""
    __tablename__ = "courses"

    title: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    cover_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)  # 以分钟为单位
    difficulty: Mapped[str] = mapped_column(
        Enum(DifficultyLevel),
        nullable=False, 
        default=DifficultyLevel.BEGINNER
    )
    instructor_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # 关系定义
    enrollments: Mapped[List["CourseEnrollment"]] = relationship("CourseEnrollment", back_populates="course")
    
class CourseEnrollment(Base):
    """课程报名模型，记录用户与课程的多对多关系"""
    __tablename__ = "course_enrollments"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    enrollment_date: Mapped[datetime] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    progress: Mapped[float] = mapped_column(default=0.0)  # 课程完成百分比 0.0 - 100.0
    
    # 关系定义
    user: Mapped["User"] = relationship("User", back_populates="enrollments")
    course: Mapped["Course"] = relationship("Course", back_populates="enrollments") 