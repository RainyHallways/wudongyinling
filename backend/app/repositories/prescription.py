from typing import Optional, List, Dict, Any
from datetime import datetime, date
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import RepositoryBase
from ..models.prescription import Prescription, PrescriptionExercise
from ..schemas.prescription import PrescriptionCreate, PrescriptionUpdate, PrescriptionExerciseCreate, PrescriptionExerciseUpdate

class PrescriptionExerciseRepository(RepositoryBase[PrescriptionExercise, PrescriptionExerciseCreate, PrescriptionExerciseUpdate]):
    """
    处方训练项目数据访问层
    """
    
    def __init__(self):
        super().__init__(PrescriptionExercise)
    
    async def get_by_prescription_id(
        self, 
        db: AsyncSession, 
        *, 
        prescription_id: int
    ) -> List[PrescriptionExercise]:
        """
        获取处方的所有训练项目
        
        Args:
            db: 数据库会话
            prescription_id: 处方ID
            
        Returns:
            训练项目列表
        """
        query = (
            select(PrescriptionExercise)
            .where(PrescriptionExercise.prescription_id == prescription_id)
        )
        result = await db.execute(query)
        return result.scalars().all()

class PrescriptionRepository(RepositoryBase[Prescription, PrescriptionCreate, PrescriptionUpdate]):
    """
    处方数据访问层
    """
    
    def __init__(self):
        super().__init__(Prescription)
        self.exercise_repository = PrescriptionExerciseRepository()
    
    async def get_with_exercises(
        self, 
        db: AsyncSession, 
        *, 
        id: int
    ) -> Optional[Prescription]:
        """
        获取处方及其训练项目
        
        Args:
            db: 数据库会话
            id: 处方ID
            
        Returns:
            处方对象，如未找到返回None
        """
        query = (
            select(Prescription)
            .options(selectinload(Prescription.exercises))
            .where(Prescription.id == id)
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_user_id(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        skip: int = 0, 
        limit: int = 100,
        include_exercises: bool = False
    ) -> List[Prescription]:
        """
        获取用户的处方
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            include_exercises: 是否包含训练项目
            
        Returns:
            处方列表
        """
        query = (
            select(Prescription)
            .where(Prescription.user_id == user_id)
            .order_by(desc(Prescription.created_at))
            .offset(skip)
            .limit(limit)
        )
        
        if include_exercises:
            query = query.options(selectinload(Prescription.exercises))
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_status(
        self, 
        db: AsyncSession, 
        *, 
        status: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Prescription]:
        """
        获取指定状态的处方
        
        Args:
            db: 数据库会话
            status: 状态
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            处方列表
        """
        query = (
            select(Prescription)
            .where(Prescription.status == status)
            .order_by(desc(Prescription.created_at))
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
    ) -> List[Prescription]:
        """
        获取指定日期范围内的处方
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            处方列表
        """
        # 将日期转换为datetime
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        query = (
            select(Prescription)
            .where(
                and_(
                    Prescription.user_id == user_id,
                    or_(
                        and_(
                            Prescription.start_date >= start_datetime,
                            Prescription.start_date <= end_datetime
                        ),
                        and_(
                            Prescription.end_date >= start_datetime,
                            Prescription.end_date <= end_datetime
                        ),
                        and_(
                            Prescription.start_date <= start_datetime,
                            or_(
                                Prescription.end_date >= end_datetime,
                                Prescription.end_date == None
                            )
                        )
                    )
                )
            )
            .order_by(desc(Prescription.start_date))
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_disease_type(
        self, 
        db: AsyncSession, 
        *, 
        disease_type: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Prescription]:
        """
        获取指定疾病类型的处方
        
        Args:
            db: 数据库会话
            disease_type: 疾病类型
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            处方列表
        """
        query = (
            select(Prescription)
            .where(Prescription.disease_type == disease_type)
            .order_by(desc(Prescription.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create_with_exercises(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: PrescriptionCreate
    ) -> Prescription:
        """
        创建处方及其训练项目
        
        Args:
            db: 数据库会话
            obj_in: 处方创建数据
            
        Returns:
            创建的处方
        """
        # 提取训练项目数据
        exercises_data = obj_in.exercises
        obj_in_data = obj_in.model_dump(exclude={"exercises"})
        
        # 创建处方
        db_obj = Prescription(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        
        # 创建训练项目
        for exercise_data in exercises_data:
            exercise = PrescriptionExercise(**exercise_data.model_dump(), prescription_id=db_obj.id)
            db.add(exercise)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_summary_by_doctor(
        self, 
        db: AsyncSession, 
        *, 
        doctor_id: int
    ) -> Dict[str, Any]:
        """
        获取医生的处方摘要统计
        
        Args:
            db: 数据库会话
            doctor_id: 医生ID
            
        Returns:
            摘要统计
        """
        # 处方总数
        total_query = (
            select(func.count())
            .select_from(Prescription)
            .where(Prescription.doctor_id == doctor_id)
        )
        total_result = await db.execute(total_query)
        total = total_result.scalar()
        
        # 按状态统计
        status_query = (
            select(Prescription.status, func.count())
            .where(Prescription.doctor_id == doctor_id)
            .group_by(Prescription.status)
        )
        status_result = await db.execute(status_query)
        status_counts = {status: count for status, count in status_result.all()}
        
        # 按疾病类型统计
        disease_query = (
            select(Prescription.disease_type, func.count())
            .where(Prescription.doctor_id == doctor_id)
            .group_by(Prescription.disease_type)
        )
        disease_result = await db.execute(disease_query)
        disease_counts = {disease: count for disease, count in disease_result.all()}
        
        return {
            "total": total,
            "by_status": status_counts,
            "by_disease": disease_counts
        } 