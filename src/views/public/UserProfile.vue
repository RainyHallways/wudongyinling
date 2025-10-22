<template>
  <div class="user-profile-container page-with-nav">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <!-- 主要内容 -->
    <div v-else>
      <page-header title="个人中心" subtitle="管理您的账户信息和舞蹈历程"></page-header>
    
      <el-row :gutter="20">
        <!-- 左侧信息卡 -->
        <el-col :xs="24" :md="8">
          <el-card class="profile-card" shadow="hover">
          <div class="user-avatar-wrapper">
            <el-avatar :size="120" :src="userInfo.avatar || defaultAvatar"></el-avatar>
            <div class="edit-avatar">
              <el-button size="small" type="primary" circle>
                <el-icon><Edit /></el-icon>
              </el-button>
            </div>
          </div>
          
          <h2 class="user-name">{{ userInfo.nickname || '未设置昵称' }}</h2>
          <p class="user-email">{{ userInfo.email }}</p>
          
          <div class="user-stats">
            <div class="stat-item">
              <div class="stat-value">{{ userStats.danceHours || 0 }}</div>
              <div class="stat-label">舞蹈时长</div>
            </div>
            <el-divider direction="vertical" />
            <div class="stat-item">
              <div class="stat-value">{{ userStats.completedCourses || 0 }}</div>
              <div class="stat-label">完成课程</div>
            </div>
            <el-divider direction="vertical" />
            <div class="stat-item">
              <div class="stat-value">{{ userStats.achievements || 0 }}</div>
              <div class="stat-label">获得成就</div>
            </div>
          </div>
          
          <div class="user-level">
            <div class="level-text">
              <span class="level-label">当前等级:</span>
              <span class="level-value">{{ userLevel.name || '初学者' }}</span>
            </div>
            <el-progress :percentage="userLevel.progress || 0" :format="() => `${userLevel.currentExp || 0}/${userLevel.nextLevelExp || 100}`"></el-progress>
          </div>
          </el-card>
        </el-col>
        
        <!-- 右侧选项卡 -->
        <el-col :xs="24" :md="16">
        <el-card shadow="hover">
          <el-tabs v-model="activeTab" @tab-change="handleTabChange">
            <el-tab-pane label="基本信息" name="profile">
              <el-form 
                ref="profileFormRef"
                :model="userForm" 
                :rules="profileRules"
                label-width="100px"
              >
                <el-form-item label="用户昵称" prop="nickname">
                  <el-input v-model="userForm.nickname" placeholder="请输入昵称"></el-input>
                </el-form-item>
                
                <el-form-item label="性别" prop="gender">
                  <el-radio-group v-model="userForm.gender">
                                    <el-radio :value="1">男</el-radio>
                <el-radio :value="2">女</el-radio>
                <el-radio :value="0">保密</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="年龄" prop="age">
                  <el-input-number v-model="userForm.age" :min="1" :max="120"></el-input-number>
                </el-form-item>
                
                <el-form-item label="手机号码" prop="phone">
                  <el-input v-model="userForm.phone" placeholder="请输入手机号码"></el-input>
                </el-form-item>
                
                <el-form-item label="个人简介" prop="bio">
                  <el-input 
                    v-model="userForm.bio" 
                    type="textarea" 
                    placeholder="介绍一下自己吧" 
                    :rows="4">
                  </el-input>
                </el-form-item>
                
                <el-form-item>
                  <el-button 
                    type="primary" 
                    @click="saveUserInfo"
                    :loading="saving"
                  >
                    保存信息
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <el-tab-pane label="舞蹈历程" name="history">
              <el-empty v-if="danceHistory.length === 0" description="暂无舞蹈历程记录"></el-empty>
              <el-timeline v-else>
                <el-timeline-item
                  v-for="(history, index) in danceHistory"
                  :key="index"
                  :timestamp="history.date"
                  :type="history.type"
                >
                  {{ history.content }}
                </el-timeline-item>
              </el-timeline>
            </el-tab-pane>
            
            <el-tab-pane label="我的收藏" name="favorites">
              <el-empty v-if="favoriteCourses.length === 0" description="暂无收藏的课程"></el-empty>
              <div v-else class="course-grid">
                <el-card 
                  v-for="course in favoriteCourses" 
                  :key="course.id" 
                  class="course-card" 
                  shadow="hover"
                  @click="viewCourse(course.id)"
                >
                  <img :src="course.coverImg" class="course-cover" />
                  <div class="course-info">
                    <h3 class="course-title">{{ course.title }}</h3>
                    <div class="course-meta">
                      <el-tag size="small">{{ course.category }}</el-tag>
                      <div class="course-stats">
                        <span><el-icon><View /></el-icon> {{ course.viewCount }}</span>
                        <span><el-icon><Star /></el-icon> {{ course.favoriteCount }}</span>
                      </div>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="账号安全" name="security">
              <el-form label-width="100px">
                <el-form-item label="修改密码">
                  <el-button type="primary" @click="showChangePasswordDialog">修改密码</el-button>
                </el-form-item>
                
                <el-form-item label="绑定手机">
                  <div class="bind-status">
                    <span v-if="userInfo.phone">{{ maskPhone(userInfo.phone) }}</span>
                    <span v-else>未绑定</span>
                    <el-button type="primary" link @click="showBindPhoneDialog">
                      {{ userInfo.phone ? '更换' : '绑定' }}
                    </el-button>
                  </div>
                </el-form-item>
                
                <el-form-item label="绑定邮箱">
                  <div class="bind-status">
                    <span v-if="userInfo.email">{{ maskEmail(userInfo.email) }}</span>
                    <span v-else>未绑定</span>
                    <el-button type="primary" link @click="showBindEmailDialog">
                      {{ userInfo.email ? '更换' : '绑定' }}
                    </el-button>
                  </div>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <el-tab-pane label="修改密码" name="password">
              <el-form 
                ref="passwordFormRef"
                :model="passwordForm" 
                :rules="passwordRules"
                label-width="120px"
                style="max-width: 400px"
              >
                <el-form-item label="当前密码" prop="currentPassword">
                  <el-input 
                    v-model="passwordForm.currentPassword" 
                    type="password" 
                    placeholder="请输入当前密码"
                    show-password
                  />
                </el-form-item>
                
                <el-form-item label="新密码" prop="newPassword">
                  <el-input 
                    v-model="passwordForm.newPassword" 
                    type="password" 
                    placeholder="请输入新密码（至少6位）"
                    show-password
                  />
                </el-form-item>
                
                <el-form-item label="确认新密码" prop="confirmPassword">
                  <el-input 
                    v-model="passwordForm.confirmPassword" 
                    type="password" 
                    placeholder="请再次输入新密码"
                    show-password
                  />
                </el-form-item>
                
                <el-form-item>
                  <el-button 
                    type="primary" 
                    @click="changePassword"
                    :loading="passwordChanging"
                  >
                    修改密码
                  </el-button>
                  <el-button @click="resetPasswordForm">重置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
            </el-card>
          </el-col>
          </el-row>
      
      
      <!-- 修改密码对话框（保留作为备用） -->
      <el-dialog
      v-model="changePasswordDialog"
      title="修改密码"
      width="500px"
    >
      <el-form 
        ref="dialogPasswordFormRef"
        :model="dialogPasswordForm" 
        :rules="passwordRules"
        label-width="120px"
      >
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input 
            v-model="dialogPasswordForm.currentPassword" 
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input 
            v-model="dialogPasswordForm.newPassword" 
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input 
            v-model="dialogPasswordForm.confirmPassword" 
            type="password"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="changePasswordDialog = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="changePasswordFromDialog"
            :loading="passwordChanging"
          >
            确认
          </el-button>
        </span>
      </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { request } from '@/utils/request'
