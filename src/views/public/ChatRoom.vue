<template>
  <div class="chat-container page-with-nav">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <div class="header-info">
        <el-avatar :size="40" :src="currentChat?.avatar || defaultAvatar" />
        <div class="chat-info">
          <h3>{{ currentChat?.name || '选择聊天对象' }}</h3>
          <p class="status" v-if="currentChat">
            <el-icon v-if="isOnline(currentChat.id)" class="online"><Circle /></el-icon>
            <el-icon v-else class="offline"><Circle /></el-icon>
            {{ isOnline(currentChat.id) ? '在线' : '离线' }}
          </p>
        </div>
      </div>
      <div class="header-actions">
        <el-button @click="showUserList = !showUserList" type="primary" text>
          <el-icon><User /></el-icon>
          在线用户
        </el-button>
      </div>
    </div>

    <div class="chat-body">
      <!-- 侧边栏 - 用户列表 -->
      <div class="sidebar" :class="{ 'show': showUserList }">
        <div class="sidebar-header">
          <h4>在线用户 ({{ onlineUsers.length }})</h4>
          <el-button @click="showUserList = false" size="small" text>
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
        <div class="user-list">
          <div 
            v-for="user in onlineUsers" 
            :key="user.user_id"
            class="user-item"
            :class="{ 'active': currentChat?.id === user.user_id }"
            @click="selectUser(user)"
          >
            <el-avatar :size="32" :src="user.avatar || defaultAvatar" />
            <div class="user-info">
              <div class="username">{{ user.nickname || user.username }}</div>
              <div class="last-seen">刚刚在线</div>
            </div>
            <div class="unread-badge" v-if="getUnreadCount(user.user_id) > 0">
              {{ getUnreadCount(user.user_id) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 消息区域 -->
      <div class="message-area">
        <div class="messages" ref="messagesContainer">
          <div v-if="!currentChat" class="no-chat">
            <el-icon size="64" color="#c0c4cc"><ChatDotRound /></el-icon>
            <p>选择一个用户开始聊天</p>
          </div>
          
          <div v-else>
            <div v-if="messages.length === 0" class="no-messages">
              <p>还没有消息，发送第一条消息开始聊天吧！</p>
            </div>
            
            <div 
              v-for="message in messages" 
              :key="message.id"
              class="message-item"
              :class="{ 'own': message.sender_id === userStore.userInfo.id }"
            >
              <div class="message-avatar">
                <el-avatar 
                  :size="32" 
                  :src="message.sender_avatar || defaultAvatar" 
                />
              </div>
              <div class="message-content">
                <div class="message-header">
                  <span class="sender-name">{{ message.sender_nickname || message.sender_username }}</span>
                  <span class="message-time">{{ formatTime(message.created_at) }}</span>
                </div>
                <div class="message-body">
                  <div v-if="message.message_type === 'text'" class="text-message">
                    {{ message.content }}
                  </div>
                  <div v-else-if="message.message_type === 'image'" class="image-message">
                    <el-image :src="message.content" fit="cover" />
                  </div>
                  <div v-else class="other-message">
                    不支持的消息类型
                  </div>
                </div>
              </div>
            </div>

            <!-- 正在输入提示 -->
            <div v-if="typingUsers.length > 0" class="typing-indicator">
              <div class="typing-avatar">
                <el-avatar :size="24" :src="defaultAvatar" />
              </div>
              <div class="typing-content">
                <span>{{ typingUsers[0].nickname || typingUsers[0].username }} 正在输入...</span>
                <div class="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area" v-if="currentChat">
          <div class="input-toolbar">
            <el-button size="small" text @click="showEmojiPicker = !showEmojiPicker">
              <el-icon><Platform /></el-icon>
            </el-button>
            <el-button size="small" text>
              <el-icon><Picture /></el-icon>
            </el-button>
            <el-button size="small" text>
              <el-icon><VideoCamera /></el-icon>
            </el-button>
          </div>
          
          <div class="input-box">
            <el-input
              v-model="messageInput"
              type="textarea"
              :autosize="{ minRows: 1, maxRows: 4 }"
              placeholder="输入消息..."
              @keyup.enter.exact="sendMessage"
              @keyup.shift.enter="addNewLine"
              @input="handleTyping"
              @blur="stopTyping"
            />
            <el-button 
              type="primary" 
              @click="sendMessage"
              :disabled="!messageInput.trim()"
              class="send-button"
            >
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Circle, 
  User, 
  Close, 
  ChatDotRound, 
  Platform, 
  Picture, 
  VideoCamera 
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { wsManager } from '@/utils/websocket'

const userStore = useUserStore()

// 响应式数据
const showUserList = ref(false)
const onlineUsers = ref<any[]>([])
const currentChat = ref<any>(null)
const messages = ref<any[]>([])
const messageInput = ref('')
const messagesContainer = ref<HTMLElement>()
const typingUsers = ref<any[]>([])
const showEmojiPicker = ref(false)
const unreadCounts = ref<Record<number, number>>({})

const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

// 输入防抖定时器
let typingTimer: NodeJS.Timeout | null = null

// 初始化WebSocket连接
onMounted(async () => {
  await initWebSocket()
})

onUnmounted(() => {
  wsManager.disconnect()
})

// 初始化WebSocket
const initWebSocket = async () => {
  try {
    const connected = await wsManager.connect()
    if (connected) {
      setupWebSocketHandlers()
      ElMessage.success('连接聊天服务成功')
    } else {
      ElMessage.error('连接聊天服务失败')
    }
  } catch (error) {
    console.error('WebSocket connection failed:', error)
    ElMessage.error('连接聊天服务失败')
  }
}

// 设置WebSocket事件处理器
const setupWebSocketHandlers = () => {
  // 处理在线用户列表
  wsManager.addMessageHandler('online_users', (users) => {
    onlineUsers.value = users.filter((user: any) => user.user_id !== userStore.userInfo.id)
  })

  // 处理用户状态变化
  wsManager.addMessageHandler('user_status', (data) => {
    const { user_id, status } = data
    if (status === 'online') {
      const existingUser = onlineUsers.value.find(user => user.user_id === user_id)
      if (!existingUser) {
        onlineUsers.value.push({
          user_id,
          username: data.username,
          nickname: data.nickname,
          avatar: data.avatar,
          connected_at: data.timestamp
        })
      }
    } else if (status === 'offline') {
      onlineUsers.value = onlineUsers.value.filter(user => user.user_id !== user_id)
    }
  })

  // 处理私聊消息
  wsManager.addMessageHandler('private_message', (messageData) => {
    const message = messageData.data || messageData
    
    // 如果是当前聊天对象的消息，添加到消息列表
    if (currentChat.value && 
        (message.sender_id === currentChat.value.id || message.receiver_id === currentChat.value.id)) {
      messages.value.push(message)
      scrollToBottom()
      
      // 标记消息为已读
      if (message.sender_id !== userStore.userInfo.id) {
        wsManager.markMessageAsRead(message.id)
      }
    } else {
      // 更新未读消息计数
      const senderId = message.sender_id
      if (senderId !== userStore.userInfo.id) {
        unreadCounts.value[senderId] = (unreadCounts.value[senderId] || 0) + 1
      }
    }
  })

  // 处理消息发送确认
  wsManager.addMessageHandler('message_sent', (data) => {
    console.log('Message sent confirmation:', data)
  })

  // 处理正在输入状态
  wsManager.addMessageHandler('typing_status', (data) => {
    if (currentChat.value && data.user_id === currentChat.value.id) {
      if (data.is_typing) {
        const existingUser = typingUsers.value.find(user => user.user_id === data.user_id)
        if (!existingUser) {
          typingUsers.value.push({
            user_id: data.user_id,
            username: data.username,
            nickname: data.nickname
          })
        }
      } else {
        typingUsers.value = typingUsers.value.filter(user => user.user_id !== data.user_id)
      }
    }
  })

  // 处理错误消息
  wsManager.addMessageHandler('error', (data) => {
    ElMessage.error(data.message || '发生错误')
  })
}

// 选择聊天用户
const selectUser = (user: any) => {
  currentChat.value = {
    id: user.user_id,
    name: user.nickname || user.username,
    avatar: user.avatar
  }
  
  // 清除未读计数
  unreadCounts.value[user.user_id] = 0
  
  // 加载聊天历史（这里可以调用API获取历史消息）
  loadChatHistory(user.user_id)
  
  showUserList.value = false
}

// 加载聊天历史
const loadChatHistory = async (userId: number) => {
  // 这里应该调用API获取聊天历史
  // 暂时清空消息列表
  messages.value = []
}

// 发送消息
const sendMessage = () => {
  if (!messageInput.value.trim() || !currentChat.value) return

  const success = wsManager.sendPrivateMessage(
    currentChat.value.id,
    messageInput.value.trim(),
    'text'
  )

  if (success) {
    // 添加消息到本地列表（发送确认后会收到服务器消息）
    const tempMessage = {
      id: Date.now(), // 临时ID
      sender_id: userStore.userInfo.id,
      sender_username: userStore.userInfo.username,
      sender_nickname: userStore.userInfo.nickname,
      sender_avatar: userStore.userInfo.avatar,
      receiver_id: currentChat.value.id,
      content: messageInput.value.trim(),
      message_type: 'text',
      created_at: new Date().toISOString(),
      is_read: false
    }
    
    messages.value.push(tempMessage)
    messageInput.value = ''
    scrollToBottom()
    stopTyping()
  } else {
    ElMessage.error('消息发送失败')
  }
}

// 处理输入事件
const handleTyping = () => {
  if (!currentChat.value) return

  // 发送正在输入状态
  wsManager.sendTypingStatus(currentChat.value.id, 'user', true)

  // 清除之前的定时器
  if (typingTimer) {
    clearTimeout(typingTimer)
  }

  // 设置新的定时器，3秒后停止输入状态
  typingTimer = setTimeout(() => {
    stopTyping()
  }, 3000)
}

// 停止输入状态
const stopTyping = () => {
  if (currentChat.value) {
    wsManager.sendTypingStatus(currentChat.value.id, 'user', false)
  }
  if (typingTimer) {
    clearTimeout(typingTimer)
    typingTimer = null
  }
}

// 添加换行
const addNewLine = () => {
  messageInput.value += '\n'
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 检查用户是否在线
const isOnline = (userId: number) => {
  return wsManager.isUserOnline(userId)
}

// 获取未读消息数
const getUnreadCount = (userId: number) => {
  return unreadCounts.value[userId] || 0
}

// 格式化时间
const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return '刚刚'
  if (diffMins < 60) return `${diffMins}分钟前`
  if (diffMins < 1440) return `${Math.floor(diffMins / 60)}小时前`
  
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString().slice(0, 5)
}

// 监听当前聊天对象变化
watch(currentChat, () => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: var(--gradient-sunset);
  color: white;
  box-shadow: var(--shadow-gold);
  position: relative;
}

.chat-header::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-gold);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-info h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: white;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.status {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 4px 0 0;
  font-size: 12px;
  color: rgba(255,255,255,0.9);
}

.online {
  color: #90EE90;
  text-shadow: 0 0 5px #90EE90;
}

.offline {
  color: #FFB6C1;
}

.chat-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: white;
  border-right: 2px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
  box-shadow: var(--shadow-warm);
}

