import { useUserStore } from '@/stores/user'

export interface WebSocketMessage {
  type: string
  data: any
}

interface ChatMessage {
  id: number
  sender_id: number
  sender_username: string
  sender_nickname: string
  sender_avatar?: string
  receiver_id?: number
  room_id?: number
  content: string
  message_type: string
  created_at: string
  is_read: boolean
}

export class WebSocketManager {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectInterval = 3000
  private messageHandlers: Map<string, (data: any) => void> = new Map()
  private onlineUsers: any[] = []
  
  constructor() {
    // 绑定方法
    this.connect = this.connect.bind(this)
    this.disconnect = this.disconnect.bind(this)
    this.sendMessage = this.sendMessage.bind(this)
    this.addMessageHandler = this.addMessageHandler.bind(this)
    this.removeMessageHandler = this.removeMessageHandler.bind(this)
  }

  async connect(): Promise<boolean> {
    try {
      const userStore = useUserStore()
      if (!userStore.token) {
        console.error('No token available for WebSocket connection')
        return false
      }

      // 构造WebSocket URL
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = import.meta.env.VITE_API_BASE_URL?.replace(/^https?:\/\//, '') || 'localhost:8000'
      const wsUrl = `${protocol}//${host}/api/v1/ws/${userStore.token}`

      this.ws = new WebSocket(wsUrl)

      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
      }

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          this.handleMessage(message)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason)
        this.ws = null
        
        // 自动重连
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          setTimeout(() => {
            this.reconnectAttempts++
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
            this.connect()
          }, this.reconnectInterval)
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      return true
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error)
      return false
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  sendMessage(message: WebSocketMessage): boolean {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(JSON.stringify(message))
        return true
      } catch (error) {
        console.error('Error sending WebSocket message:', error)
        return false
      }
    }
    console.warn('WebSocket is not connected')
    return false
  }

  private handleMessage(message: WebSocketMessage) {
    const handler = this.messageHandlers.get(message.type)
    if (handler) {
      handler(message.data)
    } else {
      console.log('Unhandled message type:', message.type, message.data)
    }

    // 处理内置消息类型
    switch (message.type) {
      case 'online_users':
        this.onlineUsers = message.data
        break
      case 'user_status':
        this.handleUserStatus(message.data)
        break
    }
  }

  private handleUserStatus(data: any) {
    const { user_id, status } = data
    if (status === 'online') {
      // 添加到在线用户列表
      if (!this.onlineUsers.find(user => user.user_id === user_id)) {
        this.onlineUsers.push({
          user_id,
          username: data.username,
          nickname: data.nickname,
          avatar: data.avatar,
          connected_at: data.timestamp
        })
      }
    } else if (status === 'offline') {
      // 从在线用户列表移除
      this.onlineUsers = this.onlineUsers.filter(user => user.user_id !== user_id)
    }
  }

  addMessageHandler(type: string, handler: (data: any) => void) {
    this.messageHandlers.set(type, handler)
  }

  removeMessageHandler(type: string) {
    this.messageHandlers.delete(type)
  }

  // 发送私聊消息
  sendPrivateMessage(receiverId: number, content: string, messageType: string = 'text'): boolean {
    return this.sendMessage({
      type: 'private_message',
      data: {
        receiver_id: receiverId,
        content,
        message_type: messageType
      }
    })
  }

  // 发送群聊消息
  sendRoomMessage(roomId: number, content: string, messageType: string = 'text'): boolean {
    return this.sendMessage({
      type: 'room_message',
      data: {
        room_id: roomId,
        content,
        message_type: messageType
      }
    })
  }

  // 发送正在输入状态
  sendTypingStatus(targetId: number, targetType: 'user' | 'room', isTyping: boolean): boolean {
    return this.sendMessage({
      type: 'typing',
      data: {
        target_id: targetId,
        target_type: targetType,
        is_typing: isTyping
      }
    })
  }

  // 标记消息已读
  markMessageAsRead(messageId: number): boolean {
    return this.sendMessage({
      type: 'read_message',
      data: {
        message_id: messageId
      }
    })
  }

  // 获取在线用户列表
  getOnlineUsers(): any[] {
    return this.onlineUsers
  }

  // 检查用户是否在线
  isUserOnline(userId: number): boolean {
    return this.onlineUsers.some(user => user.user_id === userId)
  }

  // 获取连接状态
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }
}

// 全局WebSocket管理器实例
export const wsManager = new WebSocketManager() 