import PageHeader from '@/components/common/PageHeader.vue'
import { Edit, View, Star } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const defaultAvatar = '/images/default-avatar.png'

// 当前激活的标签页
const activeTab = ref('profile')

// 表单引用
const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()
const dialogPasswordFormRef = ref<FormInstance>()

// 加载状态
const saving = ref(false)
const passwordChanging = ref(false)

// 用户信息
const userInfo = ref({
  id: 1,
  username: 'user123',
  nickname: '舞动爱好者',
  email: 'user123@example.com',
  phone: '13800138000',
  avatar: null,
  gender: 1,
  age: 65,
  bio: '退休后爱上了舞蹈，希望通过舞蹈保持健康活力！'
})

// 用户表单数据
const userForm = reactive({
  nickname: userInfo.value.nickname,
  gender: userInfo.value.gender,
  age: userInfo.value.age,
  phone: userInfo.value.phone,
  bio: userInfo.value.bio
})

// 表单验证规则
const profileRules: FormRules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度应为2-20个字符', trigger: 'blur' }
  ],
  phone: [
    { 
      pattern: /^1[3-9]\d{9}$/, 
      message: '请输入正确的手机号码', 
      trigger: 'blur' 
    }
  ]
}

// 用户统计数据
const userStats = ref({
  danceHours: 32,
  completedCourses: 8,
  achievements: 5
})

