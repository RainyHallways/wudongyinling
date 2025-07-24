from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import Field, field_validator

from .base import BaseSchema

class PrescriptionExerciseBase(BaseSchema):
    """处方训练项目基础模型"""
    name: str = Field(..., min_length=2, max_length=100, description="训练项目名称")
    description: str = Field(..., description="训练项目描述")
    duration: int = Field(..., gt=0, description="训练时长(分钟)")
    frequency: str = Field(..., description="训练频率，如'每天一次'")
    sets: Optional[int] = Field(None, gt=0, description="组数")
    reps: Optional[int] = Field(None, gt=0, description="每组重复次数")
    image_url: Optional[str] = Field(None, description="训练图片URL")
    video_url: Optional[str] = Field(None, description="训练视频URL")

class PrescriptionExerciseCreate(PrescriptionExerciseBase):
    """创建处方训练项目的请求模型"""
    pass

class PrescriptionExerciseUpdate(BaseSchema):
    """更新处方训练项目的请求模型"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="训练项目名称")
    description: Optional[str] = Field(None, description="训练项目描述")
    duration: Optional[int] = Field(None, gt=0, description="训练时长(分钟)")
    frequency: Optional[str] = Field(None, description="训练频率，如'每天一次'")
    sets: Optional[int] = Field(None, gt=0, description="组数")
    reps: Optional[int] = Field(None, gt=0, description="每组重复次数")
    image_url: Optional[str] = Field(None, description="训练图片URL")
    video_url: Optional[str] = Field(None, description="训练视频URL")

class PrescriptionExerciseInDB(PrescriptionExerciseBase):
    """数据库中的处方训练项目模型"""
    id: int = Field(..., description="训练项目ID")
    prescription_id: int = Field(..., description="所属处方ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class PrescriptionExercisePublic(PrescriptionExerciseBase):
    """返回给客户端的处方训练项目模型"""
    id: int = Field(..., description="训练项目ID")
    prescription_id: int = Field(..., description="所属处方ID")

class PrescriptionBase(BaseSchema):
    """处方基础模型"""
    user_id: int = Field(..., description="用户ID")
    disease_type: str = Field(..., min_length=2, max_length=50, description="疾病类型")
    training_plan: str = Field(..., description="训练计划概述")
    schedule: Dict[str, Any] = Field(..., description="训练计划日程表，JSON格式")
    start_date: datetime = Field(..., description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    status: str = Field("active", description="状态：active/completed/cancelled")
    comments: Optional[str] = Field(None, description="备注")
    doctor_id: Optional[int] = Field(None, description="医生/教练ID")
    
    @field_validator('status')
    def validate_status(cls, v):
        """验证状态值"""
        allowed_values = ['active', 'completed', 'cancelled']
        if v not in allowed_values:
            raise ValueError(f"状态必须是以下之一: {', '.join(allowed_values)}")
        return v
    
    @field_validator('end_date')
    def validate_end_date(cls, v, values):
        """验证结束日期必须晚于开始日期"""
        if v is not None and 'start_date' in values.data and v < values.data['start_date']:
            raise ValueError("结束日期必须晚于开始日期")
        return v

class PrescriptionCreate(PrescriptionBase):
    """创建处方的请求模型"""
    exercises: List[PrescriptionExerciseCreate] = Field(..., min_length=1, description="训练项目列表")

class PrescriptionUpdate(BaseSchema):
    """更新处方的请求模型"""
    disease_type: Optional[str] = Field(None, min_length=2, max_length=50, description="疾病类型")
    training_plan: Optional[str] = Field(None, description="训练计划概述")
    schedule: Optional[Dict[str, Any]] = Field(None, description="训练计划日程表，JSON格式")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    status: Optional[str] = Field(None, description="状态：active/completed/cancelled")
    comments: Optional[str] = Field(None, description="备注")
    
    @field_validator('status')
    def validate_status(cls, v):
        """验证状态值"""
        if v is None:
            return v
        allowed_values = ['active', 'completed', 'cancelled']
        if v not in allowed_values:
            raise ValueError(f"状态必须是以下之一: {', '.join(allowed_values)}")
        return v

class PrescriptionInDB(PrescriptionBase):
    """数据库中的处方模型"""
    id: int = Field(..., description="处方ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class PrescriptionPublic(PrescriptionBase):
    """返回给客户端的处方模型"""
    id: int = Field(..., description="处方ID")
    created_at: datetime = Field(..., description="创建时间")
    exercises: List[PrescriptionExercisePublic] = Field(default_factory=list, description="训练项目列表") 