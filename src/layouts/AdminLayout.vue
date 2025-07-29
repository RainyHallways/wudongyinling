<template>
  <div class="admin-layout">
    <el-container class="layout-container">
      <!-- 侧边导航 -->
      <el-aside 
        :width="isCollapse ? '64px' : '240px'" 
        class="aside"
        :class="{ 'is-collapse': isCollapse }"
      >
        <div class="logo">
          <h1 v-show="!isCollapse">舞动银龄</h1>
          <h1 v-show="isCollapse" class="logo-mini">舞</h1>
          <p v-show="!isCollapse">管理后台</p>
        </div>
        
        <el-menu
          class="el-menu-vertical"
          :default-active="activeMenu"
          :collapse="isCollapse"
          :router="true"
        >
          <el-menu-item index="/admin">
            <el-icon><Monitor /></el-icon>
            <template #title>仪表盘</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <template #title>用户管理</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/courses">
            <el-icon><VideoCamera /></el-icon>
            <template #title>课程管理</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/challenges">
            <el-icon><Trophy /></el-icon>
            <template #title>挑战活动</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/health-records">
            <el-icon><Suitcase /></el-icon>
            <template #title>健康记录</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/prescriptions">
            <el-icon><Document /></el-icon>
            <template #title>处方管理</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/posts">
            <el-icon><ChatDotRound /></el-icon>
            <template #title>动态广场</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/heritage">
            <el-icon><Compass /></el-icon>
            <template #title>非遗传承</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/chat">
            <el-icon><Message /></el-icon>
            <template #title>私信管理</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/statistics">
            <el-icon><DataLine /></el-icon>
            <template #title>数据统计</template>
          </el-menu-item>
          
          <el-menu-item index="/admin/system">
            <el-icon><Setting /></el-icon>
            <template #title>系统设置</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主体区域 -->
      <el-container class="main-container">
        <!-- 顶部导航 -->
        <el-header height="60px" class="header">
          <div class="header-left">
            <el-button 
              class="toggle-btn" 
              @click="toggleSidebar"
              :icon="isCollapse ? Expand : Fold"
              text
            />
            
            <!-- 面包屑导航 -->
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="$route.meta.title">{{ $route.meta.title }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <!-- 用户信息 -->
            <el-dropdown trigger="click">
              <div class="user-info">
                <el-avatar :size="32" :src="userStore.userInfo.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
                <span class="username">{{ userStore.nickname }}</span>
                <el-icon><ArrowDown /></el-icon>
              </div>
              
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="toUserProfile">个人信息</el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 内容区域 -->
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { 
  Monitor, 
  User, 
  VideoCamera, 
  Trophy, 
  Suitcase, 
  Document, 
  DataLine, 
  Setting,
  Fold,
  Expand,
  ArrowDown,
  ChatDotRound,
  Compass,
  Message
} from '@element-plus/icons-vue'

// 路由和存储
const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 侧边栏折叠状态
const isCollapse = ref(false)
const isMobile = ref(false)

// 计算当前激活的菜单
const activeMenu = computed(() => {
  return route.path
})

// 检查是否是移动端
const checkMobile = () => {
  const wasMobile = isMobile.value
  isMobile.value = window.innerWidth <= 768
  
  // 移动端默认折叠，桌面端默认展开
  if (isMobile.value && !wasMobile) {
    isCollapse.value = true // 移动端默认折叠
  }
  else if (!isMobile.value && wasMobile) {
    isCollapse.value = false // 桌面端默认展开
  }
}

// 切换侧边栏
const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 监听窗口大小变化
const handleResize = () => {
  checkMobile()
}

// 点击外部区域收回侧边栏（仅移动端）
const handleClickOutside = (event: Event) => {
  if (isMobile.value && !isCollapse.value) {
    const aside = document.querySelector('.aside')
    const toggleBtn = document.querySelector('.toggle-btn')
    const target = event.target as Node
    
    if (aside && !aside.contains(target) && toggleBtn && !toggleBtn.contains(target)) {
      isCollapse.value = true
    }
  }
}

// 组件挂载时检查屏幕尺寸
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', handleResize)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('click', handleClickOutside)
})

// 跳转到个人信息页
const toUserProfile = () => {
  router.push('/admin/profile')
}

// 处理退出登录
const handleLogout = async () => {
  await userStore.logout()
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  overflow: hidden;
  padding-top: 0;
  margin-top: 0;
}

.layout-container {
  height: 100%;
}

/* 侧边栏样式 */
.aside {
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  transition: width 0.3s;
  overflow-x: hidden;
  position: relative;
  z-index: 100;
}

.aside.is-collapse {
  box-shadow: 2px 0 6px rgba(44, 62, 80, 0.3);
}

.logo {
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.logo h1 {
  font-size: 16px;
  margin: 0;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.logo p {
  font-size: 11px;
  margin: 0;
  color: white;
  opacity: 0.8;
}

.logo-mini {
  font-size: 20px;
}

/* Element Plus 菜单样式覆盖 */
:deep(.el-menu) {
  border-right: none;
  background: transparent;
}

:deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
  height: 50px;
  line-height: 50px;
  margin: 4px 8px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

:deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(3px);
}

:deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

:deep(.el-menu-item .el-icon) {
  width: 20px;
  text-align: center;
  font-size: 16px;
  margin-right: 8px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
}

/* 主容器 */
.main-container {
  background-color: #f0f2f5;
}

/* 头部样式 */
.header {
  background: white;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid #e8e8e8;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.toggle-btn {
  font-size: 16px;
  color: #666;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f5f5;
}

.username {
  font-size: 13px;
  color: #333;
}

/* 主体内容 */
.main {
  padding: 16px;
  overflow-y: auto;
  background-color: #f0f2f5;
  min-height: calc(100vh - 60px);
  font-size: 13px;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .aside {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 1001;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    width: 240px !important;
  }
  
  .aside:not(.is-collapse) {
    transform: translateX(0);
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.3);
  }
  
  .main-container {
    margin-left: 0;
    width: 100%;
  }
  
  .header {
    padding: 0 16px;
  }
  
  .main {
    padding: 12px;
  }
  
  /* 移动端遮罩 */
  .aside:not(.is-collapse)::after {
    content: '';
    position: fixed;
    top: 0;
    left: 240px;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: -1;
    pointer-events: auto;
  }
}

@media screen and (max-width: 480px) {
  .username {
    display: none;
  }
  
  .main {
    padding: 10px;
  }
  
  .aside {
    width: 280px !important;
  }
  
  .aside:not(.is-collapse)::after {
    left: 280px;
  }
}
</style> 