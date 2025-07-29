from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Type, TypeVar, Optional, Generic
import logging
from jose import JWTError, jwt

from .core.database import get_async_db
from .core.config import settings
from .repositories.base import RepositoryBase
from .services.base_service import BaseService
from .schemas.user import UserPublic
from .models.user import UserRole
from .repositories import (
    user_repository,
    course_repository,
    health_repository,
    prescription_repository,
    prescription_exercise_repository,
    challenge_repository,
    challenge_participant_repository,
    challenge_record_repository,
    chat_message_repository,
    chat_room_repository,
    chat_room_member_repository
)
from .services import (
    user_service,
    auth_service,
    course_service,
    health_service,
    prescription_service,
    challenge_service,
    chat_service,
    ai_service
)

# 定义类型变量
T = TypeVar('T')
RepoT = TypeVar('RepoT', bound=RepositoryBase)
ServiceT = TypeVar('ServiceT', bound=BaseService)

# 数据库会话依赖项
def get_db_session() -> AsyncSession:
    """
    获取异步数据库会话
    可以直接使用此依赖项，或者使用已有的get_async_db
    """
    return get_async_db()

# 通用Repository依赖项生成器
def get_repository(
    repo_type: Type[RepoT],
    repo_instance: Optional[RepoT] = None
) -> Callable[[], RepoT]:
    """
    创建用于获取Repository实例的依赖函数
    
    Args:
        repo_type: Repository类型
        repo_instance: Repository实例，如果已经有实例可以直接传入
    
    Returns:
        一个依赖函数，返回Repository实例
    """
    if repo_instance:
        def get_repo() -> RepoT:
            return repo_instance
    else:
        def get_repo() -> RepoT:
            return repo_type()
    
    return get_repo

# 通用Service依赖项生成器
def get_service(
    service_type: Type[ServiceT],
    service_instance: Optional[ServiceT] = None
) -> Callable[[], ServiceT]:
    """
    创建用于获取Service实例的依赖函数
    
    Args:
        service_type: Service类型
        service_instance: Service实例，如果已经有实例可以直接传入
    
    Returns:
        一个依赖函数，返回Service实例
    """
    if service_instance:
        def get_svc() -> ServiceT:
            return service_instance
    else:
        def get_svc() -> ServiceT:
            return service_type()
    
    return get_svc

# ============== Repository依赖项 ==============
def get_user_repository() -> Callable[[], 'UserRepository']:
    from .repositories.user import UserRepository
    return get_repository(UserRepository, user_repository)

def get_course_repository() -> Callable[[], 'CourseRepository']:
    from .repositories.course import CourseRepository
    return get_repository(CourseRepository, course_repository)

def get_health_repository() -> Callable[[], 'HealthRepository']:
    from .repositories.health import HealthRepository
    return get_repository(HealthRepository, health_repository)

def get_prescription_repository() -> Callable[[], 'PrescriptionRepository']:
    from .repositories.prescription import PrescriptionRepository
    return get_repository(PrescriptionRepository, prescription_repository)

def get_prescription_exercise_repository() -> Callable[[], 'PrescriptionExerciseRepository']:
    from .repositories.prescription import PrescriptionExerciseRepository
    return get_repository(PrescriptionExerciseRepository, prescription_exercise_repository)

def get_challenge_repository() -> Callable[[], 'ChallengeRepository']:
    from .repositories.challenge import ChallengeRepository
    return get_repository(ChallengeRepository, challenge_repository)

def get_challenge_participant_repository() -> Callable[[], 'ChallengeParticipantRepository']:
    from .repositories.challenge import ChallengeParticipantRepository
    return get_repository(ChallengeParticipantRepository, challenge_participant_repository)

def get_challenge_record_repository() -> Callable[[], 'ChallengeRecordRepository']:
    from .repositories.challenge import ChallengeRecordRepository
    return get_repository(ChallengeRecordRepository, challenge_record_repository)

def get_chat_message_repository() -> Callable[[], 'ChatMessageRepository']:
    from .repositories.chat import ChatMessageRepository
    return get_repository(ChatMessageRepository, chat_message_repository)

def get_chat_room_repository() -> Callable[[], 'ChatRoomRepository']:
    from .repositories.chat import ChatRoomRepository
    return get_repository(ChatRoomRepository, chat_room_repository)

def get_chat_room_member_repository() -> Callable[[], 'ChatRoomMemberRepository']:
    from .repositories.chat import ChatRoomMemberRepository
    return get_repository(ChatRoomMemberRepository, chat_room_member_repository)

# ============== Service依赖项 ==============
def get_user_service() -> 'UserService':
    """获取用户服务实例"""
    from .services.user_service import UserService
    return user_service

def get_auth_service() -> 'AuthService':
    """获取认证服务实例"""
    from .services.auth_service import AuthService
    return auth_service

def get_course_service() -> 'CourseService':
    """获取课程服务实例"""
    from .services.course_service import CourseService
    return course_service

def get_health_service() -> 'HealthService':
    """获取健康服务实例"""
    from .services.health_service import HealthService
    return health_service

def get_prescription_service() -> 'PrescriptionService':
    """获取处方服务实例"""
    from .services.prescription_service import PrescriptionService
    return prescription_service

def get_challenge_service() -> 'ChallengeService':
    """获取挑战服务实例"""
    from .services.challenge_service import ChallengeService
    return challenge_service

def get_chat_service() -> 'ChatService':
    """获取聊天服务实例"""
    from .services.chat_service import ChatService
    return chat_service

def get_ai_service() -> 'AIService':
    """获取AI服务实例"""
    from .services.ai_service import AIService
    return ai_service 

async def get_current_user_websocket(token: str) -> Optional[UserPublic]:
    """WebSocket用户认证"""
    try:
        from .services.auth_service import AuthService
        auth_service = AuthService()
        
        # 验证token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        
        # 获取用户信息
        user = await auth_service.get_user_by_username(username)
        if user is None:
            return None
        
        return UserPublic(
            id=user.id,
            username=user.username,
            email=user.email,
            nickname=user.nickname or user.username,
            is_active=user.is_active,
            role=user.role or UserRole.ELDERLY,
            unique_id=user.unique_id or f"E{user.id:06d}",
            created_at=user.created_at
        )
    except JWTError:
        return None
    except Exception as e:
        logging.error(f"WebSocket auth error: {e}")
        return None 