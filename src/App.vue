<!-- App.vue -->
<template>
  <div class="app">
    <!-- 导航栏 -->
    <header>
      <div class="header-container">
        <div class="logo">
          <h1>舞动银龄</h1>
        </div>
        
        <!-- 添加一个汉堡菜单按钮 -->
        <div class="mobile-toggle" @click="toggleMobileMenu">
          <el-icon size="24"><Menu /></el-icon>
        </div>

        <div class="nav-wrapper" :class="{ 'nav-active': isMobileMenuOpen }">
          <nav>
            <ul class="nav-links">
              <li><router-link to="/" @click="closeMobileMenu">首页</router-link></li>
              <li><router-link to="/coach" @click="closeMobileMenu">AI教练</router-link></li>
              <li><router-link to="/health" @click="closeMobileMenu">健康管理</router-link></li>
              <li><router-link to="/social" @click="closeMobileMenu">社交激励</router-link></li>
              <li><router-link to="/dance-courses" @click="closeMobileMenu">舞蹈课程</router-link></li>
              <li><router-link to="/about" @click="closeMobileMenu">关于我们</router-link></li>
            </ul>
          </nav>
          
          <div class="auth-buttons">
            <template v-if="isLoggedIn">
              <span class="welcome-text">欢迎，{{ username }}</span>
              <el-button link @click="logout">退出登录</el-button>
            </template>
            <template v-else>
              <router-link to="/login" class="login-btn">登录/注册</router-link>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <router-view></router-view>
    </main>

    <!-- 页脚 -->
    <footer>
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <h5>舞动银龄</h5>
            <p>专为老年人设计的舞蹈教学与健康管理平台，让银龄生活更精彩。</p>
          </div>
          <div class="col-md-2">
            <div class="footer-links">
              <ul>
                <li><router-link to="/">首页</router-link></li>
                <li><router-link to="/coach">AI教练</router-link></li>
                <li><router-link to="/health">健康管理</router-link></li>
                <li><router-link to="/social">社交激励</router-link></li>
                <li><router-link to="/dance-courses">舞蹈课程</router-link></li>
                <li><router-link to="/about">关于我们</router-link></li>
              </ul>
            </div>
          </div>
          <div class="col-md-3">
            <div class="footer-links">
              <ul>
                <li><router-link to="/faq">常见问题</router-link></li>
                <li><router-link to="/contact">联系我们</router-link></li>
                <li><router-link to="/privacy-policy">隐私政策</router-link></li>
                <li><router-link to="/user-agreement">用户协议</router-link></li>
                <li><router-link to="/originality-guarantee">原创性保证</router-link></li>
                <li><router-link to="/original-license">原创授权协议</router-link></li>
              </ul>
            </div>
          </div>
          <div class="col-md-3">
            <div class="footer-links">
              <h5>联系我们</h5>
              <ul>
                <li><i class="fas fa-envelope me-2"></i> contact@wdyl.cnies.org</li>
                <li><i class="fas fa-map-marker-alt me-2"></i> 山东省济南市</li>
              </ul>
              <div class="mt-3">
                <a href="#" class="text-white me-2"><i class="fab fa-weixin fa-lg"></i></a>
                <a href="#" class="text-white me-2"><i class="fab fa-weibo fa-lg"></i></a>
                <a href="#" class="text-white"><i class="fab fa-qq fa-lg"></i></a>
              </div>
            </div>
          </div>
        </div>
        <div class="copyright">
          <p>&copy; 2025 舞动银龄 版权所有</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterView, useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Menu } from '@element-plus/icons-vue'

const router = useRouter()

// 从本地存储获取用户信息
const userInfo = ref(null)
const isLoggedIn = computed(() => !!userInfo.value)
const username = computed(() => userInfo.value?.username || '未登录')

// 移动端菜单状态
const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// 初始化时获取用户信息
onMounted(() => {
  checkLoginStatus()
})

