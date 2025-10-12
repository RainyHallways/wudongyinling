from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, WebSocket
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional

from ...core.database import get_async_db
from ...core.security import get_current_active_user
from ...schemas.base import DataResponse
from ...services.ai_service import AIService
from ...models.user import User

router = APIRouter()

@router.post("/analyze", response_model=DataResponse[Dict[str, Any]])
async def analyze_dance(
    video: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends()
):
    """
    分析用户上传的舞蹈视频
    """
    try:
        contents = await video.read()
        result = await ai_service.analyze_dance_video(contents)
        return DataResponse(data=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/feedback/{video_id}", response_model=DataResponse[Dict[str, Any]])
async def get_feedback(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    ai_service: AIService = Depends()
):
    """
    获取特定视频的AI反馈
    """
    try:
        result = await ai_service.get_dance_feedback(db, video_id=video_id)
        return DataResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/compare", response_model=DataResponse[Dict[str, Any]])
async def compare_videos(
    user_video: UploadFile = File(...),
    standard_video_id: Optional[int] = None,
    standard_video: Optional[UploadFile] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    ai_service: AIService = Depends()
):
    """
    将用户视频与标准动作视频进行对比
    """
    if not standard_video_id and not standard_video:
        raise HTTPException(status_code=400, detail="必须提供标准视频ID或上传标准视频")
    
    try:
        user_contents = await user_video.read()
        
        if standard_video:
            standard_contents = await standard_video.read()
            result = await ai_service.compare_with_standard_video(
                user_contents,
                standard_contents
            )
        else:
            result = await ai_service.compare_with_standard_by_id(
                db,
                user_contents,
                standard_video_id
            )
        
        return DataResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/health-analysis/{user_id}", response_model=DataResponse[Dict[str, Any]])
async def analyze_health_data(
    user_id: int,
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    ai_service: AIService = Depends()
):
    """
    分析用户健康数据
    """
    # 检查权限（只能查看自己的数据或管理员可以查看所有人）
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    result = await ai_service.analyze_health_data(db, user_id=user_id, days=days)
    return DataResponse(data=result)

@router.post("/generate-prescription", response_model=DataResponse[Dict[str, Any]])
async def generate_prescription(
    user_id: int,
    disease_type: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    ai_service: AIService = Depends()
):
    """
    基于用户健康数据生成训练处方
    """
    # 检查权限（只能为自己生成处方或管理员可以为所有人生成）
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    result = await ai_service.generate_prescription(
        db, 
        user_id=user_id,
        disease_type=disease_type
    )
    
    return DataResponse(data=result)

@router.post("/coach-advice", response_model=DataResponse[Dict[str, Any]])
async def get_ai_coach_advice(
    question: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    ai_service: AIService = Depends()
):
    """
    获取AI教练建议
    """
    result = await ai_service.get_ai_coach_advice(
        db, 
        user_id=current_user.id,
        question=question
    )
    
    return DataResponse(data=result)

@router.websocket("/realtime-analysis")
async def realtime_analysis(
    websocket: WebSocket,
    ai_service: AIService = Depends()
):
    """
    实时分析摄像头输入
    """
    await websocket.accept()
    try:
        while True:
            # 接收视频帧数据
            frame_data = await websocket.receive_bytes()
            
            # 进行AI分析
            result = await ai_service.analyze_dance_frame(frame_data)
            
            # 发送分析结果
            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.close()

# AI分析历史记录接口
@router.get("/analysis-history", response_model=DataResponse[Dict[str, Any]])
async def get_analysis_history(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    ai_service: AIService = Depends(),
    skip: int = 0,
    limit: int = 20
):
    """
    获取用户的AI分析历史记录
    """
    history = await ai_service.get_analysis_history(
        db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit
    )
    
    return DataResponse(data=history)

@router.get("/analysis/{analysis_id}", response_model=DataResponse[Dict[str, Any]])
async def get_analysis_details(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    ai_service: AIService = Depends()
):
    """
    获取特定分析记录的详细信息
    """
    # 检查权限（只能查看自己的记录或管理员可以查看所有人）
    analysis = await ai_service.get_analysis_by_id(db, analysis_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="分析记录不存在")
    
    if analysis.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return DataResponse(data=analysis) 