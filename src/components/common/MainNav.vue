<template>
  <!-- 桌面端导航栏 -->
  <header class="main-nav desktop-nav">
    <div class="container">
      <el-row class="nav-container">
        <!-- 响应式logo区域 -->
        <el-col :xs="8" :sm="5" :md="4" :lg="3" :xl="3" class="logo-container">
          <router-link to="/" class="logo">
            <img src="/fonticon.png" alt="舞动银龄" class="logo-img" />
          </router-link>
        </el-col>
        
        <!-- 响应式导航菜单 -->
        <el-col :xs="10" :sm="13" :md="14" :lg="16" :xl="17" class="nav-links-desktop">
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
        <el-icon :size="24" class="nav-icon" v-if="!userStore.isLoggedIn">
          <User />
        </el-icon>
        <el-avatar 
          v-else
          :size="24" 
          :src="userStore.userInfo.avatar || defaultAvatar"
          class="nav-icon"
        />
        <span class="nav-label user-label" :class="{ 'hide-on-small': userStore.isLoggedIn }">
          {{ userStore.isLoggedIn ? '我的' : '登录' }}
        </span>
      </div>
    </div>
    
    <!-- 用户菜单弹出层 -->
    <el-drawer
      v-model="showUserMenu"
      direction="btt"
      size="auto"
      class="user-menu-drawer"
      :z-index="9999"
      :modal="true"
      :append-to-body="true"
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
  height: 64px;
  background: rgba(212, 175, 55, 0.92);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 9999; /* 确保在最顶层 */
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
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
  z-index: 1001;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  white-space: nowrap;
  z-index: 1001;
}

.logo-img {
  height: 40px;
  width: auto;
  flex-shrink: 0;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
  z-index: 1001;
  position: relative;
}

/* 响应式logo */
@media (max-width: 1000px) and (min-width: 769px) {
  .logo-img {
    height: 38px;
  }
  
  .username {
    display: none;
  }
  
  .user-info {
    gap: 4px;
  }
  
  .nav-actions {
    max-width: 90px;
  }
}

@media (max-width: 768px) {
  .logo-img {
    height: 36px;
  }
}

@media (max-width: 576px) {
  .logo-img {
    height: 32px;
  }
}

@media (max-width: 480px) {
  .logo-img {
    height: 28px;
  }
}

@media (max-width: 375px) {
  .logo-img {
    height: 24px;
  }
  
  .user-label.hide-on-small {
    display: none !important;
  }
  
  .user-menu-item .el-avatar {
    margin-bottom: 0 !important;
  }
  
  /* 进一步减少用户操作区域的宽度 */
  .nav-actions {
    max-width: 60px;
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
  background: transparent;
}

.main-menu .el-menu-item {
  color: white;
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 25px;
  margin: 0 4px;
  position: relative;
  border-bottom: none !important;
}

.main-menu .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-2px);
  border-radius: 25px;
}

.main-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  font-weight: 600;
  border-radius: 25px;
  box-shadow: var(--shadow-light);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.main-menu .el-menu-item.is-active .menu-text {
  color: white;
  font-weight: 600;
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

/* 用户操作区域 */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1000;
  position: relative;
}

.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.action-buttons .el-button {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 20px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-buttons .el-button:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.15);
}

.username {
  font-weight: 500;
  color: white;
}

/* 移动端底部导航栏 */
.mobile-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(212, 175, 55, 0.92);
  backdrop-filter: blur(10px);
  border-top: 2px solid rgba(212, 175, 55, 0.3);
  z-index: 999;
  display: block;
}

@media (min-width: 640px) {
  .mobile-bottom-nav {
    display: none;
  }
}

.mobile-nav-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 18px 0;
  padding-bottom: calc(env(safe-area-inset-bottom, 18px) + 6px);
  min-height: 90px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px 6px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  min-width: 0;
  flex: 1;
  max-width: 80px;
  min-height: 60px;
}

.nav-item.active {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
}

.nav-item.active .nav-icon {
  color: white;
  transform: scale(1.2);
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.5));
}

.nav-icon {
  margin-bottom: 10px;
  transition: all 0.3s ease;
  font-size: 22px;
}

.nav-label {
  font-size: 12px;
  line-height: 18px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  font-weight: 500;
  color: inherit;
}

.user-label.hide-on-small {
  display: block;
}

@media (max-width: 580px) {
  .username {
    display: none;
  }
}

