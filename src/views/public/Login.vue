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

// 将多个协议状态合并为一个
const allAgreed = ref(false)

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

  // 检查是否同意所有协议
  if (!allAgreed.value) {
    ElMessage.warning('请阅读并同意所有用户协议后登录')
    return
  }
  
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
  loginForm.password = 'admin123'
  
  // 自动同意所有协议
  allAgreed.value = true
  
  handleLogin()
}
</script>

<template>
  <div class="login-container">
    <div class="background-orb orb1"></div>
    <div class="background-orb orb2"></div>
    
    <ElCard class="login-card">
      <h2 class="login-title">舞动银龄 - 用户登录</h2>
      
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
        
        <div class="agreements-section-integrated">
          <ElCheckbox v-model="allAgreed">
            <span class="agreement-text">
              我已阅读并同意
              <ElLink type="primary" @click.stop href="/policy/user-agreement" target="_blank">《网站协议》</ElLink>
              <ElLink type="primary" @click.stop href="/policy/privacy-policy" target="_blank">《隐私保护协议》</ElLink>
              <ElLink type="primary" @click.stop href="/policy/original-license-agreement" target="_blank">《原创作品授权协议》</ElLink>
              <ElLink type="primary" @click.stop href="/policy/user-originality-guarantee" target="_blank">《原创性保证书》</ElLink>
            </span>
          </ElCheckbox>
        </div>
        
        <ElFormItem>
          <ElButton type="primary" native-type="submit" :loading="loading" class="login-button">
            登录
          </ElButton>
        </ElFormItem>
        
        <div class="demo-login">
          <ElButton type="success" @click="demoLogin" :loading="loading">
            使用演示账号登录
          </ElButton>
        </div>
        
        <div class="register-link">
          没有账号？<ElLink type="primary" href="/register">立即注册</ElLink>
        </div>
      </ElForm>
    </ElCard>
  </div>
</template>

<style scoped>
.login-container {
  position: relative;
  min-height: 100vh;
  padding-top: 64px;
  padding-bottom: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(45deg, #f7d060 0%, #a57c00 100%);
  overflow: hidden;
  z-index: 1;
}

@media (max-width: 640px) {
  .login-container {
    padding-top: 20px;
    padding-bottom: 80px;
  }
}

.background-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  z-index: 0;
}

.orb1 {
  width: 400px;
  height: 400px;
  background-color: rgba(255, 230, 150, 0.7);
  top: 5%;
  left: 10%;
  animation: moveOrb1 20s infinite alternate;
}

.orb2 {
  width: 450px;
  height: 450px;
  background-color: rgba(255, 190, 80, 0.5);
  bottom: 10%;
  right: 15%;
  animation: moveOrb2 25s infinite alternate-reverse;
}

@keyframes moveOrb1 {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(100px, -120px) scale(1.1); }
}

@keyframes moveOrb2 {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(-80px, 90px) scale(0.9); }
}

.login-card {
  width: 400px;
  max-width: 90%;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
  border-radius: 20px;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
  margin: 20px 0;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.3);
}

.login-title {
  text-align: center;
  margin: 0 0 30px 0;
  font-size: 24px;
  color: #5a4620;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.5);
  font-weight: 600;
}

.login-button {
  width: 100%;
}

.agreements-section-integrated {
  margin-bottom: 22px;
}

/* --- 修改开始 --- */
.agreements-section-integrated :deep(.el-checkbox) {
  /* 确保复选框容器不会限制内部文本的换行 */
  height: auto;
  /* 关键：让复选框的方块与多行文本的顶部对齐 */
  align-items: flex-start;
}

.agreements-section-integrated :deep(.el-checkbox__label) {
  /* 关键：允许文本换行 */
  white-space: normal;
}

.agreements-section-integrated .agreement-text {
  font-size: 13px;
  color: #606266;
  line-height: 1.6; /* 调整行高，让换行后更美观 */
}
/* --- 修改结束 --- */


.agreements-section-integrated :deep(.el-link) {
  vertical-align: baseline;
}

.demo-login {
  margin-top: 20px;
  text-align: center;
}

.register-link {
  margin-top: 15px;
  text-align: center;
}

@media (max-width: 480px) {
  .login-card {
    width: 320px;
  }
}
</style>