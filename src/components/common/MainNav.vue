<template>
  <!-- 桌面端导航栏 -->
  <header class="main-nav desktop-nav">
    <div class="container">
      <el-row class="nav-container">
        <!-- 响应式logo区域 -->
        <el-col :xs="6" :sm="4" :md="3" :lg="3" :xl="3" class="logo-container">
          <router-link to="/" class="logo">
            <img src="/fonticon.png" alt="舞动银龄" class="logo-img" />
          </router-link>
        </el-col>
        
        <!-- 响应式导航菜单 -->
        <el-col :xs="12" :sm="14" :md="15" :lg="16" :xl="17" class="nav-links-desktop">
          <el-menu 
            mode="horizontal" 
            :router="true"
            :ellipsis="false"
            :default-active="$route.path"
            class="main-menu"
          >
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span class="menu-text">首页</span>
            </el-menu-item>
            
            <el-menu-item index="/dance-courses">
              <el-icon><VideoCameraFilled /></el-icon>
              <span class="menu-text">舞蹈课程</span>
            </el-menu-item>
            
            <el-menu-item index="/ai-coach">
              <el-icon><Cpu /></el-icon>
              <span class="menu-text">AI教练</span>
            </el-menu-item>
            
            <el-menu-item index="/health-management">
              <el-icon><FirstAidKit /></el-icon>
              <span class="menu-text">健康管理</span>
            </el-menu-item>
            
            <el-menu-item index="/social-platform">
              <el-icon><ChatDotRound /></el-icon>
              <span class="menu-text">社交平台</span>
            </el-menu-item>
            
            <el-menu-item index="/about">
              <el-icon><InfoFilled /></el-icon>
              <span class="menu-text">关于我们</span>
            </el-menu-item>
          </el-menu>
        </el-col>
        
        <!-- 响应式用户操作区域 -->
        <el-col :xs="6" :sm="6" :md="6" :lg="5" :xl="4" class="nav-actions">
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
                  <el-dropdown-item @click="router.push('/user-profile?tab=password')">
                    <el-icon><Lock /></el-icon>修改密码
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
        </el-col>
      </el-row>
    </div>
  </header>
    
  <!-- 移动端底部导航栏 -->
  <nav class="mobile-bottom-nav">
    <div class="mobile-nav-container">
      <router-link 
        v-for="item in mobileNavItems" 
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ 'active': $route.path === item.path || ($route.path === '/' && item.path === '/dance-courses') }"
      >
        <el-icon :size="24" class="nav-icon">
          <component :is="item.icon" />
        </el-icon>
        <span class="nav-label">{{ item.label }}</span>
      </router-link>
      
      <!-- 用户菜单项 -->
      <div class="nav-item user-menu-item" @click="showUserMenu = !showUserMenu">
        <el-icon :size="24" class="nav-icon">
          <User v-if="!userStore.isLoggedIn" />
          <el-avatar 
            v-else
            :size="24" 
            :src="userStore.userInfo.avatar || defaultAvatar"
          />
        </el-icon>
        <span class="nav-label">{{ userStore.isLoggedIn ? '我的' : '登录' }}</span>
      </div>
    </div>
    
    <!-- 用户菜单弹出层 -->
    <el-drawer
      v-model="showUserMenu"
      direction="btt"
      size="auto"
      class="user-menu-drawer"
    >
      <template #header>
        <div class="drawer-header">
          <el-avatar 
            :size="60" 
            :src="userStore.userInfo.avatar || defaultAvatar"
          />
          <div class="user-info-text">
            <h3 v-if="userStore.isLoggedIn">{{ userStore.nickname }}</h3>
            <p v-if="userStore.isLoggedIn">{{ userStore.userInfo.email }}</p>
            <el-button v-else type="primary" @click="router.push('/login')">立即登录</el-button>
          </div>
        </div>
      </template>
      
      <div class="menu-content">
        <template v-if="userStore.isLoggedIn">
          <el-row :gutter="16" class="menu-grid">
            <el-col :span="12">
              <div class="menu-card" @click="router.push('/user-profile')">
                <el-icon><User /></el-icon>
                <span>个人中心</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="menu-card" @click="router.push('/user-profile?tab=password')">
                <el-icon><Lock /></el-icon>
                <span>修改密码</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="menu-card" @click="router.push('/ai-coach')">
          <el-icon><Cpu /></el-icon>
                <span>我的课程</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="menu-card" @click="router.push('/health-management')">
                <el-icon><FirstAidKit /></el-icon>
                <span>健康档案</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="menu-card" @click="router.push('/about')">
          <el-icon><InfoFilled /></el-icon>
          <span>关于我们</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="menu-card logout-btn" @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            <span>退出登录</span>
              </div>
            </el-col>
          </el-row>
        </template>
      </div>
    </el-drawer>
  </nav>
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
  ArrowDown,
  SwitchButton,
  Lock
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const showUserMenu = ref(false)
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

