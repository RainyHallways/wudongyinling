from datetime import datetime
from typing import Optional, List
from pydantic import Field, field_validator

from .base import BaseSchema
from .user import UserPublic

class ChatMessageBase(BaseSchema):
    """聊天消息基础模型"""
    sender_id: int = Field(..., description="发送者ID")
    receiver_id: int = Field(..., description="接收者ID")
    content: str = Field(..., description="消息内容")
    message_type: str = Field("text", description="消息类型: text/image/video/audio/file")
    
    @field_validator('message_type')
    def validate_message_type(cls, v):
        """验证消息类型"""
        allowed_values = ['text', 'image', 'video', 'audio', 'file']
        if v not in allowed_values:
            raise ValueError(f"消息类型必须是以下之一: {', '.join(allowed_values)}")
        return v

class ChatMessageCreate(ChatMessageBase):
    """创建聊天消息的请求模型"""
    sender_id: Optional[int] = Field(None, description="发送者ID，默认为当前用户")
    chat_room_id: Optional[int] = Field(None, description="聊天室ID")

class ChatMessageUpdate(BaseSchema):
    """更新聊天消息的请求模型"""
    is_read: Optional[bool] = Field(None, description="是否已读")
    content: Optional[str] = Field(None, description="消息内容")

class ChatMessageInDB(ChatMessageBase):
    """数据库中的聊天消息模型"""
    id: int = Field(..., description="消息ID")
    is_read: bool = Field(False, description="是否已读")
    read_at: Optional[datetime] = Field(None, description="已读时间")
    chat_room_id: Optional[int] = Field(None, description="聊天室ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class ChatMessagePublic(ChatMessageBase):
    """返回给客户端的聊天消息模型"""
    id: int = Field(..., description="消息ID")
    is_read: bool = Field(..., description="是否已读")
    read_at: Optional[datetime] = Field(None, description="已读时间")
    created_at: datetime = Field(..., description="创建时间")
    sender: UserPublic = Field(..., description="发送者信息")
    receiver: UserPublic = Field(..., description="接收者信息")
    chat_room_id: Optional[int] = Field(None, description="聊天室ID")

class ChatRoomBase(BaseSchema):
    """聊天室基础模型"""
    name: Optional[str] = Field(None, max_length=100, description="聊天室名称")
    is_group: bool = Field(False, description="是否为群聊")
    creator_id: int = Field(..., description="创建者ID")

class ChatRoomCreate(ChatRoomBase):
    """创建聊天室的请求模型"""
    creator_id: Optional[int] = Field(None, description="创建者ID，默认为当前用户")
    member_ids: List[int] = Field(..., min_length=1, description="成员ID列表")

class ChatRoomUpdate(BaseSchema):
    """更新聊天室的请求模型"""
    name: Optional[str] = Field(None, max_length=100, description="聊天室名称")

class ChatRoomInDB(ChatRoomBase):
    """数据库中的聊天室模型"""
    id: int = Field(..., description="聊天室ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class ChatRoomPublic(ChatRoomBase):
    """返回给客户端的聊天室模型"""
    id: int = Field(..., description="聊天室ID")
    created_at: datetime = Field(..., description="创建时间")
    member_count: int = Field(0, description="成员数量")
    last_message: Optional[ChatMessagePublic] = Field(None, description="最新消息")
    creator: UserPublic = Field(..., description="创建者信息")

class ChatRoomMemberBase(BaseSchema):
    """聊天室成员基础模型"""
    room_id: int = Field(..., description="聊天室ID")
    user_id: int = Field(..., description="用户ID")
    join_date: datetime = Field(..., description="加入时间")
    nickname: Optional[str] = Field(None, max_length=50, description="在聊天室中的昵称")
    is_admin: bool = Field(False, description="是否为管理员")

class ChatRoomMemberCreate(BaseSchema):
    """创建聊天室成员的请求模型"""
    room_id: int = Field(..., description="聊天室ID")
    user_id: int = Field(..., description="用户ID")
    nickname: Optional[str] = Field(None, max_length=50, description="在聊天室中的昵称")
    is_admin: Optional[bool] = Field(False, description="是否为管理员")

class ChatRoomMemberUpdate(BaseSchema):
    """更新聊天室成员的请求模型"""
    nickname: Optional[str] = Field(None, max_length=50, description="在聊天室中的昵称")
    is_admin: Optional[bool] = Field(None, description="是否为管理员")

class ChatRoomMemberInDB(ChatRoomMemberBase):
    """数据库中的聊天室成员模型"""
    pass

class ChatRoomMemberPublic(ChatRoomMemberBase):
    """返回给客户端的聊天室成员模型"""
    user: UserPublic = Field(..., description="用户信息") 