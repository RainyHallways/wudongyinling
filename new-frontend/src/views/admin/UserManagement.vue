<template>
  <div class="user-management-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>用户管理</h2>
          <div class="header-actions">
            <el-input
              v-model="searchQuery"
              placeholder="搜索用户名/邮箱"
              clearable
              @clear="fetchUsers"
              @keyup.enter="handleSearch"
              class="search-input"
            >
              <template #append>
                <el-button @click="handleSearch">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
            
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              添加用户
            </el-button>
          </div>
        </div>
      </template>

      <!-- 用户表格 -->
      <el-table 
        :data="users" 
        v-loading="loading" 
        border 
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="nickname" label="昵称" min-width="120">
          <template #default="{ row }">
            {{ row.nickname || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">
              {{ getRoleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" size="small" @click="handleEdit(row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button type="warning" size="small" @click="handleResetPwd(row)">
                <el-icon><Key /></el-icon>
                重置密码
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(row)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.limit"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="formTitle"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="教师" value="teacher" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch
            v-model="form.is_active"
            :active-value="true"
            :inactive-value="false"
            active-text="正常"
            inactive-text="禁用"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPwdDialogVisible"
      title="重置密码"
      width="400px"
      destroy-on-close
    >
      <el-form
        ref="resetPwdFormRef"
        :model="resetPwdForm"
        :rules="resetPwdRules"
        label-width="100px"
      >
        <el-form-item label="新密码" prop="password">
          <el-input v-model="resetPwdForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="resetPwdForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetPwdDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitResetPwd" :loading="resetPwdLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userApi, type UserData, type UserQueryParams } from '@/api/user'
import { 
  Plus, 
  Edit, 
  Delete, 
  Search, 
  Key 
} from '@element-plus/icons-vue'

// 状态
const users = ref<UserData[]>([])
const loading = ref(false)
const total = ref(0)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const submitLoading = ref(false)
const resetPwdDialogVisible = ref(false)
const resetPwdLoading = ref(false)
const searchQuery = ref('')
const currentUserId = ref<number | null>(null)

// 表单引用
const formRef = ref<FormInstance>()
const resetPwdFormRef = ref<FormInstance>()

// 查询参数
const queryParams = reactive<UserQueryParams>({
  page: 1,
  limit: 10,
  search: '',
  role: '',
  is_active: undefined
})

// 表单数据
const defaultForm = {
  username: '',
  nickname: '',
  email: '',
  password: '',
  role: 'user',
  is_active: true
}

const form = reactive({ ...defaultForm })

// 重置密码表单
const resetPwdForm = reactive({
  password: '',
  confirmPassword: ''
})

// 表单验证规则
const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度应为3到20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
})

// 重置密码表单验证规则
const resetPwdRules = reactive<FormRules>({
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== resetPwdForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
})

// 计算属性
const formTitle = computed(() => dialogType.value === 'add' ? '添加用户' : '编辑用户')

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    // 转换参数格式
    const params: UserQueryParams = {
      skip: (queryParams.page - 1) * queryParams.limit,
      limit: queryParams.limit,
      search: queryParams.search,
      role: queryParams.role,
      is_active: queryParams.is_active
    }
    
    const res = await userApi.getUsers(params)
    users.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  queryParams.page = 1
  queryParams.search = searchQuery.value
  fetchUsers()
}

// 添加用户
const handleAdd = () => {
  dialogType.value = 'add'
  Object.assign(form, defaultForm)
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = (row: UserData) => {
  dialogType.value = 'edit'
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

// 删除用户
const handleDelete = async (row: UserData) => {
  try {
    await ElMessageBox.confirm(`确定要删除用户 "${row.username}" 吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await userApi.deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error('删除用户失败')
    }
  }
}

// 重置密码
const handleResetPwd = (row: UserData) => {
  currentUserId.value = row.id
  resetPwdForm.password = ''
  resetPwdForm.confirmPassword = ''
  resetPwdDialogVisible.value = true
}

// 提交重置密码
const submitResetPwd = async () => {
  if (!resetPwdFormRef.value) return
  
  await resetPwdFormRef.value.validate(async (valid) => {
    if (valid && currentUserId.value) {
      resetPwdLoading.value = true
      try {
        await userApi.resetPassword(currentUserId.value, { 
          password: resetPwdForm.password 
        })
        
        ElMessage.success('密码重置成功')
        resetPwdDialogVisible.value = false
      } catch (error) {
        console.error('重置密码失败:', error)
        ElMessage.error('重置密码失败')
      } finally {
        resetPwdLoading.value = false
      }
    }
  })
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (dialogType.value === 'add') {
          await userApi.createUser({
            username: form.username,
            email: form.email,
            password: form.password,
            role: form.role,
            is_active: form.is_active
          })
          ElMessage.success('添加成功')
        } else {
          await userApi.updateUser(form.id, {
            username: form.username,
            email: form.email,
            nickname: form.nickname,
            role: form.role,
            is_active: form.is_active
          })
          ElMessage.success('更新成功')
        }
        
        dialogVisible.value = false
        fetchUsers()
      } catch (error) {
        console.error(dialogType.value === 'add' ? '添加用户失败:' : '更新用户失败:', error)
        ElMessage.error(dialogType.value === 'add' ? '添加用户失败' : '更新用户失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 分页相关方法
const handleSizeChange = (val: number) => {
  queryParams.limit = val
  fetchUsers()
}

const handleCurrentChange = (val: number) => {
  queryParams.page = val
  fetchUsers()
}

// 角色标签类型
const getRoleType = (role: string): '' | 'success' | 'warning' | 'danger' => {
  switch (role) {
    case 'admin':
      return 'danger'
    case 'teacher':
      return 'warning'
    case 'user':
      return 'success'
    default:
      return ''
  }
}

// 角色标签文本
const getRoleLabel = (role: string): string => {
  switch (role) {
    case 'admin':
      return '管理员'
    case 'teacher':
      return '教师'
    case 'user':
      return '普通用户'
    default:
      return role
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-management-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.card-header h2 {
  margin: 0;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  width: 250px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .user-management-container {
    padding: 10px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
}
</style> 