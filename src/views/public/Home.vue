<script setup lang="ts">
import { onMounted } from 'vue'

// 页面加载动画
onMounted(() => {
  // 添加渐入动画
  const cards = document.querySelectorAll('.fade-in')
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
      }
    })
  })
  
  cards.forEach((card) => {
    observer.observe(card)
  })
})
</script>

<template>
  <div class="home-container page-with-nav">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">舞动银龄</h1>
        <p class="hero-subtitle">
          专为银发族打造的智能舞蹈学习平台<br>
          让舞蹈成为健康生活的美好伴侣
        </p>
        <div class="hero-actions">
          <el-button 
            type="primary" 
            size="large" 
            @click="$router.push('/courses')"
            class="hero-btn primary-btn"
          >
            <i class="el-icon-video-play"></i>
            开始学习舞蹈
          </el-button>
          <el-button 
            size="large" 
            @click="$router.push('/about')"
            class="hero-btn secondary-btn"
          >
            <i class="el-icon-info"></i>
            了解更多
          </el-button>
        </div>
      </div>
    </section>

    <!-- 特色功能区域 -->
    <section class="features-section">
      <div class="section-header">
        <h2 class="section-title">平台特色</h2>
        <p class="section-subtitle">为银发族量身定制的贴心功能</p>
      </div>
      
      <div class="features-grid">
        <div class="feature-card fade-in">
          <div class="feature-icon">🎵</div>
          <h3 class="feature-title">专业舞蹈课程</h3>
          <p class="feature-description">
            涵盖广场舞、太极、民族舞等多种舞蹈形式，
            由专业老师录制，动作简单易学
          </p>
        </div>
        
        <div class="feature-card fade-in">
          <div class="feature-icon">🏥</div>
          <h3 class="feature-title">健康管理</h3>
          <p class="feature-description">
            记录运动数据，监测身体状况，
            提供个性化健康建议和运动处方
          </p>
        </div>
        
        <div class="feature-card fade-in">
          <div class="feature-icon">🤖</div>
          <h3 class="feature-title">AI智能指导</h3>
          <p class="feature-description">
            AI教练实时纠正动作，提供个性化学习建议，
            让每一次练习都更加高效
          </p>
        </div>
        
        <div class="feature-card fade-in">
          <div class="feature-icon">👥</div>
          <h3 class="feature-title">社交互动</h3>
          <p class="feature-description">
            与舞友们分享学习心得，参与打卡挑战，
            在欢乐的氛围中坚持运动
          </p>
        </div>
        
        <div class="feature-card fade-in">
          <div class="feature-icon">🏆</div>
          <h3 class="feature-title">学习激励</h3>
          <p class="feature-description">
            完成学习目标获得奖章，参与挑战赛事，
            让舞蹈学习充满成就感
          </p>
        </div>
        
        <div class="feature-card fade-in">
          <div class="feature-icon">🎭</div>
          <h3 class="feature-title">非遗传承</h3>
          <p class="feature-description">
            学习传统民族舞蹈，了解文化内涵，
            在舞蹈中感受中华文化之美
          </p>
        </div>
      </div>
    </section>

    <!-- 数据统计区域 -->
    <section class="stats-section">
      <div class="stats-container">
        <div class="stat-item">
          <div class="stat-number">10,000+</div>
          <div class="stat-label">注册用户</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">500+</div>
          <div class="stat-label">精品课程</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">50+</div>
          <div class="stat-label">专业老师</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">98%</div>
          <div class="stat-label">用户满意度</div>
        </div>
      </div>
    </section>

    <!-- 快速入门区域 -->
    <section class="quick-start-section">
      <div class="section-header">
        <h2 class="section-title">快速开始</h2>
        <p class="section-subtitle">三步开启您的舞蹈之旅</p>
      </div>
      
      <div class="steps-container">
        <div class="step-item">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3 class="step-title">注册账户</h3>
            <p class="step-description">简单注册，立即开始舞蹈学习之旅</p>
          </div>
        </div>
        
        <div class="step-item">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3 class="step-title">选择课程</h3>
            <p class="step-description">根据兴趣和身体状况选择合适的课程</p>
          </div>
        </div>
        
        <div class="step-item">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3 class="step-title">开始学习</h3>
            <p class="step-description">跟随视频教程，享受舞蹈带来的快乐</p>
          </div>
        </div>
      </div>
      
      <div class="quick-start-actions">
        <el-button 
          type="primary" 
          size="large" 
          @click="$router.push('/register')"
          class="start-btn"
        >
          立即开始
        </el-button>
      </div>
    </section>

    <!-- 用户评价区域 -->
    <section class="testimonials-section">
      <div class="section-header">
        <h2 class="section-title">用户心声</h2>
        <p class="section-subtitle">听听他们的舞蹈故事</p>
      </div>
      
      <div class="testimonials-grid">
        <div class="testimonial-card">
          <div class="testimonial-avatar">
            <img src="/images/zym.png" alt="张玉梅">
          </div>
          <div class="testimonial-content">
            <p class="testimonial-text">
              "在这个平台上学会了好多舞蹈，身体越来越健康，
              心情也变得更好了。老师讲解得很仔细，动作简单易学。"
            </p>
            <div class="testimonial-author">
              <div class="author-name">张玉梅</div>
              <div class="author-age">65岁</div>
            </div>
          </div>
        </div>
        
        <div class="testimonial-card">
          <div class="testimonial-avatar">
            <img src="/images/wdf.png" alt="王德福">
          </div>
          <div class="testimonial-content">
            <p class="testimonial-text">
              "以前不敢跳舞，现在跟着视频学，没有心理压力。
              AI教练还能纠正我的动作，进步很快！"
            </p>
            <div class="testimonial-author">
              <div class="author-name">王德福</div>
              <div class="author-age">68岁</div>
            </div>
          </div>
        </div>
        
        <div class="testimonial-card">
          <div class="testimonial-avatar">
            <img src="/images/csf.png" alt="陈淑芬">
          </div>
          <div class="testimonial-content">
            <p class="testimonial-text">
              "社交功能很棒，认识了很多舞友，大家互相鼓励，
              一起打卡挑战，让运动变得更有趣。"
            </p>
            <div class="testimonial-author">
              <div class="author-name">陈淑芬</div>
              <div class="author-age">62岁</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* 主页特殊样式调整 */
