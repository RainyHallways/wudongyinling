from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.sql import func
from ..core.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    cover_url = Column(String(255))
    video_url = Column(String(255))
    duration = Column(Integer)  # 课程时长（分钟）
    difficulty = Column(Enum('beginner', 'intermediate', 'advanced', name='course_difficulty'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 