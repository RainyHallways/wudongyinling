from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from typing import Optional
import json
import logging
from datetime import datetime

from ...core.websocket import manager
from ...dependencies import get_current_user_websocket
from ...services.chat_service import ChatService
from ...schemas.user import UserPublic
from ...schemas.chat import ChatMessageCreate

logger = logging.getLogger(__name__)
router = APIRouter()

# 依赖注入
def get_chat_service() -> ChatService:
    return ChatService()

@router.websocket("/ws/{token}")
async def websocket_endpoint(
    websocket: WebSocket, 
    token: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """WebSocket连接端点"""
    try:
        # 验证token并获取用户信息
        user = await get_current_user_websocket(token)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # 建立连接
        user_info = {
            "username": user.username,
            "nickname": user.nickname,
            "avatar": getattr(user, 'avatar', None)
        }
        await manager.connect(websocket, user.id, user_info)
        
        # 发送在线用户列表
        online_users = await manager.get_online_users()
        await manager.send_personal_message({
            "type": "online_users",
            "data": online_users
        }, user.id)
        
        try:
            while True:
                # 接收客户端消息
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                await handle_websocket_message(message_data, user, chat_service)
                
        except WebSocketDisconnect:
            await manager.disconnect(user.id)
            logger.info(f"WebSocket connection closed for user {user.id}")
        except Exception as e:
            logger.error(f"WebSocket error for user {user.id}: {e}")
            await manager.disconnect(user.id)
            
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass

async def handle_websocket_message(message_data: dict, user: UserPublic, chat_service: ChatService):
    """处理WebSocket消息"""
    message_type = message_data.get("type")
    
    if message_type == "private_message":
        # 处理私聊消息
        await handle_private_message(message_data, user, chat_service)
    elif message_type == "room_message":
        # 处理群聊消息
        await handle_room_message(message_data, user, chat_service)
    elif message_type == "typing":
        # 处理正在输入状态
        await handle_typing_status(message_data, user)
    elif message_type == "read_message":
        # 处理消息已读状态
        await handle_read_message(message_data, user, chat_service)
    else:
        logger.warning(f"Unknown message type: {message_type}")

async def handle_private_message(message_data: dict, user: UserPublic, chat_service: ChatService):
    """处理私聊消息"""
    try:
        receiver_id = message_data.get("receiver_id")
        content = message_data.get("content")
        message_type = message_data.get("message_type", "text")
        
        if not receiver_id or not content:
            return
        
        # 保存消息到数据库
        message_create = ChatMessageCreate(
            receiver_id=receiver_id,
            content=content,
            message_type=message_type
        )
        
        saved_message = await chat_service.send_message(user.id, message_create)
        
        if saved_message:
            # 构造消息数据
            message_payload = {
                "type": "private_message",
                "data": {
                    "id": saved_message.id,
                    "sender_id": user.id,
                    "sender_username": user.username,
                    "sender_nickname": user.nickname,
                    "sender_avatar": getattr(user, 'avatar', None),
                    "receiver_id": receiver_id,
                    "content": content,
                    "message_type": message_type,
                    "created_at": saved_message.created_at.isoformat(),
                    "is_read": False
                }
            }
            
            # 发送给接收者
            sent = await manager.send_personal_message(message_payload, receiver_id)
            
            # 发送确认给发送者
            confirmation = {
                "type": "message_sent",
                "data": {
                    "message_id": saved_message.id,
                    "receiver_id": receiver_id,
                    "delivered": sent,
                    "timestamp": datetime.now().isoformat()
                }
            }
            await manager.send_personal_message(confirmation, user.id)
            
    except Exception as e:
        logger.error(f"Error handling private message: {e}")
        # 发送错误消息给发送者
        error_message = {
            "type": "error",
            "data": {
                "message": "消息发送失败",
                "error": str(e)
            }
        }
        await manager.send_personal_message(error_message, user.id)

async def handle_room_message(message_data: dict, user: UserPublic, chat_service: ChatService):
    """处理群聊消息"""
    try:
        room_id = message_data.get("room_id")
        content = message_data.get("content")
        message_type = message_data.get("message_type", "text")
        
        if not room_id or not content:
            return
        
        # 保存消息到数据库（需要实现room消息保存）
        # 这里简化处理，直接广播
        message_payload = {
            "type": "room_message",
            "data": {
                "room_id": room_id,
                "sender_id": user.id,
                "sender_username": user.username,
                "sender_nickname": user.nickname,
                "sender_avatar": getattr(user, 'avatar', None),
                "content": content,
                "message_type": message_type,
                "created_at": datetime.now().isoformat()
            }
        }
        
        # 广播给房间所有成员（除了发送者）
        await manager.send_room_message(message_payload, room_id, exclude_user=user.id)
        
    except Exception as e:
        logger.error(f"Error handling room message: {e}")

async def handle_typing_status(message_data: dict, user: UserPublic):
    """处理正在输入状态"""
    try:
        target_id = message_data.get("target_id")  # 私聊对象或群聊房间
        target_type = message_data.get("target_type", "user")  # "user" or "room"
        is_typing = message_data.get("is_typing", False)
        
        typing_message = {
            "type": "typing_status",
            "data": {
                "user_id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "target_id": target_id,
                "target_type": target_type,
                "is_typing": is_typing,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        if target_type == "user":
            # 发送给指定用户
            await manager.send_personal_message(typing_message, target_id)
        elif target_type == "room":
            # 发送给房间所有成员（除了发送者）
            await manager.send_room_message(typing_message, target_id, exclude_user=user.id)
            
    except Exception as e:
        logger.error(f"Error handling typing status: {e}")

async def handle_read_message(message_data: dict, user: UserPublic, chat_service: ChatService):
    """处理消息已读状态"""
    try:
        message_id = message_data.get("message_id")
        if not message_id:
            return
        
        # 更新消息已读状态
        await chat_service.mark_message_as_read(message_id, user.id)
        
        # 通知发送者消息已被读取（可选）
        # 这里需要获取消息详情来确定发送者
        # 简化处理，先跳过
        
    except Exception as e:
        logger.error(f"Error handling read message: {e}")

@router.get("/online-users")
async def get_online_users():
    """获取当前在线用户列表"""
    try:
        online_users = await manager.get_online_users()
        return {"online_users": online_users}
    except Exception as e:
        logger.error(f"Error getting online users: {e}")
        raise HTTPException(status_code=500, detail="获取在线用户失败") 