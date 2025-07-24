from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from sqlalchemy import select, func, desc, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from .base import RepositoryBase
from ..models.health import HealthRecord
from ..schemas.health import HealthRecordCreate, HealthRecordUpdate

class HealthRepository(RepositoryBase[HealthRecord, HealthRecordCreate, HealthRecordUpdate]):
    """
    健康记录数据访问层
    """
    
    def __init__(self):
        super().__init__(HealthRecord)
    
    async def get_by_user_id(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[HealthRecord]:
        """
        获取指定用户的健康记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            健康记录列表
        """
        query = (
            select(HealthRecord)
            .where(HealthRecord.user_id == user_id)
            .order_by(desc(HealthRecord.recorded_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_date_range(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        start_date: date,
        end_date: date
    ) -> List[HealthRecord]:
        """
        获取指定日期范围内的健康记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            健康记录列表
        """
        # 将日期转换为datetime
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        query = (
            select(HealthRecord)
            .where(
                and_(
                    HealthRecord.user_id == user_id,
                    HealthRecord.recorded_at >= start_datetime,
                    HealthRecord.recorded_at <= end_datetime
                )
            )
            .order_by(desc(HealthRecord.recorded_at))
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_latest_record(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int
    ) -> Optional[HealthRecord]:
        """
        获取最新的健康记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            最新的健康记录，如未找到返回None
        """
        query = (
            select(HealthRecord)
            .where(HealthRecord.user_id == user_id)
            .order_by(desc(HealthRecord.recorded_at))
            .limit(1)
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_statistics(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        获取健康统计数据
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            days: 统计天数
            
        Returns:
            统计数据字典
        """
        # 计算开始日期
        now = datetime.now()
        start_date = datetime(now.year, now.month, now.day) - timedelta(days=days)
        
        # 获取最新记录
        latest_record = await self.get_latest_record(db, user_id=user_id)
        
        # 获取平均心率
        avg_heart_rate_query = (
            select(func.avg(HealthRecord.heart_rate))
            .where(
                and_(
                    HealthRecord.user_id == user_id,
                    HealthRecord.recorded_at >= start_date,
                    HealthRecord.heart_rate != None
                )
            )
        )
        avg_heart_rate_result = await db.execute(avg_heart_rate_query)
        avg_heart_rate = avg_heart_rate_result.scalar()
        
        # 获取平均血糖
        avg_blood_sugar_query = (
            select(func.avg(HealthRecord.blood_sugar))
            .where(
                and_(
                    HealthRecord.user_id == user_id,
                    HealthRecord.recorded_at >= start_date,
                    HealthRecord.blood_sugar != None
                )
            )
        )
        avg_blood_sugar_result = await db.execute(avg_blood_sugar_query)
        avg_blood_sugar = avg_blood_sugar_result.scalar()
        
        # 获取记录数量
        count_query = (
            select(func.count())
            .where(
                and_(
                    HealthRecord.user_id == user_id,
                    HealthRecord.recorded_at >= start_date
                )
            )
        )
        count_result = await db.execute(count_query)
        records_count = count_result.scalar()
        
        # 构建统计数据
        statistics = {
            "avg_heart_rate": float(avg_heart_rate) if avg_heart_rate else None,
            "avg_blood_sugar": float(avg_blood_sugar) if avg_blood_sugar else None,
            "latest_weight": float(latest_record.weight) if latest_record and latest_record.weight else None,
            "latest_bmi": float(latest_record.bmi) if latest_record and latest_record.bmi else None,
            "records_count": records_count,
            "latest_record": latest_record
        }
        
        return statistics
    
    async def get_monthly_summary(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        year: int,
        month: int
    ) -> List[Dict[str, Any]]:
        """
        获取月度健康记录摘要
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            year: 年份
            month: 月份
            
        Returns:
            月度健康记录摘要列表
        """
        query = (
            select(
                func.date(HealthRecord.recorded_at).label("record_date"),
                func.avg(HealthRecord.heart_rate).label("avg_heart_rate"),
                func.avg(HealthRecord.blood_sugar).label("avg_blood_sugar"),
                func.avg(HealthRecord.weight).label("avg_weight")
            )
            .where(
                and_(
                    HealthRecord.user_id == user_id,
                    extract('year', HealthRecord.recorded_at) == year,
                    extract('month', HealthRecord.recorded_at) == month
                )
            )
            .group_by(func.date(HealthRecord.recorded_at))
            .order_by(func.date(HealthRecord.recorded_at))
        )
        
        result = await db.execute(query)
        
        summary = []
        for row in result:
            summary.append({
                "date": row.record_date,
                "avg_heart_rate": float(row.avg_heart_rate) if row.avg_heart_rate else None,
                "avg_blood_sugar": float(row.avg_blood_sugar) if row.avg_blood_sugar else None,
                "avg_weight": float(row.avg_weight) if row.avg_weight else None
            })
            
        return summary 