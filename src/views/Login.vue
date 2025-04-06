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
          <p>演示账号: demo</p>
          <p>演示密码: demo123</p>
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

const handleLogin = () => {
  loading.value = true
  
  // 这里只是简单演示，实际项目中应该调用API进行验证
  setTimeout(() => {
    if (loginForm.username === 'demo' && loginForm.password === 'demo123') {
      // 登录成功逻辑
      localStorage.setItem('user-token', 'demo-token')
      localStorage.setItem('user-info', JSON.stringify({
        username: loginForm.username,
        role: 'user'
      }))
      
      ElMessage.success('登录成功')
      
      // 如果有重定向参数，跳转到对应页面，否则跳转到首页
      const redirectPath = route.query.redirect || '/'
      router.push(redirectPath)
    } else {
      ElMessage.error('用户名或密码错误')
    }
    loading.value = false
  }, 1000)
}

const demoLogin = () => {
  loginForm.username = 'demo'
  loginForm.password = 'demo123'
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