@media (max-width: 480px) {
  .user-label.hide-on-small {
    display: none;
  }
  
  .user-menu-item .el-avatar {
    margin-bottom: 0;
  }
}

.user-menu-item .el-avatar {
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.user-menu-item:hover .el-avatar {
  border-color: rgba(255, 255, 255, 0.8);
  transform: scale(1.1);
}

.user-menu-item {
  cursor: pointer;
}

/* 用户菜单抽屉 */
.user-menu-drawer {
  @apply border-radius-t-lg;
}

:deep(.user-menu-drawer .el-drawer) {
  z-index: 9999 !important;
}

:deep(.user-menu-drawer .el-drawer__wrapper) {
  z-index: 9999 !important;
}

:deep(.user-menu-drawer .el-overlay) {
  z-index: 9998 !important;
}

:deep(.user-menu-drawer .el-drawer__body) {
  padding: 0;
  overflow-y: auto;
  max-height: 60vh;
}

:deep(.user-menu-drawer .el-drawer__header) {
  margin-bottom: 0;
  padding: 0;
}

/* 移动端抽屉优化 */
@media (max-width: 640px) {
  :deep(.user-menu-drawer .el-drawer) {
    z-index: 9999 !important;
    position: fixed !important;
  }
  
  :deep(.user-menu-drawer .el-drawer__wrapper) {
    z-index: 9999 !important;
  }
  
  :deep(.user-menu-drawer .el-overlay) {
    z-index: 9998 !important;
    background-color: rgba(0, 0, 0, 0.5) !important;
  }
}

.drawer-header {
  background: var(--gradient-primary);
  @apply flex items-center p-4;
  @apply text-white;
}

.user-info-text {
  @apply ml-4 flex-1;
}

.user-info-text h3 {
  @apply text-lg font-medium mb-1;
  color: white;
}

.user-info-text p {
  @apply text-sm opacity-90;
}

.menu-content {
  @apply p-4;
  background: var(--bg-primary);
}

.menu-grid {
  @apply gap-4;
}

.menu-card {
  @apply flex flex-col items-center justify-center;
  @apply p-8 rounded-xl bg-white;
  @apply cursor-pointer transition-all duration-300;
  @apply border border-gray-100 shadow-sm;
  min-height: 120px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow);
  gap: 12px;
}

.menu-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-warm);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.menu-card:hover {
  background: white;
  border-color: var(--primary-color);
  box-shadow: var(--shadow-heavy);
  transform: translateY(-2px);
}

.menu-card:hover::before {
  opacity: 0.1;
}

.menu-card:active {
  transform: scale(0.95);
  transition-duration: 0.1s;
}

.menu-card .el-icon {
  margin-bottom: 0;
  font-size: 32px;
  color: var(--primary-color);
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.menu-card:hover .el-icon {
  color: var(--primary-dark);
  transform: scale(1.1);
}

.menu-card span {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
  text-align: center;
}

.menu-card:hover span {
  color: var(--primary-dark);
}

.logout-btn {
  background: #fff5f5;
  border-color: #fecaca;
}

.logout-btn::before {
  background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
}

.logout-btn:hover {
  background: #fff5f5;
  border-color: #f87171;
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.3);
}

.logout-btn .el-icon,
.logout-btn span {
  color: #dc2626;
}

.logout-btn:hover .el-icon,
.logout-btn:hover span {
  color: #b91c1c;
}

/* 自定义 Element Plus 菜单样式 */
:deep(.el-menu--horizontal > .el-menu-item) {
  border-radius: 25px !important;
  margin: 0 4px !important;
  color: white !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
  border-bottom: none !important;
}

:deep(.el-menu--horizontal > .el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  transform: translateY(-2px) !important;
  border-bottom: none !important;
  border-radius: 25px !important;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.25) !important;
  color: white !important;
  border-radius: 25px !important;
  box-shadow: var(--shadow-light) !important;
  border-bottom: none !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active .menu-text) {
  color: white !important;
  font-weight: 600 !important;
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

/* 关闭按钮样式 */
:deep(.user-menu-drawer .el-drawer__close-btn) {
  width: 48px !important;
  height: 48px !important;
  background: rgba(255, 255, 255, 0.2) !important;
  border-radius: 50% !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: white !important;
  font-size: 20px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  transition: all 0.3s ease !important;
}

:deep(.user-menu-drawer .el-drawer__close-btn:hover) {
  background: rgba(255, 255, 255, 0.3) !important;
  transform: scale(1.1) !important;
}
</style> 