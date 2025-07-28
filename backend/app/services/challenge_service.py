from typing import List, Optional, Dict, Any, Union, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date, timedelta

from .base_service import BaseService
from ..models.challenge import Challenge, challenge_participants, ChallengeRecord
from ..repositories import (
    challenge_repository, 
    challenge_participant_repository,
    challenge_record_repository
)
from ..schemas.challenge import (
    ChallengeCreate, ChallengeUpdate,
    ChallengeParticipantCreate, ChallengeParticipantInDB,
    ChallengeRecordCreate, ChallengeRecordUpdate
)

class ChallengeService(BaseService[Challenge, ChallengeCreate, ChallengeUpdate]):
    """
    挑战服务，处理挑战相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化挑战服务
        """
        super().__init__(challenge_repository)
        self.participant_repository = challenge_participant_repository
        self.record_repository = challenge_record_repository
    
    async def get_active_challenges(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Challenge]:
        """
        获取当前活跃的挑战
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            挑战列表
        """
        return await self.repository.get_active_challenges(db, skip=skip, limit=limit)
    
    async def get_upcoming_challenges(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Challenge]:
        """
        获取即将开始的挑战
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            挑战列表
        """
        return await self.repository.get_upcoming_challenges(db, skip=skip, limit=limit)
    
    async def get_by_creator(
        self, 
        db: AsyncSession, 
        *, 
        creator_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Challenge]:
        """
        获取指定创建者的挑战
        
        Args:
            db: 数据库会话
            creator_id: 创建者ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            挑战列表
        """
        return await self.repository.get_by_creator(db, creator_id=creator_id, skip=skip, limit=limit)
    
    async def get_challenge_with_participant_count(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int
    ) -> Optional[Tuple[Challenge, int]]:
        """
        获取挑战及其参与者数量
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            
        Returns:
            (挑战对象, 参与者数量)元组，如未找到挑战返回(None, 0)
        """
        return await self.repository.get_with_participant_count(db, id=challenge_id)
    
    async def check_user_joined(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int, 
        user_id: int
    ) -> bool:
        """
        检查用户是否已参与挑战
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            user_id: 用户ID
            
        Returns:
            是否已参与
        """
        return await self.repository.check_user_joined(
            db, 
            challenge_id=challenge_id, 
            user_id=user_id
        )
    
    async def get_popular_challenges(
        self, 
        db: AsyncSession, 
        *, 
        limit: int = 10
    ) -> List[Tuple[Challenge, int]]:
        """
        获取最受欢迎的挑战
        
        Args:
            db: 数据库会话
            limit: 返回的最大记录数
            
        Returns:
            (挑战对象, 参与者数量)元组列表
        """
        return await self.repository.get_popular_challenges(db, limit=limit)
    
    async def join_challenge(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        加入挑战
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            user_id: 用户ID
            
        Returns:
            参与记录
        """
        # 检查挑战是否存在
        challenge = await self.repository.get(db, challenge_id)
        if not challenge:
            raise ValueError("挑战不存在")
        
        # 检查挑战是否活跃
        if not challenge.is_active:
            raise ValueError("挑战已结束或被禁用")
            
        # 检查挑战是否已经开始
        now = datetime.now()
        if challenge.end_date < now:
            raise ValueError("挑战已结束")
            
        # 检查用户是否已参与
        is_joined = await self.repository.check_user_joined(
            db, 
            challenge_id=challenge_id, 
            user_id=user_id
        )
        
        if is_joined:
            raise ValueError("已经参与该挑战")
            
        # 检查是否达到最大参与人数
        if challenge.max_participants:
            participant_count = await self.participant_repository.count_participants(
                db, 
                challenge_id=challenge_id
            )
            if participant_count >= challenge.max_participants:
                raise ValueError("挑战已达到最大参与人数")
                
        # 创建参与记录
        participant_data = ChallengeParticipantCreate(
            user_id=user_id,
            challenge_id=challenge_id
        )
        
        participant = await self.participant_repository.create(
            db, 
            obj_in=participant_data
        )
        return participant
    
    async def quit_challenge(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int, 
        user_id: int
    ) -> bool:
        """
        退出挑战
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            user_id: 用户ID
            
        Returns:
            是否成功退出
        """
        participant = await self.participant_repository.get_by_user_and_challenge(
            db, 
            user_id=user_id, 
            challenge_id=challenge_id
        )
        
        if not participant:
            return False
            
        await self.participant_repository.remove(
            db,
            user_id=user_id,
            challenge_id=challenge_id
        )
        return True
    
    async def get_user_challenges(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False
    ) -> List[Challenge]:
        """
        获取用户参与的挑战
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            include_inactive: 是否包含非活跃挑战
            
        Returns:
            挑战列表
        """
        return await self.participant_repository.get_challenges_by_user(
            db, 
            user_id=user_id, 
            skip=skip, 
            limit=limit,
            include_inactive=include_inactive
        )
    
    async def get_challenge_participants(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        获取挑战的参与者
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            参与者列表
        """
        return await self.participant_repository.get_participants_by_challenge(
            db, 
            challenge_id=challenge_id, 
            skip=skip, 
            limit=limit
        )
    
    async def check_in(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int, 
        user_id: int,
        record_in: ChallengeRecordCreate
    ) -> ChallengeRecord:
        """
        挑战打卡
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            user_id: 用户ID
            record_in: 打卡记录创建数据
            
        Returns:
            打卡记录
        """
        # 检查用户是否已参与挑战
        is_joined = await self.repository.check_user_joined(
            db, 
            challenge_id=challenge_id, 
            user_id=user_id
        )
        
        if not is_joined:
            raise ValueError("未参与该挑战")
            
        # 检查挑战是否活跃
        challenge = await self.repository.get(db, challenge_id)
        if not challenge or not challenge.is_active:
            raise ValueError("挑战已结束或被禁用")
            
        # 检查今日是否已打卡
        today = datetime.now().date()
        today_record = await self.record_repository.get_by_date(
            db, 
            user_id=user_id, 
            challenge_id=challenge_id,
            check_in_date=today
        )
        
        if today_record:
            raise ValueError("今日已打卡")
            
        # 创建打卡记录
        record_data = record_in.model_dump()
        if not record_data.get("user_id"):
            record_data["user_id"] = user_id
        record_data["challenge_id"] = challenge_id
        if not record_data.get("check_in_date"):
            record_data["check_in_date"] = datetime.now()
            
        # 计算积分奖励
        if record_data.get("completed", True) and not record_data.get("points_earned"):
            # 默认给予挑战设置的奖励积分
            record_data["points_earned"] = challenge.reward_points
            
        record = await self.record_repository.create(
            db, 
            obj_in=ChallengeRecordCreate(**record_data)
        )
        return record
    
    async def get_user_challenge_records(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int, 
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChallengeRecord]:
        """
        获取用户在指定挑战的记录
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            打卡记录列表
        """
        return await self.record_repository.get_by_user_and_challenge(
            db, 
            user_id=user_id, 
            challenge_id=challenge_id,
            skip=skip,
            limit=limit
        )
    
    async def get_challenge_progress(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        获取用户挑战进度
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            user_id: 用户ID
            
        Returns:
            进度信息
        """
        # 获取挑战信息
        challenge = await self.repository.get(db, challenge_id)
        if not challenge:
            raise ValueError("挑战不存在")
            
        # 计算挑战总天数
        start_date = challenge.start_date.date() if isinstance(challenge.start_date, datetime) else challenge.start_date
        end_date = challenge.end_date.date() if isinstance(challenge.end_date, datetime) else challenge.end_date
        total_days = (end_date - start_date).days + 1
        
        # 获取已打卡天数
        check_in_count = await self.record_repository.count_check_ins(
            db, 
            user_id=user_id, 
            challenge_id=challenge_id
        )
        
        # 计算获得的总积分
        total_points = await self.record_repository.get_total_points(
            db, 
            user_id=user_id, 
            challenge_id=challenge_id
        )
        
        # 计算打卡进度
        progress = (check_in_count / total_days) * 100 if total_days > 0 else 0
        
        # 获取是否今日已打卡
        today = datetime.now().date()
        today_record = await self.record_repository.get_by_date(
            db, 
            user_id=user_id, 
            challenge_id=challenge_id,
            check_in_date=today
        )
        
        # 判断挑战当前状态
        now = datetime.now()
        status = "upcoming"
        if challenge.start_date <= now:
            if challenge.end_date >= now:
                status = "active"
            else:
                status = "ended"
                
        return {
            "challenge_id": challenge.id,
            "title": challenge.title,
            "start_date": challenge.start_date.isoformat(),
            "end_date": challenge.end_date.isoformat(),
            "total_days": total_days,
            "check_in_count": check_in_count,
            "total_points": total_points,
            "progress": round(progress, 2),
            "is_checked_today": today_record is not None,
            "status": status
        }
    
    async def get_leaderboard(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        获取挑战排行榜
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            limit: 返回的最大记录数
            
        Returns:
            排行榜数据列表
        """
        return await self.record_repository.get_leaderboard(
            db, 
            challenge_id=challenge_id,
            limit=limit
        ) 