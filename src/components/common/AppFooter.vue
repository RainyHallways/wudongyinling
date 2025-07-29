<template>
  <footer class="app-footer">
    <div class="container">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="24" :md="8" :lg="8">
          <h5 class="footer-title">舞动银龄</h5>
          <p class="footer-desc">基于多模态AI的舞蹈教学与反馈系统，专为老年人设计的智能舞蹈学习平台。</p>
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
  background: var(--bg-secondary);
  color: var(--text-primary);
  padding: 48px 0 24px;
  border-top: 1px solid var(--border-color);
}

.container {
  @apply max-w-6xl mx-auto px-4;
}

.footer-title {
  @apply text-xl font-medium mb-4;
  color: var(--text-primary);
}

.footer-desc {
  color: var(--text-secondary);
  font-size: var(--font-size-large);
}

.link-list {
  @apply list-none p-0 m-0;
}

.link-list li {
  @apply mb-3;
}

.link-list a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--font-size-large);
  transition: all 0.3s ease;
}

.link-list a:hover {
  color: var(--primary-color);
}

.contact-list {
  @apply list-none p-0 m-0;
}

.contact-list li {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: var(--text-secondary);
  font-size: var(--font-size-large);
}

.contact-list .el-icon {
  margin-right: 8px;
  color: var(--primary-color);
  font-size: 24px; /* 放大图标 */
}

.social-links {
  display: flex;
  gap: 20px;
  margin-top: 24px;
}

.social-link {
  color: var(--text-secondary);
  font-size: 24px; /* 增大社交图标 */
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px; /* 增大点击区域 */
  height: 56px;
  border-radius: 50%;
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
}

.social-link:hover {
  color: var(--primary-color);
  background: var(--bg-hover);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-light);
}

.copyright {
  border-top: 1px solid var(--border-color);
  margin-top: 32px;
  padding-top: 24px;
  text-align: center;
  color: var(--text-light);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .footer-links, .footer-contact {
    @apply mt-6;
  }
}
</style> 