// 用户等级信息
const userLevel = ref({
  name: '舞蹈新手',
  currentExp: 75,
  nextLevelExp: 100,
  progress: 75
})

// 舞蹈历程
const danceHistory = ref([
  {
    date: '2023-05-10',
    type: 'success',
    content: '完成了第一个基础舞蹈课程《舞动基础入门》'
  },
  {
    date: '2023-06-01',
    type: 'primary',
    content: '参加了线上舞蹈挑战，获得"初级舞者"称号'
  },
  {
    date: '2023-07-15',
    type: 'success',
    content: '完成了《中国古典舞基础》课程，达到初级水平'
  }
])

// 收藏的课程
const favoriteCourses = ref([
  {
    id: 1,
    title: '太极舞基础入门',
    coverImg: '/images/dance1.jpg',
    category: '太极舞',
    viewCount: 1253,
    favoriteCount: 328
  },
  {
    id: 2,
    title: '广场舞健身课程',
    coverImg: '/images/dance2.jpg',
    category: '广场舞',
    viewCount: 2156,
    favoriteCount: 512
  },
  {
    id: 3,
    title: '民族舞蹈欣赏',
    coverImg: '/images/dance3.jpg',
    category: '民族舞',
    viewCount: 1855,
    favoriteCount: 423
  }
])

// 修改密码相关
const changePasswordDialog = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const dialogPasswordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 密码验证规则
const passwordRules: FormRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword && value !== dialogPasswordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 监听路由参数变化
watch(() => route.query.tab, (newTab) => {
  if (newTab && typeof newTab === 'string') {
    activeTab.value = newTab
  }
}, { immediate: true })

// 加载状态
const loading = ref(true)

// 页面加载时获取用户数据
onMounted(async () => {
  // 模拟数据加载
  await new Promise(resolve => setTimeout(resolve, 800))
  await fetchUserData()
  loading.value = false
  
  // 检查路由参数中的tab
  if (route.query.tab) {
    activeTab.value = route.query.tab as string
  }
})

// 标签页切换处理
const handleTabChange = (tabName: string) => {
  // 更新路由参数，但不刷新页面
  router.replace({ 
    path: route.path, 
    query: { ...route.query, tab: tabName }
  })
}

// 获取用户数据
const fetchUserData = async () => {
  try {
    // 从用户store获取当前用户信息
    if (userStore.userInfo && userStore.userInfo.id) {
      userInfo.value = { ...userInfo.value, ...userStore.userInfo }
      
      // 更新表单数据
      Object.assign(userForm, {
        nickname: userInfo.value.nickname,
        gender: userInfo.value.gender,
        age: userInfo.value.age,
        phone: userInfo.value.phone,
        bio: userInfo.value.bio
      })
    }
    
    // 模拟获取用户统计数据
    userStats.value = {
      danceHours: Math.floor(Math.random() * 100) + 10,
      completedCourses: Math.floor(Math.random() * 20) + 1,
      achievements: Math.floor(Math.random() * 15) + 1
    }
    
    userLevel.value = {
      name: '舞蹈新手',
      currentExp: Math.floor(Math.random() * 100),
      nextLevelExp: 100,
      progress: Math.floor(Math.random() * 100)
    }
    
    // 获取用户详细信息的API调用可以在这里添加
    // const response = await request.get(`/users/${userStore.userInfo.id}`)
    // userInfo.value = response
  } catch (error) {
    console.error('获取用户数据失败:', error)
    ElMessage.error('获取用户数据失败，请稍后重试')
  }
}

// 保存用户信息
const saveUserInfo = async () => {
  if (!profileFormRef.value) return
  
  try {
    const valid = await profileFormRef.value.validate()
    if (!valid) return
    
    saving.value = true
    
    // API调用保存用户信息
    // await request.put(`/users/${userInfo.value.id}`, userForm)
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 更新本地userInfo数据
    Object.assign(userInfo.value, userForm)
    
    // 更新用户store中的信息
    userStore.setUserInfo({ ...userStore.userInfo, ...userForm })
    
    ElMessage.success('个人信息保存成功')
  } catch (error) {
    console.error('保存用户信息失败:', error)
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    saving.value = false
  }
}

