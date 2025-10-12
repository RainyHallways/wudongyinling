<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock,Key } from '@element-plus/icons-vue'
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
      <img src="/fonticon.png" alt="舞动银龄" class="logo-img" />
      <h2>登录到管理系统</h2>
      <ElForm
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="auto"
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
            <Key style="width: 1em; height: 1em; margin-right: 8px" /> 登录
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
}

.login-card {
  width: 400px;
  padding: 10px;
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.95);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.15);
}

.login-card h2 {
  text-align: center;
  margin-bottom: 30px;
  color: var(--el-text-color-primary);
  font-size: 23px;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 5px;
  transition: all 0.3s ease;
  border: none;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.el-form-item {
  margin-bottom: 24px;
}

.el-input {
  border-radius: 22px;
  height: 44px;
  transition: all 0.3s ease;
}

.el-input__wrapper {
  border-radius: 22px;
  height: 44px;
  border: 1px solid #e0e6ed;
}

.el-input__prefix {
  left: 15px;
}

.logo-img {
  height: 40px;
  width: auto;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
  display: block;
  margin: 0 auto 20px auto; /* 居中显示，并添加底部间距 */
}

.el-input__inner {
  height: 44px;
  padding-left: 45px;
  border-radius: 22px;
}

@media (max-width: 768px) {
  .login-card {
    width: 95%;
    max-width: 400px;
    padding: 30px 25px;
  }
  
  .login-card h2 {
    font-size: 20px;
    margin-bottom: 30px;
  }
}
</style>