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
        <ElTableColumn prop="email" label="邮箱" />
        <ElTableColumn prop="role" label="角色">
          <template #default="{ row }">
            <ElTag :type="row.role === 'admin' ? 'danger' : row.role === 'teacher' ? 'warning' : 'info'">
              {{ row.role }}
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
        <ElTableColumn label="操作" width="200">
          <template #default="{ row }">
            <ElButtonGroup>
              <ElButton type="primary" @click="handleEdit(row)">编辑</ElButton>
              <ElButton type="danger" @click="handleDelete(row)">删除</ElButton>
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

    <!-- 用户表单对话框 -->
    <ElDialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
      width="500px"
    >
      <ElForm
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <ElFormItem label="用户名" prop="username">
          <ElInput v-model="form.username" />
        </ElFormItem>
        <ElFormItem label="邮箱" prop="email">
          <ElInput v-model="form.email" />
        </ElFormItem>
        <ElFormItem label="密码" prop="password" v-if="dialogType === 'add'">
          <ElInput v-model="form.password" type="password" />
        </ElFormItem>
        <ElFormItem label="角色" prop="role">
          <ElSelect v-model="form.role">
            <ElOption label="管理员" value="admin" />
            <ElOption label="教师" value="teacher" />
            <ElOption label="用户" value="user" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="状态" prop="is_active">
          <ElSwitch v-model="form.is_active" />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

// 这里应该导入用户相关的API，但目前还没有创建，先注释掉
// import { getUsers, register, updateUser, deleteUser } from '@/api/user'

interface User {
  id: string | number
  username: string
  email: string
  password?: string
  role: 'admin' | 'teacher' | 'user'
  is_active: boolean
}

interface UserQueryParams {
  skip: number
  limit: number
}

const users = ref<User[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

const form = ref<User>({
  id: '',
  username: '',
  email: '',
  password: '',
  role: 'user',
  is_active: true
})

const rules = reactive<FormRules>({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
})

const fetchUsers = async () => {
  loading.value = true
  try {
    // 模拟API调用，实际项目中应该使用真实API
    // const res = await getUsers({
    //   skip: (currentPage.value - 1) * pageSize.value,
    //   limit: pageSize.value
    // })
    // users.value = res.items
    // total.value = res.total
    
    // 模拟数据
    setTimeout(() => {
      users.value = [
        {
          id: 1,
          username: 'admin',
          email: 'admin@example.com',
          role: 'admin',
          is_active: true
        },
        {
          id: 2,
          username: 'teacher1',
          email: 'teacher1@example.com',
          role: 'teacher',
          is_active: true
        },
        {
          id: 3,
          username: 'user1',
          email: 'user1@example.com',
          role: 'user',
          is_active: true
        }
      ]
      total.value = 3
      loading.value = false
    }, 500)
  } catch (error) {
    ElMessage.error('获取用户列表失败')
    loading.value = false
  }
}

const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    id: '',
    username: '',
    email: '',
    password: '',
    role: 'user',
    is_active: true
  }
  dialogVisible.value = true
}

const handleEdit = (row: User) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      type: 'warning'
    })
    // await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          // await register(form.value)
          ElMessage.success('添加成功')
        } else {
          // await updateUser(form.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchUsers()
      } catch (error) {
        ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
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
</style> 