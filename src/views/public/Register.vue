<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { userApi } from '@/api/user'

const router = useRouter()
const loading = ref(false)
const registerFormRef = ref<FormInstance>()

// 同意协议复选框
const agreements = reactive({
  userAgreement: false,
  privacyPolicy: false,
  originalLicenseAgreement: false,
  userOriginalityGuarantee: false
})

// 全选复选框
const allAgreed = ref(false)

interface RegisterForm {
  username: string
  email: string
  password: string
  confirmPassword: string
}

const registerForm = reactive<RegisterForm>({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 表单验证规则
const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少为6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
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

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  // 检查是否同意所有协议
  if (!Object.values(agreements).every(val => val === true)) {
    ElMessage.warning('请阅读并同意所有用户协议')
    return
  }
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await userApi.register({
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
          role: 'user',
          is_active: true
        })
        
        ElMessage.success('注册成功，请登录')
        router.push('/login')
      } catch (error: any) {
        console.error('Registration failed:', error)
        ElMessage.error(error.message || '注册失败')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <div class="register-container">
    <ElCard class="register-card">
      <template #header>
        <div class="card-header">
          <h2>舞动银龄 - 用户注册</h2>
        </div>
      </template>
      
      <ElForm
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <ElFormItem label="用户名" prop="username">
          <ElInput v-model="registerForm.username" placeholder="请输入用户名"></ElInput>
        </ElFormItem>
        
        <ElFormItem label="邮箱" prop="email">
          <ElInput v-model="registerForm.email" placeholder="请输入邮箱"></ElInput>
        </ElFormItem>
        
        <ElFormItem label="密码" prop="password">
          <ElInput
            v-model="registerForm.password"
            placeholder="请输入密码"
            type="password"
            show-password
          ></ElInput>
        </ElFormItem>
        
        <ElFormItem label="确认密码" prop="confirmPassword">
          <ElInput
            v-model="registerForm.confirmPassword"
            placeholder="请确认密码"
            type="password"
            show-password
          ></ElInput>
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
          <ElButton type="primary" native-type="submit" :loading="loading" class="register-button">
            注册
          </ElButton>
        </ElFormItem>
        
        <div class="login-link">
          已有账号？<ElLink type="primary" href="/login">立即登录</ElLink>
        </div>
      </ElForm>
    </ElCard>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
  background-color: var(--el-fill-color-light);
}

.register-card {
  width: 450px;
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

.agreements-section {
  margin-bottom: 20px;
}

.agreements-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.register-button {
  width: 100%;
}

.login-link {
  margin-top: 15px;
  text-align: center;
}

@media (max-width: 480px) {
  .register-card {
    width: 320px;
  }
}
</style> 