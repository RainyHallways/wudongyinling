from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional
from datetime import datetime, date

from ...core.database import get_async_db
from ...schemas.prescription import (
    PrescriptionCreate, PrescriptionUpdate, PrescriptionPublic,
    PrescriptionExerciseCreate, PrescriptionExerciseUpdate, PrescriptionExercisePublic
)
from ...schemas.base import DataResponse, PaginatedResponse
from ...services.prescription_service import PrescriptionService

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[PrescriptionPublic])
async def get_prescriptions(
    user_id: Optional[int] = None,
    disease_type: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 10,
    include_exercises: bool = False,
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    获取处方列表，支持按用户ID、疾病类型、状态筛选
    """
    if user_id:
        prescriptions = await prescription_service.get_user_prescriptions(
            db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            include_exercises=include_exercises
        )
        
        # 获取用户处方总数
        total = await prescription_service.repository.count(
            db,
            filters={"user_id": user_id}
        )
    elif disease_type:
        prescriptions = await prescription_service.get_by_disease_type(
            db,
            disease_type=disease_type,
            skip=skip,
            limit=limit
        )
        
        # 获取指定疾病类型的处方总数
        total = await prescription_service.repository.count(
            db,
            filters={"disease_type": disease_type}
        )
    elif status:
        prescriptions = await prescription_service.get_by_status(
            db,
            status=status,
            skip=skip,
            limit=limit
        )
        
        # 获取指定状态的处方总数
        total = await prescription_service.repository.count(
            db,
            filters={"status": status}
        )
    elif start_date and end_date and user_id:
        prescriptions = await prescription_service.get_by_date_range(
            db,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # 简单处理，直接返回查询结果的长度
        total = len(prescriptions)
    else:
        # 无特定筛选条件，获取所有处方
        prescriptions = await prescription_service.get_multi(db, skip=skip, limit=limit)
        total = await prescription_service.repository.count(db)
    
    return PaginatedResponse(
        data=prescriptions,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.post("/", response_model=DataResponse[PrescriptionPublic])
async def create_prescription(
    prescription: PrescriptionCreate, 
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    创建新处方
    """
    db_prescription = await prescription_service.create_with_exercises(db, obj_in=prescription)
    return DataResponse(data=db_prescription, message="处方创建成功")

@router.get("/{prescription_id}", response_model=DataResponse[PrescriptionPublic])
async def get_prescription(
    prescription_id: int, 
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    通过ID获取处方详情
    """
    prescription = await prescription_service.get_with_exercises(db, prescription_id=prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="处方不存在")
    
    return DataResponse(data=prescription)

@router.put("/{prescription_id}", response_model=DataResponse[PrescriptionPublic])
async def update_prescription(
    prescription_id: int,
    prescription_update: PrescriptionUpdate,
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    更新处方信息
    """
    db_prescription = await prescription_service.get(db, prescription_id)
    if not db_prescription:
        raise HTTPException(status_code=404, detail="处方不存在")
    
    updated_prescription = await prescription_service.update(
        db, 
        db_obj=db_prescription, 
        obj_in=prescription_update
    )
    
    return DataResponse(data=updated_prescription, message="处方更新成功")

@router.delete("/{prescription_id}", response_model=DataResponse)
async def delete_prescription(
    prescription_id: int, 
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    删除处方
    """
    db_prescription = await prescription_service.delete(db, id=prescription_id)
    if not db_prescription:
        raise HTTPException(status_code=404, detail="处方不存在")
    
    return DataResponse(message="处方已删除")

@router.patch("/{prescription_id}/status", response_model=DataResponse[PrescriptionPublic])
async def update_prescription_status(
    prescription_id: int,
    status: str = Query(..., description="处方状态: active, completed, cancelled"),
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    更新处方状态
    """
    if status not in ["active", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="无效的状态值")
    
    updated_prescription = await prescription_service.update_prescription_status(
        db,
        prescription_id=prescription_id,
        status=status
    )
    
    if not updated_prescription:
        raise HTTPException(status_code=404, detail="处方不存在")
    
    return DataResponse(data=updated_prescription, message=f"处方状态已更新为{status}")

@router.post("/{prescription_id}/exercises", response_model=DataResponse[PrescriptionExercisePublic])
async def add_prescription_exercise(
    prescription_id: int,
    exercise: PrescriptionExerciseCreate,
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    为处方添加训练项目
    """
    try:
        new_exercise = await prescription_service.add_exercise(
            db,
            prescription_id=prescription_id,
            exercise_in=exercise
        )
        
        return DataResponse(data=new_exercise, message="训练项目添加成功")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/exercises/{exercise_id}", response_model=DataResponse[PrescriptionExercisePublic])
async def update_prescription_exercise(
    exercise_id: int,
    exercise_update: PrescriptionExerciseUpdate,
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    更新处方训练项目
    """
    updated_exercise = await prescription_service.update_exercise(
        db,
        exercise_id=exercise_id,
        exercise_in=exercise_update
    )
    
    if not updated_exercise:
        raise HTTPException(status_code=404, detail="训练项目不存在")
    
    return DataResponse(data=updated_exercise, message="训练项目更新成功")

@router.delete("/exercises/{exercise_id}", response_model=DataResponse)
async def delete_prescription_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_async_db),
    prescription_service: PrescriptionService = Depends()
):
    """
    删除处方训练项目
    """
    deleted_exercise = await prescription_service.remove_exercise(db, exercise_id=exercise_id)
    
    if not deleted_exercise:
        raise HTTPException(status_code=404, detail="训练项目不存在")
    
    return DataResponse(message="训练项目删除成功") 