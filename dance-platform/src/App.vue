<!-- App.vue -->
<template>
  <div class="app">
    <!-- 导航栏 -->
    <header>
      <div class="header-container">
        <div class="logo">
          <h1>舞动银龄</h1>
        </div>
        <nav>
          <div class="mobile-menu">&#9776;</div>
          <ul class="nav-links">
            <li><router-link to="/" exact>首页</router-link></li>
            <li><router-link to="/coach">AI教练</router-link></li>
            <li><router-link to="/health">健康管理</router-link></li>
            <li><router-link to="/social">社交激励</router-link></li>
            <li><router-link to="/dance-courses">舞蹈课程</router-link></li>
            <li><router-link to="/about">关于我们</router-link></li>
          </ul>
        </nav>
        <div class="ms-3">
          <template v-if="isLoggedIn">
            <span class="welcome-text">欢迎，{{ username }}</span>
            <a @click="logout" class="nav-item">退出登录</a>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-outline-primary">登录/注册</router-link>
          </template>
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
              <h5>快速链接</h5>
              <ul>
                <li><router-link to="/">首页</router-link></li>
                <li><router-link to="/coach">AI教练</router-link></li>
                <li><router-link to="/health">健康管理</router-link></li>
                <li><router-link to="/social">社交激励</router-link></li>
                <li><router-link to="/dance-courses">舞蹈课程</router-link></li>
              </ul>
            </div>
          </div>
          <div class="col-md-3">
            <div class="footer-links">
              <h5>帮助中心</h5>
              <ul>
                <li><a href="#">常见问题</a></li>
                <li><a href="#">使用教程</a></li>
                <li><a href="#">联系我们</a></li>
                <li><a href="#">隐私政策</a></li>
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

const router = useRouter()

// 从本地存储获取用户信息
const userInfo = ref(null)
const isLoggedIn = computed(() => !!userInfo.value)
const username = computed(() => userInfo.value?.username || '未登录')

// 初始化时获取用户信息
onMounted(() => {
  checkLoginStatus()
  
  // 绑定移动端菜单事件
  document.querySelector('.mobile-menu').addEventListener('click', function() {
    document.querySelector('.nav-links').classList.toggle('active')
  })
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
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo h1 {
  font-size: 28px;
  color: var(--primary-color);
  font-weight: bold;
  margin: 0;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 30px;
  margin-bottom: 0;
  padding: 0;
}

.nav-links a {
  color: var(--text-color);
  text-decoration: none;
  font-size: 20px;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.nav-links a:hover, 
.nav-links a.router-link-active {
  background-color: var(--primary-color);
  color: var(--white);
}

.mobile-menu {
  display: none;
  font-size: 30px;
  cursor: pointer;
}

.btn-outline-primary {
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  padding: 8px 16px;
  border-radius: 20px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: var(--primary-color);
  color: var(--white);
}

.welcome-text {
  padding: 0 15px;
  color: var(--text-color);
}

.nav-item {
  color: var(--primary-color);
  cursor: pointer;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: rgba(92, 107, 192, 0.1);
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
  .mobile-menu {
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