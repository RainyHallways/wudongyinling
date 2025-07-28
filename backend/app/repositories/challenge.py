from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, date, timedelta
from sqlalchemy import select, func, and_, or_, desc, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import RepositoryBase
from ..models.challenge import Challenge, challenge_participants, ChallengeRecord
from ..schemas.challenge import (
    ChallengeCreate, ChallengeUpdate, 
    ChallengeParticipantCreate, ChallengeParticipantInDB,
    ChallengeRecordCreate, ChallengeRecordUpdate
)

class ChallengeRepository(RepositoryBase[Challenge, ChallengeCreate, ChallengeUpdate]):
    """
    挑战活动数据访问层
    """
    
    def __init__(self):
        super().__init__(Challenge)
    
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
        now = datetime.now()
        query = (
            select(Challenge)
            .where(
                and_(
                    Challenge.is_active == True,
                    Challenge.start_date <= now,
                    Challenge.end_date >= now
                )
            )
            .order_by(desc(Challenge.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
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
        now = datetime.now()
        query = (
            select(Challenge)
            .where(
                and_(
                    Challenge.is_active == True,
                    Challenge.start_date > now
                )
            )
            .order_by(Challenge.start_date)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
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
        query = (
            select(Challenge)
            .where(Challenge.creator_id == creator_id)
            .order_by(desc(Challenge.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_with_participant_count(
        self, 
        db: AsyncSession, 
        *, 
        id: int
    ) -> Optional[Tuple[Challenge, int]]:
        """
        获取挑战及其参与者数量
        
        Args:
            db: 数据库会话
            id: 挑战ID
            
        Returns:
            (挑战对象, 参与者数量)元组，如未找到挑战返回(None, 0)
        """
        challenge = await self.get(db, id)
        if not challenge:
            return None, 0
        
        count_query = (
            select(func.count())
            .select_from(challenge_participants)
            .where(challenge_participants.c.challenge_id == id)
        )
        result = await db.execute(count_query)
        count = result.scalar()
        
        return challenge, count
    
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
        query = (
            select(func.count())
            .select_from(challenge_participants)
            .where(
                and_(
                    challenge_participants.c.challenge_id == challenge_id,
                    challenge_participants.c.user_id == user_id
                )
            )
        )
        result = await db.execute(query)
        return result.scalar() > 0
    
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
        # 使用 text() 函数执行原生 SQL
        query = text("""
            SELECT 
                c.*, 
                COUNT(cp.user_id) AS participant_count
            FROM 
                challenge c
            LEFT JOIN 
                challenge_participant cp ON c.id = cp.challenge_id
            WHERE 
                c.is_active = true
            GROUP BY 
                c.id
            ORDER BY 
                participant_count DESC, 
                c.created_at DESC
            LIMIT :limit
        """)
        
        result = await db.execute(query, {"limit": limit})
        rows = result.all()
        
        challenges = []
        for row in rows:
            challenge_dict = {}
            for column, value in row._mapping.items():
                if column != 'participant_count':
                    challenge_dict[column] = value
            
            challenge = Challenge(**challenge_dict)
            participant_count = row.participant_count
            challenges.append((challenge, participant_count))
            
        return challenges

class ChallengeParticipantRepository:
    """
    挑战参与者数据访问层
    """
    
    async def create(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: ChallengeParticipantCreate
    ):
        """
        创建挑战参与记录
        """
        now = datetime.now()
        values = {
            "user_id": obj_in.user_id, 
            "challenge_id": obj_in.challenge_id,
            "joined_at": now
        }
        query = challenge_participants.insert().values(**values)
        await db.execute(query)
        await db.commit()
        return values
    
    async def remove(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        challenge_id: int
    ):
        """
        删除挑战参与记录
        """
        query = challenge_participants.delete().where(
            and_(
                challenge_participants.c.user_id == user_id,
                challenge_participants.c.challenge_id == challenge_id
            )
        )
        await db.execute(query)
        await db.commit()
        return {"user_id": user_id, "challenge_id": challenge_id}
    
    async def get_by_user_and_challenge(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        challenge_id: int
    ) -> Optional[Dict]:
        """
        获取用户参与的指定挑战
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            challenge_id: 挑战ID
            
        Returns:
            参与记录，如未找到返回None
        """
        query = (
            select(challenge_participants)
            .where(
                and_(
                    challenge_participants.c.user_id == user_id,
                    challenge_participants.c.challenge_id == challenge_id
                )
            )
        )
        result = await db.execute(query)
        record = result.first()
        return record._mapping if record else None
    
    async def get_participants_by_challenge(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
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
        query = (
            select(challenge_participants)
            .where(challenge_participants.c.challenge_id == challenge_id)
            .order_by(challenge_participants.c.joined_at)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return [row._mapping for row in result.all()]
    
    async def get_challenges_by_user(
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
        query = (
            select(Challenge)
            .join(
                challenge_participants,
                challenge_participants.c.challenge_id == Challenge.id
            )
            .where(challenge_participants.c.user_id == user_id)
        )
        
        if not include_inactive:
            query = query.where(Challenge.is_active == True)
            
        query = query.order_by(desc(Challenge.end_date)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def count_participants(
        self, 
        db: AsyncSession, 
        *, 
        challenge_id: int
    ) -> int:
        """
        计算挑战的参与者数量
        
        Args:
            db: 数据库会话
            challenge_id: 挑战ID
            
        Returns:
            参与者数量
        """
        query = (
            select(func.count())
            .select_from(challenge_participants)
            .where(challenge_participants.c.challenge_id == challenge_id)
        )
        result = await db.execute(query)
        return result.scalar()

class ChallengeRecordRepository(RepositoryBase[ChallengeRecord, ChallengeRecordCreate, ChallengeRecordUpdate]):
    """
    挑战记录数据访问层
    """
    
    def __init__(self):
        super().__init__(ChallengeRecord)
    
    async def get_by_user_and_challenge(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        challenge_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChallengeRecord]:
        """
        获取用户在指定挑战的记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            challenge_id: 挑战ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            挑战记录列表
        """
        query = (
            select(ChallengeRecord)
            .where(
                and_(
                    ChallengeRecord.user_id == user_id,
                    ChallengeRecord.challenge_id == challenge_id
                )
            )
            .order_by(desc(ChallengeRecord.check_in_date))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_date(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        challenge_id: int,
        check_in_date: date
    ) -> Optional[ChallengeRecord]:
        """
        获取用户在指定日期的挑战记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            challenge_id: 挑战ID
            check_in_date: 打卡日期
            
        Returns:
            挑战记录，如未找到返回None
        """
        # 将日期转换为datetime范围
        start_datetime = datetime.combine(check_in_date, datetime.min.time())
        end_datetime = datetime.combine(check_in_date, datetime.max.time())
        
        query = (
            select(ChallengeRecord)
            .where(
                and_(
                    ChallengeRecord.user_id == user_id,
                    ChallengeRecord.challenge_id == challenge_id,
                    ChallengeRecord.check_in_date >= start_datetime,
                    ChallengeRecord.check_in_date <= end_datetime
                )
            )
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_records_by_date_range(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        challenge_id: int,
        start_date: date,
        end_date: date
    ) -> List[ChallengeRecord]:
        """
        获取用户在指定日期范围内的挑战记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            challenge_id: 挑战ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            挑战记录列表
        """
        # 将日期转换为datetime
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        query = (
            select(ChallengeRecord)
            .where(
                and_(
                    ChallengeRecord.user_id == user_id,
                    ChallengeRecord.challenge_id == challenge_id,
                    ChallengeRecord.check_in_date >= start_datetime,
                    ChallengeRecord.check_in_date <= end_datetime
                )
            )
            .order_by(ChallengeRecord.check_in_date)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def count_check_ins(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        challenge_id: int
    ) -> int:
        """
        计算用户在挑战中的打卡次数
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            challenge_id: 挑战ID
            
        Returns:
            打卡次数
        """
        query = (
            select(func.count())
            .select_from(ChallengeRecord)
            .where(
                and_(
                    ChallengeRecord.user_id == user_id,
                    ChallengeRecord.challenge_id == challenge_id,
                    ChallengeRecord.completed == True
                )
            )
        )
        result = await db.execute(query)
        return result.scalar()
    
    async def get_total_points(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        challenge_id: Optional[int] = None
    ) -> int:
        """
        计算用户在挑战中获得的总积分
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            challenge_id: 挑战ID，如果为None则计算所有挑战的积分
            
        Returns:
            总积分
        """
        query = (
            select(func.sum(ChallengeRecord.points_earned))
            .where(
                and_(
                    ChallengeRecord.user_id == user_id,
                    ChallengeRecord.completed == True
                )
            )
        )
        
        if challenge_id is not None:
            query = query.where(ChallengeRecord.challenge_id == challenge_id)
            
        result = await db.execute(query)
        total_points = result.scalar()
        return total_points or 0
    
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
        # 使用 text() 函数执行原生 SQL
        query = text("""
            SELECT 
                cr.user_id,
                u.username,
                u.nickname,
                u.avatar,
                SUM(cr.points_earned) AS total_points,
                COUNT(cr.id) AS check_in_count
            FROM 
                challenge_record cr
            JOIN 
                "user" u ON cr.user_id = u.id
            WHERE 
                cr.challenge_id = :challenge_id
                AND cr.completed = true
            GROUP BY 
                cr.user_id, u.username, u.nickname, u.avatar
            ORDER BY 
                total_points DESC, 
                check_in_count DESC
            LIMIT :limit
        """)
        
        result = await db.execute(query, {"challenge_id": challenge_id, "limit": limit})
        
        leaderboard = []
        for row in result:
            leaderboard.append({
                "user_id": row.user_id,
                "username": row.username,
                "nickname": row.nickname,
                "avatar": row.avatar,
                "total_points": row.total_points,
                "check_in_count": row.check_in_count
            })
            
        return leaderboard 