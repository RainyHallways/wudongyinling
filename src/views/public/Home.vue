<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeStep = ref(0)
// 标记是否已经执行过数字动画
const animationExecuted = ref(false)

// 页面加载动画
onMounted(() => {
  // 添加渐入动画
  const cards = document.querySelectorAll('.fade-in')
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('visible')
        }, index * 100)
      }
    })
  }, { threshold: 0.1 })
  
  cards.forEach((card) => {
    observer.observe(card)
  })
  
  // 设置数字动画的可见性监测
  setupNumberAnimationObserver()
  
  // 步骤轮播效果
  startStepAnimation()
})

function getStepClass(index: number) {
    interface PositionMap {
      [key: number]: number[];
    }

    const positions: PositionMap = {
      0: [2, 1, 0],
      1: [0, 2, 1],
      2: [1, 0, 2],
    };

    const position = positions[activeStep.value][index];
    return `step-${position}`;
}
// 设置数字动画的可见性监测
function setupNumberAnimationObserver() {
  const statsSection = document.querySelector('.stats-section')
  if (!statsSection) return
  
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animationExecuted.value) {
        // 当统计区域进入视口且动画尚未执行过时，开始动画
        animateNumbers()
        animationExecuted.value = true
        // 动画执行后停止观察
        statsObserver.unobserve(entry.target)
      }
    })
  }, { threshold: 0.3 }) // 当30%的区域可见时触发
  
  statsObserver.observe(statsSection)
}

// 数字增长动画
function animateNumbers() {
  const statElements = document.querySelectorAll('.stat-number')
  
  statElements.forEach((element, index) => {
    // 为不同数字添加延迟，创建错落有致的动画效果
    setTimeout(() => {
      const target = parseInt(element.textContent?.replace(/,|\+|%/g, '') || '0')
      const duration = 2000
      const startTime = performance.now()
      const suffix = element.textContent?.match(/,|\+|%/g)?.[0] || ''
      
      function updateCount(currentTime: number) {
        const elapsedTime = currentTime - startTime
        
        if (elapsedTime < duration) {
          const progress = Math.min(elapsedTime / duration, 1)
          // 使用缓动函数使动画更自然
          const easeOutQuad = progress * (2 - progress)
          const current = Math.floor(target * easeOutQuad)
          
          // 无论数字大小，都应用千分位分隔符
          element.textContent = current.toLocaleString() + suffix
          
          requestAnimationFrame(updateCount)
        } else {
          element.textContent = target.toLocaleString() + suffix
        }
      }
      
      requestAnimationFrame(updateCount)
    }, index * 200) // 每个数字动画延迟200毫秒
  })
}

// 步骤轮播动画
function startStepAnimation() {
  setInterval(() => {
    activeStep.value = (activeStep.value + 1) % 3
  }, 3000)
}

// 滚动到指定区域
function scrollToSection(sectionId: string) {
  const section = document.getElementById(sectionId)
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <div class="home-container page-with-nav">
    
    <!-- 英雄区域 -->
    <section class="hero-section">
      <!-- 装饰性元素 -->
      <div class="hero-decor"></div>
      
      <div class="hero-content">
        <h1 class="hero-title" style="color: azure;">舞动银龄</h1>
        <p class="hero-subtitle" style="color: azure;">
          专为银发族打造的智能舞蹈学习平台<br>
          让舞蹈成为健康生活的美好伴侣
        </p>
        <div class="hero-actions">
          <el-button 
            type="primary" 
            size="large" 
            @click="$router.push('/courses')"
            class="hero-btn primary-btn"
            :hover-effect="true"
          >
            <i class="el-icon-video-play"></i>
            开始学习舞蹈
          </el-button>
          <el-button 
            size="large" 
            @click="$router.push('/about')"
            class="hero-btn secondary-btn"
            :hover-effect="true"
          >
            <i class="el-icon-info"></i>
            了解更多
          </el-button>
        </div>
      </div>
    </section>

    <!-- 特色功能区域 -->
    <section class="features-section" id="features">
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
            在欢乐氛围中坚持运动
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
      <div class="hero-particles"></div>
      <div class="stats-container">
        <div class="stat-item">
          <div class="stat-number">10000+</div>
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
    <section class="quick-start-section" id="quick-start">
      <div class="section-header">
        <h2 class="section-title">快速开始</h2>
        <p class="section-subtitle">三步开启您的舞蹈之旅</p>
      </div>
      
      <div class="steps-carousel">
        <div class="steps-container">
          <div 
            class="step-item" 
            v-for="(step, index) in 3" 
            :key="index"
            :class="getStepClass(index)"
          >
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <h3 class="step-title" v-if="index === 0">注册账户</h3>
              <h3 class="step-title" v-if="index === 1">选择课程</h3>
              <h3 class="step-title" v-if="index === 2">开始学习</h3>
        
              <p class="step-description" v-if="index === 0">简单注册，立即开始舞蹈学习之旅</p>
              <p class="step-description" v-if="index === 1">根据兴趣和身体状况选择合适的课程</p>
              <p class="step-description" v-if="index === 2">跟随视频教程，享受舞蹈带来的快乐</p>
            </div>
          </div>
        </div>
        
        <!-- 轮播指示器 -->
        <div class="step-indicators">
          <span 
            class="step-indicator" 
            v-for="(step, index) in 3" 
            :key="index"
            :class="{ active: activeStep === index }"
            @click="activeStep = index"
          ></span>
        </div>
      </div>
      
      <div class="quick-start-actions">
        <el-button 
          type="primary" 
          size="large" 
          @click="$router.push('/register')"
          class="start-btn"
          :hover-effect="true"
        >
          立即开始
        </el-button>
      </div>
    </section>

    <!-- 用户评价区域 -->
    <section class="testimonials-section" id="testimonials">
      <div class="section-header">
        <h2 class="section-title">用户心声</h2>
        <p class="section-subtitle">听听他们的舞蹈故事</p>
      </div>
      
      <div class="testimonials-grid">
        <div class="testimonial-card fade-in">
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
        
        <div class="testimonial-card fade-in">
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
        
        <div class="testimonial-card fade-in">
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
    
    <!-- 底部行动号召区域 -->
    <section class="cta-section">
      <div class="hero-particles"></div>
      <div class="cta-content">
        <h2 class="cta-title" style="color: azure;">准备好开始您的舞蹈之旅了吗？</h2>
        <p class="cta-subtitle"style="color: azure;">加入我们，开启健康快乐的晚年生活</p>
        <div class="cta-actions">
          <el-button 
            type="primary" 
            size="large" 
            @click="$router.push('/register')"
            class="cta-btn primary-btn"
            :hover-effect="true"
          >
            立即注册
          </el-button>
          <el-button 
            size="large" 
            @click="$router.push('/courses')"
            class="cta-btn secondary-btn"
            :hover-effect="true"
          >
            浏览课程
          </el-button>
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
  overflow-x: hidden;
}

