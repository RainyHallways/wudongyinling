from fastapi import WebSocket
from typing import Dict, Set
import json

class ChatManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.user_rooms: Dict[int, Set[int]] = {}  # user_id -> set of room_ids

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_rooms[user_id] = set()

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str, exclude_user: int = None):
        for user_id, connection in self.active_connections.items():
            if user_id != exclude_user:
                await connection.send_text(message)

    def join_room(self, user_id: int, room_id: int):
        if user_id in self.user_rooms:
            self.user_rooms[user_id].add(room_id)

    def leave_room(self, user_id: int, room_id: int):
        if user_id in self.user_rooms:
            self.user_rooms[user_id].discard(room_id)

    async def broadcast_to_room(self, room_id: int, message: str, exclude_user: int = None):
        for user_id, rooms in self.user_rooms.items():
            if room_id in rooms and user_id != exclude_user:
                await self.send_personal_message(message, user_id)

chat_manager = ChatManager() 