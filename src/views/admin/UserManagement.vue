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
        <ElTableColumn prop="username" label="用户名" />
        <ElTableColumn prop="unique_id" label="用户ID" />
        <ElTableColumn prop="email" label="邮箱" />
        <ElTableColumn prop="nickname" label="昵称" />
        <ElTableColumn prop="role" label="角色">
          <template #default="{ row }">
            <ElTag :type="getRoleType(row.role || (row.is_admin ? 'ADMIN' : 'USER'))">
              {{ getRoleText(row.role || (row.is_admin ? 'ADMIN' : 'USER')) }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="is_active" label="状态">
          <template #default="{ row }">
            <ElTag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="操作" width="280">
          <template #default="{ row }">
            <ElButtonGroup>
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
        <ElFormItem label="用户名" prop="username">
          <ElInput v-model="form.username" placeholder="请输入用户名" />
        </ElFormItem>
        <ElFormItem label="邮箱" prop="email">
          <ElInput v-model="form.email" placeholder="请输入邮箱" />
        </ElFormItem>
        <ElFormItem label="昵称" prop="nickname">
          <ElInput v-model="form.nickname" placeholder="请输入昵称" />
        </ElFormItem>
        <ElFormItem label="密码" prop="password" v-if="dialogType === 'add'">
          <ElInput v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </ElFormItem>
        <ElFormItem label="角色" prop="role">
          <ElSelect v-model="form.role" placeholder="请选择角色">
            <ElOption label="老年人" value="ELDERLY" />
            <ElOption label="子女" value="CHILD" />
            <ElOption label="志愿者" value="VOLUNTEER" />
            <ElOption label="教师" value="TEACHER" />
            <ElOption label="医生" value="DOCTOR" />
            <ElOption label="管理员" value="ADMIN" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="状态" prop="is_active">
          <ElSwitch v-model="form.is_active" />
        </ElFormItem>
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

const form = ref<Partial<User> & { password?: string }>({
  username: '',
  email: '',
  nickname: '',
  password: '',
  is_admin: false,
  is_active: true,
  role: 'USER'
})

const passwordForm = ref({
  userId: 0,
  password: '',
  confirmPassword: ''
})

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
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 