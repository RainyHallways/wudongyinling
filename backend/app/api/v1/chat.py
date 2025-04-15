from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Dict
from ...core.database import get_db
from ...models.chat import ChatMessage
from ...core.chat import chat_manager
from ...core.security import get_current_active_user
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter()

class MessageBase(BaseModel):
    content: str
    message_type: str = 'text'

class MessageCreate(MessageBase):
    receiver_id: int

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    is_read: int
    created_at: datetime
    class Config:
        from_attributes = True

@router.get("/messages", response_model=List[MessageResponse])
async def get_messages(
    other_user_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取与特定用户的聊天记录
    messages = db.query(ChatMessage).filter(
        ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == other_user_id)) |
        ((ChatMessage.sender_id == other_user_id) & (ChatMessage.receiver_id == current_user.id))
    ).order_by(ChatMessage.created_at.desc()).offset(skip).limit(limit).all()
    
    # 标记消息为已读
    for msg in messages:
        if msg.receiver_id == current_user.id and not msg.is_read:
            msg.is_read = 1
    db.commit()
    
    return messages

@router.post("/messages", response_model=MessageResponse)
async def create_message(
    message: MessageCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_message = ChatMessage(
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        content=message.content,
        message_type=message.message_type
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # 如果接收者在线，发送WebSocket消息
    await chat_manager.send_personal_message(
        json.dumps({
            "type": "new_message",
            "data": {
                "id": db_message.id,
                "sender_id": db_message.sender_id,
                "content": db_message.content,
                "message_type": db_message.message_type,
                "created_at": db_message.created_at.isoformat()
            }
        }),
        message.receiver_id
    )
    
    return db_message

@router.get("/unread_count")
async def get_unread_count(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    count = db.query(ChatMessage).filter(
        ChatMessage.receiver_id == current_user.id,
        ChatMessage.is_read == 0
    ).count()
    return {"unread_count": count}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db)
):
    await chat_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 创建新消息
            db_message = ChatMessage(
                sender_id=user_id,
                receiver_id=message_data["receiver_id"],
                content=message_data["content"],
                message_type=message_data.get("message_type", "text")
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            
            # 发送给接收者
            await chat_manager.send_personal_message(
                json.dumps({
                    "type": "new_message",
                    "data": {
                        "id": db_message.id,
                        "sender_id": db_message.sender_id,
                        "content": db_message.content,
                        "message_type": db_message.message_type,
                        "created_at": db_message.created_at.isoformat()
                    }
                }),
                message_data["receiver_id"]
            )
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)
    except Exception as e:
        chat_manager.disconnect(user_id)
        raise e 