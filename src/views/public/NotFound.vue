<template>
  <div class="not-found-container page-with-nav">
    <div class="not-found-content">
      <div class="error-animation">
        <div class="error-number">4</div>
        <div class="error-zero">
          <div class="zero-circle"></div>
          <div class="zero-dance">
            <div class="dance-figure">💃</div>
          </div>
        </div>
        <div class="error-number">4</div>
      </div>
      
      <div class="error-message">
        <h1 class="error-title">哎呀，页面走丢了</h1>
        <p class="error-description">
          很抱歉，您访问的页面不存在或已被移动。<br>
          让我们帮您找到正确的地方吧！
        </p>
      </div>
      
      <div class="action-buttons">
        <el-button type="primary" size="large" @click="router.push('/')" class="primary-action">
          <el-icon><House /></el-icon> 返回首页
        </el-button>
        <el-button size="large" @click="goBack" class="secondary-action">
          <el-icon><ArrowLeft /></el-icon> 返回上页
        </el-button>
      </div>
      
      <div class="not-found-suggestions">
        <h3>您可能想要访问：</h3>
        <div class="suggestion-grid">
          <el-card class="suggestion-card" shadow="hover" @click="router.push('/dance-courses')">
            <div class="card-icon">
              <el-icon><VideoCameraFilled /></el-icon>
            </div>
            <div class="card-content">
              <h4>舞蹈课程</h4>
              <p>探索丰富的舞蹈教学资源</p>
            </div>
          </el-card>
          
          <el-card class="suggestion-card" shadow="hover" @click="router.push('/ai-coach')">
            <div class="card-icon">
              <el-icon><Cpu /></el-icon>
            </div>
            <div class="card-content">
              <h4>AI教练</h4>
              <p>智能评估您的舞蹈动作</p>
            </div>
          </el-card>
          
          <el-card class="suggestion-card" shadow="hover" @click="router.push('/about')">
            <div class="card-icon">
              <el-icon><InfoFilled /></el-icon>
            </div>
            <div class="card-content">
              <h4>关于我们</h4>
              <p>了解舞动银龄平台</p>
            </div>
          </el-card>
          
          <el-card class="suggestion-card" shadow="hover" @click="router.push('/contact')">
            <div class="card-icon">
              <el-icon><Phone /></el-icon>
            </div>
            <div class="card-content">
              <h4>联系我们</h4>
              <p>获取帮助与支持</p>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { VideoCameraFilled, Cpu, InfoFilled, Phone, House, ArrowLeft } from '@element-plus/icons-vue';

const router = useRouter();

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1);
  } else {
    router.push('/');
  }
};
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 40px 20px;
  background: linear-gradient(135deg, #f7d060 0%, #a57c00 100%);
  position: relative;
  overflow: hidden;
}

.not-found-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  animation: moveGrid 20s linear infinite;
}

@keyframes moveGrid {
  0% { transform: translate(0, 0); }
  100% { transform: translate(20px, 20px); }
}

.not-found-content {
  max-width: 800px;
  width: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
}

.error-animation {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 40px;
  gap: 10px;
}

.error-number {
  font-size: 120px;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: bounce 2s ease-in-out infinite;
}

.error-number:nth-child(3) {
  animation-delay: 0.5s;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-20px); }
  60% { transform: translateY(-10px); }
}

.error-zero {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.zero-circle {
  position: absolute;
  width: 120px;
  height: 120px;
  border: 8px solid rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.zero-dance {
  position: absolute;
  animation: dance 3s ease-in-out infinite;
}

.dance-figure {
  font-size: 60px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

@keyframes dance {
  0%, 100% { transform: rotate(-5deg) translateY(0); }
  25% { transform: rotate(5deg) translateY(-5px); }
  50% { transform: rotate(-3deg) translateY(0); }
  75% { transform: rotate(3deg) translateY(-3px); }
}

.error-message {
  margin-bottom: 40px;
}

.error-title {
  font-size: 36px;
  font-weight: 700;
  color: white;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.error-description {
  font-size: 18px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 50px;
  flex-wrap: wrap;
}

.primary-action {
  background: white;
  color: var(--el-color-primary);
  border: none;
  border-radius: 25px;
  height: 50px;
  padding: 0 30px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.primary-action:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  background: var(--el-color-primary-light-9);
}

.secondary-action {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  border-radius: 25px;
  height: 50px;
  padding: 0 30px;
  font-size: 16px;
  font-weight: 600;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.secondary-action:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.not-found-suggestions {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.not-found-suggestions h3 {
  font-size: 24px;
  font-weight: 600;
  color: white;
  margin-bottom: 25px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.suggestion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.suggestion-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  backdrop-filter: blur(10px);
}

.suggestion-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
  background: white;
}

.card-icon {
  width: 50px;
  height: 50px;
  background: var(--el-color-primary-light-9);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 15px auto;
  font-size: 24px;
  color: var(--el-color-primary);
  transition: all 0.3s ease;
}

.suggestion-card:hover .card-icon {
  background: var(--el-color-primary);
  color: white;
  transform: scale(1.1);
}

.card-content h4 {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
}

.card-content p {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
  line-height: 1.4;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .not-found-container {
    padding: 30px 15px;
  }
  
  .error-animation {
    gap: 5px;
    margin-bottom: 30px;
  }
  
  .error-number {
    font-size: 80px;
  }
  
  .error-zero {
    width: 80px;
    height: 80px;
  }
  
  .zero-circle {
    width: 80px;
    height: 80px;
    border-width: 6px;
  }
  
  .dance-figure {
    font-size: 40px;
  }
  
  .error-title {
    font-size: 28px;
    margin-bottom: 15px;
  }
  
  .error-description {
    font-size: 16px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: 15px;
    margin-bottom: 40px;
  }
  
  .primary-action,
  .secondary-action {
    width: 200px;
  }
  
  .not-found-suggestions {
    padding: 20px;
  }
  
  .not-found-suggestions h3 {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .suggestion-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .not-found-container {
    padding: 20px 10px;
  }
  
  .error-number {
    font-size: 60px;
  }
  
  .error-zero {
    width: 60px;
    height: 60px;
  }
  
  .zero-circle {
    width: 60px;
    height: 60px;
    border-width: 4px;
  }
  
  .dance-figure {
    font-size: 30px;
  }
  
  .error-title {
    font-size: 24px;
  }
  
  .error-description {
    font-size: 15px;
  }
  
  .not-found-suggestions {
    padding: 15px;
  }
  
  .suggestion-card {
    padding: 15px;
  }
}
</style> 