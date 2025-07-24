<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import request from '@/utils/request'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const loginFormRef = ref<FormInstance>()

interface LoginForm {
  username: string
  password: string
  remember: boolean
}

const loginForm = reactive<LoginForm>({
  username: '',
  password: '',
  remember: false
})

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少为6个字符', trigger: 'blur' }
  ]
})

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const result = await userStore.login({
          username: loginForm.username,
          password: loginForm.password
        })
        
        if (result) {
          ElMessage.success('登录成功')
          
          // 重定向到之前的页面或首页
          const redirectPath = route.query.redirect as string || '/'
          await router.replace(redirectPath)
        }
      } catch (error) {
        console.error('Login failed:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

const demoLogin = () => {
  loginForm.username = 'admin'
  loginForm.password = 'admin'
  handleLogin()
}
</script>

<template>
  <div class="login-container">
    <ElCard class="login-card">
      <template #header>
        <div class="card-header">
          <h2>舞动银龄 - 用户登录</h2>
        </div>
      </template>
      
      <ElForm
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <ElFormItem label="用户名" prop="username">
          <ElInput v-model="loginForm.username" placeholder="请输入用户名"></ElInput>
        </ElFormItem>
        
        <ElFormItem label="密码" prop="password">
          <ElInput
            v-model="loginForm.password"
            placeholder="请输入密码"
            type="password"
            show-password
          ></ElInput>
        </ElFormItem>
        
        <ElFormItem>
          <ElCheckbox v-model="loginForm.remember">记住我</ElCheckbox>
        </ElFormItem>
        
        <ElFormItem>
          <ElButton type="primary" native-type="submit" :loading="loading" class="login-button">
            登录
          </ElButton>
        </ElFormItem>
        
        <div class="login-tips">
          <p>演示账号: admin</p>
          <p>演示密码: admin</p>
        </div>
        
        <div class="demo-login">
          <ElButton type="success" @click="demoLogin" :loading="loading">
            使用演示账号登录
          </ElButton>
        </div>
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
  max-width: 90%;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: var(--el-color-primary);
}

.login-button {
  width: 100%;
}

.login-tips {
  margin-top: 20px;
  background-color: var(--el-fill-color);
  padding: 10px;
  border-radius: 4px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.login-tips p {
  margin: 5px 0;
}

.demo-login {
  margin-top: 20px;
  text-align: center;
}

@media (max-width: 480px) {
  .login-card {
    width: 320px;
  }
}
</style> 