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
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
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
            <el-icon 
              class="toggle-btn" 
              @click="toggleSidebar"
              :class="{ 'is-active': isCollapse }"
            >
              <Fold v-if="!isCollapse" />
              <Expand v-else />
            </el-icon>
            
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
  ArrowDown
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
  
  // 只在初次检测或从桌面端切换到移动端时设置默认折叠状态
  if (isMobile.value && !wasMobile) {
    isCollapse.value = true // 移动端默认折叠
  }
  // 从移动端切换回桌面端时展开侧边栏
  else if (!isMobile.value && wasMobile) {
    isCollapse.value = false
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

// 点击外部区域收回侧边栏
const handleClickOutside = (event: Event) => {
  if (isMobile.value && !isCollapse.value) {
    const aside = document.querySelector('.aside')
    const target = event.target as Node
    
    if (aside && !aside.contains(target)) {
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
}

.layout-container {
  height: 100%;
}

/* 侧边栏样式 */
.aside {
  background-color: #304156;
  transition: width 0.3s;
  overflow-x: hidden;
  position: relative;
  z-index: 100;
}

.aside.is-collapse {
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.logo {
  height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.logo h1 {
  color: #fff;
  font-size: 18px;
  margin: 0;
  line-height: 1.2;
  transition: opacity 0.3s;
}

.logo-mini {
  font-size: 24px !important;
  font-weight: bold;
}

.logo p {
  color: #bfcbd9;
  font-size: 12px;
  margin: 5px 0 0;
  transition: opacity 0.3s;
}

.el-menu-vertical {
  border-right: none;
  height: calc(100vh - 60px);
}

/* 顶部导航样式 */
.header {
  background-color: #fff;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px;
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-btn {
  margin-right: 15px;
  font-size: 20px;
  cursor: pointer;
  color: #606266;
}

.toggle-btn:hover {
  color: #409EFF;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin: 0 8px;
  color: #606266;
}

/* 主内容区域样式 */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main {
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f7fa;
  height: calc(100vh - 60px);
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .aside {
    position: fixed;
    z-index: 1000;
    height: 100%;
    transform: translateX(0);
    transition: transform 0.3s;
    width: 240px !important; /* 移动端固定宽度 */
  }
  
  .aside.is-collapse {
    transform: translateX(-240px);
  }
  
  .main-container {
    margin-left: 0;
  }
  
  .header {
    padding: 0 10px;
  }
  
  .main {
    padding: 15px;
  }
  
  /* 移动端遮罩 */
  .aside:not(.is-collapse)::after {
    content: '';
    position: fixed;
    top: 0;
    left: 240px;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 99;
  }
}

@media screen and (max-width: 480px) {
  .username {
    display: none; /* 小屏幕隐藏用户名 */
  }
  
  .header {
    padding: 0 5px;
  }
  
  .main {
    padding: 10px;
  }
}
</style> 