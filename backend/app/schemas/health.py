from datetime import datetime
from typing import Optional
from pydantic import Field, field_validator

from .base import BaseSchema

class HealthRecordBase(BaseSchema):
    """健康记录基础模型"""
    user_id: int = Field(..., description="用户ID")
    blood_pressure: Optional[str] = Field(None, description="血压，格式: '120/80'")
    heart_rate: Optional[int] = Field(None, ge=30, le=220, description="心率")
    blood_sugar: Optional[float] = Field(None, ge=1.0, le=30.0, description="血糖")
    weight: Optional[float] = Field(None, gt=0, description="体重(kg)")
    height: Optional[float] = Field(None, gt=0, description="身高(cm)")
    bmi: Optional[float] = Field(None, description="BMI指数")
    notes: Optional[str] = Field(None, max_length=500, description="备注信息")
    
    @field_validator('blood_pressure')
    def validate_blood_pressure(cls, v):
        """验证血压格式"""
        if v is None:
            return v
        try:
            systolic, diastolic = v.split('/')
            systolic_val = int(systolic.strip())
            diastolic_val = int(diastolic.strip())
            if not (60 <= systolic_val <= 250 and 40 <= diastolic_val <= 150):
                raise ValueError("血压值不在合理范围内")
        except ValueError as e:
            raise ValueError("血压格式无效，应为'收缩压/舒张压'，例如'120/80'") from e
        return v

class HealthRecordCreate(HealthRecordBase):
    """创建健康记录的请求模型"""
    recorded_at: Optional[datetime] = Field(None, description="记录时间，默认为当前时间")

class HealthRecordUpdate(BaseSchema):
    """更新健康记录的请求模型"""
    blood_pressure: Optional[str] = Field(None, description="血压，格式: '120/80'")
    heart_rate: Optional[int] = Field(None, ge=30, le=220, description="心率")
    blood_sugar: Optional[float] = Field(None, ge=1.0, le=30.0, description="血糖")
    weight: Optional[float] = Field(None, gt=0, description="体重(kg)")
    height: Optional[float] = Field(None, gt=0, description="身高(cm)")
    bmi: Optional[float] = Field(None, description="BMI指数")
    notes: Optional[str] = Field(None, max_length=500, description="备注信息")
    
    @field_validator('blood_pressure')
    def validate_blood_pressure(cls, v):
        """验证血压格式"""
        if v is None:
            return v
        try:
            systolic, diastolic = v.split('/')
            systolic_val = int(systolic.strip())
            diastolic_val = int(diastolic.strip())
            if not (60 <= systolic_val <= 250 and 40 <= diastolic_val <= 150):
                raise ValueError("血压值不在合理范围内")
        except ValueError as e:
            raise ValueError("血压格式无效，应为'收缩压/舒张压'，例如'120/80'") from e
        return v

class HealthRecordInDB(HealthRecordBase):
    """数据库中的健康记录模型"""
    id: int = Field(..., description="记录ID")
    recorded_at: datetime = Field(..., description="记录时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class HealthRecordPublic(HealthRecordBase):
    """返回给客户端的健康记录模型"""
    id: int = Field(..., description="记录ID")
    recorded_at: datetime = Field(..., description="记录时间")
    created_at: datetime = Field(..., description="创建时间")

class HealthStatistics(BaseSchema):
    """健康统计数据"""
    avg_heart_rate: Optional[float] = Field(None, description="平均心率")
    avg_blood_sugar: Optional[float] = Field(None, description="平均血糖")
    latest_weight: Optional[float] = Field(None, description="最新体重")
    latest_bmi: Optional[float] = Field(None, description="最新BMI")
    records_count: int = Field(..., description="记录数量")
    latest_record: Optional[HealthRecordPublic] = Field(None, description="最新记录") 