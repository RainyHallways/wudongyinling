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

# 创建服务实例
def get_chat_service() -> ChatService:
    return ChatService()

router = APIRouter()

# ===================== 管理员聊天管理 =====================

@router.get("/admin/messages", response_model=PaginatedResponse[ChatMessagePublic])
async def get_all_messages_admin(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    sender_role: Optional[str] = Query(None, description="发送者角色"),
    receiver_role: Optional[str] = Query(None, description="接收者角色"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员获取所有私信消息列表
    """
    messages = await chat_service.get_all_messages_for_admin(
        db, skip, limit, sender_role, receiver_role, keyword, start_date, end_date
    )
    total = await chat_service.get_messages_count_for_admin(
        db, sender_role, receiver_role, keyword, start_date, end_date
    )
    
    return PaginatedResponse(
        data=messages,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.delete("/admin/messages/{message_id}", response_model=DataResponse)
async def delete_message_admin(
    message_id: int,
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员删除私信消息
    """
    success = await chat_service.delete_message_admin(db, message_id)
    if not success:
        raise HTTPException(status_code=404, detail="消息不存在")
    
    return DataResponse(message="消息删除成功")


@router.delete("/admin/messages/batch", response_model=DataResponse)
async def batch_delete_messages_admin(
    message_ids: List[int],
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员批量删除私信消息
    """
    deleted_count = await chat_service.batch_delete_messages_admin(db, message_ids)
    return DataResponse(message=f"成功删除 {deleted_count} 条消息")


@router.get("/admin/rooms", response_model=PaginatedResponse[ChatRoomPublic])
async def get_all_rooms_admin(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    room_type: Optional[str] = Query(None, description="群聊类型"),
    is_active: Optional[bool] = Query(None, description="是否活跃"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    min_members: Optional[int] = Query(None, description="最少成员数"),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员获取所有群聊房间列表
    """
    rooms = await chat_service.get_all_rooms_for_admin(
        db, skip, limit, room_type, is_active, keyword, min_members
    )
    total = await chat_service.get_rooms_count_for_admin(
        db, room_type, is_active, keyword, min_members
    )
    
    return PaginatedResponse(
        data=rooms,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.post("/admin/rooms", response_model=DataResponse[ChatRoomPublic])
async def create_room_admin(
    room_data: ChatRoomCreate,
    creator_id: int = Query(..., description="创建者ID"),  # 临时用query参数
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员创建群聊房间
    """
    room = await chat_service.create_room_admin(db, obj_in=room_data, creator_id=creator_id)
    return DataResponse(data=room, message="群聊创建成功")


@router.patch("/admin/rooms/{room_id}/status", response_model=DataResponse[ChatRoomPublic])
async def toggle_room_status_admin(
    room_id: int,
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员切换群聊房间状态
    """
    room = await chat_service.toggle_room_status_admin(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="群聊房间不存在")
    
    return DataResponse(
        data=room,
        message=f"群聊已{'启用' if room.is_active else '停用'}"
    )


@router.delete("/admin/rooms/{room_id}", response_model=DataResponse)
async def delete_room_admin(
    room_id: int,
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员删除群聊房间
    """
    success = await chat_service.delete_room_admin(db, room_id)
    if not success:
        raise HTTPException(status_code=404, detail="群聊房间不存在")
    
    return DataResponse(message="群聊删除成功")


@router.get("/admin/rooms/{room_id}/members", response_model=DataResponse[List[Any]])
async def get_room_members_admin(
    room_id: int,
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员获取群聊成员列表
    """
    members = await chat_service.get_room_members_admin(db, room_id)
    return DataResponse(data=members, message="获取成功")


@router.post("/admin/rooms/{room_id}/members", response_model=DataResponse)
async def add_room_member_admin(
    room_id: int,
    user_id: int = Query(..., description="用户ID"),
    role: str = Query("member", description="角色"),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员添加群聊成员
    """
    success = await chat_service.add_room_member_admin(db, room_id, user_id, role)
    if not success:
        raise HTTPException(status_code=400, detail="添加成员失败")
    
    return DataResponse(message="成员添加成功")


@router.patch("/admin/rooms/{room_id}/members/{user_id}/role", response_model=DataResponse)
async def update_member_role_admin(
    room_id: int,
    user_id: int,
    role: str = Query(..., description="新角色"),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员更新群聊成员角色
    """
    success = await chat_service.update_member_role_admin(db, room_id, user_id, role)
    if not success:
        raise HTTPException(status_code=404, detail="成员不存在")
    
    return DataResponse(message="角色更新成功")


@router.delete("/admin/rooms/{room_id}/members/{user_id}", response_model=DataResponse)
async def remove_room_member_admin(
    room_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    管理员移除群聊成员
    """
    success = await chat_service.remove_room_member_admin(db, room_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="成员不存在")
    
    return DataResponse(message="成员移除成功")


# ===================== 用户聊天功能 =====================

@router.get("/messages", response_model=PaginatedResponse[ChatMessagePublic])
async def get_messages(
    receiver_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db),
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
    chat_service: ChatService = Depends(get_chat_service)
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
