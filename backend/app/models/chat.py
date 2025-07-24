from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import String, Text, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class MessageType(str, PyEnum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"

class ChatMessage(Base):
    """聊天消息模型"""
    __tablename__ = "chat_messages"

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(
        Enum(MessageType), 
        default=MessageType.TEXT, 
        nullable=False
    )
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
    read_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    chat_room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chat_rooms.id"), nullable=True)

    # 关系定义
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    chat_room: Mapped[Optional["ChatRoom"]] = relationship("ChatRoom", back_populates="messages")

class ChatRoom(Base):
    """聊天室模型"""
    __tablename__ = "chat_rooms"
    
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_group: Mapped[bool] = mapped_column(default=False, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # 关系定义
    messages: Mapped[list["ChatMessage"]] = relationship("ChatMessage", back_populates="chat_room")
    members: Mapped[list["ChatRoomMember"]] = relationship("ChatRoomMember", back_populates="room")
    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id])

class ChatRoomMember(Base):
    """聊天室成员模型"""
    __tablename__ = "chat_room_members"
    
    room_id: Mapped[int] = mapped_column(ForeignKey("chat_rooms.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    join_date: Mapped[datetime] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # 关系定义
    room: Mapped["ChatRoom"] = relationship("ChatRoom", back_populates="members")
    user: Mapped["User"] = relationship("User") 