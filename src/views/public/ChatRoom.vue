<template>
  <div class="chat-container">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <div class="header-info">
        <el-avatar :size="40" :src="currentChat?.avatar || defaultAvatar" />
        <div class="chat-info">
          <h3>{{ currentChat?.name || '选择聊天对象' }}</h3>
          <p class="status" v-if="currentChat">
            <el-icon v-if="isOnline(currentChat.id)" class="online"><CircleFilled /></el-icon>
            <el-icon v-else class="offline"><CircleFilled /></el-icon>
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
  CircleFilled, 
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
  background: #f5f7fa;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.status {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 4px 0 0;
  font-size: 12px;
  color: #909399;
}

.online {
  color: #67c23a;
}

.offline {
  color: #f56c6c;
}

.chat-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    z-index: 1000;
    transform: translateX(-100%);
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
  border-bottom: 1px solid #e4e7ed;
}

.sidebar-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.user-list {
  flex: 1;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  position: relative;
}

.user-item:hover {
  background: #f5f7fa;
}

.user-item.active {
  background: #ecf5ff;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 2px;
}

.last-seen {
  font-size: 12px;
  color: #909399;
}

.unread-badge {
  background: #f56c6c;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.message-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}

.no-chat, .no-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #909399;
}

.no-chat p, .no-messages p {
  margin: 16px 0 0;
  font-size: 14px;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.message-item.own {
  flex-direction: row-reverse;
}

.message-item.own .message-content {
  background: #409eff;
  color: white;
}

.message-item.own .message-header {
  text-align: right;
}

.message-content {
  max-width: 60%;
  padding: 12px 16px;
  background: #f0f2f5;
  border-radius: 12px;
  position: relative;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  font-size: 12px;
  opacity: 0.8;
}

.sender-name {
  font-weight: 500;
}

.message-time {
  margin-left: 8px;
}

.text-message {
  word-wrap: break-word;
  white-space: pre-wrap;
}

.image-message {
  max-width: 200px;
}

.typing-indicator {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 8px 0;
  color: #909399;
  font-size: 12px;
}

.typing-dots {
  display: flex;
  gap: 2px;
}

.typing-dots span {
  width: 4px;
  height: 4px;
  background: #909399;
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
    transform: scale(1.2);
    opacity: 1;
  }
}

.input-area {
  border-top: 1px solid #e4e7ed;
  padding: 16px 20px;
  background: white;
}

.input-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.input-box {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-box :deep(.el-textarea) {
  flex: 1;
}

.send-button {
  height: 32px;
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
    max-width: 80%;
  }
}
</style> 