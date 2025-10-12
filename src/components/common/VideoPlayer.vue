<template>
  <div class="video-player" :class="{ 'fullscreen': isFullscreen }">
    <video
      ref="videoRef"
      :src="src"
      :poster="poster"
      :controls="controls"
      :autoplay="autoplay"
      :muted="muted"
      :loop="loop"
      :playsinline="playsinline"
      class="video-element"
      @loadstart="onLoadStart"
      @loadeddata="onLoadedData"
      @play="onPlay"
      @pause="onPause"
      @ended="onEnded"
      @timeupdate="onTimeUpdate"
      @error="onError"
    ></video>
    
    <!-- 自定义控制栏 -->
    <div v-if="!controls" class="video-controls">
      <div class="control-bar">
        <!-- 播放/暂停按钮 -->
        <button class="control-btn" @click="togglePlay">
          <el-icon size="20">
            <VideoPlay v-if="!isPlaying" />
            <VideoPause v-else />
          </el-icon>
        </button>
        
        <!-- 进度条 -->
        <div class="progress-container" @click="seekTo">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>
        </div>
        
        <!-- 时间显示 -->
        <span class="time-display">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
        
        <!-- 音量控制 -->
        <div class="volume-control">
          <button class="control-btn" @click="toggleMute">
            <el-icon size="18">
              <Mute v-if="isMuted || volume === 0" />
              <Microphone v-else />
            </el-icon>
          </button>
          <input
            type="range"
            v-model="volume"
            min="0"
            max="1"
            step="0.1"
            class="volume-slider"
            @input="changeVolume"
          />
        </div>
        
        <!-- 全屏按钮 -->
        <button class="control-btn" @click="toggleFullscreen">
          <el-icon size="20">
            <FullScreen />
          </el-icon>
        </button>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="video-loading">
      <el-icon class="is-loading" size="40">
        <Loading />
      </el-icon>
      <span>加载中...</span>
    </div>
    
    <!-- 错误状态 -->
    <div v-if="error" class="video-error">
      <el-icon size="40" color="#f56c6c">
        <WarningFilled />
      </el-icon>
      <span>{{ errorMessage }}</span>
      <el-button type="primary" size="small" @click="retry">重试</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { 
  VideoPlay, 
  VideoPause, 
  FullScreen, 
  Mute, 
  Microphone, 
  Loading, 
  WarningFilled 
} from '@element-plus/icons-vue'

interface Props {
  src: string
  poster?: string
  controls?: boolean
  autoplay?: boolean
  muted?: boolean
  loop?: boolean
  playsinline?: boolean
  width?: string | number
  height?: string | number
}

const props = withDefaults(defineProps<Props>(), {
  controls: true,
  autoplay: false,
  muted: false,
  loop: false,
  playsinline: true
})

const emit = defineEmits<{
  play: []
  pause: []
  ended: []
  error: [error: Event]
  timeupdate: [currentTime: number]
  loadstart: []
  loadeddata: []
}>()

const videoRef = ref<HTMLVideoElement>()
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(1)
const isMuted = ref(false)
const isFullscreen = ref(false)
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')

const progressPercentage = computed(() => {
  return duration.value > 0 ? (currentTime.value / duration.value) * 100 : 0
})

// 格式化时间
const formatTime = (time: number): string => {
  if (!time || isNaN(time)) return '00:00'
  const minutes = Math.floor(time / 60)
  const seconds = Math.floor(time % 60)
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

// 播放/暂停切换
const togglePlay = () => {
  if (!videoRef.value) return
  
  if (isPlaying.value) {
    videoRef.value.pause()
  } else {
    videoRef.value.play()
  }
}

// 静音切换
const toggleMute = () => {
  if (!videoRef.value) return
  
  isMuted.value = !isMuted.value
  videoRef.value.muted = isMuted.value
}

// 音量调整
const changeVolume = () => {
  if (!videoRef.value) return
  
  videoRef.value.volume = volume.value
  isMuted.value = volume.value === 0
}

// 进度跳转
const seekTo = (event: MouseEvent) => {
  if (!videoRef.value) return
  
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
  const percent = (event.clientX - rect.left) / rect.width
  videoRef.value.currentTime = percent * duration.value
}

// 全屏切换
const toggleFullscreen = () => {
  if (!videoRef.value) return
  
  if (!isFullscreen.value) {
    if (videoRef.value.requestFullscreen) {
      videoRef.value.requestFullscreen()
    } else if ((videoRef.value as any).webkitRequestFullscreen) {
      (videoRef.value as any).webkitRequestFullscreen()
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
    } else if ((document as any).webkitExitFullscreen) {
      (document as any).webkitExitFullscreen()
    }
  }
}

// 重试播放
const retry = () => {
  error.value = false
  errorMessage.value = ''
  if (videoRef.value) {
    videoRef.value.load()
  }
}

// 视频事件处理
const onLoadStart = () => {
  loading.value = true
  emit('loadstart')
}

const onLoadedData = () => {
  loading.value = false
  if (videoRef.value) {
    duration.value = videoRef.value.duration
    volume.value = videoRef.value.volume
  }
  emit('loadeddata')
}

const onPlay = () => {
  isPlaying.value = true
  emit('play')
}

const onPause = () => {
  isPlaying.value = false
  emit('pause')
}

const onEnded = () => {
  isPlaying.value = false
  emit('ended')
}

const onTimeUpdate = () => {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime
    emit('timeupdate', currentTime.value)
  }
}

const onError = (event: Event) => {
  loading.value = false
  error.value = true
  errorMessage.value = '视频加载失败，请检查网络连接或视频文件'
  emit('error', event)
}

// 监听全屏状态变化
const handleFullscreenChange = () => {
  isFullscreen.value = !!(
    document.fullscreenElement ||
    (document as any).webkitFullscreenElement
  )
}

// 监听属性变化
watch(() => props.src, () => {
  error.value = false
  errorMessage.value = ''
})

onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange)
  document.addEventListener('webkitfullscreenchange', handleFullscreenChange)
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
  document.removeEventListener('webkitfullscreenchange', handleFullscreenChange)
})

// 暴露方法给父组件
defineExpose({
  play: () => videoRef.value?.play(),
  pause: () => videoRef.value?.pause(),
  togglePlay,
  seekTo,
  setVolume: (vol: number) => {
    volume.value = vol
    if (videoRef.value) videoRef.value.volume = vol
  },
  getCurrentTime: () => currentTime.value,
  getDuration: () => duration.value
})
</script>

<style scoped>
.video-player {
  position: relative;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.video-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 20px 15px 15px;
  opacity: 0;
  transition: opacity 0.3s;
}

.video-player:hover .video-controls {
  opacity: 1;
}

.control-bar {
  display: flex;
  align-items: center;
  gap: 15px;
}

.control-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.progress-container {
  flex: 1;
  height: 6px;
  cursor: pointer;
}

.progress-bar {
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #409eff;
  border-radius: 3px;
  transition: width 0.1s;
}

.time-display {
  color: white;
  font-size: 12px;
  min-width: 100px;
  text-align: center;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.volume-slider {
  width: 60px;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  outline: none;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
}

.volume-slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

.video-loading,
.video-error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: white;
  text-align: center;
}

.video-error {
  color: #f56c6c;
}

.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  border-radius: 0;
}

@media (max-width: 768px) {
  .control-bar {
    gap: 10px;
  }
  
  .time-display {
    font-size: 10px;
    min-width: 80px;
  }
  
  .volume-slider {
    width: 40px;
  }
}
</style>