@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    z-index: 1000;
    transform: translateX(-100%);
    border-radius: 0 15px 15px 0;
  }
  
  .sidebar.show {
    transform: translateX(0);
  }
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: var(--gradient-warm);
  color: var(--text-primary);
  border-bottom: 2px solid var(--border-color);
}

.sidebar-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.user-list {
  flex: 1;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  border-bottom: 1px solid var(--bg-accent);
}

.user-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 0;
  background: var(--gradient-sunset);
  transition: width 0.3s ease;
}

.user-item:hover {
  background: var(--bg-accent);
  transform: translateX(5px);
}

.user-item:hover::before {
  width: 4px;
}

.user-item.active {
  background: linear-gradient(135deg, var(--bg-accent) 0%, var(--bg-secondary) 100%);
  border-left: 4px solid var(--primary-color);
}

.user-info {
  flex: 1;
  min-width: 0;
}

.username {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.last-seen {
  font-size: 12px;
  color: var(--text-light);
}

.unread-badge {
  background: var(--gradient-sunset);
  color: white;
  font-size: 10px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 12px;
  min-width: 20px;
  text-align: center;
  box-shadow: var(--shadow-warm);
}

.message-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 0 0 15px 15px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: linear-gradient(to bottom, var(--bg-primary), white);
}

