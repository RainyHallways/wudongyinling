from datetime import datetime
from typing import Optional, List
from pydantic import Field, field_validator

from .base import BaseSchema

class CourseBase(BaseSchema):
    """课程基础模型"""
    title: str = Field(..., min_length=3, max_length=100, description="课程标题")
    description: str = Field(..., description="课程描述")
    difficulty: str = Field(..., description="难度级别，beginner/intermediate/advanced")
    duration: int = Field(..., gt=0, description="课程时长（分钟）")
    
    @field_validator('difficulty')
    def difficulty_validator(cls, v):
        """验证难度级别是否有效"""
        allowed_values = ['beginner', 'intermediate', 'advanced']
        if v not in allowed_values:
            raise ValueError(f'难度级别必须是以下之一: {", ".join(allowed_values)}')
        return v

class CourseCreate(CourseBase):
    """创建课程的请求模型"""
    cover_url: Optional[str] = Field(None, description="封面图片URL")
    video_url: Optional[str] = Field(None, description="视频URL")
    instructor_id: Optional[int] = Field(None, description="讲师ID")

class CourseUpdate(BaseSchema):
    """更新课程的请求模型"""
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="课程标题")
    description: Optional[str] = Field(None, description="课程描述")
    difficulty: Optional[str] = Field(None, description="难度级别，beginner/intermediate/advanced")
    duration: Optional[int] = Field(None, gt=0, description="课程时长（分钟）")
    cover_url: Optional[str] = Field(None, description="封面图片URL")
    video_url: Optional[str] = Field(None, description="视频URL")
    instructor_id: Optional[int] = Field(None, description="讲师ID")
    
    @field_validator('difficulty')
    def difficulty_validator(cls, v):
        """验证难度级别是否有效"""
        if v is None:
            return v
        allowed_values = ['beginner', 'intermediate', 'advanced']
        if v not in allowed_values:
            raise ValueError(f'难度级别必须是以下之一: {", ".join(allowed_values)}')
        return v

class CourseInDB(CourseBase):
    """数据库中的课程模型"""
    id: int = Field(..., description="课程ID")
    cover_url: Optional[str] = Field(None, description="封面图片URL")
    video_url: Optional[str] = Field(None, description="视频URL")
    instructor_id: Optional[int] = Field(None, description="讲师ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class CoursePublic(CourseBase):
    """返回给客户端的课程模型"""
    id: int = Field(..., description="课程ID")
    cover_url: Optional[str] = Field(None, description="封面图片URL")
    video_url: Optional[str] = Field(None, description="视频URL")
    created_at: datetime = Field(..., description="创建时间")
    instructor_id: Optional[int] = Field(None, description="讲师ID")

class CourseEnrollmentBase(BaseSchema):
    """课程报名基础模型"""
    course_id: int = Field(..., description="课程ID")
    user_id: int = Field(..., description="用户ID")

class CourseEnrollmentCreate(CourseEnrollmentBase):
    """创建课程报名的请求模型"""
    pass

class CourseEnrollmentUpdate(BaseSchema):
    """更新课程报名的请求模型"""
    progress: Optional[float] = Field(None, ge=0, le=100, description="课程进度，0-100的百分比")
    completed: Optional[bool] = Field(None, description="是否完成")

class CourseEnrollmentInDB(CourseEnrollmentBase):
    """数据库中的课程报名模型"""
    enrollment_date: datetime = Field(..., description="报名时间")
    progress: float = Field(0, ge=0, le=100, description="课程进度，0-100的百分比")
    completed: bool = Field(False, description="是否完成")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class CourseEnrollmentPublic(CourseEnrollmentBase):
    """返回给客户端的课程报名模型"""
    enrollment_date: datetime = Field(..., description="报名时间")
    progress: float = Field(..., description="课程进度，0-100的百分比")
    completed: bool = Field(..., description="是否完成")
    course: CoursePublic = Field(..., description="课程信息") 