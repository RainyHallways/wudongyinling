from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from .base import BaseSchema


# Post相关Schema
class PostBase(BaseSchema):
    """动态基础模型"""
    title: Optional[str] = Field(None, description="动态标题")
    content: str = Field(..., description="动态内容")
    post_type: str = Field(default="text", description="动态类型")
    media_url: Optional[str] = Field(None, description="媒体文件URL")
    thumbnail_url: Optional[str] = Field(None, description="缩略图URL")
    is_public: bool = Field(default=True, description="是否公开")
    is_featured: bool = Field(default=False, description="是否精选")


class PostCreate(PostBase):
    """创建动态"""
    pass


class PostUpdate(BaseSchema):
    """更新动态"""
    title: Optional[str] = Field(None, description="动态标题")
    content: Optional[str] = Field(None, description="动态内容")
    post_type: Optional[str] = Field(None, description="动态类型")
    media_url: Optional[str] = Field(None, description="媒体文件URL")
    thumbnail_url: Optional[str] = Field(None, description="缩略图URL")
    is_public: Optional[bool] = Field(None, description="是否公开")
    is_featured: Optional[bool] = Field(None, description="是否精选")


class PostPublic(PostBase):
    """返回给客户端的动态模型"""
    id: int = Field(..., description="动态ID")
    user_id: int = Field(..., description="发布者ID")
    likes_count: int = Field(..., description="点赞数")
    comments_count: int = Field(..., description="评论数")
    shares_count: int = Field(..., description="分享数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class PostWithUser(PostPublic):
    """包含用户信息的动态"""
    user: Optional[dict] = Field(None, description="发布者信息")


# PostComment相关Schema
class PostCommentBase(BaseSchema):
    """评论基础模型"""
    content: str = Field(..., description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID")


class PostCommentCreate(PostCommentBase):
    """创建评论"""
    post_id: int = Field(..., description="动态ID")


class PostCommentUpdate(BaseSchema):
    """更新评论"""
    content: Optional[str] = Field(None, description="评论内容")


class PostCommentPublic(PostCommentBase):
    """返回给客户端的评论模型"""
    id: int = Field(..., description="评论ID")
    post_id: int = Field(..., description="动态ID")
    user_id: int = Field(..., description="评论者ID")
    created_at: datetime = Field(..., description="创建时间")


class PostCommentWithUser(PostCommentPublic):
    """包含用户信息的评论"""
    user: Optional[dict] = Field(None, description="评论者信息")
    replies: List[dict] = Field(default_factory=list, description="回复列表")


# PostLike相关Schema
class PostLikeCreate(BaseSchema):
    """点赞动态"""
    post_id: int = Field(..., description="动态ID")


class PostLikeUpdate(BaseSchema):
    """更新点赞 - 基本上不会用到"""
    pass


class PostLikePublic(BaseSchema):
    """点赞信息"""
    id: int = Field(..., description="点赞ID")
    post_id: int = Field(..., description="动态ID")
    user_id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="点赞时间")


# HeritageProject相关Schema
class HeritageProjectBase(BaseSchema):
    """非遗项目基础模型"""
    name: str = Field(..., description="项目名称")
    description: str = Field(..., description="项目描述")
    origin_location: str = Field(..., description="发源地")
    category: str = Field(..., description="项目类别")
    level: str = Field(..., description="保护级别")
    cover_image: Optional[str] = Field(None, description="封面图片")
    video_url: Optional[str] = Field(None, description="视频链接")
    history: Optional[str] = Field(None, description="历史背景")
    characteristics: Optional[str] = Field(None, description="特色特点")
    inheritor_id: Optional[int] = Field(None, description="传承人ID")


class HeritageProjectCreate(HeritageProjectBase):
    """创建非遗项目"""
    pass


class HeritageProjectUpdate(BaseSchema):
    """更新非遗项目"""
    name: Optional[str] = Field(None, description="项目名称")
    description: Optional[str] = Field(None, description="项目描述")
    origin_location: Optional[str] = Field(None, description="发源地")
    category: Optional[str] = Field(None, description="项目类别")
    level: Optional[str] = Field(None, description="保护级别")
    cover_image: Optional[str] = Field(None, description="封面图片")
    video_url: Optional[str] = Field(None, description="视频链接")
    history: Optional[str] = Field(None, description="历史背景")
    characteristics: Optional[str] = Field(None, description="特色特点")
    inheritor_id: Optional[int] = Field(None, description="传承人ID")
    is_active: Optional[bool] = Field(None, description="是否启用")


class HeritageProjectPublic(HeritageProjectBase):
    """返回给客户端的非遗项目模型"""
    id: int = Field(..., description="项目ID")
    is_active: bool = Field(..., description="是否启用")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class HeritageProjectWithInheritor(HeritageProjectPublic):
    """包含传承人信息的非遗项目"""
    inheritor: Optional[dict] = Field(None, description="传承人信息")


# HeritageInheritor相关Schema
class HeritageInheritorBase(BaseSchema):
    """传承人基础模型"""
    name: str = Field(..., description="姓名")
    gender: str = Field(..., description="性别")
    birth_year: Optional[int] = Field(None, description="出生年份")
    hometown: str = Field(..., description="籍贯")
    specialty: str = Field(..., description="专长")
    biography: Optional[str] = Field(None, description="个人简介")
    achievements: Optional[str] = Field(None, description="主要成就")
    avatar: Optional[str] = Field(None, description="头像")
    contact_info: Optional[str] = Field(None, description="联系方式")


class HeritageInheritorCreate(HeritageInheritorBase):
    """创建传承人"""
    pass


class HeritageInheritorUpdate(BaseSchema):
    """更新传承人"""
    name: Optional[str] = Field(None, description="姓名")
    gender: Optional[str] = Field(None, description="性别")
    birth_year: Optional[int] = Field(None, description="出生年份")
    hometown: Optional[str] = Field(None, description="籍贯")
    specialty: Optional[str] = Field(None, description="专长")
    biography: Optional[str] = Field(None, description="个人简介")
    achievements: Optional[str] = Field(None, description="主要成就")
    avatar: Optional[str] = Field(None, description="头像")
    contact_info: Optional[str] = Field(None, description="联系方式")
    is_active: Optional[bool] = Field(None, description="是否启用")


class HeritageInheritorPublic(HeritageInheritorBase):
    """返回给客户端的传承人模型"""
    id: int = Field(..., description="传承人ID")
    is_active: bool = Field(..., description="是否启用")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class HeritageInheritorWithProjects(HeritageInheritorPublic):
    """包含项目信息的传承人"""
    projects: List[HeritageProjectPublic] = Field(default_factory=list, description="相关项目")


# 延迟导入和模型重建将在模块末尾处理 