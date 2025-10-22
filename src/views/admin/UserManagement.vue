<template>
  <div class="users-container admin-responsive">
    <!-- 搜索和筛选栏 -->
    <div class="search-filter-bar">
      <div class="search-filter-item search-input">
        <el-input 
          v-model="searchKeyword" 
          placeholder="搜索用户名、邮箱、昵称"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="search-filter-item">
        <el-select v-model="roleFilter" placeholder="角色筛选" clearable @change="handleSearch">
          <el-option label="全部" value="" />
          <el-option label="管理员" value="admin" />
          <el-option label="老年人" value="elderly" />
          <el-option label="子女" value="child" />
          <el-option label="志愿者" value="volunteer" />
          <el-option label="教师" value="teacher" />
          <el-option label="医生" value="doctor" />
        </el-select>
      </div>
      <div class="search-filter-item">
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="handleSearch">
          <el-option label="全部" value="" />
          <el-option label="正常" :value="true" />
          <el-option label="禁用" :value="false" />
        </el-select>
      </div>
      <div class="search-filter-actions">
        <el-button type="primary" @click="handleSearch" class="touch-friendly">搜索</el-button>
        <el-button @click="handleReset" class="touch-friendly">重置</el-button>
        <el-button type="success" @click="handleAdd" class="touch-friendly desktop-only">添加用户</el-button>
      </div>
    </div>

    <!-- 浮动添加按钮（移动端） -->
    <div class="floating-action-button mobile-only">
      <el-button type="success" circle size="large" @click="handleAdd">
        <el-icon><Plus /></el-icon>
      </el-button>
    </div>

    <!-- 桌面端表格 -->
    <ElCard class="desktop-table">
      <div class="table-container">
        <ElTable :data="users" v-loading="loading" class="admin-responsive">
          <ElTableColumn prop="id" label="ID" width="80" />
          <ElTableColumn label="基本信息" width="200">
            <template #default="{ row }">
              <div class="user-info">
                <el-avatar :src="row.avatar" :size="40">
                  {{ row.nickname?.[0] || row.username?.[0] }}
                </el-avatar>
                <div class="user-details">
                  <div class="username">{{ row.username }}</div>
                  <div class="nickname">{{ row.nickname || '未设置' }}</div>
                  <div class="unique-id">ID: {{ row.unique_id }}</div>
                </div>
              </div>
            </template>
          </ElTableColumn>
          <ElTableColumn label="联系信息" width="200">
            <template #default="{ row }">
              <div class="contact-info">
                <div class="mobile-wrap">📧 {{ row.email }}</div>
                <div v-if="row.phone">📱 {{ row.phone }}</div>
                <div v-else class="text-gray-400">📱 未设置</div>
              </div>
            </template>
          </ElTableColumn>
          <ElTableColumn label="个人信息" width="150">
            <template #default="{ row }">
              <div class="personal-info">
                <div v-if="row.gender">{{ getGenderText(row.gender) }}</div>
                <div v-if="row.birthdate">{{ formatAge(row.birthdate) }}岁</div>
                <div v-if="!row.gender && !row.birthdate" class="text-gray-400">未完善</div>
              </div>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="role" label="角色" width="100">
            <template #default="{ row }">
              <ElTag :type="getRoleType(row.role || (row.is_admin ? 'ADMIN' : 'USER'))">
                {{ getRoleText(row.role || (row.is_admin ? 'ADMIN' : 'USER')) }}
              </ElTag>
            </template>
          </ElTableColumn>
          <ElTableColumn label="健康信息" width="120" v-if="showHealthInfo">
            <template #default="{ row }">
              <div v-if="row.role === 'elderly' || row.role === 'ELDERLY'">
                <div v-if="row.medical_history" class="text-orange-600">有病史</div>
                <div v-if="row.chronic_diseases" class="text-red-600">有慢性病</div>
                <div v-if="!row.medical_history && !row.chronic_diseases" class="text-green-600">无记录</div>
              </div>
              <div v-else class="text-gray-400">-</div>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="is_active" label="状态" width="80">
            <template #default="{ row }">
              <ElTag :type="row.is_active ? 'success' : 'danger'">
                {{ row.is_active ? '正常' : '禁用' }}
              </ElTag>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="created_at" label="创建时间" width="120">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </ElTableColumn>
          <ElTableColumn label="操作" width="280" fixed="right">
            <template #default="{ row }">
              <div class="table-actions">
                <el-dropdown trigger="click" class="dropdown-responsive">
                  <el-button type="primary" size="small">
                    操作 <el-icon><ArrowDown /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="handleView(row)">
                        <el-icon><View /></el-icon> 详情
                      </el-dropdown-item>
                      <el-dropdown-item @click="handleEdit(row)">
                        <el-icon><Edit /></el-icon> 编辑
                      </el-dropdown-item>
                      <el-dropdown-item @click="handleResetPassword(row)">
                        <el-icon><RefreshLeft /></el-icon> 重置密码
                      </el-dropdown-item>
                      <el-dropdown-item divided @click="handleDelete(row)" class="text-danger">
                        <el-icon><Delete /></el-icon> 删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>
          </ElTableColumn>
        </ElTable>
      </div>

      <div class="pagination-container">
        <ElPagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </ElCard>

    <!-- 移动端卡片列表 -->
    <div class="mobile-table-cards">
      <div v-for="user in users" :key="user.id" class="mobile-card-item" v-loading="loading">
        <div class="mobile-card-header">
          <div class="mobile-card-title">
            <el-avatar :src="user.avatar" :size="32" class="mobile-avatar">
              {{ user.nickname?.[0] || user.username?.[0] }}
            </el-avatar>
            <span>{{ user.username }}</span>
          </div>
          <div class="mobile-card-status">
            <ElTag :type="user.is_active ? 'success' : 'danger'">
              {{ user.is_active ? '正常' : '禁用' }}
            </ElTag>
            <ElTag :type="getRoleType(user.role || (user.is_admin ? 'ADMIN' : 'USER'))">
              {{ getRoleText(user.role || (user.is_admin ? 'ADMIN' : 'USER')) }}
            </ElTag>
          </div>
        </div>
        
        <div class="mobile-card-content">
          <div class="mobile-card-field" v-if="user.email">
            <span class="mobile-card-label">邮箱：</span>
            <span class="mobile-card-value mobile-wrap">{{ user.email }}</span>
          </div>
          <div class="mobile-card-field" v-if="user.phone">
            <span class="mobile-card-label">手机：</span>
            <span class="mobile-card-value">{{ user.phone }}</span>
          </div>
          <div class="mobile-card-field" v-if="user.nickname">
            <span class="mobile-card-label">昵称：</span>
            <span class="mobile-card-value">{{ user.nickname }}</span>
          </div>
          <div class="mobile-card-field" v-if="user.gender || user.birthdate">
            <span class="mobile-card-label">个人信息：</span>
            <span class="mobile-card-value">
              <span v-if="user.gender">{{ getGenderText(user.gender) }}</span>
              <span v-if="user.birthdate"> {{ formatAge(user.birthdate) }}岁</span>
            </span>
          </div>
          <div class="mobile-card-field" v-if="user.unique_id">
            <span class="mobile-card-label">用户ID：</span>
            <span class="mobile-card-value">{{ user.unique_id }}</span>
          </div>
          <div class="mobile-card-field">
            <span class="mobile-card-label">创建时间：</span>
            <span class="mobile-card-value">{{ formatDate(user.created_at) }}</span>
          </div>
        </div>
        
        <div class="mobile-card-actions">
          <el-button type="info" size="small" @click="handleView(user)" class="touch-friendly">
            <el-icon><View /></el-icon> 详情
          </el-button>
          <el-button type="primary" size="small" @click="handleEdit(user)" class="touch-friendly">
            <el-icon><Edit /></el-icon> 编辑
          </el-button>
          <el-button type="warning" size="small" @click="handleResetPassword(user)" class="touch-friendly">
            <el-icon><RefreshLeft /></el-icon> 重置
          </el-button>
          <el-button type="danger" size="small" @click="handleDelete(user)" class="touch-friendly">
            <el-icon><Delete /></el-icon> 删除
          </el-button>
        </div>
      </div>
    </div>

    <!-- 添加/编辑用户对话框 -->
    <ElDialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
      :width="dialogWidth"
      class="dialog-responsive"
    >
      <ElForm ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="基本信息" name="basic">
            <ElFormItem label="用户名" prop="username">
              <ElInput v-model="form.username" placeholder="请输入用户名" />
            </ElFormItem>
            <ElFormItem label="邮箱" prop="email">
              <ElInput v-model="form.email" placeholder="请输入邮箱" />
            </ElFormItem>
            <ElFormItem label="手机号" prop="phone">
              <ElInput v-model="form.phone" placeholder="请输入手机号" />
            </ElFormItem>
            <ElFormItem label="昵称" prop="nickname">
              <ElInput v-model="form.nickname" placeholder="请输入昵称" />
            </ElFormItem>
            <ElFormItem label="密码" prop="password" v-if="dialogType === 'add'">
              <ElInput v-model="form.password" type="password" placeholder="请输入密码" show-password />
            </ElFormItem>
            <ElFormItem label="头像" prop="avatar">
              <ElInput v-model="form.avatar" placeholder="请输入头像URL" />
            </ElFormItem>
          </el-tab-pane>
          
          <el-tab-pane label="个人信息" name="personal">
            <ElFormItem label="性别" prop="gender">
              <ElRadioGroup v-model="form.gender">
                <ElRadio label="male">男</ElRadio>
                <ElRadio label="female">女</ElRadio>
              </ElRadioGroup>
            </ElFormItem>
            <ElFormItem label="出生日期" prop="birthdate">
              <ElDatePicker
                v-model="form.birthdate"
                type="date"
                placeholder="请选择出生日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </ElFormItem>
            <ElFormItem label="角色" prop="role">
              <ElSelect v-model="form.role" placeholder="请选择角色">
                <ElOption label="老年人" value="elderly" />
                <ElOption label="子女" value="child" />
                <ElOption label="志愿者" value="volunteer" />
                <ElOption label="教师" value="teacher" />
                <ElOption label="医生" value="doctor" />
                <ElOption label="管理员" value="admin" />
              </ElSelect>
            </ElFormItem>
            <ElFormItem label="状态" prop="is_active">
              <ElSwitch v-model="form.is_active" />
            </ElFormItem>
          </el-tab-pane>
          
          <el-tab-pane label="健康信息" name="health" v-if="form.role === 'elderly'">
            <ElFormItem label="病史" prop="medical_history">
              <ElInput
                v-model="form.medical_history"
                type="textarea"
                :rows="3"
                placeholder="请输入病史信息"
              />
            </ElFormItem>
            <ElFormItem label="慢性病" prop="chronic_diseases">
              <ElInput
                v-model="form.chronic_diseases"
                type="textarea"
                :rows="3"
                placeholder="请输入慢性病信息"
              />
            </ElFormItem>
            <ElFormItem label="紧急联系人" prop="emergency_contact">
              <ElInput v-model="form.emergency_contact" placeholder="请输入紧急联系人姓名" />
            </ElFormItem>
            <ElFormItem label="紧急联系电话" prop="emergency_phone">
              <ElInput v-model="form.emergency_phone" placeholder="请输入紧急联系电话" />
            </ElFormItem>
          </el-tab-pane>
        </el-tabs>
      </ElForm>
      
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="handleSubmit" :loading="submitting">
            {{ dialogType === 'add' ? '添加' : '更新' }}
          </ElButton>
        </span>
      </template>
    </ElDialog>

    <!-- 重置密码对话框 -->
    <ElDialog
      v-model="passwordDialogVisible"
      title="重置密码"
      :width="passwordDialogWidth"
      class="dialog-responsive"
    >
      <ElForm ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="100px">
        <ElFormItem label="新密码" prop="password">
          <ElInput 
            v-model="passwordForm.password" 
            type="password" 
            placeholder="请输入新密码（至少6位）" 
            show-password 
          />
        </ElFormItem>
        <ElFormItem label="确认密码" prop="confirmPassword">
          <ElInput 
            v-model="passwordForm.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码" 
            show-password 
          />
        </ElFormItem>
      </ElForm>
      
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="passwordDialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="handlePasswordSubmit" :loading="passwordResetting">
            重置密码
          </ElButton>
        </span>
      </template>
    </ElDialog>

    <!-- 用户详情对话框 -->
    <ElDialog
      v-model="viewDialogVisible"
      title="用户详情"
      :width="viewDialogWidth"
      class="dialog-responsive"
    >
      <div class="user-detail">
        <div class="detail-section">
          <h3>基本信息</h3>
          <div class="detail-grid">
            <div class="detail-item">
              <label>用户名：</label>
              <span>{{ viewUser.username }}</span>
            </div>
            <div class="detail-item">
              <label>邮箱：</label>
              <span>{{ viewUser.email }}</span>
            </div>
            <div class="detail-item">
              <label>手机号：</label>
              <span>{{ viewUser.phone || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <label>昵称：</label>
              <span>{{ viewUser.nickname || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <label>用户ID：</label>
              <span>{{ viewUser.unique_id }}</span>
            </div>
          </div>
        </div>
        
        <div class="detail-section">
          <h3>个人信息</h3>
          <div class="detail-grid">
            <div class="detail-item">
              <label>性别：</label>
              <span>{{ getGenderText(viewUser.gender) }}</span>
            </div>
            <div class="detail-item">
              <label>出生日期：</label>
              <span>{{ viewUser.birthdate || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <label>年龄：</label>
              <span>{{ viewUser.birthdate ? formatAge(viewUser.birthdate) + '岁' : '未知' }}</span>
            </div>
            <div class="detail-item">
              <label>角色：</label>
              <span>{{ getRoleText(viewUser.role) }}</span>
            </div>
            <div class="detail-item">
              <label>状态：</label>
              <ElTag :type="viewUser.is_active ? 'success' : 'danger'">
                {{ viewUser.is_active ? '正常' : '禁用' }}
              </ElTag>
            </div>
          </div>
        </div>
        
        <div class="detail-section" v-if="viewUser.role === 'elderly'">
          <h3>健康信息</h3>
          <div class="detail-grid">
            <div class="detail-item full-width">
              <label>病史：</label>
              <span>{{ viewUser.medical_history || '无' }}</span>
            </div>
            <div class="detail-item full-width">
              <label>慢性病：</label>
              <span>{{ viewUser.chronic_diseases || '无' }}</span>
            </div>
            <div class="detail-item">
              <label>紧急联系人：</label>
              <span>{{ viewUser.emergency_contact || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <label>紧急联系电话：</label>
              <span>{{ viewUser.emergency_phone || '未设置' }}</span>
            </div>
          </div>
        </div>
        
        <div class="detail-section">
          <h3>系统信息</h3>
          <div class="detail-grid">
            <div class="detail-item">
              <label>创建时间：</label>
              <span>{{ formatDate(viewUser.created_at) }}</span>
            </div>
            <div class="detail-item">
              <label>最后更新：</label>
              <span>{{ formatDate(viewUser.updated_at) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <ElButton @click="viewDialogVisible = false">关闭</ElButton>
        <ElButton type="primary" @click="handleEdit(viewUser); viewDialogVisible = false">编辑</ElButton>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { request } from '@/utils/request'
import { 
  Search, 
  Plus, 
  ArrowDown, 
  View, 
  Edit, 
  Delete, 
  RefreshLeft 
} from '@element-plus/icons-vue'

// 用户数据接口
interface User {
  id: number
  username: string
  email: string
  nickname?: string
  avatar?: string
  phone?: string
  is_admin: boolean
  is_active: boolean
  role?: 'USER' | 'ADMIN' | 'TEACHER' | 'DOCTOR'
  unique_id?: string
  created_at?: string
  updated_at?: string // Added for updated_at
  gender?: 'MALE' | 'FEMALE' | 'OTHER'
  birthdate?: string
  medical_history?: boolean
  chronic_diseases?: boolean
  emergency_contact?: string
  emergency_phone?: string
}

// 响应式数据
const users = ref<User[]>([])
const loading = ref(false)
const submitting = ref(false)
const passwordResetting = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const passwordDialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

const showHealthInfo = ref(true)
const activeTab = ref('basic')

// 搜索和筛选
const searchKeyword = ref('')
const roleFilter = ref('')
const statusFilter = ref('')

// 响应式相关
const isMobile = ref(false)

// 计算对话框宽度
const dialogWidth = computed(() => {
  return isMobile.value ? '95vw' : '600px'
})

const passwordDialogWidth = computed(() => {
  return isMobile.value ? '90vw' : '400px'
})

const viewDialogWidth = computed(() => {
  return isMobile.value ? '95vw' : '600px'
})

// 检测移动端
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

// 性别文本转换
const getGenderText = (gender: string) => {
  return gender === 'male' ? '男' : gender === 'female' ? '女' : '未设置'
}

// 计算年龄
const formatAge = (birthdate: string) => {
  if (!birthdate) return '未知'
  const birth = new Date(birthdate)
  const today = new Date()
  const age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    return age - 1
  }
  return age
}

// 搜索处理
const handleSearch = async () => {
  currentPage.value = 1
  await fetchUsers()
}

// 重置搜索
const handleReset = () => {
  searchKeyword.value = ''
  roleFilter.value = ''
  statusFilter.value = ''
  handleSearch()
}

// 查看用户详情
const handleView = (row: any) => {
  viewDialogVisible.value = true
  viewUser.value = { ...row }
}

// 表单数据
const form = ref({
  id: null,
  username: '',
  email: '',
  phone: '',
  nickname: '',
  password: '',
  avatar: '',
  gender: '',
  birthdate: '',
  role: 'elderly',
  is_active: true,
  medical_history: '',
  chronic_diseases: '',
  emergency_contact: '',
  emergency_phone: ''
})

// 用户详情对话框
const viewDialogVisible = ref(false)
const viewUser = ref({})

// 表单验证规则
const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 50, message: '密码长度为6-50个字符', trigger: 'blur' }
  ],
  nickname: [
    { max: 50, message: '昵称长度不能超过50个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择用户角色', trigger: 'change' }
  ]
})

const passwordRules = reactive<FormRules>({
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
})

// 获取角色标签类型
const getRoleType = (role: string) => {
  switch (role?.toUpperCase()) {
    case 'ADMIN':
      return 'danger'
    case 'TEACHER':
      return 'warning'
    case 'DOCTOR':
      return 'success'
    case 'VOLUNTEER':
      return 'primary'
    case 'CHILD':
      return 'info'
    case 'ELDERLY':
      return 'success'
    case 'USER':
    default:
      return 'success'
  }
}

// 获取角色文本
const getRoleText = (role: string) => {
  switch (role?.toUpperCase()) {
    case 'ADMIN':
      return '管理员'
    case 'TEACHER':
      return '教师'
    case 'DOCTOR':
      return '医生'
    case 'VOLUNTEER':
      return '志愿者'
    case 'CHILD':
      return '子女'
    case 'ELDERLY':
      return '老年人'
    case 'USER':
    default:
      return '老年人'
  }
}

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    const params: any = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    // 添加搜索和筛选参数
    if (searchKeyword.value.trim()) {
      params.search = searchKeyword.value.trim()
    }
    if (roleFilter.value) {
      params.role = roleFilter.value
    }
    if (statusFilter.value !== '') {
      params.is_active = statusFilter.value
    }
    
    const response = await request.get('/users/', params)
    
    // 检查响应格式
    console.log('用户列表响应:', response)
    
    // 处理分页响应
    if (response && typeof response === 'object' && response.data) {
      // 分页响应格式 {data: [...], total: number, page: number, page_size: number}
      users.value = response.data || []
      total.value = response.total || 0
    } else if (Array.isArray(response)) {
      // 直接数组响应
      users.value = response
      total.value = response.length
    } else {
      users.value = []
      total.value = 0
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
    users.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 添加用户
const handleAdd = () => {
  dialogType.value = 'add'
  
  // 重置表单验证
  if (formRef.value) {
    formRef.value.resetFields()
  }
  
  form.value = {
    username: '',
    email: '',
    nickname: '',
    password: '',
    is_admin: false,
    is_active: true,
    role: 'USER'
  }
  
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = (row: User) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  delete form.value.password // 编辑时不显示密码字段
  dialogVisible.value = true
}

// 删除用户
const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(`确定要删除用户 "${row.username}" 吗？`, '提示', {
      type: 'warning'
    })
    
    await request.delete(`/users/${row.id}`)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 重置密码
const handleResetPassword = (row: User) => {
  passwordForm.value = {
    userId: row.id,
    password: '',
    confirmPassword: ''
  }
  passwordDialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    submitting.value = true
    
    if (dialogType.value === 'add') {
      // 创建用户
      await request.post('/users', {
        username: form.value.username,
        email: form.value.email,
        nickname: form.value.nickname,
        password: form.value.password,
        is_admin: form.value.is_admin,
        is_active: form.value.is_active
      })
      ElMessage.success('添加成功')
    } else {
      // 更新用户
      await request.put(`/users/${form.value.id}`, {
        username: form.value.username,
        email: form.value.email,
        nickname: form.value.nickname,
        is_admin: form.value.is_admin,
        is_active: form.value.is_active
      })
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    fetchUsers()
  } catch (error: any) {
    console.error('操作失败:', error)
    
    // 显示具体的错误信息
    let errorMessage = dialogType.value === 'add' ? '添加失败' : '更新失败'
    
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.message) {
      errorMessage = error.message
    }
    
    ElMessage.error(errorMessage)
  } finally {
    submitting.value = false
  }
}

// 提交密码重置
const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value) return
  
  try {
    const valid = await passwordFormRef.value.validate()
    if (!valid) return
    
    passwordResetting.value = true
    
    await request.patch(`/users/${passwordForm.value.userId}/change-password`, {
      current_password: 'admin', // 管理员重置时的临时密码
      new_password: passwordForm.value.password,
      confirm_password: passwordForm.value.confirmPassword
    })
    
    ElMessage.success('密码重置成功')
    passwordDialogVisible.value = false
  } catch (error) {
    console.error('密码重置失败:', error)
    ElMessage.error('密码重置失败')
  } finally {
    passwordResetting.value = false
  }
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  fetchUsers()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchUsers()
}

onMounted(() => {
  fetchUsers()
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.users-container {
  padding: 16px;
  min-height: 100vh;
}

/* 搜索和筛选栏 */
.search-filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.search-filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 200px;
  flex: 1;
}

.search-filter-item.search-input {
  min-width: 250px;
  flex: 2;
}

.search-filter-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* 表格容器 */
.table-container {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
}

.table-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.table-actions .el-button {
  margin: 0;
  min-width: 80px;
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
  flex-wrap: wrap;
  gap: 12px;
}

/* 用户信息样式 */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.username {
  font-weight: 500;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.nickname {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.unique-id {
  font-size: 11px;
  color: var(--text-light);
}

.contact-info {
  font-size: 12px;
  line-height: 1.5;
}

.personal-info {
  font-size: 12px;
  line-height: 1.5;
}

.personal-info {
  font-size: 12px;
  line-height: 1.5;
}

/* 文本颜色工具类 */
.text-gray-400 {
  color: var(--text-light);
}

.text-orange-600 {
  color: var(--warning-color);
}

.text-red-600 {
  color: var(--error-color);
}

.text-green-600 {
  color: var(--success-color);
}

.text-danger {
  color: var(--error-color) !important;
}

/* 移动端头像 */
.mobile-avatar {
  margin-right: 8px;
}

/* 详情对话框样式 */
.user-detail {
  max-height: 500px;
  overflow-y: auto;
  padding: 16px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 8px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
  align-items: flex-start;
  flex-direction: column;
  gap: 4px;
}

.detail-item label {
  font-weight: 500;
  color: var(--text-secondary);
  margin-right: 8px;
  min-width: 100px;
  flex-shrink: 0;
}

.detail-item span {
  color: var(--text-primary);
  word-break: break-all;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 16px 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .users-container {
    padding: 12px;
  }
  
  .search-filter-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    padding: 12px;
  }
  
  .search-filter-item {
    width: 100%;
    min-width: auto;
    flex: none;
  }
  
  .search-filter-item.search-input {
    order: -1;
  }
  
  .search-filter-actions {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }
  
  .search-filter-actions .el-button {
    flex: 1;
    min-height: var(--mobile-button-height);
    font-size: 16px;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .detail-item label {
    min-width: auto;
    margin-right: 0;
    font-size: 15px;
  }
  
  .detail-item span {
    font-size: 15px;
  }
  
  .user-detail {
    max-height: 70vh;
    padding: 12px;
  }
  
  .dialog-footer {
    flex-direction: column;
    padding: 12px 16px 0;
  }
  
  .dialog-footer .el-button {
    width: 100%;
    min-height: var(--mobile-button-height);
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .users-container {
    padding: 8px;
  }
  
  .search-filter-bar {
    padding: 10px;
  }
  
  .detail-section {
    margin-bottom: 16px;
  }
  
  .detail-section h3 {
    font-size: 15px;
  }
  
  .dialog-footer {
    gap: 6px;
  }
}

</style> 