// 修改密码
const changePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    const valid = await passwordFormRef.value.validate()
    if (!valid) return
    
    passwordChanging.value = true
    
    // 调用后端API修改密码
    await request.patch(`/users/${userInfo.value.id}/change-password`, {
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword,
      confirm_password: passwordForm.confirmPassword
    })
    
    ElMessage.success('密码修改成功')
    resetPasswordForm()
    
    // 提示用户重新登录
    ElMessageBox.confirm(
      '密码修改成功，为了安全起见，请重新登录',
      '提示',
      {
        confirmButtonText: '重新登录',
        cancelButtonText: '稍后登录',
        type: 'success'
      }
    ).then(() => {
      userStore.logout()
    }).catch(() => {
      // 用户选择稍后登录
    })
    
  } catch (error: any) {
    console.error('修改密码失败:', error)
    const message = error.response?.data?.detail || '修改密码失败，请稍后重试'
    ElMessage.error(message)
  } finally {
    passwordChanging.value = false
  }
}

// 从对话框修改密码
const changePasswordFromDialog = async () => {
  if (!dialogPasswordFormRef.value) return
  
  try {
    const valid = await dialogPasswordFormRef.value.validate()
    if (!valid) return
    
    passwordChanging.value = true
    
    // 调用后端API修改密码
    await request.patch(`/users/${userInfo.value.id}/change-password`, {
      current_password: dialogPasswordForm.currentPassword,
      new_password: dialogPasswordForm.newPassword,
      confirm_password: dialogPasswordForm.confirmPassword
    })
    
    ElMessage.success('密码修改成功')
    changePasswordDialog.value = false
    resetDialogPasswordForm()
    
    // 提示用户重新登录
    ElMessageBox.confirm(
      '密码修改成功，为了安全起见，请重新登录',
      '提示',
      {
        confirmButtonText: '重新登录',
        cancelButtonText: '稍后登录',
        type: 'success'
      }
    ).then(() => {
      userStore.logout()
    }).catch(() => {
      // 用户选择稍后登录
    })
    
  } catch (error: any) {
    console.error('修改密码失败:', error)
    const message = error.response?.data?.detail || '修改密码失败，请稍后重试'
    ElMessage.error(message)
  } finally {
    passwordChanging.value = false
  }
}

