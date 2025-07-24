from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy import select, func, and_, or_, desc, asc, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import RepositoryBase
from ..models.chat import ChatMessage, ChatRoom, ChatRoomMember
from ..schemas.chat import (
    ChatMessageCreate, ChatMessageUpdate, 
    ChatRoomCreate, ChatRoomUpdate,
    ChatRoomMemberCreate, ChatRoomMemberUpdate
)

class ChatMessageRepository(RepositoryBase[ChatMessage, ChatMessageCreate, ChatMessageUpdate]):
    """
    聊天消息数据访问层
    """
    
    def __init__(self):
        super().__init__(ChatMessage)
    
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
        query = (
            select(ChatMessage)
            .where(
                or_(
                    and_(
                        ChatMessage.sender_id == user_id1,
                        ChatMessage.receiver_id == user_id2
                    ),
                    and_(
                        ChatMessage.sender_id == user_id2,
                        ChatMessage.receiver_id == user_id1
                    )
                )
            )
            .order_by(desc(ChatMessage.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
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
        query = (
            select(ChatMessage)
            .where(ChatMessage.chat_room_id == room_id)
            .order_by(desc(ChatMessage.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        messages = result.scalars().all()
        # 反转列表以使消息按时间顺序排列
        messages.reverse()
        return messages
    
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
        query = (
            select(func.count())
            .select_from(ChatMessage)
            .where(
                and_(
                    ChatMessage.receiver_id == user_id,
                    ChatMessage.is_read == False
                )
            )
        )
        result = await db.execute(query)
        return result.scalar()
    
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
        now = datetime.now()
        update_data = {
            "is_read": True,
            "read_at": now
        }
        
        return await self.bulk_update(
            db,
            ids=message_ids,
            obj_in=update_data
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
        # 找出所有未读消息ID
        query = (
            select(ChatMessage.id)
            .where(
                and_(
                    ChatMessage.sender_id == sender_id,
                    ChatMessage.receiver_id == receiver_id,
                    ChatMessage.is_read == False
                )
            )
        )
        result = await db.execute(query)
        message_ids = [row[0] for row in result.all()]
        
        if not message_ids:
            return 0
            
        return await self.mark_as_read(db, message_ids=message_ids, user_id=receiver_id)
    
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
        # 使用原生SQL以获得更好的性能
        query = text("""
            WITH last_message AS (
                SELECT 
                    CASE 
                        WHEN sender_id = :user_id THEN receiver_id 
                        ELSE sender_id 
                    END AS contact_id,
                    MAX(created_at) AS last_time
                FROM 
                    chat_message
                WHERE 
                    sender_id = :user_id OR receiver_id = :user_id
                GROUP BY 
                    contact_id
            )
            SELECT 
                u.id,
                u.username,
                u.nickname,
                u.avatar,
                lm.last_time,
                (
                    SELECT COUNT(*) 
                    FROM chat_message cm 
                    WHERE cm.sender_id = u.id 
                    AND cm.receiver_id = :user_id 
                    AND cm.is_read = false
                ) AS unread_count
            FROM 
                "user" u
            JOIN 
                last_message lm ON u.id = lm.contact_id
            ORDER BY 
                lm.last_time DESC
            LIMIT :limit
        """)
        
        result = await db.execute(query, {"user_id": user_id, "limit": limit})
        
        contacts = []
        for row in result:
            contacts.append({
                "id": row.id,
                "username": row.username,
                "nickname": row.nickname,
                "avatar": row.avatar,
                "last_time": row.last_time,
                "unread_count": row.unread_count
            })
            
        return contacts

class ChatRoomRepository(RepositoryBase[ChatRoom, ChatRoomCreate, ChatRoomUpdate]):
    """
    聊天室数据访问层
    """
    
    def __init__(self):
        super().__init__(ChatRoom)
    
    async def get_with_last_message(
        self, 
        db: AsyncSession, 
        *, 
        id: int
    ) -> Optional[Tuple[ChatRoom, Optional[ChatMessage]]]:
        """
        获取聊天室及其最后一条消息
        
        Args:
            db: 数据库会话
            id: 聊天室ID
            
        Returns:
            (聊天室对象, 最后一条消息)元组，如未找到聊天室返回(None, None)
        """
        room = await self.get(db, id)
        if not room:
            return None, None
        
        # 获取最后一条消息
        message_query = (
            select(ChatMessage)
            .where(ChatMessage.chat_room_id == id)
            .order_by(desc(ChatMessage.created_at))
            .limit(1)
        )
        message_result = await db.execute(message_query)
        last_message = message_result.scalars().first()
        
        return room, last_message
    
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
        # 使用原生SQL以获得更好的性能和复杂查询
        query = text("""
            WITH room_info AS (
                SELECT 
                    cr.id AS room_id,
                    cr.name,
                    cr.is_group,
                    cr.creator_id,
                    cr.created_at,
                    cr.updated_at,
                    (
                        SELECT COUNT(*) 
                        FROM chat_message cm 
                        WHERE cm.chat_room_id = cr.id 
                        AND cm.sender_id != :user_id 
                        AND cm.is_read = false
                    ) AS unread_count
                FROM 
                    chat_room cr
                JOIN 
                    chat_room_member crm ON cr.id = crm.room_id
                WHERE 
                    crm.user_id = :user_id
                ORDER BY 
                    cr.updated_at DESC
                OFFSET :skip LIMIT :limit
            ),
            last_messages AS (
                SELECT DISTINCT ON (chat_room_id)
                    chat_room_id,
                    id,
                    sender_id,
                    receiver_id,
                    content,
                    message_type,
                    is_read,
                    created_at
                FROM 
                    chat_message
                WHERE 
                    chat_room_id IN (SELECT room_id FROM room_info)
                ORDER BY 
                    chat_room_id, created_at DESC
            )
            SELECT 
                ri.*,
                lm.id AS message_id,
                lm.sender_id,
                lm.receiver_id,
                lm.content,
                lm.message_type,
                lm.is_read,
                lm.created_at AS message_created_at
            FROM 
                room_info ri
            LEFT JOIN 
                last_messages lm ON ri.room_id = lm.chat_room_id
            ORDER BY 
                ri.updated_at DESC
        """)
        
        result = await db.execute(query, {"user_id": user_id, "skip": skip, "limit": limit})
        rows = result.all()
        
        rooms = []
        for row in rows:
            # 构建聊天室对象
            room = ChatRoom(
                id=row.room_id,
                name=row.name,
                is_group=row.is_group,
                creator_id=row.creator_id,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            
            # 构建最后一条消息对象（如果有）
            last_message = None
            if row.message_id:
                last_message = ChatMessage(
                    id=row.message_id,
                    sender_id=row.sender_id,
                    receiver_id=row.receiver_id,
                    content=row.content,
                    message_type=row.message_type,
                    is_read=row.is_read,
                    chat_room_id=row.room_id,
                    created_at=row.message_created_at
                )
            
            rooms.append((room, row.unread_count, last_message))
            
        return rooms
    
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
        # 检查是否已存在私聊聊天室
        query = text("""
            SELECT 
                cr.id
            FROM 
                chat_room cr
            JOIN 
                chat_room_member crm1 ON cr.id = crm1.room_id AND crm1.user_id = :user_id1
            JOIN 
                chat_room_member crm2 ON cr.id = crm2.room_id AND crm2.user_id = :user_id2
            WHERE 
                cr.is_group = false
            LIMIT 1
        """)
        
        result = await db.execute(query, {"user_id1": user_id1, "user_id2": user_id2})
        existing_room = result.first()
        
        if existing_room:
            return await self.get(db, existing_room.id)
        
        # 创建新的聊天室
        room_data = {
            "name": None,
            "is_group": False,
            "creator_id": user_id1
        }
        room = ChatRoom(**room_data)
        db.add(room)
        await db.flush()
        
        # 添加成员
        member1 = ChatRoomMember(
            room_id=room.id,
            user_id=user_id1,
            join_date=datetime.now(),
            is_admin=True
        )
        member2 = ChatRoomMember(
            room_id=room.id,
            user_id=user_id2,
            join_date=datetime.now(),
            is_admin=False
        )
        db.add(member1)
        db.add(member2)
        
        await db.commit()
        await db.refresh(room)
        
        return room
    
    async def count_members(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int
    ) -> int:
        """
        计算聊天室成员数量
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            
        Returns:
            成员数量
        """
        query = (
            select(func.count())
            .select_from(ChatRoomMember)
            .where(ChatRoomMember.room_id == room_id)
        )
        result = await db.execute(query)
        return result.scalar()

class ChatRoomMemberRepository(RepositoryBase[ChatRoomMember, ChatRoomMemberCreate, ChatRoomMemberUpdate]):
    """
    聊天室成员数据访问层
    """
    
    def __init__(self):
        super().__init__(ChatRoomMember)
    
    async def get_by_user_and_room(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        room_id: int
    ) -> Optional[ChatRoomMember]:
        """
        获取用户在指定聊天室的成员记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            room_id: 聊天室ID
            
        Returns:
            成员记录，如未找到返回None
        """
        query = (
            select(ChatRoomMember)
            .where(
                and_(
                    ChatRoomMember.user_id == user_id,
                    ChatRoomMember.room_id == room_id
                )
            )
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_members_by_room(
        self, 
        db: AsyncSession, 
        *, 
        room_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChatRoomMember]:
        """
        获取聊天室的所有成员
        
        Args:
            db: 数据库会话
            room_id: 聊天室ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            成员列表
        """
        query = (
            select(ChatRoomMember)
            .where(ChatRoomMember.room_id == room_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def is_admin(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        room_id: int
    ) -> bool:
        """
        判断用户是否是聊天室管理员
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            room_id: 聊天室ID
            
        Returns:
            是否为管理员
        """
        query = (
            select(ChatRoomMember.is_admin)
            .where(
                and_(
                    ChatRoomMember.user_id == user_id,
                    ChatRoomMember.room_id == room_id
                )
            )
        )
        result = await db.execute(query)
        is_admin = result.scalar()
        return bool(is_admin)
    
    async def remove_member(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        room_id: int
    ) -> bool:
        """
        从聊天室移除成员
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            room_id: 聊天室ID
            
        Returns:
            是否成功移除
        """
        query = (
            select(ChatRoomMember)
            .where(
                and_(
                    ChatRoomMember.user_id == user_id,
                    ChatRoomMember.room_id == room_id
                )
            )
        )
        result = await db.execute(query)
        member = result.scalars().first()
        
        if not member:
            return False
            
        await db.delete(member)
        await db.commit()
        return True 