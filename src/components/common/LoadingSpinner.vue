<template>
  <div class="loading-spinner" :class="containerClass">
    <!-- 默认加载动画 -->
    <div v-if="type === 'default'" class="default-spinner">
      <el-icon :size="size" class="is-loading">
        <Loading />
      </el-icon>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
    
    <!-- 圆形进度条 -->
    <div v-else-if="type === 'circle'" class="circle-spinner">
      <svg :width="size" :height="size" viewBox="0 0 50 50">
        <circle
          cx="25"
          cy="25"
          r="20"
          fill="none"
          stroke="var(--el-border-color-light)"
          stroke-width="3"
        />
        <circle
          cx="25"
          cy="25"
          r="20"
          fill="none"
          :stroke="color"
          stroke-width="3"
          stroke-linecap="round"
          stroke-dasharray="31.416"
          stroke-dashoffset="31.416"
          class="progress-circle"
        />
      </svg>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
    
    <!-- 点状动画 -->
    <div v-else-if="type === 'dots'" class="dots-spinner">
      <div class="dots-container">
        <div class="dot" v-for="i in 3" :key="i"></div>
      </div>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
    
    <!-- 波浪动画 -->
    <div v-else-if="type === 'wave'" class="wave-spinner">
      <div class="wave-container">
        <div class="wave-bar" v-for="i in 5" :key="i"></div>
      </div>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
    
    <!-- 脉冲动画 -->
    <div v-else-if="type === 'pulse'" class="pulse-spinner">
      <div class="pulse-circle"></div>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
    
    <!-- 骨架屏 -->
    <div v-else-if="type === 'skeleton'" class="skeleton-spinner">
      <div class="skeleton-content">
        <div v-if="skeletonConfig.avatar" class="skeleton-avatar"></div>
        <div class="skeleton-main">
          <div v-if="skeletonConfig.title" class="skeleton-title"></div>
          <div v-if="skeletonConfig.lines" class="skeleton-lines">
            <div 
              class="skeleton-line" 
              v-for="i in skeletonConfig.lines" 
              :key="i"
              :style="{ width: i === skeletonConfig.lines ? '60%' : '100%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 自定义插槽 -->
    <div v-else-if="type === 'custom'" class="custom-spinner">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Loading } from '@element-plus/icons-vue'

interface SkeletonConfig {
  avatar?: boolean
  title?: boolean
  lines?: number
}

interface Props {
  type?: 'default' | 'circle' | 'dots' | 'wave' | 'pulse' | 'skeleton' | 'custom'
  size?: number | string
  color?: string
  text?: string
  background?: boolean
  fullscreen?: boolean
  transparent?: boolean
  skeletonConfig?: SkeletonConfig
}

const props = withDefaults(defineProps<Props>(), {
  type: 'default',
  size: 40,
  color: '#409eff',
  background: true,
  transparent: false,
  skeletonConfig: () => ({
    avatar: true,
    title: true,
    lines: 3
  })
})

const containerClass = computed(() => ({
  'with-background': props.background,
  'fullscreen': props.fullscreen,
  'transparent': props.transparent
}))
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.loading-spinner.with-background {
  background: var(--el-fill-color-light);
  border-radius: 8px;
}

.loading-spinner.transparent {
  background: transparent;
}

.loading-spinner.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  background: rgba(255, 255, 255, 0.9);
}

.loading-text {
  margin-top: 16px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  text-align: center;
}

/* 默认样式 */
.default-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 圆形进度条 */
.circle-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.progress-circle {
  transform-origin: center;
  animation: circle-rotate 2s linear infinite;
}

@keyframes circle-rotate {
  0% {
    transform: rotate(0deg);
    stroke-dashoffset: 31.416;
  }
  50% {
    stroke-dashoffset: 0;
  }
  100% {
    transform: rotate(360deg);
    stroke-dashoffset: 31.416;
  }
}

/* 点状动画 */
.dots-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dots-container {
  display: flex;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: v-bind(color);
  animation: dot-bounce 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes dot-bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 波浪动画 */
.wave-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.wave-container {
  display: flex;
  align-items: flex-end;
  height: 40px;
  gap: 4px;
}

.wave-bar {
  width: 4px;
  background: v-bind(color);
  border-radius: 2px;
  animation: wave-stretch 1.2s ease-in-out infinite;
}

.wave-bar:nth-child(1) { animation-delay: -1.1s; }
.wave-bar:nth-child(2) { animation-delay: -1.0s; }
.wave-bar:nth-child(3) { animation-delay: -0.9s; }
.wave-bar:nth-child(4) { animation-delay: -0.8s; }
.wave-bar:nth-child(5) { animation-delay: -0.7s; }

@keyframes wave-stretch {
  0%, 40%, 100% {
    height: 8px;
  }
  20% {
    height: 40px;
  }
}

/* 脉冲动画 */
.pulse-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pulse-circle {
  width: v-bind(size + 'px');
  height: v-bind(size + 'px');
  border-radius: 50%;
  background: v-bind(color);
  animation: pulse-scale 1.5s ease-in-out infinite;
}

@keyframes pulse-scale {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

/* 骨架屏 */
.skeleton-spinner {
  width: 100%;
  max-width: 400px;
}

.skeleton-content {
  display: flex;
  gap: 16px;
  padding: 16px;
}

.skeleton-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-main {
  flex: 1;
}

.skeleton-title {
  height: 20px;
  border-radius: 4px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  margin-bottom: 12px;
}

.skeleton-lines {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-line {
  height: 14px;
  border-radius: 4px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* 自定义内容 */
.custom-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .loading-spinner {
    padding: 16px;
  }
  
  .loading-text {
    font-size: 13px;
  }
  
  .skeleton-content {
    padding: 12px;
  }
  
  .skeleton-avatar {
    width: 50px;
    height: 50px;
  }
}

@media (max-width: 480px) {
  .loading-spinner {
    padding: 12px;
  }
  
  .dots-container {
    gap: 6px;
  }
  
  .dot {
    width: 6px;
    height: 6px;
  }
  
  .wave-container {
    height: 30px;
  }
  
  .wave-bar {
    width: 3px;
  }
}
</style>