// 重置密码表单
const resetPasswordForm = () => {
  Object.assign(passwordForm, {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  passwordFormRef.value?.clearValidate()
}

const resetDialogPasswordForm = () => {
  Object.assign(dialogPasswordForm, {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  dialogPasswordFormRef.value?.clearValidate()
}

// 查看课程详情
const viewCourse = (courseId: number) => {
  router.push(`/dance-courses/${courseId}`)
}

// 显示修改密码对话框
const showChangePasswordDialog = () => {
  changePasswordDialog.value = true
  resetDialogPasswordForm()
}

// 显示绑定手机对话框
const showBindPhoneDialog = () => {
  ElMessage.info('绑定手机功能开发中...')
}

// 显示绑定邮箱对话框
const showBindEmailDialog = () => {
  ElMessage.info('绑定邮箱功能开发中...')
}

// 手机号脱敏
const maskPhone = (phone: string) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 邮箱脱敏
const maskEmail = (email: string) => {
  if (!email) return ''
  const [username, domain] = email.split('@')
  return `${username.charAt(0)}***@${domain}`
}
</script>

<style scoped>
.user-profile-container {
  padding: 20px;
  padding-bottom: calc(20px + 65px + env(safe-area-inset-bottom)); /* 为底部导航留出空间 */
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

.loading-container {
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.profile-card {
  text-align: center;
  padding: 25px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.profile-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-success));
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.profile-card:hover::before {
  transform: scaleX(1);
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.user-avatar-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
}

.edit-avatar {
  position: absolute;
  right: 0;
  bottom: 0;
  transition: all 0.3s ease;
}

.edit-avatar .el-button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--el-color-primary);
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.edit-avatar .el-button:hover {
  transform: scale(1.1);
  background: var(--el-color-primary-dark-2);
}

.user-name {
  margin: 15px 0 8px 0;
  font-size: 26px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-email {
  color: var(--el-text-color-secondary);
  margin-bottom: 25px;
  font-size: 15px;
}

.user-stats {
  display: flex;
  justify-content: center;
  margin: 25px 0;
  padding: 20px;
  background: var(--el-fill-color-lighter);
  border-radius: 12px;
  gap: 10px;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 15px 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: white;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--el-color-primary);
  margin-bottom: 5px;
  display: block;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  font-weight: 500;
}

.user-level {
  margin: 25px 0;
  text-align: left;
  padding: 20px;
  background: linear-gradient(135deg, var(--el-fill-color-lighter), white);
  border-radius: 12px;
  border: 1px solid var(--el-border-color-light);
}

.level-text {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.level-label {
  color: var(--el-text-color-secondary);
  font-weight: 500;
}

.level-value {
  font-weight: 700;
  color: var(--el-color-success);
  font-size: 16px;
  background: var(--el-color-success-light-9);
  padding: 4px 12px;
  border-radius: 20px;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.course-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-cover {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.course-info {
  padding: 10px 0;
}

.course-title {
  margin: 5px 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
}

.course-stats {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #909399;
}

.bind-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 选项卡优化 */
:deep(.el-tabs__header) {
  margin-bottom: 25px;
}

:deep(.el-tabs__nav-wrap::after) {
  height: 2px;
  background: var(--el-border-color-light);
}

:deep(.el-tabs__item) {
  font-weight: 500;
  font-size: 15px;
  padding: 0 25px;
  height: 45px;
  line-height: 45px;
  transition: all 0.3s ease;
}

:deep(.el-tabs__item:hover) {
  color: var(--el-color-primary);
}

:deep(.el-tabs__item.is-active) {
  color: var(--el-color-primary);
  font-weight: 600;
}

:deep(.el-tabs__active-bar) {
  background: var(--el-color-primary);
  height: 3px;
  border-radius: 2px;
}

/* 表单优化 */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.4);
}

:deep(.el-textarea__inner) {
  border-radius: 8px;
}

/* 按钮优化 */
:deep(.el-button--primary) {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-profile-container {
    padding: 15px;
    padding-bottom: calc(15px + 65px + env(safe-area-inset-bottom));
  }
  
  .profile-card {
    padding: 20px 15px;
    margin-bottom: 20px;
  }
  
  .user-name {
    font-size: 22px;
  }
  
  .user-stats {
    padding: 15px;
    gap: 5px;
  }
  
  .stat-item {
    padding: 12px 8px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .user-level {
    padding: 15px;
  }
  
  .course-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
  
  /* 优化选项卡在移动端的显示 */
  :deep(.el-tabs__nav-wrap) {
    padding: 0 10px;
  }
  
  :deep(.el-tabs__item) {
    padding: 0 15px;
    font-size: 14px;
  }
  
  /* 优化表单在移动端的显示 */
  :deep(.el-form-item__label) {
    width: 80px !important;
    font-size: 14px;
  }
  
  :deep(.el-input__wrapper) {
    font-size: 16px; /* 防止iOS放大 */
  }
  
  :deep(.el-input__inner) {
    font-size: 16px;
  }
  
  :deep(.el-textarea__inner) {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .user-profile-container {
    padding: 10px;
    padding-bottom: calc(10px + 65px + env(safe-area-inset-bottom));
  }
  
  .profile-card {
    padding: 15px 10px;
  }
  
  .user-name {
    font-size: 20px;
  }
  
  .user-stats {
    flex-direction: column;
    padding: 10px;
    gap: 0;
  }
  
  .stat-item {
    padding: 15px 10px;
    border-bottom: 1px solid var(--el-border-color-lighter);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .stat-item:last-child {
    border-bottom: none;
  }
  
  .stat-value {
    font-size: 22px;
  }
  
  .stat-label {
    font-size: 13px;
  }
  
  .user-level {
    padding: 12px;
  }
  
  .level-text {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  /* 进一步优化小屏幕选项卡 */
  :deep(.el-tabs__item) {
    padding: 0 10px;
    font-size: 13px;
  }
  
  /* 优化表单布局 */
  :deep(.el-form) {
    padding: 0 5px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 18px;
  }
  
  :deep(.el-form-item__label) {
    width: 70px !important;
    font-size: 13px;
    line-height: 32px;
  }
  
  :deep(.el-form-item__content) {
    margin-left: 80px !important;
  }
  
  :deep(.el-button) {
    width: 100%;
    margin-top: 10px;
  }
  
  :deep(.el-button + .el-button) {
    margin-left: 0;
  }
  
  /* 优化进度条显示 */
  :deep(.el-progress) {
    margin-top: 10px;
  }
  
  :deep(.el-progress__text) {
    font-size: 12px !important;
  }
  
  /* 优化卡片网格 */
  .course-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 10px;
  }
  
  .course-cover {
    height: 100px;
  }
  
  .course-title {
    font-size: 14px;
    margin: 8px 0 4px;
  }
  
  .course-meta {
    font-size: 11px;
  }
}
</style> 