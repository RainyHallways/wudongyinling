from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional, Any
from datetime import datetime
import json

from ...core.database import get_async_db
from ...core.security import get_current_active_user
from ...core.chat import chat_manager
from ...schemas.chat import (
    ChatMessageCreate, ChatMessagePublic, 
    ChatRoomCreate, ChatRoomPublic,
    ChatRoomMemberCreate
)
from ...schemas.base import DataResponse, PaginatedResponse
from ...services.chat_service import ChatService
from ...models.user import User

router = APIRouter()

@router.get("/messages", response_model=PaginatedResponse[ChatMessagePublic])
async def get_messages(
    receiver_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    获取与指定用户的聊天记录
    """
    messages = await chat_service.get_conversation(
        db,
        user_id1=current_user.id,
        user_id2=receiver_id,
        skip=skip,
        limit=limit
    )
    
    # 标记消息为已读
    updated_count = await chat_service.mark_conversation_as_read(
        db,
        sender_id=receiver_id,
        receiver_id=current_user.id
    )
    
    # 获取总记录数
    total = await chat_service.message_repository.count_conversation(
        db,
        user_id1=current_user.id,
        user_id2=receiver_id
    )
    
    return PaginatedResponse(
        data=messages,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.post("/messages", response_model=DataResponse[ChatMessagePublic])
async def create_message(
    message: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    发送私聊消息
    """
    # 确保发送者ID正确
    message_data = message.model_dump()
    message_data["sender_id"] = current_user.id
    
    db_message = await chat_service.send_message(
        db,
        message_in=ChatMessageCreate(**message_data)
    )
    
    # 如果接收者在线，通过WebSocket发送消息
    receiver_id = message.receiver_id
    message_json = {
        "type": "new_message",
        "data": {
            "id": db_message.id,
            "sender_id": db_message.sender_id,
            "sender_name": current_user.username,  # 添加发送者名称
            "content": db_message.content,
            "message_type": db_message.message_type,
            "created_at": db_message.created_at.isoformat() if db_message.created_at else datetime.now().isoformat()
        }
    }
    
    await chat_manager.send_personal_message(json.dumps(message_json), receiver_id)
    
    return DataResponse(data=db_message, message="消息发送成功")

@router.get("/rooms", response_model=PaginatedResponse[Dict[str, Any]])
async def get_user_rooms(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    获取用户参与的聊天室
    """
    rooms_data = await chat_service.get_user_rooms(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    # 处理结果为可序列化的格式
    rooms = []
    for room, unread_count, last_message in rooms_data:
        room_dict = {
            "room": room,
            "unread_count": unread_count,
            "last_message": last_message
        }
        rooms.append(room_dict)
    
    # 获取总聊天室数
    total = await chat_service.member_repository.count_user_rooms(
        db,
        user_id=current_user.id
    )
    
    return PaginatedResponse(
        data=rooms,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.post("/rooms", response_model=DataResponse[ChatRoomPublic])
async def create_room(
    room: ChatRoomCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    创建群聊
    """
    # 确保创建者ID正确
    room_data = room.model_dump()
    room_data["creator_id"] = current_user.id
    
    # 如果成员列表中没有创建者，添加创建者
    if current_user.id not in room_data.get("member_ids", []):
        room_data["member_ids"] = room_data.get("member_ids", []) + [current_user.id]
    
    created_room = await chat_service.create_room(
        db,
        room_in=ChatRoomCreate(**room_data)
    )
    
    return DataResponse(data=created_room, message="聊天室创建成功")

@router.post("/direct-room/{user_id}", response_model=DataResponse[ChatRoomPublic])
async def create_direct_room(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    创建或获取私聊聊天室
    """
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能与自己创建私聊")
    
    direct_room = await chat_service.create_direct_room(
        db,
        user_id1=current_user.id,
        user_id2=user_id
    )
    
    return DataResponse(data=direct_room, message="私聊创建成功")

@router.get("/rooms/{room_id}/messages", response_model=PaginatedResponse[ChatMessagePublic])
async def get_room_messages(
    room_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    获取聊天室消息
    """
    # 检查用户是否是聊天室成员
    is_member = await chat_service.is_room_member(db, room_id=room_id, user_id=current_user.id)
    if not is_member:
        raise HTTPException(status_code=403, detail="不是聊天室成员")
    
    messages = await chat_service.get_room_messages(
        db,
        room_id=room_id,
        skip=skip,
        limit=limit
    )
    
    # 标记消息为已读
    # 这里应该实现一个将聊天室中发给当前用户的消息标记为已读的方法
    
    # 获取总消息数
    total = await chat_service.message_repository.count_room_messages(db, room_id=room_id)
    
    return PaginatedResponse(
        data=messages,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.post("/rooms/{room_id}/messages", response_model=DataResponse[ChatMessagePublic])
async def send_room_message(
    room_id: int,
    content: str,
    message_type: str = "text",
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    发送聊天室消息
    """
    try:
        message = await chat_service.send_room_message(
            db,
            room_id=room_id,
            sender_id=current_user.id,
            content=content,
            message_type=message_type
        )
        
        # 获取聊天室成员
        members = await chat_service.get_room_members(db, room_id=room_id)
        
        # 构建消息数据
        message_json = {
            "type": "room_message",
            "data": {
                "id": message.id,
                "room_id": room_id,
                "sender_id": message.sender_id,
                "sender_name": current_user.username,
                "content": message.content,
                "message_type": message.message_type,
                "created_at": message.created_at.isoformat() if message.created_at else datetime.now().isoformat()
            }
        }
        
        # 向聊天室所有成员发送消息
        for member in members:
            if member.user_id != current_user.id:  # 不向自己发送
                await chat_manager.send_personal_message(json.dumps(message_json), member.user_id)
        
        return DataResponse(data=message, message="消息发送成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/unread-count", response_model=DataResponse[Dict[str, int]])
async def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    获取未读消息数
    """
    unread_count = await chat_service.get_unread_count(db, user_id=current_user.id)
    return DataResponse(data={"unread_count": unread_count})

@router.get("/recent-contacts", response_model=DataResponse[List[Dict[str, Any]]])
async def get_recent_contacts(
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    获取最近联系人
    """
    contacts = await chat_service.get_recent_contacts(db, user_id=current_user.id, limit=limit)
    return DataResponse(data=contacts)

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends()
):
    """
    聊天WebSocket连接
    """
    await chat_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 判断消息类型
            if message_data.get("type") == "direct_message":
                # 私聊消息
                receiver_id = message_data.get("receiver_id")
                content = message_data.get("content")
                message_type = message_data.get("message_type", "text")
                
                # 保存消息到数据库
                db_message = await chat_service.send_direct_message(
                    db,
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    content=content,
                    message_type=message_type
                )
                
                # 发送给接收者
                response_data = {
                    "type": "new_message",
                    "data": {
                        "id": db_message.id,
                        "sender_id": db_message.sender_id,
                        "content": db_message.content,
                        "message_type": db_message.message_type,
                        "created_at": db_message.created_at.isoformat() if db_message.created_at else datetime.now().isoformat()
                    }
                }
                
                await chat_manager.send_personal_message(json.dumps(response_data), receiver_id)
                
            elif message_data.get("type") == "room_message":
                # 群聊消息
                room_id = message_data.get("room_id")
                content = message_data.get("content")
                message_type = message_data.get("message_type", "text")
                
                try:
                    # 保存消息到数据库
                    db_message = await chat_service.send_room_message(
                        db,
                        room_id=room_id,
                        sender_id=user_id,
                        content=content,
                        message_type=message_type
                    )
                    
                    # 获取聊天室成员
                    members = await chat_service.get_room_members(db, room_id=room_id)
                    
                    # 构建响应数据
                    response_data = {
                        "type": "room_message",
                        "data": {
                            "id": db_message.id,
                            "room_id": room_id,
                            "sender_id": db_message.sender_id,
                            "content": db_message.content,
                            "message_type": db_message.message_type,
                            "created_at": db_message.created_at.isoformat() if db_message.created_at else datetime.now().isoformat()
                        }
                    }
                    
                    # 向聊天室所有成员发送消息
                    for member in members:
                        if member.user_id != user_id:  # 不向自己发送
                            await chat_manager.send_personal_message(json.dumps(response_data), member.user_id)
                except ValueError as e:
                    # 发送错误消息给发送者
                    error_data = {
                        "type": "error",
                        "data": {
                            "message": str(e)
                        }
                    }
                    await websocket.send_json(error_data)
    
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)
    except Exception as e:
        chat_manager.disconnect(user_id) 