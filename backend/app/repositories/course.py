from typing import Optional, List
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from .base import RepositoryBase
from ..models.course import Course
from ..schemas.course import CourseCreate, CourseUpdate

class CourseRepository(RepositoryBase[Course, CourseCreate, CourseUpdate]):
    """
    课程数据访问层
    """
    
    def __init__(self):
        super().__init__(Course)
    
    async def get_by_title(self, db: AsyncSession, title: str) -> Optional[Course]:
        """
        通过标题获取课程
        
        Args:
            db: 数据库会话
            title: 课程标题
            
        Returns:
            课程对象，如未找到返回None
        """
        result = await db.execute(select(Course).where(Course.title == title))
        return result.scalars().first()
    
    async def search(
        self, 
        db: AsyncSession, 
        *, 
        keyword: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        搜索课程
        
        Args:
            db: 数据库会话
            keyword: 搜索关键词
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        search_term = f"%{keyword}%"
        query = (
            select(Course)
            .where(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_difficulty(
        self, 
        db: AsyncSession, 
        *, 
        difficulty: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        获取指定难度的课程
        
        Args:
            db: 数据库会话
            difficulty: 难度级别
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        query = (
            select(Course)
            .where(Course.difficulty == difficulty)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_duration_range(
        self, 
        db: AsyncSession, 
        *, 
        min_duration: int,
        max_duration: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        获取指定时长范围内的课程
        
        Args:
            db: 数据库会话
            min_duration: 最小时长
            max_duration: 最大时长
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        query = (
            select(Course)
            .where(
                and_(
                    Course.duration >= min_duration,
                    Course.duration <= max_duration
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_instructor(
        self, 
        db: AsyncSession, 
        *, 
        instructor_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        获取指定讲师的课程
        
        Args:
            db: 数据库会话
            instructor_id: 讲师ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        query = (
            select(Course)
            .where(Course.instructor_id == instructor_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_course_count_by_difficulty(self, db: AsyncSession) -> dict:
        """
        获取各难度级别的课程数量
        
        Args:
            db: 数据库会话
            
        Returns:
            各难度级别的课程数量字典
        """
        query = (
            select(Course.difficulty, func.count(Course.id))
            .group_by(Course.difficulty)
        )
        result = await db.execute(query)
        return {difficulty: count for difficulty, count in result.all()} 