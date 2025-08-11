from typing import List, Optional
from sqlalchemy import and_, or_, desc, asc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import RepositoryBase
from ..models.social import Post, PostComment, PostLike, HeritageProject, HeritageInheritor
from ..schemas.social import (
    PostCreate, PostUpdate, PostCommentCreate, PostCommentUpdate,
    PostLikeCreate, PostLikeUpdate,
    HeritageProjectCreate, HeritageProjectUpdate, 
    HeritageInheritorCreate, HeritageInheritorUpdate
)


class PostRepository(RepositoryBase[Post, PostCreate, PostUpdate]):
    """动态Repository"""
    
    def __init__(self):
        super().__init__(Post)
    
    async def get_posts_with_user(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 20,
        post_type: Optional[str] = None,
        user_role: Optional[str] = None,
        is_public: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        user_id: Optional[int] = None
    ) -> List[Post]:
        """获取带用户信息的动态列表"""
        from ..models.user import User
        
        query = select(self.model).options(selectinload(Post.user))
        
        # 筛选条件
        if post_type:
            query = query.where(Post.post_type == post_type)
        if user_role:
            # 角色以字符串存储（如 'admin','teacher','elderly'），保持前端传入的小写匹配
            query = query.join(User).where(User.role == user_role)
        if is_public is not None:
            query = query.where(Post.is_public == is_public)
        if is_featured is not None:
            query = query.where(Post.is_featured == is_featured)
        if user_id:
            query = query.where(Post.user_id == user_id)
        
        # 排序：精选在前，然后按创建时间倒序
        query = query.order_by(desc(Post.is_featured), desc(Post.created_at))
        
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def get_posts_by_user(
        self, 
        db: AsyncSession, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[Post]:
        """获取用户的动态列表"""
        query = select(self.model).where(Post.user_id == user_id)
        query = query.order_by(desc(Post.created_at))
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def toggle_featured(self, db: AsyncSession, post_id: int) -> Optional[Post]:
        """切换精选状态"""
        post = await self.get(db, post_id)
        if post:
            post.is_featured = not post.is_featured
            await db.commit()
            await db.refresh(post)
        return post
    
    async def toggle_visibility(self, db: AsyncSession, post_id: int) -> Optional[Post]:
        """切换可见性"""
        post = await self.get(db, post_id)
        if post:
            post.is_public = not post.is_public
            await db.commit()
            await db.refresh(post)
        return post
    
    async def increment_likes_count(self, db: AsyncSession, post_id: int):
        """增加点赞数"""
        post = await self.get(db, post_id)
        if post:
            post.likes_count = (post.likes_count or 0) + 1
            await db.commit()
    
    async def decrement_likes_count(self, db: AsyncSession, post_id: int):
        """减少点赞数"""
        post = await self.get(db, post_id)
        if post and (post.likes_count or 0) > 0:
            post.likes_count = post.likes_count - 1
            await db.commit()
    
    async def increment_comments_count(self, db: AsyncSession, post_id: int):
        """增加评论数"""
        post = await self.get(db, post_id)
        if post:
            post.comments_count = (post.comments_count or 0) + 1
            await db.commit()
    
    async def decrement_comments_count(self, db: AsyncSession, post_id: int):
        """减少评论数"""
        post = await self.get(db, post_id)
        if post and (post.comments_count or 0) > 0:
            post.comments_count = post.comments_count - 1
            await db.commit()

    async def get_total_count(
        self,
        db: AsyncSession,
        post_type: Optional[str] = None,
        user_role: Optional[str] = None,
        is_public: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        user_id: Optional[int] = None
    ) -> int:
        """获取符合条件的动态总数"""
        from ..models.user import User
        
        query = select(func.count(Post.id))
        
        # 筛选条件
        if post_type:
            query = query.where(Post.post_type == post_type)
        if user_role:
            query = query.join(User).where(User.role == user_role)
        if is_public is not None:
            query = query.where(Post.is_public == is_public)
        if is_featured is not None:
            query = query.where(Post.is_featured == is_featured)
        if user_id:
            query = query.where(Post.user_id == user_id)
        
        result = await db.execute(query)
        return result.scalar() or 0


class PostCommentRepository(RepositoryBase[PostComment, PostCommentCreate, PostCommentUpdate]):
    """动态评论Repository"""
    
    def __init__(self):
        super().__init__(PostComment)
    
    async def get_comments_by_post(
        self, 
        db: AsyncSession, 
        post_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[PostComment]:
        """获取动态的评论列表"""
        query = select(self.model).options(selectinload(PostComment.user))
        query = query.where(PostComment.post_id == post_id, PostComment.parent_id.is_(None))
        query = query.order_by(desc(PostComment.created_at))
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
    
    async def get_replies_by_comment(
        self, 
        db: AsyncSession, 
        comment_id: int
    ) -> List[PostComment]:
        """获取评论的回复列表"""
        query = select(self.model).options(selectinload(PostComment.user))
        query = query.where(PostComment.parent_id == comment_id)
        query = query.order_by(asc(PostComment.created_at))
        result = await db.execute(query)
        return result.scalars().all()


class PostLikeRepository(RepositoryBase[PostLike, PostLikeCreate, PostLikeUpdate]):
    """动态点赞Repository"""
    
    def __init__(self):
        super().__init__(PostLike)
    
    async def get_like_by_user_and_post(
        self, 
        db: AsyncSession, 
        user_id: int, 
        post_id: int
    ) -> Optional[PostLike]:
        """获取用户对特定动态的点赞记录"""
        query = select(self.model).where(
            and_(PostLike.user_id == user_id, PostLike.post_id == post_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_like(
        self, 
        db: AsyncSession, 
        user_id: int, 
        post_id: int
    ) -> PostLike:
        """创建点赞记录"""
        like = PostLike(user_id=user_id, post_id=post_id)
        db.add(like)
        await db.commit()
        await db.refresh(like)
        return like
    
    async def delete_like(
        self, 
        db: AsyncSession, 
        user_id: int, 
        post_id: int
    ) -> bool:
        """删除点赞记录"""
        like = await self.get_like_by_user_and_post(db, user_id, post_id)
        if not like:
            return False
        await db.delete(like)
        await db.commit()
        return True


class HeritageProjectRepository(RepositoryBase[HeritageProject, HeritageProjectCreate, HeritageProjectUpdate]):
    """非遗项目Repository"""
    
    def __init__(self):
        super().__init__(HeritageProject)

    async def get_projects_with_inheritors(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        level: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[HeritageProject]:
        """获取非遗项目列表（带传承人）"""
        query = select(self.model).options(selectinload(HeritageProject.inheritor))
        
        # 筛选条件
        if keyword:
            query = query.where(
                or_(
                    HeritageProject.name.contains(keyword),
                    HeritageProject.description.contains(keyword)
                )
            )
        if category:
            query = query.where(HeritageProject.category == category)
        if level:
            query = query.where(HeritageProject.level == level)
        if is_active is not None:
            query = query.where(HeritageProject.is_active == is_active)
        
        query = query.order_by(desc(HeritageProject.created_at))
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def get_total_count(
        self,
        db: AsyncSession,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        level: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """获取符合条件的项目总数"""
        query = select(func.count(HeritageProject.id))
        
        # 筛选条件
        if keyword:
            query = query.where(
                or_(
                    HeritageProject.name.contains(keyword),
                    HeritageProject.description.contains(keyword)
                )
            )
        if category:
            query = query.where(HeritageProject.category == category)
        if level:
            query = query.where(HeritageProject.level == level)
        if is_active is not None:
            query = query.where(HeritageProject.is_active == is_active)
        
        result = await db.execute(query)
        return result.scalar() or 0

    async def toggle_project_status(self, db: AsyncSession, project_id: int) -> Optional[HeritageProject]:
        """切换项目启用状态（兼容旧命名）"""
        project = await self.get(db, project_id)
        if project:
            project.is_active = not bool(project.is_active)
            await db.commit()
            await db.refresh(project)
        return project

    async def toggle_active_status(self, db: AsyncSession, project_id: int) -> Optional[HeritageProject]:
        """切换项目启用状态"""
        return await self.toggle_project_status(db, project_id)

    async def get_projects_with_inheritor(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        level: Optional[str] = None,
        is_active: Optional[bool] = None,
        keyword: Optional[str] = None
    ) -> List[HeritageProject]:
        """兼容服务层调用的参数顺序"""
        return await self.get_projects_with_inheritors(
            db=db,
            skip=skip,
            limit=limit,
            keyword=keyword,
            category=category,
            level=level,
            is_active=is_active
        )

    async def get_projects_by_inheritor(self, db: AsyncSession, inheritor_id: int) -> List[HeritageProject]:
        query = select(self.model).where(HeritageProject.inheritor_id == inheritor_id)
        result = await db.execute(query)
        return result.scalars().all()


class HeritageInheritorRepository(RepositoryBase[HeritageInheritor, HeritageInheritorCreate, HeritageInheritorUpdate]):
    """非遗传承人Repository"""
    
    def __init__(self):
        super().__init__(HeritageInheritor)

    async def get_inheritors_with_projects(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        keyword: Optional[str] = None,
        hometown: Optional[str] = None,
        gender: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[HeritageInheritor]:
        """获取传承人列表（带项目）"""
        query = select(self.model).options(selectinload(HeritageInheritor.projects))
        
        # 筛选条件
        if keyword:
            query = query.where(
                or_(
                    HeritageInheritor.name.contains(keyword),
                    HeritageInheritor.biography.contains(keyword)
                )
            )
        if hometown:
            query = query.where(HeritageInheritor.hometown.contains(hometown))
        if gender:
            query = query.where(HeritageInheritor.gender == gender)
        if is_active is not None:
            query = query.where(HeritageInheritor.is_active == is_active)
        
        query = query.order_by(desc(HeritageInheritor.created_at))
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def get_total_count(
        self,
        db: AsyncSession,
        keyword: Optional[str] = None,
        hometown: Optional[str] = None,
        gender: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """获取符合条件的传承人总数"""
        query = select(func.count(HeritageInheritor.id))
        
        # 筛选条件
        if keyword:
            query = query.where(
                or_(
                    HeritageInheritor.name.contains(keyword),
                    HeritageInheritor.biography.contains(keyword)
                )
            )
        if hometown:
            query = query.where(HeritageInheritor.hometown.contains(hometown))
        if gender:
            query = query.where(HeritageInheritor.gender == gender)
        if is_active is not None:
            query = query.where(HeritageInheritor.is_active == is_active)
        
        result = await db.execute(query)
        return result.scalar() or 0

    async def toggle_inheritor_status(self, db: AsyncSession, inheritor_id: int) -> Optional[HeritageInheritor]:
        """切换传承人启用状态"""
        inheritor = await self.get(db, inheritor_id)
        if inheritor:
            inheritor.is_active = not bool(inheritor.is_active)
            await db.commit()
            await db.refresh(inheritor)
        return inheritor