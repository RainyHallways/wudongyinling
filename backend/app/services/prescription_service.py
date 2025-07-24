from typing import List, Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

from .base_service import BaseService
from ..models.prescription import Prescription, PrescriptionExercise
from ..repositories import prescription_repository, prescription_exercise_repository
from ..schemas.prescription import (
    PrescriptionCreate, PrescriptionUpdate, 
    PrescriptionExerciseCreate, PrescriptionExerciseUpdate
)

class PrescriptionService(BaseService[Prescription, PrescriptionCreate, PrescriptionUpdate]):
    """
    处方服务，处理处方相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化处方服务
        """
        super().__init__(prescription_repository)
        self.exercise_repository = prescription_exercise_repository
    
    async def get_with_exercises(
        self, 
        db: AsyncSession, 
        *, 
        prescription_id: int
    ) -> Optional[Prescription]:
        """
        获取处方及其训练项目
        
        Args:
            db: 数据库会话
            prescription_id: 处方ID
            
        Returns:
            处方对象，如未找到返回None
        """
        return await self.repository.get_with_exercises(db, id=prescription_id)
    
    async def get_user_prescriptions(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        include_exercises: bool = False
    ) -> List[Prescription]:
        """
        获取用户处方
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            include_exercises: 是否包含训练项目
            
        Returns:
            处方列表
        """
        return await self.repository.get_by_user_id(
            db, 
            user_id=user_id, 
            skip=skip, 
            limit=limit,
            include_exercises=include_exercises
        )
    
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
        return await self.repository.get_by_status(db, status=status, skip=skip, limit=limit)
    
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
        return await self.repository.get_by_date_range(
            db, 
            user_id=user_id, 
            start_date=start_date, 
            end_date=end_date
        )
    
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
        return await self.repository.get_by_disease_type(
            db, 
            disease_type=disease_type, 
            skip=skip, 
            limit=limit
        )
    
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
        return await self.repository.create_with_exercises(db, obj_in=obj_in)
    
    async def add_exercise(
        self, 
        db: AsyncSession, 
        *, 
        prescription_id: int,
        exercise_in: PrescriptionExerciseCreate
    ) -> PrescriptionExercise:
        """
        为处方添加训练项目
        
        Args:
            db: 数据库会话
            prescription_id: 处方ID
            exercise_in: 训练项目创建数据
            
        Returns:
            创建的训练项目
        """
        # 检查处方是否存在
        prescription = await self.repository.get(db, prescription_id)
        if not prescription:
            raise ValueError("处方不存在")
            
        exercise_data = exercise_in.model_dump()
        exercise_data["prescription_id"] = prescription_id
        
        exercise = await self.exercise_repository.create(
            db, 
            obj_in=PrescriptionExerciseCreate(**exercise_data)
        )
        return exercise
    
    async def update_exercise(
        self, 
        db: AsyncSession, 
        *, 
        exercise_id: int,
        exercise_in: Union[PrescriptionExerciseUpdate, Dict[str, Any]]
    ) -> Optional[PrescriptionExercise]:
        """
        更新训练项目
        
        Args:
            db: 数据库会话
            exercise_id: 训练项目ID
            exercise_in: 更新数据
            
        Returns:
            更新后的训练项目，如未找到返回None
        """
        exercise = await self.exercise_repository.get(db, exercise_id)
        if not exercise:
            return None
            
        return await self.exercise_repository.update(db, db_obj=exercise, obj_in=exercise_in)
    
    async def remove_exercise(
        self, 
        db: AsyncSession, 
        *, 
        exercise_id: int
    ) -> Optional[PrescriptionExercise]:
        """
        删除训练项目
        
        Args:
            db: 数据库会话
            exercise_id: 训练项目ID
            
        Returns:
            删除的训练项目，如未找到返回None
        """
        return await self.exercise_repository.delete(db, id=exercise_id)
    
    async def update_prescription_status(
        self, 
        db: AsyncSession, 
        *, 
        prescription_id: int,
        status: str
    ) -> Optional[Prescription]:
        """
        更新处方状态
        
        Args:
            db: 数据库会话
            prescription_id: 处方ID
            status: 新状态
            
        Returns:
            更新后的处方，如未找到返回None
        """
        prescription = await self.repository.get(db, prescription_id)
        if not prescription:
            return None
            
        # 验证状态值
        if status not in ["active", "completed", "cancelled"]:
            raise ValueError("无效的状态值")
            
        update_data = {"status": status}
        
        # 如果是完成状态，设置结束日期为当前日期
        if status == "completed" and not prescription.end_date:
            update_data["end_date"] = datetime.now().date()
            
        return await self.repository.update(db, db_obj=prescription, obj_in=update_data)
    
    async def get_doctor_summary(
        self, 
        db: AsyncSession, 
        *, 
        doctor_id: int
    ) -> Dict[str, Any]:
        """
        获取医生处方摘要统计
        
        Args:
            db: 数据库会话
            doctor_id: 医生ID
            
        Returns:
            摘要统计
        """
        return await self.repository.get_summary_by_doctor(db, doctor_id=doctor_id)
    
    def generate_schedule_template(self, disease_type: str) -> Dict[str, Any]:
        """
        根据疾病类型生成训练计划日程模板
        
        Args:
            disease_type: 疾病类型
            
        Returns:
            日程模板
        """
        # 不同疾病类型的基本日程模板
        templates = {
            "腰椎间盘突出": {
                "monday": ["腰部放松", "核心力量训练"],
                "tuesday": ["有氧运动", "拉伸"],
                "wednesday": ["腰部肌肉训练", "平衡训练"],
                "thursday": ["休息日"],
                "friday": ["有氧运动", "腰部放松"],
                "saturday": ["核心力量训练", "拉伸"],
                "sunday": ["休息日"]
            },
            "膝关节炎": {
                "monday": ["水中运动", "关节活动度训练"],
                "tuesday": ["肌肉力量训练", "拉伸"],
                "wednesday": ["有氧运动", "平衡训练"],
                "thursday": ["休息日"],
                "friday": ["肌肉力量训练", "拉伸"],
                "saturday": ["有氧运动", "关节活动度训练"],
                "sunday": ["休息日"]
            },
            "肩周炎": {
                "monday": ["肩部活动度训练", "肩部肌肉力量训练"],
                "tuesday": ["有氧运动", "拉伸"],
                "wednesday": ["肩部活动度训练", "上肢力量训练"],
                "thursday": ["休息日"],
                "friday": ["有氧运动", "肩部肌肉力量训练"],
                "saturday": ["肩部活动度训练", "拉伸"],
                "sunday": ["休息日"]
            },
            "颈椎病": {
                "monday": ["颈部肌肉放松", "颈部肌肉力量训练"],
                "tuesday": ["有氧运动", "拉伸"],
                "wednesday": ["颈部活动度训练", "上肢力量训练"],
                "thursday": ["休息日"],
                "friday": ["有氧运动", "颈部肌肉放松"],
                "saturday": ["颈部肌肉力量训练", "拉伸"],
                "sunday": ["休息日"]
            },
            "运动损伤": {
                "monday": ["关节活动度训练", "力量训练"],
                "tuesday": ["有氧运动", "拉伸"],
                "wednesday": ["力量训练", "平衡训练"],
                "thursday": ["休息日"],
                "friday": ["有氧运动", "关节活动度训练"],
                "saturday": ["力量训练", "拉伸"],
                "sunday": ["休息日"]
            }
        }
        
        # 返回指定疾病类型的模板，如果没有对应模板则返回通用模板
        return templates.get(disease_type, {
            "monday": ["有氧运动", "力量训练"],
            "tuesday": ["拉伸", "平衡训练"],
            "wednesday": ["有氧运动", "肌肉训练"],
            "thursday": ["休息日"],
            "friday": ["有氧运动", "力量训练"],
            "saturday": ["拉伸", "平衡训练"],
            "sunday": ["休息日"]
        }) 