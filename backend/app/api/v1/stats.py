from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from datetime import datetime

from ...core.database import get_async_db
from ...core.security import get_current_active_user, get_current_admin_user
from ...schemas.base import DataResponse
from ...services.user_service import UserService
from ...services.course_service import CourseService
from ...services.challenge_service import ChallengeService
from ...services.health_service import HealthService
from ...models.user import User

router = APIRouter()

@router.get("/dashboard", response_model=DataResponse[Dict[str, Any]])
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends(),
    course_service: CourseService = Depends(),
    challenge_service: ChallengeService = Depends(),
    health_service: HealthService = Depends()
):
    """
    获取仪表盘统计数据 (仅管理员可访问)
    """
    # 使用各服务层的repository对象获取统计数据
    total_users = await user_service.repository.count(db)
    total_courses = await course_service.repository.count(db)
    total_challenges = await challenge_service.repository.count(db)
    total_health_records = await health_service.repository.count(db)
    
    # 获取活跃用户数
    active_users = await user_service.repository.count(db, filters={"is_active": True})
    
    # 获取各难度级别的课程数量
    course_by_difficulty = await course_service.get_course_count_by_difficulty(db)
    
    # 构建统计数据
    stats = {
        "totalUsers": total_users,
        "totalCourses": total_courses,
        "totalChallenges": total_challenges,
        "totalHealthRecords": total_health_records,
        "activeUsers": active_users,
        "coursesByDifficulty": course_by_difficulty
    }
    
    return DataResponse(data=stats)

@router.get("/user/{user_id}", response_model=DataResponse[Dict[str, Any]])
async def get_user_stats(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
    health_service: HealthService = Depends(),
    challenge_service: ChallengeService = Depends()
):
    """
    获取指定用户的统计数据 (用户本人或管理员可访问)
    """
    # 权限检查：只有用户本人或管理员可以查看用户统计
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="没有权限访问该用户的统计数据")
    
    # 获取健康记录统计
    health_stats = await health_service.get_statistics(db, user_id=user_id, days=30)
    
    # 获取用户参与的挑战数量
    user_challenges = await challenge_service.get_user_challenges(
        db, 
        user_id=user_id, 
        skip=0, 
        limit=100,  # 这里简单处理，实际场景可能需要分页
        include_inactive=True
    )
    
    # 构建统计数据
    stats = {
        "healthStats": health_stats.model_dump() if health_stats else {},
        "challengeCount": len(user_challenges),
        "lastUpdated": datetime.now().isoformat()
    }
    
    return DataResponse(data=stats) 