<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

interface LoginForm {
  username: string
  password: string
}

const form = ref<LoginForm>({
  username: '',
  password: ''
})

const rules = ref<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
})

const handleLogin = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const success = await userStore.adminLogin({
          username: form.value.username,
          password: form.value.password
        })
        if (success) {
          ElMessage.success('登录成功')
          router.push('/admin')
        }
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <div class="login-container">
    <ElCard class="login-card">
      <h2>登录到舞动银龄管理系统</h2>
      <ElForm
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="0"
      >
        <ElFormItem prop="username">
          <ElInput
            v-model="form.username"
            placeholder="用户名"
            :prefix-icon="User"
          />
        </ElFormItem>
        <ElFormItem prop="password">
          <ElInput
            v-model="form.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            show-password
          />
        </ElFormItem>
        <ElFormItem>
          <ElButton
            type="primary"
            :loading="loading"
            class="login-button"
            @click="handleLogin(formRef)"
          >
            登录
          </ElButton>
        </ElFormItem>
      </ElForm>
    </ElCard>
  </div>
</template>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--el-fill-color-light);
}

.login-card {
  width: 400px;
  padding: 20px;
}

.login-card h2 {
  text-align: center;
  margin-bottom: 30px;
  color: var(--el-text-color-primary);
}

.login-button {
  width: 100%;
}
</style> 