.home-container {
  background: var(--bg-primary);
  min-height: 100vh;
  position: relative;
}

.hero-section {
  position: relative;
  min-height: calc(100vh - 64px); /* 减去导航栏高度 */
  background: 
    linear-gradient(135deg, 
      rgba(212, 175, 55, 0.4) 0%, 
      rgba(205, 133, 63, 0.3) 50%,
      rgba(218, 165, 32, 0.4) 100%
    ),
    url('/background.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-blend-mode: multiply;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
}

/* 桌面端：为主页内容添加顶部间距 */
@media (min-width: 641px) {
  .home-container {
    padding-top: 64px;
  }
}

/* 组件特有样式 - 优雅金棕色主题 */
.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 40px;
}

.hero-btn {
  min-width: 180px;
  font-size: var(--font-size-large);
  padding: 16px 32px;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: var(--shadow);
}

.primary-btn {
  background: var(--bg-secondary);
  color: var(--primary-color);
  border: 2px solid var(--bg-secondary);
}

.primary-btn:hover {
  background: var(--primary-color);
  color: var(--text-white);
  transform: translateY(-3px);
  box-shadow: var(--shadow-heavy);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-white);
  border: 2px solid var(--text-white);
  backdrop-filter: blur(10px);
}

.secondary-btn:hover {
  background: var(--text-white);
  color: var(--primary-color);
  transform: translateY(-3px);
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.section-title {
  font-size: var(--font-size-title);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: var(--gradient-warm);
  border-radius: 2px;
}

.section-subtitle {
  font-size: var(--font-size-large);
  color: var(--text-secondary);
  margin: 0;
}

/* 数据统计样式 */
.stats-section {
  background: var(--gradient-primary);
  color: var(--text-white);
  padding: 60px 0;
  margin: 60px 0;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 12px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.stat-label {
  font-size: var(--font-size-large);
  opacity: 0.95;
  font-weight: 500;
}

/* 快速入门样式 */
.quick-start-section {
  padding: 60px 0;
  background: var(--bg-accent);
}

.steps-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  max-width: 900px;
  margin: 0 auto 40px;
  padding: 0 24px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.step-item:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-light);
}

.step-number {
  width: 60px;
  height: 60px;
  background: var(--gradient-warm);
  color: var(--text-white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xlarge);
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: var(--shadow-light);
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: var(--font-size-large);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.step-description {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.quick-start-actions {
  text-align: center;
}

.start-btn {
  min-width: 200px;
  font-size: var(--font-size-large);
  padding: 16px 40px;
  border-radius: 25px;
  font-weight: 600;
  box-shadow: var(--shadow);
  background: var(--gradient-warm);
  border: none;
  color: var(--text-white);
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

/* 用户评价样式 */
.testimonials-section {
  padding: 60px 0;
  background: var(--bg-secondary);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.testimonial-card {
  display: flex;
  gap: 20px;
  padding: 32px;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-light);
}

.testimonial-avatar {
  flex-shrink: 0;
}

.testimonial-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-color);
  box-shadow: var(--shadow-light);
}

.testimonial-content {
  flex: 1;
}

.testimonial-text {
  font-size: var(--font-size-base);
  line-height: 1.6;
  color: var(--text-primary);
  margin-bottom: 20px;
  font-style: italic;
  position: relative;
}

.testimonial-text::before {
  content: '"';
  font-size: 3em;
  color: var(--primary-light);
  position: absolute;
  left: -10px;
  top: -10px;
  line-height: 1;
  opacity: 0.3;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-name {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--primary-color);
}

.author-age {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  background: var(--bg-accent);
  padding: 4px 12px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

/* 动画效果 */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-actions {
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
  
  .hero-btn {
    min-width: 160px;
    font-size: var(--font-size-base);
    padding: 14px 28px;
  }
  
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 32px;
  }
  
  .stat-number {
    font-size: 2.5rem;
  }
  
  .steps-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .step-item {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .testimonials-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .testimonial-card {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .stats-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .features-grid {
    padding: 0 16px;
  }
  
  .testimonials-grid {
    padding: 0 16px;
  }
  
  .steps-container {
    padding: 0 16px;
  }
}
</style> 