/* 导航栏占位 */
.nav-placeholder {
  height: 64px;
}

/* 英雄区域 */
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
  background-position: center 25%;
  background-attachment: fixed;
  background-blend-mode: multiply;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
}

/* 装饰元素 */
.hero-decor {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

/* 粒子效果 */
.hero-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  background-image: 
    radial-gradient(circle, rgba(255, 255, 255, 0.7) 2px, transparent 2px),
    radial-gradient(circle, rgba(255, 255, 255, 0.4) 2px, transparent 2px);
  background-size: 80px 80px, 40px 40px;
  background-position: 0 0, 40px 40px;
  animation: float 20s linear infinite;
}

@keyframes float {
  0% {
    background-position: 0 0, 40px 40px;
  }
  100% {
    background-position: 0 80px, 40px 120px;
  }
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 20px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  letter-spacing: 2px;
  animation: fadeInUp 1s ease;
}

.hero-subtitle {
  font-size: 1.5rem;
  line-height: 1.6;
  margin-bottom: 30px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 1.2s ease 0.2s both;
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
  animation: fadeInUp 1.4s ease 0.4s both;
}

.hero-btn {
  min-width: 180px;
  font-size: var(--font-size-large);
  padding: 16px 32px;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}

.hero-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: all 0.6s ease;
}

.hero-btn:hover::before {
  left: 100%;
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
  display: inline-block;
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
  transition: all 0.3s ease;
}

.section-header:hover .section-title::after {
  width: 100px;
}

.section-subtitle {
  font-size: var(--font-size-large);
  color: var(--text-secondary);
  margin: 0;
}

/* 特色功能样式 */
.features-section {
  padding: 80px 0;
  position: relative;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.feature-card {
  padding: 32px;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

/* 移除底部线条动画 */
.feature-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-light);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
  display: inline-block;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.2) rotate(5deg);
}

.feature-title {
  font-size: var(--font-size-xlarge);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  transition: all 0.3s ease;
  position: relative;
  display: inline-block;
}

.feature-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 3px;
  background: var(--gradient-warm);
  border-radius: 2px;
  transition: width 0.35s ease-out;
}

.feature-card:hover .feature-title::after {
  width: 100%;
}

.feature-description {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  transition: all 0.3s ease;
}

/* 数据统计样式 */
.stats-section {
  background: var(--gradient-primary);
  color: var(--text-white);
  padding: 60px 0;
  margin: 60px 0;
  position: relative;
  overflow: hidden;
}

.stats-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
  position: relative;
  z-index: 1;
}

.stat-item {
  text-align: center;
  padding: 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 12px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.stat-item:hover .stat-number {
  transform: scale(1.1);
}

.stat-label {
  font-size: var(--font-size-large);
  opacity: 0.95;
  font-weight: 500;
}

/* 快速入门样式 */
.quick-start-section {
  padding: 80px 0;
  background: var(--bg-accent);
  position: relative;
}

.steps-carousel {
  max-width: 500px;
  margin: 0 auto 30px;
  position: relative;
  perspective: 1000px;
}

.steps-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  height: 300px;
  overflow: visible;
  transform-style: preserve-3d;
}

