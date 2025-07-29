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

// 同意协议复选框
const agreements = reactive({
  userAgreement: false,
  privacyPolicy: false,
  originalLicenseAgreement: false,
  userOriginalityGuarantee: false
})

// 全选复选框
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

// 处理全选复选框变化
const handleAllAgreementsChange = (val: boolean) => {
  agreements.userAgreement = val
  agreements.privacyPolicy = val
  agreements.originalLicenseAgreement = val
  agreements.userOriginalityGuarantee = val
}

// 监听单个协议复选框变化更新全选状态
const updateAllAgreed = () => {
  allAgreed.value = Object.values(agreements).every(val => val === true)
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  // 检查是否同意所有协议
  if (!Object.values(agreements).every(val => val === true)) {
    ElMessage.warning('请阅读并同意所有用户协议')
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
  loginForm.password = '123456'
  
  // 自动同意所有协议
  allAgreed.value = true
  handleAllAgreementsChange(true)
  
  handleLogin()
}
</script>

<template>
  <div class="login-container page-with-nav">
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
        
        <ElDivider>用户协议</ElDivider>
        
        <div class="agreements-section">
          <ElCheckbox v-model="allAgreed" @change="handleAllAgreementsChange">
            全选
          </ElCheckbox>
          
          <div class="agreements-list">
            <ElCheckbox v-model="agreements.userAgreement" @change="updateAllAgreed">
              同意 <ElLink type="primary" @click.stop href="/policy/user-agreement" target="_blank">《网站协议》</ElLink>
            </ElCheckbox>
            
            <ElCheckbox v-model="agreements.privacyPolicy" @change="updateAllAgreed">
              同意 <ElLink type="primary" @click.stop href="/policy/privacy-policy" target="_blank">《隐私保护协议》</ElLink>
            </ElCheckbox>
            
            <ElCheckbox v-model="agreements.originalLicenseAgreement" @change="updateAllAgreed">
              同意 <ElLink type="primary" @click.stop href="/policy/original-license-agreement" target="_blank">《原创作品授权协议》</ElLink>
            </ElCheckbox>
            
            <ElCheckbox v-model="agreements.userOriginalityGuarantee" @change="updateAllAgreed">
              同意 <ElLink type="primary" @click.stop href="/policy/user-originality-guarantee" target="_blank">《原创性保证书》</ElLink>
            </ElCheckbox>
          </div>
        </div>
        
        <ElFormItem>
          <ElButton type="primary" native-type="submit" :loading="loading" class="login-button">
            登录
          </ElButton>
        </ElFormItem>
        
        <div class="login-tips">
          <p>演示账号: admin</p>
          <p>演示密码: 123456</p>
        </div>
        
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

.agreements-section {
  margin-bottom: 20px;
}

.agreements-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
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