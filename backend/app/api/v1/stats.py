from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from datetime import datetime, date

from ...core.database import get_async_db
from ...core.security import get_current_active_user, get_current_admin_user
from ...schemas.base import DataResponse, PaginatedResponse
from ...services.user_service import UserService
from ...services.course_service import CourseService
from ...services.challenge_service import ChallengeService
from ...services.health_service import HealthService
from ...services.social_service import SocialService
from ...models.user import User
from ...core.exceptions import ForbiddenException, NotFoundException

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
        raise ForbiddenException("没有权限访问该用户的统计数据")
    
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

# 平台总体统计接口
@router.get("/users", response_model=DataResponse[Dict[str, Any]])
async def get_user_statistics(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends()
):
    """
    获取用户统计信息（仅管理员可访问）
    """
    # 获取用户注册趋势（最近30天）
    from datetime import timedelta
    thirty_days_ago = datetime.now() - timedelta(days=30)
    user_registration_trend = await user_service.get_registration_trend(db, start_date=thirty_days_ago)
    
    # 获取用户活跃度统计
    user_activity_stats = await user_service.get_user_activity_stats(db)
    
    # 获取角色分布统计
    user_role_distribution = await user_service.get_role_distribution(db)
    
    stats = {
        "registrationTrend": user_registration_trend,
        "activityStats": user_activity_stats,
        "roleDistribution": user_role_distribution,
        "totalUsers": await user_service.repository.count(db),
        "activeUsers": await user_service.repository.count(db, filters={"is_active": True})
    }
    
    return DataResponse(data=stats)

@router.get("/courses", response_model=DataResponse[Dict[str, Any]])
async def get_course_statistics(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin_user),
    course_service: CourseService = Depends()
):
    """
    获取课程统计信息（仅管理员可访问）
    """
    # 获取课程创建趋势
    from datetime import timedelta
    thirty_days_ago = datetime.now() - timedelta(days=30)
    course_creation_trend = await course_service.get_creation_trend(db, start_date=thirty_days_ago)
    
    # 获取课程参与统计
    course_participation_stats = await course_service.get_participation_stats(db)
    
    # 获取课程分类统计
    course_category_stats = await course_service.get_category_stats(db)
    
    stats = {
        "creationTrend": course_creation_trend,
        "participationStats": course_participation_stats,
        "categoryStats": course_category_stats,
        "totalCourses": await course_service.repository.count(db),
        "popularCourses": await course_service.get_popular_courses(db, limit=10)
    }
    
    return DataResponse(data=stats)

@router.get("/challenges", response_model=DataResponse[Dict[str, Any]])
async def get_challenge_statistics(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin_user),
    challenge_service: ChallengeService = Depends()
):
    """
    获取挑战统计信息（仅管理员可访问）
    """
    # 获取挑战参与统计
    challenge_participation_stats = await challenge_service.get_participation_stats(db)
    
    # 获取挑战完成情况
    completion_stats = await challenge_service.get_completion_stats(db)
    
    # 获取挑战类型分布
    challenge_type_distribution = await challenge_service.get_type_distribution(db)
    
    stats = {
        "participationStats": challenge_participation_stats,
        "completionStats": completion_stats,
        "typeDistribution": challenge_type_distribution,
        "totalChallenges": await challenge_service.repository.count(db)
    }
    
    return DataResponse(data=stats)

@router.get("/user/{user_id}/activity", response_model=DataResponse[Dict[str, Any]])
async def get_user_activity_statistics(
    user_id: int,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(),
    course_service: CourseService = Depends(),
    challenge_service: ChallengeService = Depends(),
    health_service: HealthService = Depends(),
    social_service: SocialService = Depends()
):
    """
    获取用户活动统计（用户本人或管理员可访问）
    """
    # 权限检查
    if current_user.id != user_id and not current_user.is_admin:
        raise ForbiddenException("没有权限访问该用户的活动统计")
    
    # 获取用户课程参与统计
    user_course_activity = await course_service.get_user_course_activity(db, user_id, start_date, end_date)
    
    # 获取用户挑战参与统计
    user_challenge_activity = await challenge_service.get_user_activity_stats(db, user_id, start_date, end_date)
    
    # 获取用户健康记录统计
    user_health_activity = await health_service.get_user_activity_stats(db, user_id, start_date, end_date)
    
    # 获取用户社交活动统计
    user_social_activity = await social_service.get_user_activity_stats(db, user_id, start_date, end_date)
    
    stats = {
        "courseActivity": user_course_activity,
        "challengeActivity": user_challenge_activity,
        "healthActivity": user_health_activity,
        "socialActivity": user_social_activity,
        "period": {
            "startDate": start_date.isoformat() if start_date else None,
            "endDate": end_date.isoformat() if end_date else None
        }
    }
    
    return DataResponse(data=stats) 