.step-item {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 500px;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  opacity: 0.35;
  z-index: 1;
  text-align: left;
  backface-visibility: hidden;
}

/* 根据位置设置不同的堆叠效果 */
.step-item.step-0 { /* 最底层 */
  transform: translateX(-50%) translateY(160px) translateZ(-125px) scale(0.8);
  opacity: 0.35;
  z-index: 1;
}

.step-item.step-1 { /* 中间层 */
  transform: translateX(-50%) translateY(80px) translateZ(-75px) scale(0.9);
  opacity: 0.6;
  z-index: 5;
}

.step-item.step-2 { /* 顶层/激活层 */
  transform: translateX(-50%) translateZ(0) scale(1);
  opacity: 1;
  z-index: 10;
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-light);
}

/* 悬停效果 */
.step-item:hover {
  opacity: 0.8 !important;
  transform: translateX(-50%) translateZ(10px) scale(1.02) !important;
  z-index: 8 !important;
}

.step-item.step-2:hover {
  opacity: 1 !important;
  transform: translateX(-50%) translateZ(20px) scale(1.05) !important;
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
  transition: all 0.3s ease;
}

.step-item:hover .step-number {
  transform: scale(1.1) rotate(10deg);
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

/* 轮播指示器 - 确保不受透视效果影响 */
.step-indicators {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 30px;
  position: relative;
  z-index: 20; /* 确保在所有卡片之上 */
  transform: none; /* 重置变换，不受父级透视影响 */
}

.step-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--border-color);
  cursor: pointer;
  transition: all 0.3s ease;
}

.step-indicator.active {
  width: 30px;
  border-radius: 6px;
  background: var(--primary-color);
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
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.start-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: all 0.6s ease;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.start-btn:hover::before {
  left: 100%;
}

/* 用户评价样式 */
.testimonials-section {
  padding: 80px 0;
  background: var(--bg-secondary);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
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
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.testimonial-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 80px;
  height: 80px;
  background: var(--primary-light);
  opacity: 0.1;
  border-radius: 50%;
  transform: translate(30%, 30%);
}

.testimonial-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-light);
}

.testimonial-avatar {
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.testimonial-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-color);
  box-shadow: var(--shadow-light);
  transition: all 0.3s ease;
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
  padding: 0 20px;
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

.testimonial-text::after {
  content: '"';
  font-size: 3em;
  color: var(--primary-light);
  position: absolute;
  right: -10px;
  bottom: -40px;
  line-height: 1;
  opacity: 0.3;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
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

/* 底部行动号召区域 */
.cta-section {
  background: var(--gradient-primary);
  color: var(--text-white);
  padding: 80px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 60%);
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.cta-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.cta-subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.cta-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-btn {
  min-width: 180px;
  font-size: var(--font-size-large);
  padding: 16px 32px;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}

.cta-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: all 0.6s ease;
}

.cta-btn:hover::before {
  left: 100%;
}

.cta-btn.primary-btn {
  background: var(--text-white);
  color: var(--primary-color);
  border: none;
}

.cta-btn.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-heavy);
  background: var(--bg-secondary);
}

.cta-btn.secondary-btn {
  background: transparent;
  color: var(--text-white);
  border: 2px solid var(--text-white);
}

.cta-btn.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
  box-shadow: var(--shadow);
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.8rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
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
    height: 250px;
  }
  
  .step-item {
    width: 90%;
    padding: 16px;
    gap: 12px;
  }
  
  .step-number {
    width: 50px;
    height: 50px;
    font-size: var(--font-size-large);
  }
  
  .step-title {
    font-size: var(--font-size-base);
  }
  
  .step-description {
    font-size: var(--font-size-small);
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
  
  .testimonial-avatar img {
    width: 70px;
    height: 70px;
  }
  
  .testimonial-author {
    justify-content: center;
  }
  
  .cta-title {
    font-size: 1.8rem;
  }
  
  .cta-subtitle {
    font-size: 1rem;
  }
  
  .cta-actions {
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
  
  .features-grid {
    padding: 0 16px;
    gap: 20px;
  }
  
  .feature-card {
    padding: 20px;
  }
  
  .feature-icon {
    font-size: 2rem;
  }
  
  .feature-title {
    font-size: var(--font-size-large);
  }
  
  .testimonials-grid {
    padding: 0 16px;
  }
  
  .testimonial-card {
    padding: 20px;
  }
  
  .steps-container {
    height: 250px;
  }
  
  .steps-container {
    padding: 0 16px;
  }
  
  .cta-btn {
    min-width: 150px;
    font-size: var(--font-size-base);
    padding: 12px 24px;
  }
}
</style>