// 移动端导航项
const mobileNavItems = [
  { path: '/dance-courses', label: '课程', icon: VideoCameraFilled },
  { path: '/ai-coach', label: 'AI教练', icon: Cpu },
  { path: '/health-management', label: '健康', icon: FirstAidKit },
  { path: '/social-platform', label: '社交', icon: ChatDotRound }
]

// 退出登录
const handleLogout = async () => {
  try {
    await userStore.logout()
    showUserMenu.value = false
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}
</script>

<style scoped>
/* 桌面端导航栏 */
.desktop-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  display: none;
}

/* 桌面端显示顶部导航栏 */
@media (min-width: 640px) {
  .desktop-nav {
    display: block;
  }
}

.container {
  @apply max-w-6xl mx-auto px-4;
}

.nav-container {
  @apply h-16 flex items-center;
}

.logo-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  overflow: hidden;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  white-space: nowrap;
}

.logo-img {
  height: 40px;
  width: auto;
  flex-shrink: 0;
}

/* 响应式logo */
@media (max-width: 768px) {
  .logo-img {
    height: 32px;
  }
}

.nav-links-desktop {
  display: block;
}

/* 小屏幕上的导航菜单样式调整 */
@media (max-width: 575px) {
  .nav-links-desktop .main-menu {
    justify-content: flex-start;
    overflow-x: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  .nav-links-desktop .main-menu::-webkit-scrollbar {
    display: none;
  }
  
  .nav-links-desktop .el-menu-item {
    padding: 0 8px;
    font-size: 12px;
    white-space: nowrap;
  }
}

.main-menu {
  border: none;
  justify-content: center;
}

/* 响应式菜单文字 */
@media (max-width: 1200px) {
  .menu-text {
    font-size: 13px;
  }
  
  .main-menu .el-menu-item {
    padding: 0 8px;
  }
}

@media (max-width: 1024px) {
  .menu-text {
    font-size: 12px;
  }
  
  .main-menu .el-menu-item {
    padding: 0 6px;
  }
}

@media (max-width: 768px) {
  .menu-text {
    display: none; /* 中等屏幕只显示图标 */
  }
  
  .main-menu .el-menu-item {
    padding: 0 4px;
  }
}

.nav-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  z-index: 1001;
  position: relative;
}

/* 小屏幕下进一步优化用户信息位置 */
@media (max-width: 1024px) {
  .nav-actions {
    min-width: 0;
    flex-shrink: 1;
  }
  
  .user-info {
    padding: 6px;
  }
  
  .username {
    max-width: 80px;
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .nav-actions {
    min-width: 40px;
  }
  
  .user-info {
    padding: 4px;
  }
}

.action-buttons {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-info:hover {
  background-color: rgba(64, 158, 255, 0.1);
}

.username {
  margin-left: 8px;
  margin-right: 4px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
  font-size: 14px;
}

/* 中等宽度隐藏用户名文字防止堆叠 */
@media (min-width: 769px) and (max-width: 960px) {
  .username {
    display: none;
  }
}

/* 移动端隐藏用户名文字 */
@media (max-width: 639px) {
  .username {
    display: none;
  }
}

/* 移动端底部导航栏 */
.mobile-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #ebeef5;
  z-index: 1000;
  display: block;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.1);
}

