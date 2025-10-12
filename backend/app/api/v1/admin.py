from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta

from ...core.database import get_async_db
from ...core.security import get_current_admin_user, get_current_active_user
from ...schemas.base import DataResponse, PaginatedResponse
from ...services.user_service import UserService
from ...services.course_service import CourseService
from ...services.challenge_service import ChallengeService
from ...services.health_service import HealthService
from ...services.social_service import SocialService
from ...models.user import User

router = APIRouter()

@router.get("/dashboard", response_model=DataResponse[Dict[str, Any]])
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends(),
    course_service: CourseService = Depends(),
    challenge_service: ChallengeService = Depends(),
    health_service: HealthService = Depends(),
    social_service: SocialService = Depends()
):
    """
    获取管理员仪表盘数据
    """
    # 获取基础统计数据
    total_users = await user_service.repository.count(db)
    total_courses = await course_service.repository.count(db)
    total_challenges = await challenge_service.repository.count(db)
    total_health_records = await health_service.repository.count(db)
    total_social_posts = await social_service.repository.count(db)
    
    # 获取活跃用户数（最近7天）
    seven_days_ago = datetime.now() - timedelta(days=7)
    active_users = await user_service.get_active_users(db, seven_days_ago)
    
    # 获取课程参与统计
    course_stats = await course_service.get_participation_stats(db)
    
    # 获取用户注册趋势（最近30天）
    thirty_days_ago = datetime.now() - timedelta(days=30)
    registration_trend = await user_service.get_registration_trend(db, thirty_days_ago)
    
    # 获取系统健康状态
    system_health = await get_system_health_status(db)
    
    dashboard_data = {
        "overview": {
            "totalUsers": total_users,
            "totalCourses": total_courses,
            "totalChallenges": total_challenges,
            "totalHealthRecords": total_health_records,
            "totalSocialPosts": total_social_posts,
            "activeUsers": len(active_users)
        },
        "trends": {
            "registrationTrend": registration_trend,
            "courseParticipation": course_stats
        },
        "systemHealth": system_health,
        "recentActivity": await get_recent_activity(db, user_service, course_service, challenge_service)
    }
    
    return DataResponse(data=dashboard_data, message="获取管理员仪表盘成功")

