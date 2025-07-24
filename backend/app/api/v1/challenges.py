from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from ...core.database import get_async_db
from ...schemas.challenge import (
    ChallengeCreate, ChallengeUpdate, ChallengePublic,
    ChallengeRecordCreate, ChallengeRecordPublic
)
from ...schemas.base import DataResponse, PaginatedResponse
from ...services.challenge_service import ChallengeService

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[ChallengePublic])
async def get_challenges(
    active_only: bool = False,
    upcoming: bool = False,
    creator_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    获取挑战列表，支持筛选活跃、即将开始或由特定用户创建的挑战
    """
    if active_only:
        challenges = await challenge_service.get_active_challenges(db, skip=skip, limit=limit)
    elif upcoming:
        challenges = await challenge_service.get_upcoming_challenges(db, skip=skip, limit=limit)
    elif creator_id:
        challenges = await challenge_service.get_by_creator(db, creator_id=creator_id, skip=skip, limit=limit)
    else:
        challenges = await challenge_service.get_multi(db, skip=skip, limit=limit)
    
    # 获取总挑战数
    total = len(challenges)  # 简化处理，直接使用结果长度
    
    return PaginatedResponse(
        data=challenges,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.post("/", response_model=DataResponse[ChallengePublic])
async def create_challenge(
    challenge: ChallengeCreate, 
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    创建新挑战
    """
    db_challenge = await challenge_service.create(db, obj_in=challenge)
    return DataResponse(data=db_challenge, message="挑战创建成功")

@router.get("/{challenge_id}", response_model=DataResponse[Dict[str, Any]])
async def get_challenge(
    challenge_id: int, 
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    通过ID获取挑战详情及参与人数
    """
    result = await challenge_service.get_challenge_with_participant_count(db, challenge_id=challenge_id)
    if not result or not result[0]:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    challenge, participant_count = result
    
    return DataResponse(
        data={
            "challenge": challenge,
            "participant_count": participant_count
        }
    )

@router.put("/{challenge_id}", response_model=DataResponse[ChallengePublic])
async def update_challenge(
    challenge_id: int,
    challenge_update: ChallengeUpdate,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    更新挑战信息
    """
    db_challenge = await challenge_service.get(db, challenge_id)
    if not db_challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    updated_challenge = await challenge_service.update(
        db, 
        db_obj=db_challenge, 
        obj_in=challenge_update
    )
    
    return DataResponse(data=updated_challenge, message="挑战更新成功")

@router.delete("/{challenge_id}", response_model=DataResponse)
async def delete_challenge(
    challenge_id: int, 
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    删除挑战
    """
    db_challenge = await challenge_service.delete(db, id=challenge_id)
    if not db_challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    return DataResponse(message="挑战已删除")

@router.post("/{challenge_id}/join", response_model=DataResponse)
async def join_challenge(
    challenge_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    用户加入挑战
    """
    try:
        await challenge_service.join_challenge(
            db, 
            challenge_id=challenge_id, 
            user_id=user_id
        )
        return DataResponse(message="成功加入挑战")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{challenge_id}/quit", response_model=DataResponse)
async def quit_challenge(
    challenge_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    用户退出挑战
    """
    success = await challenge_service.quit_challenge(
        db, 
        challenge_id=challenge_id, 
        user_id=user_id
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="未参与该挑战")
    
    return DataResponse(message="成功退出挑战")

@router.post("/{challenge_id}/check-in", response_model=DataResponse[ChallengeRecordPublic])
async def check_in(
    challenge_id: int,
    user_id: int,
    record: Optional[ChallengeRecordCreate] = None,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    挑战打卡
    """
    try:
        if not record:
            # 如果没有提供记录数据，创建一个默认的
            record = ChallengeRecordCreate(
                user_id=user_id,
                challenge_id=challenge_id,
                completed=True
            )
        
        challenge_record = await challenge_service.check_in(
            db, 
            challenge_id=challenge_id, 
            user_id=user_id,
            record_in=record
        )
        
        return DataResponse(data=challenge_record, message="打卡成功")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{challenge_id}/records", response_model=PaginatedResponse[ChallengeRecordPublic])
async def get_challenge_records(
    challenge_id: int,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    获取挑战打卡记录
    """
    if user_id:
        records = await challenge_service.get_user_challenge_records(
            db, 
            challenge_id=challenge_id, 
            user_id=user_id,
            skip=skip,
            limit=limit
        )
    else:
        # 这里可能需要在ChallengeService中添加获取所有挑战记录的方法
        # 简单起见，这里直接从record_repository获取
        records = await challenge_service.record_repository.get_by_challenge_id(
            db, 
            challenge_id=challenge_id,
            skip=skip,
            limit=limit
        )
    
    # 获取记录总数
    if user_id:
        filters = {"challenge_id": challenge_id, "user_id": user_id}
    else:
        filters = {"challenge_id": challenge_id}
    
    total = await challenge_service.record_repository.count(db, filters=filters)
    
    return PaginatedResponse(
        data=records,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.get("/{challenge_id}/progress/{user_id}", response_model=DataResponse[Dict[str, Any]])
async def get_challenge_progress(
    challenge_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    获取用户在挑战中的进度
    """
    progress = await challenge_service.get_challenge_progress(
        db, 
        challenge_id=challenge_id, 
        user_id=user_id
    )
    
    return DataResponse(data=progress)

@router.get("/{challenge_id}/leaderboard", response_model=DataResponse[List[Dict[str, Any]]])
async def get_challenge_leaderboard(
    challenge_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    获取挑战排行榜
    """
    leaderboard = await challenge_service.get_leaderboard(
        db, 
        challenge_id=challenge_id,
        limit=limit
    )
    
    return DataResponse(data=leaderboard)

@router.get("/popular", response_model=DataResponse[List[Dict[str, Any]]])
async def get_popular_challenges(
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    获取最受欢迎的挑战
    """
    popular_challenges = await challenge_service.get_popular_challenges(db, limit=limit)
    
    result = []
    for challenge, count in popular_challenges:
        result.append({
            "challenge": challenge,
            "participant_count": count
        })
    
    return DataResponse(data=result)

@router.get("/user/{user_id}", response_model=PaginatedResponse[ChallengePublic])
async def get_user_challenges(
    user_id: int,
    include_inactive: bool = False,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_db),
    challenge_service: ChallengeService = Depends()
):
    """
    获取用户参与的挑战
    """
    challenges = await challenge_service.get_user_challenges(
        db, 
        user_id=user_id, 
        skip=skip, 
        limit=limit, 
        include_inactive=include_inactive
    )
    
    # 简化处理，直接使用结果长度
    total = len(challenges)
    
    return PaginatedResponse(
        data=challenges,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )