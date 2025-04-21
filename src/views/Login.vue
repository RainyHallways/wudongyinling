<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>舞动银龄 - 用户登录</h2>
        </div>
      </template>
      
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            placeholder="请输入密码"
            type="password"
            show-password
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" class="login-button">
            登录
          </el-button>
        </el-form-item>
        
        <div class="login-tips">
          <p>演示账号: admin</p>
          <p>演示密码: admin</p>
        </div>
        
        <div class="demo-login">
          <el-button type="success" @click="demoLogin" :loading="loading">
            使用演示账号登录
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少为6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  loading.value = true
  try {
    const response = await request.post('/api/v1/auth/login', {
      username: loginForm.username,
      password: loginForm.password
    });

    if (response && response.access_token) {
      // 登录成功逻辑
      localStorage.setItem('user-token', response.access_token)
      // 假设后端返回了 user 信息，并存储
      if (response.user) {
        localStorage.setItem('user-info', JSON.stringify(response.user))
      }
      
      ElMessage.success('登录成功')
      
      // 触发 App.vue 更新状态 (通过导航到目标页)
      const redirectPath = route.query.redirect || '/'
      // 使用 replace 防止用户回退到登录页
      await router.replace(redirectPath) 
      // 手动调用 App.vue 的检查状态方法，确保导航栏立即更新
      // 注意：这需要 App.vue 暴露该方法，或者使用状态管理库
      // 简单起见，先依赖页面跳转触发 App.vue 的 onMounted

    } else {
      // 如果后端没有按预期返回 token
      ElMessage.error('登录失败，请稍后重试')
    }
  } catch (error) {
    // request 拦截器已经处理了 ElMessage 提示
    console.error('Login failed:', error)
  } finally {
    loading.value = false
  }
}

const demoLogin = () => {
  loginForm.username = 'admin'
  loginForm.password = 'admin'
  handleLogin()
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
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
  color: var(--primary-color);
}

.login-button {
  width: 100%;
}

.login-tips {
  margin-top: 20px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  color: #606266;
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