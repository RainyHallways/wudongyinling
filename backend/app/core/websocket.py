from typing import Dict, List, Optional
import json
import logging
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储活跃的连接：{user_id: websocket}
        self.active_connections: Dict[int, WebSocket] = {}
        # 存储用户在线状态
        self.online_users: Dict[int, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int, user_info: dict):
        """建立连接"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.online_users[user_id] = {
            "user_id": user_id,
            "username": user_info.get("username"),
            "nickname": user_info.get("nickname"),
            "avatar": user_info.get("avatar"),
            "connected_at": datetime.now().isoformat()
        }
        
        # 通知其他用户该用户上线
        await self.broadcast_user_status(user_id, "online")
        logger.info(f"User {user_id} connected to WebSocket")
    
    async def disconnect(self, user_id: int):
        """断开连接"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.online_users:
            del self.online_users[user_id]
        
        # 通知其他用户该用户下线
        await self.broadcast_user_status(user_id, "offline")
        logger.info(f"User {user_id} disconnected from WebSocket")
    
    async def send_personal_message(self, message: dict, user_id: int):
        """发送个人消息"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message, ensure_ascii=False))
                return True
            except Exception as e:
                logger.error(f"Error sending message to user {user_id}: {e}")
                # 如果发送失败，移除连接
                await self.disconnect(user_id)
                return False
        return False
    
    async def send_room_message(self, message: dict, room_id: int, exclude_user: Optional[int] = None):
        """发送群聊消息到房间所有成员"""
        # 这里需要从数据库获取房间成员列表
        # 为了简化，先发送给所有在线用户（实际应用中需要查询房间成员）
        message_data = {
            "type": "room_message",
            "room_id": room_id,
            "data": message
        }
        
        failed_connections = []
        for user_id, websocket in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            try:
                await websocket.send_text(json.dumps(message_data, ensure_ascii=False))
            except Exception as e:
                logger.error(f"Error sending room message to user {user_id}: {e}")
                failed_connections.append(user_id)
        
        # 清理失败的连接
        for user_id in failed_connections:
            await self.disconnect(user_id)
    
    async def broadcast_user_status(self, user_id: int, status: str):
        """广播用户状态变化"""
        message = {
            "type": "user_status",
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        failed_connections = []
        for uid, websocket in self.active_connections.items():
            if uid == user_id:  # 不向自己发送状态变化消息
                continue
            try:
                await websocket.send_text(json.dumps(message, ensure_ascii=False))
            except Exception as e:
                logger.error(f"Error broadcasting user status to user {uid}: {e}")
                failed_connections.append(uid)
        
        # 清理失败的连接
        for uid in failed_connections:
            await self.disconnect(uid)
    
    async def get_online_users(self) -> List[dict]:
        """获取在线用户列表"""
        return list(self.online_users.values())
    
    def is_user_online(self, user_id: int) -> bool:
        """检查用户是否在线"""
        return user_id in self.active_connections

# 全局连接管理器实例
manager = ConnectionManager() 