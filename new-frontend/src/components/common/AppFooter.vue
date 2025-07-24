<template>
  <footer class="app-footer">
    <div class="container">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="24" :md="8" :lg="8">
          <h5 class="footer-title">舞动银龄</h5>
          <p class="footer-desc">专为老年人设计的舞蹈教学与健康管理平台，让银龄生活更精彩。</p>
        </el-col>
        
        <el-col :xs="12" :sm="8" :md="4" :lg="4">
          <div class="footer-links">
            <ul class="link-list">
              <li><router-link to="/">首页</router-link></li>
              <li><router-link to="/dance-courses">舞蹈课程</router-link></li>
              <li><router-link to="/ai-coach">AI教练</router-link></li>
              <li><router-link to="/health-management">健康管理</router-link></li>
              <li><router-link to="/social-platform">社交平台</router-link></li>
              <li><router-link to="/about">关于我们</router-link></li>
            </ul>
          </div>
        </el-col>
        
        <el-col :xs="12" :sm="8" :md="6" :lg="6">
          <div class="footer-links">
            <ul class="link-list">
              <li><router-link to="/faq">常见问题</router-link></li>
              <li><router-link to="/contact">联系我们</router-link></li>
              <li><router-link to="/policy/privacy-policy">隐私政策</router-link></li>
              <li><router-link to="/policy/user-agreement">用户协议</router-link></li>
              <li><router-link to="/policy/user-originality-guarantee">原创性保证</router-link></li>
              <li><router-link to="/policy/original-license-agreement">原创授权协议</router-link></li>
            </ul>
          </div>
        </el-col>
        
        <el-col :xs="24" :sm="8" :md="6" :lg="6">
          <div class="footer-contact">
            <h5 class="footer-title">联系我们</h5>
            <ul class="contact-list">
              <li>
                <el-icon><Message /></el-icon>
                <span>contact@wdyl.cnies.org</span>
              </li>
              <li>
                <el-icon><Location /></el-icon>
                <span>山东省济南市</span>
              </li>
            </ul>
            
            <div class="social-links">
              <a href="#" aria-label="微信" class="social-link">
                <el-icon><ChatDotRound /></el-icon>
              </a>
              <a href="#" aria-label="微博" class="social-link">
                <el-icon><Share /></el-icon>
              </a>
              <a href="#" aria-label="其他社交平台" class="social-link">
                <el-icon><ElementPlus /></el-icon>
              </a>
            </div>
          </div>
        </el-col>
      </el-row>
      
      <div class="copyright">
        <p>&copy; {{ new Date().getFullYear() }} 舞动银龄 版权所有</p>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup>
import { Message, Location, ElementPlus, Share, ChatDotRound } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-footer {
  @apply bg-gray-800 text-white py-12 pb-6;
}

.container {
  @apply max-w-6xl mx-auto px-4;
}

.footer-title {
  @apply text-xl font-medium mb-4;
}

.footer-desc {
  @apply text-gray-300 text-lg;
}

.link-list {
  @apply list-none p-0 m-0;
}

.link-list li {
  @apply mb-3;
}

.link-list a {
  @apply text-gray-300 no-underline text-lg transition-colors;
}

.link-list a:hover {
  @apply text-white;
}

.contact-list {
  @apply list-none p-0 m-0;
}

.contact-list li {
  @apply flex items-center mb-3 text-gray-300 text-lg;
}

.contact-list .el-icon {
  @apply mr-2 text-blue-400;
}

.social-links {
  @apply flex gap-4 mt-6;
}

.social-link {
  @apply text-gray-300 text-2xl transition-colors inline-flex items-center justify-center w-10 h-10 rounded-full bg-gray-700;
}

.social-link:hover {
  @apply text-white bg-gray-600;
}

.copyright {
  @apply border-t border-gray-700 mt-8 pt-6 text-center text-gray-400;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .footer-links, .footer-contact {
    @apply mt-6;
  }
}
</style> 