.no-chat, .no-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--text-light);
}

.no-chat p, .no-messages p {
  margin: 16px 0 0;
  font-size: 16px;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  animation: fadeIn 0.5s ease-out;
}

.message-item.own {
  flex-direction: row-reverse;
}

.message-item.own .message-content {
  background: var(--gradient-sunset);
  color: white;
  border-radius: 18px 18px 6px 18px;
}

.message-item:not(.own) .message-content {
  background: white;
  color: var(--text-primary);
  border: 2px solid var(--border-color);
  border-radius: 6px 18px 18px 18px;
}

.message-item.own .message-header {
  text-align: right;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  position: relative;
  box-shadow: var(--shadow-warm);
  transition: all 0.3s ease;
}

.message-content:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 12px;
  opacity: 0.9;
}

.sender-name {
  font-weight: 600;
}

.message-time {
  margin-left: 8px;
  font-style: italic;
}

.text-message {
  word-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.5;
}

.image-message {
  max-width: 250px;
  border-radius: 12px;
  overflow: hidden;
}

.typing-indicator {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 12px 0;
  color: var(--text-light);
  font-size: 12px;
  font-style: italic;
}

.typing-dots {
  display: flex;
  gap: 3px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  30% {
    transform: scale(1.4);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.input-area {
  border-top: 2px solid var(--border-color);
  padding: 16px 20px;
  background: var(--bg-secondary);
  border-radius: 0 0 15px 15px;
}

.input-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.input-toolbar .el-button {
  border-radius: 50%;
  width: 36px;
  height: 36px;
  padding: 0;
  border: 2px solid var(--border-color);
  background: white;
  color: var(--primary-color);
  transition: all 0.3s ease;
}

.input-toolbar .el-button:hover {
  background: var(--gradient-warm);
  color: white;
  transform: scale(1.1);
}

.input-box {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-box :deep(.el-textarea) {
  flex: 1;
}

.input-box :deep(.el-textarea__inner) {
  border-radius: 20px;
  border: 2px solid var(--border-color);
  padding: 12px 16px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
  resize: none;
}

.input-box :deep(.el-textarea__inner):focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(255, 140, 66, 0.2);
}

.send-button {
  height: 40px;
  border-radius: 20px;
  padding: 0 20px;
  background: var(--gradient-sunset);
  border: none;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-warm);
}

.send-button:hover {
  background: var(--gradient-gold);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-header {
    padding: 12px 16px;
  }
  
  .messages {
    padding: 12px 16px;
  }
  
  .input-area {
    padding: 12px 16px;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .chat-info h3 {
    font-size: 16px;
  }
}
</style> 