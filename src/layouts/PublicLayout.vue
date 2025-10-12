<template>
  <div class="public-layout">
    <!-- 头部导航 -->
    <header class="header">
      <MainNav />
    </header>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>
    
    <!-- 页脚 -->
    <footer class="footer">
      <AppFooter />
    </footer>
  </div>
</template>

<script lang="ts" setup>
import MainNav from '../components/common/MainNav.vue'
import AppFooter from '../components/common/AppFooter.vue'
</script>

<style scoped>
.public-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.main-content {
  flex: 1;
  max-width: 100%;
  width: 100%;
  margin: 0 auto;
}
</style> 