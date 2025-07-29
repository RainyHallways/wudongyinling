<template>
  <div class="users-container">
    <ElCard>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <ElButton type="primary" @click="handleAdd">添加用户</ElButton>
        </div>
      </template>

      <ElTable :data="users" v-loading="loading">
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
              <div>📧 {{ row.email }}</div>
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
            <ElButtonGroup>
              <ElButton type="info" size="small" @click="handleView(row)">详情</ElButton>
              <ElButton type="primary" size="small" @click="handleEdit(row)">编辑</ElButton>
              <ElButton type="warning" size="small" @click="handleResetPassword(row)">重置密码</ElButton>
              <ElButton type="danger" size="small" @click="handleDelete(row)">删除</ElButton>
            </ElButtonGroup>
          </template>
        </ElTableColumn>
      </ElTable>

      <div class="pagination">
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

    <!-- 添加/编辑用户对话框 -->
    <ElDialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
      width="500px"
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
      width="400px"
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
      width="600px"
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { request } from '@/utils/request'

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
    const response = await request.get('/users/', {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    
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
})
</script>

<style scoped>
.users-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

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
  font-size: 13px;
  color: #333;
  margin-bottom: 2px;
}

.nickname {
  font-size: 12px;
  color: #666;
  margin-bottom: 2px;
}

.unique-id {
  font-size: 11px;
  color: #999;
}

.contact-info {
  font-size: 12px;
  line-height: 1.5;
}

.personal-info {
  font-size: 12px;
  line-height: 1.5;
}

.text-gray-400 {
  color: #9ca3af;
}

.text-orange-600 {
  color: #ea580c;
}

.text-red-600 {
  color: #dc2626;
}

.text-green-600 {
  color: #16a34a;
}

.user-detail {
  max-height: 500px;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #e5e7eb;
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
  font-size: 13px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
  align-items: flex-start;
}

.detail-item label {
  font-weight: 500;
  color: #374151;
  margin-right: 8px;
  min-width: 100px;
}

.detail-item span {
  color: #6b7280;
  word-break: break-all;
}

.dialog-footer {
  text-align: right;
}

.dialog-footer .el-button {
  margin-left: 10px;
}
</style> 