// 检查登录状态
const checkLoginStatus = () => {
  const token = localStorage.getItem('user-token')
  const userInfoStr = localStorage.getItem('user-info')
  
  if (token && userInfoStr) {
    try {
      userInfo.value = JSON.parse(userInfoStr)
    } catch (error) {
      console.error('解析用户信息失败', error)
      userInfo.value = null
    }
  } else {
    userInfo.value = null
  }
}

// 退出登录
const logout = () => {
  localStorage.removeItem('user-token')
  localStorage.removeItem('user-info')
  userInfo.value = null
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<style>
:root {
  --primary-color: #5c6bc0;
  --secondary-color: #ff7043;
  --background-color: #f5f5f5;
  --text-color: #333;
  --light-gray: #e0e0e0;
  --white: #ffffff;
  --shadow: 0 4px 8px rgba(0,0,0,0.1);
  --dark-color: #333333;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Microsoft YaHei', sans-serif;
}

/* 导航栏样式 */
header {
  background-color: var(--white);
  box-shadow: var(--shadow);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  position: relative;
}

.logo {
  margin-right: 40px;
}

.logo h1 {
  font-size: 28px;
  color: var(--primary-color);
  margin: 0;
}

.nav-wrapper {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  gap: 20px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-links a {
  color: var(--text-color);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 20px;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background-color: var(--primary-color);
  color: white;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-left: 20px;
}

.welcome-text {
  color: var(--text-color);
}

.login-btn {
  color: var(--primary-color);
  text-decoration: none;
  padding: 8px 16px;
  border: 1px solid var(--primary-color);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background-color: var(--primary-color);
  color: white;
}

.mobile-toggle {
  display: none;
  cursor: pointer;
}

@media (max-width: 1024px) {
  .mobile-toggle {
    display: block;
    margin-left: auto;
  }

  .nav-wrapper {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    flex-direction: column;
  }

  .nav-wrapper.nav-active {
    display: flex;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: 10px;
  }

  .nav-links a {
    display: block;
    text-align: center;
    padding: 12px;
  }

  .auth-buttons {
    margin: 20px 0 0 0;
    justify-content: center;
    width: 100%;
  }
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  min-height: calc(100vh - 350px); /* 确保内容区域有足够的最小高度 */
  padding-bottom: 40px; /* 增加底部内边距 */
}

/* 页脚样式 */
footer {
  background-color: var(--dark-color);
  color: white;
  padding: 50px 0 20px;
  margin-top: auto;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
}

.col-md-2, .col-md-3, .col-md-4 {
  position: relative;
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
}

.col-md-2 {
  flex: 0 0 16.666667%;
  max-width: 16.666667%;
}

.col-md-3 {
  flex: 0 0 25%;
  max-width: 25%;
}

.col-md-4 {
  flex: 0 0 33.333333%;
  max-width: 33.333333%;
}

footer h5 {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.footer-links ul {
  list-style: none;
  padding-left: 0;
}

.footer-links li {
  margin-bottom: 10px;
}

.footer-links a {
  color: #ccc;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: white;
}

.copyright {
  border-top: 1px solid #444;
  padding-top: 20px;
  margin-top: 30px;
  text-align: center;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.text-white {
  color: white;
}

.me-2 {
  margin-right: 0.5rem;
}

.mt-3 {
  margin-top: 1rem;
}

.ms-3 {
  margin-left: 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .mobile-toggle {
    display: block;
  }
  
  .nav-links {
    display: none;
    position: absolute;
    top: 90px;
    left: 0;
    width: 100%;
    flex-direction: column;
    background-color: var(--white);
    padding: 20px;
    box-shadow: 0 5px 10px rgba(0,0,0,0.1);
    text-align: center;
    z-index: 99;
  }
  
  .nav-links.active {
    display: flex;
  }
  
  .col-md-2, .col-md-3, .col-md-4 {
    flex: 0 0 100%;
    max-width: 100%;
    margin-bottom: 20px;
  }
}
</style>