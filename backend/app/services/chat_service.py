from typing import List, Optional, Dict, Any, Union, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from .base_service import BaseService
from ..models.chat import ChatMessage, ChatRoom, ChatRoomMember
from ..repositories import (
    chat_message_repository, 
    chat_room_repository,
    chat_room_member_repository
)
from ..schemas.chat import (
    ChatMessageCreate, ChatMessageUpdate, 
    ChatRoomCreate, ChatRoomUpdate, 
    ChatRoomMemberCreate, ChatRoomMemberUpdate
)

class ChatService(BaseService):
    """
    聊天服务，处理聊天相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化聊天服务
        """
        self.message_repository = chat_message_repository
        self.room_repository = chat_room_repository
        self.member_repository = chat_room_member_repository
    
    async def get_conversation(
        self, 
        db: AsyncSession, 
        *, 
        user_id1: int, 
        user_id2: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[ChatMessage]:
        """
        获取两个用户之间的对话
        
        Args:
            db: 数据库会话
            user_id1: 用户1 ID
            user_id2: 用户2 ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            消息列表
        """
        return await self.message_repository.get_conversation(
            db, 
            user_id1=user_id1, 
            user_id2=user_id2, 
            skip=skip, 
            limit=limit
        )
    
    async def get_room_messages(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[ChatMessage]:
        """
        获取聊天室的消息
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            消息列表
        """
        return await self.message_repository.get_room_messages(
            db, 
            room_id=room_id, 
            skip=skip, 
            limit=limit
        )
    
    async def send_message(
        self, 
        db: AsyncSession, 
        *, 
        message_in: ChatMessageCreate
    ) -> ChatMessage:
        """
        发送消息
        
        Args:
            db: 数据库会话
            message_in: 消息创建数据
            
        Returns:
            创建的消息
        """
        return await self.message_repository.create(db, obj_in=message_in)
    
    async def send_direct_message(
        self, 
        db: AsyncSession, 
        *, 
        sender_id: int,
        receiver_id: int,
        content: str,
        message_type: str = "text"
    ) -> ChatMessage:
        """
        发送私聊消息
        
        Args:
            db: 数据库会话
            sender_id: 发送者ID
            receiver_id: 接收者ID
            content: 消息内容
            message_type: 消息类型
            
        Returns:
            创建的消息
        """
        message_data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content,
            "message_type": message_type
        }
        
        return await self.message_repository.create(
            db, 
            obj_in=ChatMessageCreate(**message_data)
        )
    
    async def send_room_message(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        sender_id: int,
        content: str,
        message_type: str = "text"
    ) -> ChatMessage:
        """
        发送群聊消息
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            sender_id: 发送者ID
            content: 消息内容
            message_type: 消息类型
            
        Returns:
            创建的消息
        """
        # 检查用户是否是聊天室成员
        is_member = await self.is_room_member(db, room_id=room_id, user_id=sender_id)
        if not is_member:
            raise ValueError("不是聊天室成员")
            
        # 获取聊天室，检查是否存在
        room = await self.room_repository.get(db, room_id)
        if not room:
            raise ValueError("聊天室不存在")
            
        # 创建消息
        message_data = {
            "sender_id": sender_id,
            "receiver_id": None,  # 群聊消息没有特定接收者
            "content": content,
            "message_type": message_type,
            "chat_room_id": room_id
        }
        
        return await self.message_repository.create(
            db, 
            obj_in=ChatMessageCreate(**message_data)
        )
    
    async def mark_as_read(
        self, 
        db: AsyncSession, 
        *, 
        message_ids: List[int],
        user_id: int
    ) -> int:
        """
        标记消息为已读
        
        Args:
            db: 数据库会话
            message_ids: 消息ID列表
            user_id: 接收者ID
            
        Returns:
            更新的消息数
        """
        return await self.message_repository.mark_as_read(
            db, 
            message_ids=message_ids, 
            user_id=user_id
        )
    
    async def mark_conversation_as_read(
        self, 
        db: AsyncSession, 
        *, 
        sender_id: int,
        receiver_id: int
    ) -> int:
        """
        标记整个对话为已读
        
        Args:
            db: 数据库会话
            sender_id: 发送者ID
            receiver_id: 接收者ID
            
        Returns:
            更新的消息数
        """
        return await self.message_repository.mark_conversation_as_read(
            db, 
            sender_id=sender_id, 
            receiver_id=receiver_id
        )
    
    async def get_unread_count(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int
    ) -> int:
        """
        获取用户未读消息数量
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            未读消息数量
        """
        return await self.message_repository.get_unread_count(db, user_id=user_id)
    
    async def get_recent_contacts(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        获取用户最近联系人
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            limit: 返回的最大记录数
            
        Returns:
            联系人列表
        """
        return await self.message_repository.get_recent_contacts(
            db, 
            user_id=user_id,
            limit=limit
        )
    
    async def create_room(
        self, 
        db: AsyncSession, 
        *, 
        room_in: ChatRoomCreate
    ) -> ChatRoom:
        """
        创建聊天室
        
        Args:
            db: 数据库会话
            room_in: 聊天室创建数据
            
        Returns:
            创建的聊天室
        """
        room = await self.room_repository.create(db, obj_in=room_in)
        
        # 添加成员
        creator_id = room_in.creator_id
        member_ids = room_in.member_ids
        
        # 添加创建者
        if creator_id not in member_ids:
            member_ids.append(creator_id)
        
        # 添加成员
        for user_id in member_ids:
            member_data = {
                "room_id": room.id,
                "user_id": user_id,
                "join_date": datetime.now(),
                "is_admin": user_id == creator_id
            }
            
            await self.member_repository.create(
                db, 
                obj_in=ChatRoomMemberCreate(**member_data)
            )
        
        return room
    
    async def create_direct_room(
        self, 
        db: AsyncSession, 
        *, 
        user_id1: int,
        user_id2: int
    ) -> ChatRoom:
        """
        创建私聊聊天室
        
        Args:
            db: 数据库会话
            user_id1: 用户1 ID
            user_id2: 用户2 ID
            
        Returns:
            创建的聊天室
        """
        return await self.room_repository.create_direct_room(
            db, 
            user_id1=user_id1, 
            user_id2=user_id2
        )
    
    async def get_user_rooms(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Tuple[ChatRoom, int, Optional[ChatMessage]]]:
        """
        获取用户参与的聊天室
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            (聊天室对象, 未读消息数, 最后一条消息)元组列表
        """
        return await self.room_repository.get_user_rooms(
            db, 
            user_id=user_id, 
            skip=skip, 
            limit=limit
        )
    
    async def add_room_member(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        user_id: int,
        is_admin: bool = False
    ) -> ChatRoomMember:
        """
        添加聊天室成员
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            user_id: 用户ID
            is_admin: 是否为管理员
            
        Returns:
            创建的成员记录
        """
        # 检查聊天室是否存在
        room = await self.room_repository.get(db, room_id)
        if not room:
            raise ValueError("聊天室不存在")
            
        # 检查用户是否已经是成员
        existing_member = await self.member_repository.get_by_user_and_room(
            db, 
            user_id=user_id, 
            room_id=room_id
        )
        
        if existing_member:
            raise ValueError("用户已经是聊天室成员")
            
        # 创建成员记录
        member_data = {
            "room_id": room_id,
            "user_id": user_id,
            "join_date": datetime.now(),
            "is_admin": is_admin
        }
        
        return await self.member_repository.create(
            db, 
            obj_in=ChatRoomMemberCreate(**member_data)
        )
    
    async def remove_room_member(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        user_id: int
    ) -> bool:
        """
        移除聊天室成员
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            user_id: 用户ID
            
        Returns:
            是否成功移除
        """
        return await self.member_repository.remove_member(
            db, 
            user_id=user_id, 
            room_id=room_id
        )
    
    async def get_room_members(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChatRoomMember]:
        """
        获取聊天室成员
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            成员列表
        """
        return await self.member_repository.get_members_by_room(
            db, 
            room_id=room_id, 
            skip=skip, 
            limit=limit
        )
    
    async def is_room_member(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        user_id: int
    ) -> bool:
        """
        判断用户是否是聊天室成员
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            user_id: 用户ID
            
        Returns:
            是否为成员
        """
        member = await self.member_repository.get_by_user_and_room(
            db, 
            user_id=user_id, 
            room_id=room_id
        )
        
        return member is not None
    
    async def is_room_admin(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        user_id: int
    ) -> bool:
        """
        判断用户是否是聊天室管理员
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            user_id: 用户ID
            
        Returns:
            是否为管理员
        """
        return await self.member_repository.is_admin(
            db, 
            user_id=user_id, 
            room_id=room_id
        )
    
    async def update_room(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        room_in: Union[ChatRoomUpdate, Dict[str, Any]]
    ) -> Optional[ChatRoom]:
        """
        更新聊天室
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            room_in: 更新数据
            
        Returns:
            更新后的聊天室，如未找到返回None
        """
        room = await self.room_repository.get(db, room_id)
        if not room:
            return None
            
        return await self.room_repository.update(db, db_obj=room, obj_in=room_in)
    
    async def delete_room(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int
    ) -> Optional[ChatRoom]:
        """
        删除聊天室
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            
        Returns:
            删除的聊天室，如未找到返回None
        """
        return await self.room_repository.delete(db, id=room_id)
    
    # ===================== 管理员功能 =====================
    
    async def get_all_messages_for_admin(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        sender_role: Optional[str] = None,
        receiver_role: Optional[str] = None,
        keyword: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[ChatMessage]:
        """
        管理员获取所有私信消息列表
        """
        return await self.message_repository.get_all_for_admin(
            db, skip, limit, sender_role, receiver_role, keyword, start_date, end_date
        )
    
    async def get_messages_count_for_admin(
        self,
        db: AsyncSession,
        sender_role: Optional[str] = None,
        receiver_role: Optional[str] = None,
        keyword: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> int:
        """
        管理员获取消息总数
        """
        return await self.message_repository.count_for_admin(
            db, sender_role, receiver_role, keyword, start_date, end_date
        )
    
    async def delete_message_admin(self, db: AsyncSession, message_id: int) -> bool:
        """
        管理员删除私信消息
        """
        message = await self.message_repository.get(db, message_id)
        if message:
            await self.message_repository.delete(db, id=message_id)
            return True
        return False
    
    async def batch_delete_messages_admin(self, db: AsyncSession, message_ids: List[int]) -> int:
        """
        管理员批量删除私信消息
        """
        return await self.message_repository.batch_delete(db, message_ids)
    
    async def get_all_rooms_for_admin(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        room_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        keyword: Optional[str] = None,
        min_members: Optional[int] = None
    ) -> List[ChatRoom]:
        """
        管理员获取所有群聊房间列表
        """
        return await self.room_repository.get_all_for_admin(
            db, skip, limit, room_type, is_active, keyword, min_members
        )
    
    async def get_rooms_count_for_admin(
        self,
        db: AsyncSession,
        room_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        keyword: Optional[str] = None,
        min_members: Optional[int] = None
    ) -> int:
        """
        管理员获取群聊房间总数
        """
        return await self.room_repository.count_for_admin(
            db, room_type, is_active, keyword, min_members
        )
    
    async def create_room_admin(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: ChatRoomCreate, 
        creator_id: int
    ) -> ChatRoom:
        """
        管理员创建群聊房间
        """
        room_data = obj_in.model_dump()
        room_data['creator_id'] = creator_id
        room = await self.room_repository.create(db, obj_in=room_data)
        
        # 将创建者加入群聊
        member_data = {
            'room_id': room.id,
            'user_id': creator_id,
            'role': 'admin'
        }
        await self.member_repository.create(db, obj_in=member_data)
        
        return room
    
    async def toggle_room_status_admin(self, db: AsyncSession, room_id: int) -> Optional[ChatRoom]:
        """
        管理员切换群聊房间状态
        """
        room = await self.room_repository.get(db, room_id)
        if room:
            room.is_active = not room.is_active
            await db.commit()
            await db.refresh(room)
        return room
    
    async def delete_room_admin(self, db: AsyncSession, room_id: int) -> bool:
        """
        管理员删除群聊房间
        """
        room = await self.room_repository.get(db, room_id)
        if room:
            await self.room_repository.delete(db, id=room_id)
            return True
        return False
    
    async def get_room_members_admin(self, db: AsyncSession, room_id: int) -> List[ChatRoomMember]:
        """
        管理员获取群聊成员列表
        """
        return await self.member_repository.get_room_members(db, room_id)
    
    async def add_room_member_admin(
        self, 
        db: AsyncSession, 
        room_id: int, 
        user_id: int, 
        role: str = "member"
    ) -> bool:
        """
        管理员添加群聊成员
        """
        try:
            member_data = {
                'room_id': room_id,
                'user_id': user_id,
                'role': role
            }
            await self.member_repository.create(db, obj_in=member_data)
            return True
        except:
            return False
    
    async def update_member_role_admin(
        self, 
        db: AsyncSession, 
        room_id: int, 
        user_id: int, 
        role: str
    ) -> bool:
        """
        管理员更新群聊成员角色
        """
        member = await self.member_repository.get_room_member(db, room_id, user_id)
        if member:
            member.role = role
            await db.commit()
            return True
        return False
    
    async def remove_room_member_admin(
        self, 
        db: AsyncSession, 
        room_id: int, 
        user_id: int
    ) -> bool:
        """
        管理员移除群聊成员
        """
        member = await self.member_repository.get_room_member(db, room_id, user_id)
        if member:
            await self.member_repository.delete(db, id=member.id)
            return True
        return False 