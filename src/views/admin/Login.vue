<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

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

const handleLogin = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  
  // 检查是否同意所有协议
  if (!Object.values(agreements).every(val => val === true)) {
    ElMessage.warning('请阅读并同意所有用户协议')
    return
  }
  
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

.agreements-section {
  margin-bottom: 20px;
}

.agreements-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style> 