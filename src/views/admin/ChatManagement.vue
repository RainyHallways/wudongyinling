<template>
  <div class="chat-management">
    <PageHeader title="聊天管理" subtitle="管理私信消息和群聊房间" />
    
    <!-- 功能选项卡 -->
    <el-tabs v-model="activeTab" type="card">
      <!-- 私信管理 -->
      <el-tab-pane label="私信管理" name="messages">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>私信消息列表</span>
              <div class="header-actions">
                <el-button type="danger" @click="batchDeleteMessages" :disabled="selectedMessages.length === 0">
                  批量删除
                </el-button>
              </div>
            </div>
          </template>
          
          <!-- 消息筛选 -->
          <el-row :gutter="20" class="filter-row">
            <el-col :span="6">
              <el-input v-model="messageFilters.keyword" placeholder="搜索消息内容" clearable>
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </el-col>
            <el-col :span="4">
              <el-select v-model="messageFilters.senderRole" placeholder="发送者角色" clearable>
                <el-option label="老年人" value="elderly" />
                <el-option label="子女" value="child" />
                <el-option label="志愿者" value="volunteer" />
                <el-option label="教师" value="teacher" />
                <el-option label="医生" value="doctor" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select v-model="messageFilters.receiverRole" placeholder="接收者角色" clearable>
                <el-option label="老年人" value="elderly" />
                <el-option label="子女" value="child" />
                <el-option label="志愿者" value="volunteer" />
                <el-option label="教师" value="teacher" />
                <el-option label="医生" value="doctor" />
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-date-picker
                v-model="messageFilters.dateRange"
                type="datetimerange"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm:ss"
              />
            </el-col>
            <el-col :span="4">
              <el-button type="primary" @click="searchMessages">查询</el-button>
              <el-button @click="resetMessageFilters">重置</el-button>
            </el-col>
          </el-row>

          <!-- 消息表格 -->
          <el-table 
            :data="messages" 
            v-loading="messageLoading" 
            style="width: 100%"
            @selection-change="handleMessageSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="发送者" width="150">
              <template #default="{ row }">
                <div class="user-info">
                  <el-avatar :src="row.sender.avatar" :size="32">
                    {{ row.sender.nickname?.[0] || row.sender.username[0] }}
                  </el-avatar>
                  <div class="user-details">
                    <div class="username">{{ row.sender.nickname || row.sender.username }}</div>
                    <el-tag :type="getRoleTagType(row.sender.role)" size="small">
                      {{ getRoleText(row.sender.role) }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="接收者" width="150">
              <template #default="{ row }">
                <div class="user-info">
                  <el-avatar :src="row.receiver.avatar" :size="32">
                    {{ row.receiver.nickname?.[0] || row.receiver.username[0] }}
                  </el-avatar>
                  <div class="user-details">
                    <div class="username">{{ row.receiver.nickname || row.receiver.username }}</div>
                    <el-tag :type="getRoleTagType(row.receiver.role)" size="small">
                      {{ getRoleText(row.receiver.role) }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="消息内容" min-width="250">
              <template #default="{ row }">
                <div class="message-content">
                  <div class="message-text">{{ row.content }}</div>
                  <div v-if="row.media_url" class="message-media">
                    <el-tag size="small" type="info">包含媒体文件</el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_read ? 'success' : 'warning'">
                  {{ row.is_read ? '已读' : '未读' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="发送时间" width="180" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button-group>
                  <el-button size="small" @click="viewMessage(row)">查看</el-button>
                  <el-button size="small" type="danger" @click="deleteMessage(row)">删除</el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="messagePagination.page"
              v-model:page-size="messagePagination.size"
              :page-sizes="[10, 20, 50, 100]"
              :total="messagePagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleMessageSizeChange"
              @current-change="handleMessageCurrentChange"
            />
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 群聊管理 -->
      <el-tab-pane label="群聊管理" name="rooms">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>群聊房间列表</span>
              <el-button type="primary" @click="showCreateRoom = true">
                <el-icon><Plus /></el-icon>
                创建群聊
              </el-button>
            </div>
          </template>
          
          <!-- 群聊筛选 -->
          <el-row :gutter="20" class="filter-row">
            <el-col :span="6">
              <el-input v-model="roomFilters.keyword" placeholder="搜索群聊名称" clearable>
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </el-col>
            <el-col :span="4">
              <el-select v-model="roomFilters.type" placeholder="群聊类型" clearable>
                <el-option label="系统群聊" value="system" />
                <el-option label="用户群聊" value="user" />
                <el-option label="课程群聊" value="course" />
                <el-option label="挑战群聊" value="challenge" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select v-model="roomFilters.status" placeholder="状态" clearable>
                <el-option label="活跃" value="active" />
                <el-option label="停用" value="inactive" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-input-number v-model="roomFilters.minMembers" placeholder="最少成员数" :min="0" />
            </el-col>
            <el-col :span="6">
              <el-button type="primary" @click="searchRooms">查询</el-button>
              <el-button @click="resetRoomFilters">重置</el-button>
            </el-col>
          </el-row>

          <!-- 群聊表格 -->
          <el-table :data="rooms" v-loading="roomLoading" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="群聊信息" width="250">
              <template #default="{ row }">
                <div class="room-info">
                  <el-avatar :src="row.avatar" :size="50" shape="square">
                    {{ row.name[0] }}
                  </el-avatar>
                  <div class="room-details">
                    <div class="room-name">{{ row.name }}</div>
                    <div class="room-desc">{{ row.description }}</div>
                    <el-tag :type="getRoomTypeTagType(row.type)" size="small">
                      {{ getRoomTypeText(row.type) }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="创建者" width="120">
              <template #default="{ row }">
                {{ row.creator?.nickname || row.creator?.username || '系统' }}
              </template>
            </el-table-column>
            <el-table-column label="成员数量" width="100">
              <template #default="{ row }">
                <el-badge :value="row.member_count" class="member-badge">
                  <el-icon><User /></el-icon>
                </el-badge>
              </template>
            </el-table-column>
            <el-table-column label="最后活跃" width="180">
              <template #default="{ row }">
                {{ row.last_message_at || '暂无消息' }}
              </template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'danger'">
                  {{ row.is_active ? '活跃' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button-group>
                  <el-button size="small" @click="viewRoom(row)">查看</el-button>
                  <el-button size="small" type="primary" @click="manageMembers(row)">成员</el-button>
                  <el-button 
                    size="small" 
                    :type="row.is_active ? 'warning' : 'success'"
                    @click="toggleRoomStatus(row)"
                  >
                    {{ row.is_active ? '停用' : '启用' }}
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteRoom(row)">删除</el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="roomPagination.page"
              v-model:page-size="roomPagination.size"
              :page-sizes="[10, 20, 50]"
              :total="roomPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleRoomSizeChange"
              @current-change="handleRoomCurrentChange"
            />
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 消息详情弹窗 -->
    <el-dialog v-model="showMessageDetail" title="消息详情" width="600px">
      <div v-if="currentMessage" class="message-detail">
        <div class="message-header">
          <div class="sender-info">
            <el-avatar :src="currentMessage.sender.avatar" :size="40">
              {{ currentMessage.sender.nickname?.[0] || currentMessage.sender.username[0] }}
            </el-avatar>
            <div>
              <div class="sender-name">{{ currentMessage.sender.nickname || currentMessage.sender.username }}</div>
              <div class="send-time">{{ currentMessage.created_at }}</div>
            </div>
          </div>
          <el-icon><ArrowRight /></el-icon>
          <div class="receiver-info">
            <el-avatar :src="currentMessage.receiver.avatar" :size="40">
              {{ currentMessage.receiver.nickname?.[0] || currentMessage.receiver.username[0] }}
            </el-avatar>
            <div>
              <div class="receiver-name">{{ currentMessage.receiver.nickname || currentMessage.receiver.username }}</div>
              <el-tag :type="currentMessage.is_read ? 'success' : 'warning'" size="small">
                {{ currentMessage.is_read ? '已读' : '未读' }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="message-body">
          <p>{{ currentMessage.content }}</p>
          <div v-if="currentMessage.media_url" class="message-media">
            <img v-if="currentMessage.media_type === 'image'" :src="currentMessage.media_url" />
            <video v-else-if="currentMessage.media_type === 'video'" :src="currentMessage.media_url" controls />
            <audio v-else-if="currentMessage.media_type === 'audio'" :src="currentMessage.media_url" controls />
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 创建群聊弹窗 -->
    <el-dialog v-model="showCreateRoom" title="创建群聊" width="500px">
      <el-form :model="roomForm" :rules="roomRules" ref="roomFormRef" label-width="100px">
        <el-form-item label="群聊名称" prop="name">
          <el-input v-model="roomForm.name" placeholder="请输入群聊名称" />
        </el-form-item>
        <el-form-item label="群聊描述">
          <el-input 
            v-model="roomForm.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入群聊描述" 
          />
        </el-form-item>
        <el-form-item label="群聊类型" prop="type">
          <el-select v-model="roomForm.type" placeholder="请选择群聊类型">
            <el-option label="系统群聊" value="system" />
            <el-option label="用户群聊" value="user" />
            <el-option label="课程群聊" value="course" />
            <el-option label="挑战群聊" value="challenge" />
          </el-select>
        </el-form-item>
        <el-form-item label="群聊头像">
          <el-input v-model="roomForm.avatar" placeholder="头像URL" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateRoom = false">取消</el-button>
        <el-button type="primary" @click="createRoom">创建</el-button>
      </template>
    </el-dialog>

    <!-- 群聊成员管理弹窗 -->
    <el-dialog v-model="showMemberManagement" title="群聊成员管理" width="800px">
      <div v-if="currentRoom">
        <div class="member-header">
          <span>{{ currentRoom.name }} - 成员管理</span>
          <el-button type="primary" @click="showAddMember = true">添加成员</el-button>
        </div>
        
        <el-table :data="roomMembers" style="width: 100%">
          <el-table-column label="用户信息" width="200">
            <template #default="{ row }">
              <div class="user-info">
                <el-avatar :src="row.user.avatar" :size="40">
                  {{ row.user.nickname?.[0] || row.user.username[0] }}
                </el-avatar>
                <div class="user-details">
                  <div class="username">{{ row.user.nickname || row.user.username }}</div>
                  <el-tag :type="getRoleTagType(row.user.role)" size="small">
                    {{ getRoleText(row.user.role) }}
                  </el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="角色" width="100">
            <template #default="{ row }">
              <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
                {{ row.role === 'admin' ? '管理员' : '成员' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="joined_at" label="加入时间" width="180" />
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button-group>
                <el-button 
                  size="small" 
                  :type="row.role === 'admin' ? 'warning' : 'primary'"
                  @click="toggleMemberRole(row)"
                >
                  {{ row.role === 'admin' ? '取消管理' : '设为管理' }}
                </el-button>
                <el-button size="small" type="danger" @click="removeMember(row)">移除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, User, ArrowRight } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'

// 接口定义
interface ChatMessage {
  id: number
  sender: {
    id: number
    username: string
    nickname?: string
    avatar?: string
    role: string
  }
  receiver: {
    id: number
    username: string
    nickname?: string
    avatar?: string
    role: string
  }
  content: string
  media_url?: string
  media_type?: string
  is_read: boolean
  created_at: string
}

interface ChatRoom {
  id: number
  name: string
  description?: string
  type: string
  avatar?: string
  creator?: {
    id: number
    username: string
    nickname?: string
  }
  member_count: number
  last_message_at?: string
  is_active: boolean
  created_at: string
}

interface RoomMember {
  id: number
  user: {
    id: number
    username: string
    nickname?: string
    avatar?: string
    role: string
  }
  role: string
  joined_at: string
}

// 响应式数据
const activeTab = ref('messages')
const messageLoading = ref(false)
const roomLoading = ref(false)
const messages = ref<ChatMessage[]>([])
const rooms = ref<ChatRoom[]>([])
const selectedMessages = ref<ChatMessage[]>([])
const showMessageDetail = ref(false)
const showCreateRoom = ref(false)
const showMemberManagement = ref(false)
const showAddMember = ref(false)
const currentMessage = ref<ChatMessage | null>(null)
const currentRoom = ref<ChatRoom | null>(null)
const roomMembers = ref<RoomMember[]>([])

// 筛选条件
const messageFilters = reactive({
  keyword: '',
  senderRole: '',
  receiverRole: '',
  dateRange: null as any
})

const roomFilters = reactive({
  keyword: '',
  type: '',
  status: '',
  minMembers: null as number | null
})

// 分页
const messagePagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

const roomPagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 表单数据
const roomForm = reactive({
  name: '',
  description: '',
  type: '',
  avatar: ''
})

// 表单验证规则
const roomRules = {
  name: [{ required: true, message: '请输入群聊名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择群聊类型', trigger: 'change' }]
}

// 辅助函数
const getRoleText = (role: string) => {
  const roleMap: Record<string, string> = {
    elderly: '老年人',
    child: '子女',
    volunteer: '志愿者',
    teacher: '教师',
    doctor: '医生',
    admin: '管理员'
  }
  return roleMap[role] || role
}

const getRoleTagType = (role: string) => {
  const typeMap: Record<string, string> = {
    elderly: 'success',
    child: 'primary',
    volunteer: 'warning',
    teacher: 'info',
    doctor: 'danger',
    admin: 'danger'
  }
  return typeMap[role] || ''
}

const getRoomTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    system: '系统群聊',
    user: '用户群聊',
    course: '课程群聊',
    challenge: '挑战群聊'
  }
  return typeMap[type] || type
}

const getRoomTypeTagType = (type: string) => {
  const typeMap: Record<string, string> = {
    system: 'danger',
    user: 'primary',
    course: 'success',
    challenge: 'warning'
  }
  return typeMap[type] || ''
}

// 消息相关方法
const loadMessages = async () => {
  messageLoading.value = true
  try {
    const response = await fetch(`/api/v1/chat/admin/messages?${new URLSearchParams({
      skip: ((messagePagination.page - 1) * messagePagination.size).toString(),
      limit: messagePagination.size.toString(),
      ...(messageFilters.keyword && { keyword: messageFilters.keyword }),
      ...(messageFilters.senderRole && { sender_role: messageFilters.senderRole }),
      ...(messageFilters.receiverRole && { receiver_role: messageFilters.receiverRole }),
      ...(messageFilters.dateRange && messageFilters.dateRange[0] && { start_date: messageFilters.dateRange[0] }),
      ...(messageFilters.dateRange && messageFilters.dateRange[1] && { end_date: messageFilters.dateRange[1] })
    })}`)
    
    if (!response.ok) {
      throw new Error('获取消息列表失败')
    }
    
    const data = await response.json()
    messages.value = data.data || []
    messagePagination.total = data.total || 0
  } catch (error) {
    ElMessage.error('加载消息列表失败')
    // 回退到模拟数据
    messages.value = [
      {
        id: 1,
        sender: {
          id: 1,
          username: 'zhangsan',
          nickname: '张大爷',
          avatar: '',
          role: 'elderly'
        },
        receiver: {
          id: 2,
          username: 'lisi',
          nickname: '李医生',
          avatar: '',
          role: 'doctor'
        },
        content: '李医生，我最近腰疼，能帮我看看吗？',
        is_read: true,
        created_at: '2024-01-20 09:30:00'
      }
    ]
    messagePagination.total = 1
  } finally {
    messageLoading.value = false
  }
}

const loadRooms = async () => {
  roomLoading.value = true
  try {
    // TODO: 调用API
    // 模拟数据
    rooms.value = [
      {
        id: 1,
        name: '舞蹈交流群',
        description: '老年人舞蹈学习交流群',
        type: 'user',
        avatar: '',
        creator: {
          id: 1,
          username: 'admin',
          nickname: '管理员'
        },
        member_count: 25,
        last_message_at: '2024-01-20 15:30:00',
        is_active: true,
        created_at: '2024-01-01 09:00:00'
      }
    ]
    roomPagination.total = 1
  } catch (error) {
    ElMessage.error('加载群聊列表失败')
  } finally {
    roomLoading.value = false
  }
}

const searchMessages = () => {
  messagePagination.page = 1
  loadMessages()
}

const resetMessageFilters = () => {
  Object.assign(messageFilters, {
    keyword: '',
    senderRole: '',
    receiverRole: '',
    dateRange: null
  })
  searchMessages()
}

const searchRooms = () => {
  roomPagination.page = 1
  loadRooms()
}

const resetRoomFilters = () => {
  Object.assign(roomFilters, {
    keyword: '',
    type: '',
    status: '',
    minMembers: null
  })
  searchRooms()
}

const handleMessageSelectionChange = (selection: ChatMessage[]) => {
  selectedMessages.value = selection
}

const viewMessage = (message: ChatMessage) => {
  currentMessage.value = message
  showMessageDetail.value = true
}

const deleteMessage = async (message: ChatMessage) => {
  try {
    await ElMessageBox.confirm('确定要删除这条消息吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // TODO: 调用API删除
    ElMessage.success('删除成功')
    loadMessages()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const batchDeleteMessages = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedMessages.value.length} 条消息吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // TODO: 调用API批量删除
    ElMessage.success('批量删除成功')
    selectedMessages.value = []
    loadMessages()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

// 群聊相关方法
const viewRoom = (room: ChatRoom) => {
  // TODO: 显示群聊详情
  ElMessage.info('查看群聊详情功能待开发')
}

const manageMembers = async (room: ChatRoom) => {
  currentRoom.value = room
  // TODO: 加载群聊成员
  roomMembers.value = [
    {
      id: 1,
      user: {
        id: 1,
        username: 'zhangsan',
        nickname: '张大爷',
        avatar: '',
        role: 'elderly'
      },
      role: 'member',
      joined_at: '2024-01-01 09:00:00'
    }
  ]
  showMemberManagement.value = true
}

const toggleRoomStatus = async (room: ChatRoom) => {
  try {
    // TODO: 调用API
    room.is_active = !room.is_active
    ElMessage.success(room.is_active ? '群聊已启用' : '群聊已停用')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteRoom = async (room: ChatRoom) => {
  try {
    await ElMessageBox.confirm('确定要删除这个群聊吗？删除后无法恢复！', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // TODO: 调用API删除
    ElMessage.success('删除成功')
    loadRooms()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const createRoom = async () => {
  try {
    // TODO: 表单验证和API调用
    ElMessage.success('群聊创建成功')
    showCreateRoom.value = false
    Object.assign(roomForm, {
      name: '',
      description: '',
      type: '',
      avatar: ''
    })
    loadRooms()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const toggleMemberRole = async (member: RoomMember) => {
  try {
    // TODO: 调用API
    member.role = member.role === 'admin' ? 'member' : 'admin'
    ElMessage.success(member.role === 'admin' ? '已设为管理员' : '已取消管理员')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const removeMember = async (member: RoomMember) => {
  try {
    await ElMessageBox.confirm('确定要移除这个成员吗？', '确认移除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // TODO: 调用API移除
    ElMessage.success('成员已移除')
    // 重新加载成员列表
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('移除失败')
    }
  }
}

// 分页处理
const handleMessageSizeChange = (size: number) => {
  messagePagination.size = size
  loadMessages()
}

const handleMessageCurrentChange = (page: number) => {
  messagePagination.page = page
  loadMessages()
}

const handleRoomSizeChange = (size: number) => {
  roomPagination.size = size
  loadRooms()
}

const handleRoomCurrentChange = (page: number) => {
  roomPagination.page = page
  loadRooms()
}

onMounted(() => {
  loadMessages()
  loadRooms()
})
</script>

<style scoped>
.chat-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-row {
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.username {
  font-weight: 500;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message-text {
  color: #333;
  line-height: 1.4;
}

.room-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.room-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.room-name {
  font-weight: 500;
  color: #333;
}

.room-desc {
  font-size: 12px;
  color: #666;
}

.member-badge {
  margin-right: 10px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.message-detail {
  padding: 20px;
}

.message-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.sender-info,
.receiver-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sender-name,
.receiver-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.send-time {
  font-size: 12px;
  color: #999;
}

.message-body {
  line-height: 1.6;
}

.message-body p {
  margin: 0 0 15px 0;
  color: #333;
}

.message-media img,
.message-media video {
  max-width: 100%;
  border-radius: 8px;
}

.member-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}
</style> 