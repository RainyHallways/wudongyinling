from typing import List, Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date, timedelta

from .base_service import BaseService
from ..models.health import HealthRecord
from ..repositories import health_repository
from ..schemas.health import HealthRecordCreate, HealthRecordUpdate, HealthStatistics

class HealthService(BaseService[HealthRecord, HealthRecordCreate, HealthRecordUpdate]):
    """
    健康服务，处理健康记录相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化健康服务
        """
        super().__init__(health_repository)
    
    async def get_user_records(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[HealthRecord]:
        """
        获取用户健康记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            健康记录列表
        """
        return await self.repository.get_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    
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
        return await self.repository.get_by_date_range(db, user_id=user_id, start_date=start_date, end_date=end_date)
    
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
            最新健康记录，如未找到返回None
        """
        return await self.repository.get_latest_record(db, user_id=user_id)
    
    async def create_record(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: HealthRecordCreate
    ) -> HealthRecord:
        """
        创建健康记录
        
        Args:
            db: 数据库会话
            obj_in: 健康记录创建数据
            
        Returns:
            创建的健康记录
        """
        # 如果没有记录时间，设置为当前时间
        if not obj_in.recorded_at:
            record_data = obj_in.model_dump()
            record_data["recorded_at"] = datetime.now()
            obj_in = HealthRecordCreate(**record_data)
            
        # 如果提供了身高和体重，但没有BMI，则计算BMI
        if obj_in.height and obj_in.weight and not obj_in.bmi:
            height_m = obj_in.height / 100  # 转换为米
            bmi = obj_in.weight / (height_m * height_m)
            record_data = obj_in.model_dump()
            record_data["bmi"] = round(bmi, 2)
            obj_in = HealthRecordCreate(**record_data)
            
        return await super().create(db, obj_in=obj_in)
    
    async def update_record(
        self, 
        db: AsyncSession, 
        *, 
        record_id: int,
        obj_in: Union[HealthRecordUpdate, Dict[str, Any]]
    ) -> Optional[HealthRecord]:
        """
        更新健康记录
        
        Args:
            db: 数据库会话
            record_id: 记录ID
            obj_in: 更新数据
            
        Returns:
            更新后的健康记录，如未找到返回None
        """
        record = await self.repository.get(db, record_id)
        if not record:
            return None
            
        # 如果提供了身高和体重，重新计算BMI
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        
        height = update_data.get('height') or record.height
        weight = update_data.get('weight') or record.weight
        
        if height and weight:
            height_m = height / 100  # 转换为米
            bmi = weight / (height_m * height_m)
            update_data['bmi'] = round(bmi, 2)
            
        return await self.repository.update(db, db_obj=record, obj_in=update_data)
    
    async def get_statistics(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        days: int = 30
    ) -> HealthStatistics:
        """
        获取健康统计数据
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            days: 统计天数
            
        Returns:
            健康统计数据
        """
        stats_data = await self.repository.get_statistics(db, user_id=user_id, days=days)
        return HealthStatistics(**stats_data)
    
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
            月度健康记录摘要
        """
        return await self.repository.get_monthly_summary(db, user_id=user_id, year=year, month=month)
    
    def analyze_health_trend(self, records: List[HealthRecord]) -> Dict[str, Any]:
        """
        分析健康趋势
        
        Args:
            records: 健康记录列表
            
        Returns:
            健康趋势分析结果
        """
        if not records or len(records) < 2:
            return {
                "trend": "insufficient_data",
                "message": "数据不足，无法分析趋势"
            }
            
        # 按记录时间排序
        sorted_records = sorted(records, key=lambda r: r.recorded_at)
        
        # 分析体重趋势
        weights = [r.weight for r in sorted_records if r.weight]
        weight_trend = self._analyze_trend(weights) if weights and len(weights) >= 2 else None
        
        # 分析BMI趋势
        bmis = [r.bmi for r in sorted_records if r.bmi]
        bmi_trend = self._analyze_trend(bmis) if bmis and len(bmis) >= 2 else None
        
        # 分析心率趋势
        heart_rates = [r.heart_rate for r in sorted_records if r.heart_rate]
        heart_rate_trend = self._analyze_trend(heart_rates) if heart_rates and len(heart_rates) >= 2 else None
        
        # 分析血糖趋势
        blood_sugars = [r.blood_sugar for r in sorted_records if r.blood_sugar]
        blood_sugar_trend = self._analyze_trend(blood_sugars) if blood_sugars and len(blood_sugars) >= 2 else None
        
        return {
            "weight_trend": weight_trend,
            "bmi_trend": bmi_trend,
            "heart_rate_trend": heart_rate_trend,
            "blood_sugar_trend": blood_sugar_trend,
            "analysis_date": datetime.now().isoformat(),
            "data_points": len(sorted_records)
        }
    
    def _analyze_trend(self, values: List[float]) -> Dict[str, Any]:
        """
        分析数值趋势
        
        Args:
            values: 数值列表
            
        Returns:
            趋势分析结果
        """
        if not values or len(values) < 2:
            return {
                "trend": "insufficient_data",
                "change": 0,
                "change_percent": 0
            }
            
        first = values[0]
        last = values[-1]
        change = last - first
        change_percent = (change / first) * 100 if first != 0 else 0
        
        if abs(change_percent) < 1:
            trend = "stable"
        elif change_percent > 0:
            trend = "increasing"
        else:
            trend = "decreasing"
            
        return {
            "trend": trend,
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "first_value": first,
            "last_value": last
        }

    async def get_user_activity_stats(
        self,
        db: AsyncSession,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        获取用户健康活动统计
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            用户健康活动统计信息
        """
        # 获取指定时间范围内的健康记录
        if start_date and end_date:
            records = await self.get_by_date_range(db, user_id=user_id, start_date=start_date, end_date=end_date)
        else:
            # 默认获取最近30天的记录
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
            records = await self.get_by_date_range(db, user_id=user_id, start_date=start_date, end_date=end_date)
        
        # 统计各类健康记录数量
        total_records = len(records)
        records_with_exercise = len([r for r in records if r.exercise_duration and r.exercise_duration > 0])
        records_with_weight = len([r for r in records if r.weight])
        records_with_heart_rate = len([r for r in records if r.heart_rate])
        records_with_blood_pressure = len([r for r in records if r.systolic_pressure and r.diastolic_pressure])
        
        # 计算平均值
        avg_weight = sum([r.weight for r in records if r.weight]) / records_with_weight if records_with_weight > 0 else 0
        avg_heart_rate = sum([r.heart_rate for r in records if r.heart_rate]) / records_with_heart_rate if records_with_heart_rate > 0 else 0
        avg_exercise_duration = sum([r.exercise_duration for r in records if r.exercise_duration]) / records_with_exercise if records_with_exercise > 0 else 0
        
        return {
            "totalRecords": total_records,
            "exerciseRecords": records_with_exercise,
            "weightRecords": records_with_weight,
            "heartRateRecords": records_with_heart_rate,
            "bloodPressureRecords": records_with_blood_pressure,
            "averageWeight": round(avg_weight, 1),
            "averageHeartRate": round(avg_heart_rate, 1),
            "averageExerciseDuration": round(avg_exercise_duration, 1),
            "period": {
                "startDate": start_date.isoformat() if start_date else None,
                "endDate": end_date.isoformat() if end_date else None
            }
        } 