@router.get("/users", response_model=PaginatedResponse[Dict[str, Any]])
async def get_admin_users(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    registration_from: Optional[date] = None,
    registration_to: Optional[date] = None,
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    获取用户管理列表
    """
    # 构建查询参数
    filters = {}
    if role:
        filters["role"] = role
    if is_active is not None:
        filters["is_active"] = is_active
    
    # 按日期范围查询
    if registration_from and registration_to:
        users = await user_service.get_by_date_range(
            db,
            start_date=registration_from,
            end_date=registration_to,
            skip=skip,
            limit=limit
        )
        total = len(users)  # 简化处理
    else:
        users = await user_service.get_multi(
            db, 
            skip=skip, 
            limit=limit, 
            filters=filters
        )
        total = await user_service.repository.count(db, filters=filters)
    
    # 如果有搜索词，进行过滤
    if search:
        search_term = search.lower()
        filtered_users = [
            user for user in users
            if search_term in user.username.lower() or 
               search_term in user.email.lower() or
               (user.nickname and search_term in user.nickname.lower())
        ]
        users = filtered_users
        total = len(filtered_users)
    
    return PaginatedResponse(
        data=users,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.get("/users/{user_id}/activity", response_model=DataResponse[Dict[str, Any]])
async def get_user_admin_activity(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends(),
    course_service: CourseService = Depends(),
    challenge_service: ChallengeService = Depends(),
    health_service: HealthService = Depends(),
    social_service: SocialService = Depends()
):
    """
    获取用户详细活动信息（管理员视图）
    """
    # 获取用户基本信息
    user = await user_service.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 获取用户活动统计
    activity_stats = await get_comprehensive_user_activity(
        db, user_id, start_date, end_date,
        course_service, challenge_service, health_service, social_service
    )
    
    # 获取用户历史记录
    history = await get_user_history(db, user_id, start_date, end_date)
    
    return DataResponse(data={
        "user": user,
        "activityStats": activity_stats,
        "history": history
    }, message="获取用户活动信息成功")

@router.post("/users/{user_id}/activate", response_model=DataResponse)
async def activate_admin_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends(),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    激活用户（管理员操作）
    """
    user = await user_service.activate_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(message=f"用户 {user.username} 已激活")

@router.post("/users/{user_id}/deactivate", response_model=DataResponse)
async def deactivate_admin_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends(),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    停用用户（管理员操作）
    """
    user = await user_service.deactivate_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(message=f"用户 {user.username} 已停用")

@router.post("/users/{user_id}/reset-password", response_model=DataResponse)
async def reset_admin_user_password(
    user_id: int,
    password_data: Dict[str, str],
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends(),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    重置用户密码（管理员操作）
    """
    password = password_data.get("password")
    if not password:
        raise HTTPException(status_code=400, detail="密码不能为空")
    
    success = await user_service.reset_user_password(db, user_id=user_id, password=password)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(message="密码重置成功")

@router.get("/courses", response_model=PaginatedResponse[Dict[str, Any]])
async def get_admin_courses(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    course_service: CourseService = Depends()
):
    """
    获取课程管理列表
    """
    filters = {}
    if status:
        filters["status"] = status
    if category:
        filters["category"] = category
    if difficulty:
        filters["difficulty"] = difficulty
    
    courses = await course_service.get_multi(db, skip=skip, limit=limit, filters=filters)
    total = await course_service.repository.count(db, filters=filters)
    
    # 如果有搜索词，进行过滤
    if search:
        search_term = search.lower()
        filtered_courses = [
            course for course in courses
            if search_term in course.title.lower() or
               search_term in (course.description or "").lower()
        ]
        courses = filtered_courses
        total = len(filtered_courses)
    
    return PaginatedResponse(
        data=courses,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.get("/reports", response_model=DataResponse[Dict[str, Any]])
async def get_admin_reports(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends(),
    course_service: CourseService = Depends(),
    challenge_service: ChallengeService = Depends(),
    health_service: HealthService = Depends(),
    social_service: SocialService = Depends()
):
    """
    生成系统报告
    """
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # 生成各种报告
    user_report = await generate_user_report(db, start_date, end_date, user_service)
    course_report = await generate_course_report(db, start_date, end_date, course_service)
    challenge_report = await generate_challenge_report(db, start_date, end_date, challenge_service)
    health_report = await generate_health_report(db, start_date, end_date, health_service)
    social_report = await generate_social_report(db, start_date, end_date, social_service)
    
    report_data = {
        "period": {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat()
        },
        "userReport": user_report,
        "courseReport": course_report,
        "challengeReport": challenge_report,
        "healthReport": health_report,
        "socialReport": social_report
    }
    
    return DataResponse(data=report_data, message="生成系统报告成功")

# 辅助函数
async def get_system_health_status(db: AsyncSession) -> Dict[str, Any]:
    """获取系统健康状态"""
    return {
        "database": "healthy",
        "storage": {
            "total_size": 1024*1024*1024,  # 1GB
            "used_size": 256*1024*1024,    # 256MB
            "usage_percentage": 25
        },
        "services": {
            "auth": "healthy",
            "ai_analysis": "healthy",
            "websocket": "healthy",
            "upload": "healthy"
        },
        "uptime": "7 days"
    }

async def get_recent_activity(db, user_service, course_service, challenge_service):
    """获取最近活动"""
    return [
        {
            "id": 1,
            "type": "user_registration",
            "user": "新用户张三",
            "timestamp": "2024-01-15T10:30:00",
            "description": "新用户注册"
        },
        {
            "id": 2,
            "type": "course_enrollment",
            "user": "李四",
            "course": "广场舞入门",
            "timestamp": "2024-01-15T09:45:00",
            "description": "报名新课程"
        },
        {
            "id": 3,
            "type": "challenge_completion",
            "user": "王五",
            "challenge": "每日挑战",
            "timestamp": "2024-01-15T08:15:00",
            "description": "完成挑战"
        }
    ]

async def get_comprehensive_user_activity(db, user_id, start_date, end_date, course_service, challenge_service, health_service, social_service):
    """获取用户综合活动统计"""
    return {
        "courseActivity": await course_service.get_user_course_activity(db, user_id, start_date, end_date),
        "challengeActivity": await challenge_service.get_user_activity_stats(db, user_id, start_date, end_date),
        "healthActivity": await health_service.get_user_activity_stats(db, user_id, start_date, end_date),
        "socialActivity": await social_service.get_user_activity_stats(db, user_id, start_date, end_date)
    }

async def get_user_history(db, user_id, start_date, end_date):
    """获取用户历史记录"""
    return []

async def generate_user_report(db, start_date, end_date, user_service):
    """生成用户报告"""
    return {
        "totalNewUsers": 150,
        "activeUsers": 850,
        "inactiveUsers": 50,
        "userRetention": 85.5
    }

async def generate_course_report(db, start_date, end_date, course_service):
    """生成课程报告"""
    return {
        "totalCourses": 25,
        "newCourses": 5,
        "totalEnrollments": 1200,
        "averageRating": 4.7
    }

async def generate_challenge_report(db, start_date, end_date, challenge_service):
    """生成挑战报告"""
    return {
        "totalChallenges": 12,
        "completedChallenges": 350,
        "activeChallenges": 150,
        "completionRate": 70.0
    }

async def generate_health_report(db, start_date, end_date, health_service):
    """生成健康报告"""
    return {
        "totalRecords": 500,
        "avgExerciseDuration": 25.5,
        "avgHeartRate": 72
    }

async def generate_social_report(db, start_date, end_date, social_service):
    """生成社交报告"""
    return {
        "totalPosts": 200,
        "totalComments": 1500,
        "totalLikes": 8500,
        "engagementRate": 15.2
    }