/* 桌面端隐藏移动端导航栏 */
@media (min-width: 640px) {
  .mobile-bottom-nav {
    display: none;
  }
}

.mobile-nav-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0;
  padding-bottom: env(safe-area-inset-bottom, 8px);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4px 8px;
  border-radius: 8px;
  color: #606266;
  text-decoration: none;
  transition: all 0.2s;
  min-width: 0;
  flex: 1;
  max-width: 80px;
}

.nav-item.active {
  color: #409eff;
}

.nav-item.active .nav-icon {
  color: #409eff;
  transform: scale(1.1);
}

.nav-icon {
  margin-bottom: 4px;
  transition: all 0.2s;
}

.nav-label {
  font-size: 10px;
  line-height: 12px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.user-menu-item {
  @apply cursor-pointer;
}

/* 用户菜单抽屉 */
.user-menu-drawer {
  @apply border-radius-t-lg;
}

.drawer-header {
  @apply flex items-center p-4 bg-gradient-to-r from-blue-500 to-purple-600;
  @apply text-white;
}

.user-info-text {
  @apply ml-4 flex-1;
}

.user-info-text h3 {
  @apply text-lg font-medium mb-1;
}

.user-info-text p {
  @apply text-sm opacity-90;
}

.menu-content {
  @apply p-4;
}

.menu-grid {
  @apply gap-4;
}

.menu-card {
  @apply flex flex-col items-center justify-center;
  @apply p-6 rounded-xl bg-white; /* 改为白色背景，增加圆角 */
  @apply cursor-pointer transition-all duration-300; /* 增加动画时长 */
  @apply border border-gray-100 shadow-sm; /* 添加轻微阴影 */
  min-height: 90px; /* 增加高度 */
  position: relative;
  overflow: hidden;
}

.menu-card::before {
  @apply absolute inset-0 bg-gradient-to-br from-blue-50 to-purple-50;
  content: '';
  opacity: 0;
  transition: opacity 0.3s ease;
}

.menu-card:hover {
  @apply bg-white border-blue-200 shadow-md; /* 悬停时增加阴影 */
  transform: translateY(-2px); /* 悬停时轻微上浮 */
}

.menu-card:hover::before {
  opacity: 1;
}

.menu-card:active {
  @apply transform scale-95;
  transition-duration: 0.1s;
}

.menu-card .el-icon {
  @apply mb-3 text-2xl; /* 增加图标大小和间距 */
  color: #606266;
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.menu-card:hover .el-icon {
  color: #409eff;
  transform: scale(1.1);
}

.menu-card span {
  @apply text-sm font-medium text-gray-700; /* 增加字体粗细 */
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.menu-card:hover span {
  color: #409eff;
}

.logout-btn {
  @apply bg-red-50 border-red-100;
}

.logout-btn::before {
  @apply bg-gradient-to-br from-red-50 to-red-100;
}

.logout-btn:hover {
  @apply bg-red-50 border-red-200 shadow-md;
}

.logout-btn .el-icon,
.logout-btn span {
  @apply text-red-600;
}

.logout-btn:hover .el-icon,
.logout-btn:hover span {
  @apply text-red-700;
}

/* 自定义 Element Plus 菜单样式 */
:deep(.el-menu--horizontal > .el-menu-item) {
  @apply text-lg;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  @apply text-blue-500 border-blue-500;
}

/* 为页面内容添加上下边距 */
:global(body) {
  margin: 0;
  padding: 0;
  padding-bottom: 70px; /* 默认移动端底部导航栏高度 */
}

/* 桌面端：顶部导航栏 */
@media (min-width: 640px) {
  :global(body) {
    padding-top: 64px; /* 桌面端顶部导航栏高度 */
    padding-bottom: 0; /* 桌面端取消底部边距 */
  }
}

/* 安全区域适配 */
.safe-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .nav-links-desktop {
    @apply hidden;
  }
}

@media (max-width: 768px) {
  .nav-container {
    @apply justify-between;
  }
  
  .logo-container {
    @apply flex-grow;
  }
  
  .action-buttons {
    @apply hidden;
  }
}
</style> 