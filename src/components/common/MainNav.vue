<template>
  <header class="main-nav">
    <div class="container">
      <el-row class="nav-container">
        <el-col :span="6" class="logo-container">
          <router-link to="/" class="logo">
            <img src="/fonticon.png" alt="舞动银龄" class="logo-img" />
            <span class="logo-text">舞动银龄</span>
          </router-link>
        </el-col>
        
        <el-col :span="12" class="nav-links-desktop">
          <el-menu 
            mode="horizontal" 
            :router="true"
            :ellipsis="false"
            class="main-menu"
          >
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            
            <el-menu-item index="/dance-courses">
              <el-icon><VideoCameraFilled /></el-icon>
              <span>舞蹈课程</span>
            </el-menu-item>
            
            <el-menu-item index="/ai-coach">
              <el-icon><Cpu /></el-icon>
              <span>AI教练</span>
            </el-menu-item>
            
            <el-menu-item index="/health-management">
              <el-icon><FirstAidKit /></el-icon>
              <span>健康管理</span>
            </el-menu-item>
            
            <el-menu-item index="/social-platform">
              <el-icon><ChatDotRound /></el-icon>
              <span>社交平台</span>
            </el-menu-item>
            
            <el-menu-item index="/about">
              <el-icon><InfoFilled /></el-icon>
              <span>关于我们</span>
            </el-menu-item>
          </el-menu>
        </el-col>
        
        <el-col :span="6" class="nav-actions">
          <div class="action-buttons">
            <el-button v-if="!userStore.isLoggedIn" type="primary" @click="router.push('/login')">
              <el-icon><User /></el-icon>
              <span>登录</span>
            </el-button>
            
            <el-dropdown v-else>
              <div class="user-info">
                <el-avatar 
                  :size="40" 
                  :src="userStore.userInfo.avatar || defaultAvatar"
                />
                <span class="username">{{ userStore.nickname }}</span>
                <el-icon><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="router.push('/user-profile')">
                    <el-icon><User /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item @click="router.push('/ai-coach')">
                    <el-icon><Cpu /></el-icon>我的课程
                  </el-dropdown-item>
                  <el-dropdown-item @click="router.push('/health-management')">
                    <el-icon><FirstAidKit /></el-icon>健康档案
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          
          <div class="mobile-menu-toggle">
            <el-button link @click="drawerVisible = true">
              <el-icon size="26"><Menu /></el-icon>
            </el-button>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <!-- 移动端导航抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="舞动银龄"
      direction="rtl"
      size="70%"
    >
      <el-menu 
        :router="true"
        class="mobile-menu"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        
        <el-menu-item index="/dance-courses">
          <el-icon><VideoCameraFilled /></el-icon>
          <span>舞蹈课程</span>
        </el-menu-item>
        
        <el-menu-item index="/ai-coach">
          <el-icon><Cpu /></el-icon>
          <span>AI教练</span>
        </el-menu-item>
        
        <el-menu-item index="/health-management">
          <el-icon><FirstAidKit /></el-icon>
          <span>健康管理</span>
        </el-menu-item>
        
        <el-menu-item index="/social-platform">
          <el-icon><ChatDotRound /></el-icon>
          <span>社交平台</span>
        </el-menu-item>
        
        <el-menu-item index="/about">
          <el-icon><InfoFilled /></el-icon>
          <span>关于我们</span>
        </el-menu-item>
        
        <el-divider />
        
        <el-menu-item v-if="!userStore.isLoggedIn" index="/login">
          <el-icon><User /></el-icon>
          <span>登录/注册</span>
        </el-menu-item>
        
        <template v-else>
          <el-sub-menu index="user">
            <template #title>
              <el-icon><User /></el-icon>
              <span>{{ userStore.nickname }}</span>
            </template>
            <el-menu-item index="/user-profile">
              <el-icon><User /></el-icon>个人中心
            </el-menu-item>
            <el-menu-item index="/ai-coach">
              <el-icon><Cpu /></el-icon>我的课程
            </el-menu-item>
            <el-menu-item index="/health-management">
              <el-icon><FirstAidKit /></el-icon>健康档案
            </el-menu-item>
          </el-sub-menu>
          
          <el-menu-item @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            <span>退出登录</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-drawer>
  </header>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { 
  HomeFilled, 
  VideoCameraFilled, 
  Cpu, 
  FirstAidKit, 
  ChatDotRound, 
  InfoFilled,
  User,
  Menu,
  ArrowDown,
  SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const drawerVisible = ref(false)
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

// 退出登录
const handleLogout = async () => {
  try {
    await userStore.logout()
    drawerVisible.value = false
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}
</script>

<style scoped>
.main-nav {
  @apply bg-white shadow-md;
}

.container {
  @apply max-w-6xl mx-auto px-4;
}

.nav-container {
  @apply h-16 flex items-center;
}

.logo-container {
  @apply h-full flex items-center;
}

.logo {
  @apply flex items-center no-underline;
}

.logo-img {
  @apply h-10 w-auto mr-2;
}

.logo-text {
  @apply text-xl font-medium text-gray-800;
}

.nav-links-desktop {
  @apply hidden md:block;
}

.main-menu {
  @apply border-0 justify-center;
}

.nav-actions {
  @apply flex justify-end items-center;
}

.action-buttons {
  @apply hidden md:flex items-center;
}

.user-info {
  @apply flex items-center cursor-pointer;
}

.username {
  @apply ml-2 mr-1 text-gray-700;
}

.mobile-menu-toggle {
  @apply block md:hidden;
}

.mobile-menu {
  @apply border-0;
}

.mobile-menu .el-menu-item {
  @apply text-lg h-14;
}

/* 自定义 Element Plus 菜单样式 */
:deep(.el-menu--horizontal > .el-menu-item) {
  @apply text-lg;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  @apply text-blue-500 border-blue-500;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .nav-container {
    @apply justify-between;
  }
  
  .logo-container {
    @apply flex-grow;
  }
}
</style> 