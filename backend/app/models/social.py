from typing import List, Optional
from enum import Enum
from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class PostType(str, Enum):
    """动态类型枚举"""
    TEXT = "text"           # 文字动态
    IMAGE = "image"         # 图片动态
    VIDEO = "video"         # 视频动态
    DANCE = "dance"         # 舞蹈分享
    HERITAGE = "heritage"   # 非遗传承

class Post(Base):
    """动态模型"""
    __tablename__ = "posts"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    post_type: Mapped[PostType] = mapped_column(SQLEnum(PostType), default=PostType.TEXT)
    media_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)
    shares_count: Mapped[int] = mapped_column(Integer, default=0)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否精选
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系定义
    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["PostComment"]] = relationship("PostComment", back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[List["PostLike"]] = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")

class PostComment(Base):
    """动态评论模型"""
    __tablename__ = "post_comments"

    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("post_comments.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系定义
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="post_comments")
    parent: Mapped[Optional["PostComment"]] = relationship("PostComment", remote_side="PostComment.id", back_populates="replies")
    replies: Mapped[List["PostComment"]] = relationship("PostComment", back_populates="parent")

class PostLike(Base):
    """动态点赞模型"""
    __tablename__ = "post_likes"

    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系定义
    post: Mapped["Post"] = relationship("Post", back_populates="likes")
    user: Mapped["User"] = relationship("User", back_populates="post_likes")

class HeritageProject(Base):
    """非遗传承项目模型"""
    __tablename__ = "heritage_projects"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    origin_location: Mapped[str] = mapped_column(String(100), nullable=False)  # 发源地
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # 类别
    level: Mapped[str] = mapped_column(String(50), nullable=False)  # 保护级别
    cover_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    history: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 历史背景
    characteristics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 特色特点
    inheritor_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("heritage_inheritors.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系定义
    inheritor: Mapped[Optional["HeritageInheritor"]] = relationship("HeritageInheritor", back_populates="projects")

class HeritageInheritor(Base):
    """非遗传承人模型"""
    __tablename__ = "heritage_inheritors"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    birth_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    hometown: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(200), nullable=False)  # 专长
    biography: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 个人简介
    achievements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 主要成就
    avatar: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    contact_info: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系定义
    projects: Mapped[List["HeritageProject"]] = relationship("HeritageProject", back_populates="inheritor") 