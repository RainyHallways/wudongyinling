<template>
  <footer class="app-footer">
    <div class="container">
      <el-row :gutter="24">
        <el-col :xs="24" :sm="24" :md="8" :lg="8">
          <img src="/fonticon.png" alt="舞动银龄" class="logo-img" />
          <p class="footer-desc">基于多模态AI的舞蹈教学与反馈系统，专为老年人设计的智能舞蹈学习平台。</p>
          <div class="footer-links" style="display: flex; flex-direction: row; gap: 12px;">
            <p class="link-list"><router-link to="/about"><el-icon><InfoFilled /></el-icon> <span>关于我们</span></router-link></p>
            <p class="link-list"><router-link to="/faq"><el-icon><Help /></el-icon> <span>常见问题</span></router-link></p>
          </div>
        </el-col>
        
        <el-col :xs="24" :sm="24" :md="8" :lg="8">
          <div class="footer-links" style="margin-left: 20px;">
            <h4 class="footer-title link-list" style="margin-left: 10px;"><p style="font-size: medium;"><el-icon><List /></el-icon>服务条款</p></h4>
            <ul class="link-list">
              <span><router-link to="/policy/privacy-policy">隐私政策</router-link></span>
              <span><router-link to="/policy/user-agreement">用户协议</router-link></span>
              <span><router-link to="/policy/user-originality-guarantee">原创性保证</router-link></span>
              <span><router-link to="/policy/original-license-agreement">原创授权协议</router-link></span>
            </ul>
          </div>
        </el-col>
        
        <el-col :xs="24" :sm="24" :md="8" :lg="8">
          <div class="footer-contact">
            <h4 class="footer-title link-list"><router-link to="/contact"><el-icon><Promotion /></el-icon><span>联系我们</span></router-link></h4>
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
import { Message, Location, ElementPlus, Share, ChatDotRound, InfoFilled, Help, Promotion, List } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-footer {
  background: var(--bg-secondary);
  color: var(--text-primary);
  padding: 48px 0 24px;
  border-top: 1px solid var(--border-color);
}

.logo-img {
  height: 40px;
  width: auto;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
  display: block;
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
  margin-top: 12px;
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
  display: flex;
  align-items: center;
  gap: 8px;
}

.link-list p {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--font-size-large);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.link-list a:hover {
  color: var(--primary-color);
  background-color: unset !important;
}

.link-list span:hover{
  transform: scale(1.05);
}

.link-list .el-icon {
  align-items: center;
  justify-content: center;
  font-size: 20px;
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