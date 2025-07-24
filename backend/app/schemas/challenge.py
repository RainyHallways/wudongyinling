from datetime import datetime
from typing import Optional, List
from pydantic import Field, field_validator

from .base import BaseSchema
from .user import UserPublic

class ChallengeBase(BaseSchema):
    """挑战活动基础模型"""
    title: str = Field(..., min_length=3, max_length=100, description="挑战标题")
    description: str = Field(..., description="挑战描述")
    start_date: datetime = Field(..., description="开始日期")
    end_date: datetime = Field(..., description="结束日期")
    image_url: Optional[str] = Field(None, description="挑战图片URL")
    creator_id: int = Field(..., description="创建者ID")
    max_participants: Optional[int] = Field(None, gt=0, description="最大参与人数")
    reward_points: int = Field(0, ge=0, description="奖励积分")
    
    @field_validator('end_date')
    def validate_end_date(cls, v, values):
        """验证结束日期必须晚于开始日期"""
        if 'start_date' in values.data and v <= values.data['start_date']:
            raise ValueError("结束日期必须晚于开始日期")
        return v

class ChallengeCreate(ChallengeBase):
    """创建挑战的请求模型"""
    pass

class ChallengeUpdate(BaseSchema):
    """更新挑战的请求模型"""
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="挑战标题")
    description: Optional[str] = Field(None, description="挑战描述")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    image_url: Optional[str] = Field(None, description="挑战图片URL")
    is_active: Optional[bool] = Field(None, description="是否激活")
    max_participants: Optional[int] = Field(None, gt=0, description="最大参与人数")
    reward_points: Optional[int] = Field(None, ge=0, description="奖励积分")
    
    @field_validator('end_date')
    def validate_end_date(cls, v, values):
        """验证结束日期必须晚于开始日期"""
        if v is not None and 'start_date' in values.data and values.data['start_date'] is not None and v <= values.data['start_date']:
            raise ValueError("结束日期必须晚于开始日期")
        return v

class ChallengeInDB(ChallengeBase):
    """数据库中的挑战模型"""
    id: int = Field(..., description="挑战ID")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class ChallengePublic(ChallengeBase):
    """返回给客户端的挑战模型"""
    id: int = Field(..., description="挑战ID")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")
    participants_count: int = Field(0, description="参与人数")
    is_joined: Optional[bool] = Field(None, description="当前用户是否参与")

class ChallengeParticipantBase(BaseSchema):
    """挑战参与者基础模型"""
    user_id: int = Field(..., description="用户ID")
    challenge_id: int = Field(..., description="挑战ID")
    joined_at: datetime = Field(..., description="参与时间")

class ChallengeParticipantCreate(BaseSchema):
    """创建挑战参与记录的请求模型"""
    challenge_id: int = Field(..., description="挑战ID")
    user_id: Optional[int] = Field(None, description="用户ID，默认为当前用户")

class ChallengeParticipantInDB(ChallengeParticipantBase):
    """数据库中的挑战参与记录模型"""
    pass

class ChallengeParticipantPublic(ChallengeParticipantBase):
    """返回给客户端的挑战参与记录模型"""
    user: UserPublic = Field(..., description="用户信息")
    challenge: ChallengePublic = Field(..., description="挑战信息")

class ChallengeRecordBase(BaseSchema):
    """挑战记录基础模型"""
    user_id: int = Field(..., description="用户ID")
    challenge_id: int = Field(..., description="挑战ID")
    check_in_date: datetime = Field(..., description="打卡日期")
    completed: bool = Field(True, description="是否完成")
    points_earned: int = Field(0, ge=0, description="获得积分")
    duration: Optional[int] = Field(None, gt=0, description="活动时长(分钟)")
    notes: Optional[str] = Field(None, description="备注")
    evidence_url: Optional[str] = Field(None, description="完成证明URL")

class ChallengeRecordCreate(ChallengeRecordBase):
    """创建挑战记录的请求模型"""
    user_id: Optional[int] = Field(None, description="用户ID，默认为当前用户")

class ChallengeRecordUpdate(BaseSchema):
    """更新挑战记录的请求模型"""
    completed: Optional[bool] = Field(None, description="是否完成")
    points_earned: Optional[int] = Field(None, ge=0, description="获得积分")
    duration: Optional[int] = Field(None, gt=0, description="活动时长(分钟)")
    notes: Optional[str] = Field(None, description="备注")
    evidence_url: Optional[str] = Field(None, description="完成证明URL")

class ChallengeRecordInDB(ChallengeRecordBase):
    """数据库中的挑战记录模型"""
    id: int = Field(..., description="记录ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class ChallengeRecordPublic(ChallengeRecordBase):
    """返回给客户端的挑战记录模型"""
    id: int = Field(..., description="记录ID")
    created_at: datetime = Field(..., description="创建时间")
    user: UserPublic = Field(..., description="用户信息")
    challenge: ChallengePublic = Field(..., description="挑战信息") 