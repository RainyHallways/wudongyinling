from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.sql import func
from .base import BaseModel

class Course(BaseModel):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=False)
    cover_url = Column(String(255))
    video_url = Column(String(255))
    duration = Column(Integer, nullable=False)  # in minutes
    difficulty = Column(Enum('beginner', 'intermediate', 'advanced', name='difficulty_level'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 