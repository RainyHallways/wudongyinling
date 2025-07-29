<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { userApi } from '@/api/user'

const router = useRouter()
const loading = ref(false)
const registerFormRef = ref<FormInstance>()

// 协议状态
const agreements = reactive({
  userAgreement: false,
  privacyPolicy: false,
  originalLicenseAgreement: false,
  userOriginalityGuarantee: false
})

// 全选复选框
const allAgreed = ref(false)

// 注册表单数据
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  nickname: '',
  role: 'elderly' as 'elderly' | 'child' | 'volunteer' | 'teacher',
  gender: '' as 'male' | 'female' | '',
  birthdate: '',
  phone: ''
})

// 表单验证规则
const registerRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email' as const, message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' },
    { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{6,}$/, message: '密码必须包含大小写字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: Function) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择用户角色', trigger: 'change' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
})

// 处理全选
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
        const registerData = {
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
          nickname: registerForm.nickname,
          role: registerForm.role,
          is_active: true
        }
        
        // 过滤空值字段
        const filteredData = Object.fromEntries(
          Object.entries(registerData).filter(([_, value]) => value !== '' && value !== null && value !== undefined)
        )
        
        await userApi.register(filteredData)
        
        ElMessage.success('注册成功！请登录')
        router.push('/login')
      } catch (error: any) {
        console.error('Registration failed:', error)
        ElMessage.error(error.message || '注册失败，请检查信息后重试')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <div class="register-container page-with-nav">
    <ElCard class="register-card">
      <template #header>
        <div class="card-header">
          <h2>舞动银龄 - 用户注册</h2>
        </div>
      </template>
      
      <ElForm ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="100px" @submit.prevent="handleRegister">
        <ElFormItem label="用户名" prop="username">
          <ElInput
            v-model="registerForm.username"
            placeholder="请输入用户名（3-20个字符，支持字母数字下划线）"
          ></ElInput>
        </ElFormItem>
        
        <ElFormItem label="昵称" prop="nickname">
          <ElInput
            v-model="registerForm.nickname"
            placeholder="请输入昵称（2-20个字符）"
          ></ElInput>
        </ElFormItem>
        
        <ElFormItem label="邮箱" prop="email">
          <ElInput
            v-model="registerForm.email"
            placeholder="请输入邮箱地址"
            type="email"
          ></ElInput>
        </ElFormItem>
        
        <ElFormItem label="手机号" prop="phone">
          <ElInput
            v-model="registerForm.phone"
            placeholder="请输入手机号码（可选）"
          ></ElInput>
        </ElFormItem>
        
        <ElFormItem label="用户角色" prop="role">
          <ElSelect v-model="registerForm.role" placeholder="请选择用户角色">
            <ElOption label="老年人" value="elderly" />
            <ElOption label="子女" value="child" />
            <ElOption label="志愿者" value="volunteer" />
            <ElOption label="教师" value="teacher" />
          </ElSelect>
        </ElFormItem>
        
        <ElFormItem label="性别">
          <ElRadioGroup v-model="registerForm.gender">
            <ElRadio label="male">男</ElRadio>
            <ElRadio label="female">女</ElRadio>
          </ElRadioGroup>
        </ElFormItem>
        
        <ElFormItem label="出生日期">
          <ElDatePicker
            v-model="registerForm.birthdate"
            type="date"
            placeholder="请选择出生日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </ElFormItem>
        
        <ElFormItem label="密码" prop="password">
          <ElInput
            v-model="registerForm.password"
            placeholder="请输入密码（至少6位，包含大小写字母和数字）"
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