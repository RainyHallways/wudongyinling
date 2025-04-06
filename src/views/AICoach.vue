<template>
  <div class="ai-coach">
    <h1 class="page-title">AI 智能教练</h1>
    <p class="section-subtitle">实时分析您的舞蹈动作，提供专业指导</p>

    <!-- 视频区域 -->
    <el-row :gutter="20" class="mt-4">
      <el-col :xs="24" :sm="24" :md="24" :lg="16">
        <el-card class="video-section">
          <div class="video-container">
            <div class="video-placeholder">
              <el-icon :size="50"><VideoCameraFilled /></el-icon>
              <h3>准备开始练习</h3>
              <p>请启动摄像头，选择一种舞蹈开始练习</p>
            </div>
          </div>
          <div class="video-controls">
            <el-button type="primary" size="large" @click="startCamera">
              <el-icon><VideoCamera /></el-icon>
              启动摄像头
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="24" :lg="8">
        <el-card class="score-section">
          <template #header>
            <div class="card-header">
              <span>实时得分</span>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :xs="8" :sm="8" :md="8" :lg="8" class="score-item">
              <el-progress type="dashboard" :percentage="85" :width="100" status="success">
                <template #default>
                  <div class="percentage">85<span>分</span></div>
                  <div class="progress-label">总体评分</div>
                </template>
              </el-progress>
            </el-col>
            <el-col :xs="8" :sm="8" :md="8" :lg="8" class="score-item">
              <el-progress type="dashboard" :percentage="92" :width="100" color="#409eff">
                <template #default>
                  <div class="percentage">92<span>分</span></div>
                  <div class="progress-label">动作协调</div>
                </template>
              </el-progress>
            </el-col>
            <el-col :xs="8" :sm="8" :md="8" :lg="8" class="score-item">
              <el-progress type="dashboard" :percentage="78" :width="100" color="#e6a23c">
                <template #default>
                  <div class="percentage">78<span>分</span></div>
                  <div class="progress-label">节奏感</div>
                </template>
              </el-progress>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <!-- 动作指导与建议 -->
    <el-row :gutter="20" class="mt-4">
      <el-col :xs="24" :sm="24" :md="12">
        <el-card class="guidance-section">
          <template #header>
            <div class="card-header">
              <span>动作要点</span>
            </div>
          </template>
          <div class="feedback-container">
            <div 
              v-for="point in keyPoints" 
              :key="point.id" 
              class="feedback-item"
              :style="{ backgroundColor: `${point.color}10`, color: point.color }"
            >
              <el-icon><Check /></el-icon>
              {{ point.content }}
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="24" :md="12">
        <el-card class="suggestions-section">
          <template #header>
            <div class="card-header">
              <span>练习建议</span>
            </div>
          </template>
          <el-collapse v-model="activeCollapse">
            <el-collapse-item 
              v-for="suggestion in suggestions" 
              :key="suggestion.id" 
              :title="suggestion.title" 
              :name="suggestion.id"
            >
              {{ suggestion.content }}
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-col>
    </el-row>

    <!-- 练习历史 -->
    <el-row class="mt-4">
      <el-col :span="24">
        <el-card class="history-section">
          <template #header>
            <div class="card-header">
              <span>练习历史</span>
            </div>
          </template>
          <el-table :data="practiceHistory" stripe style="width: 100%">
            <el-table-column prop="date" label="日期时间" />
            <el-table-column prop="duration" label="时长" />
            <el-table-column prop="dance" label="舞蹈类型" />
            <el-table-column prop="score" label="得分" />
            <el-table-column prop="improvement" label="改进建议" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Icons from '../utils/icons'

// 图标组件
const videoCameraIcon = Icons.VideoCamera
const videoPlayIcon = Icons.VideoPlay
const videoPauseIcon = Icons.VideoPause
const refreshRightIcon = Icons.RefreshRight

// 评分数据
const scores = ref([
  { name: '动作准确度', value: 85, color: '#67c23a' },
  { name: '节奏感', value: 78, color: '#e6a23c' },
  { name: '姿态标准度', value: 92, color: '#409eff' }
])

// 实时反馈
const realtimeFeedback = ref([
  {
    id: 1,
    type: 'success',
    icon: Icons.CircleCheck,
    message: '手臂抬起角度标准'
  },
  {
    id: 2,
    type: 'warning',
    icon: Icons.Warning,
    message: '请注意膝盖弯曲幅度'
  },
  {
    id: 3,
    type: 'info',
    icon: Icons.InfoFilled,
    message: '建议放慢节奏'
  }
])

// 动作要点
const keyPoints = ref([
  {
    id: 1,
    content: '双脚与肩同宽，保持重心稳定',
    type: 'primary',
    color: '#409eff'
  },
  {
    id: 2,
    content: '手臂自然弯曲，保持在胸前位置',
    type: 'success',
    color: '#67c23a'
  },
  {
    id: 3,
    content: '跟随音乐节奏，保持呼吸均匀',
    type: 'warning',
    color: '#e6a23c'
  },
  {
    id: 4,
    content: '注意保护膝关节，避免过度弯曲',
    type: 'danger',
    color: '#f56c6c'
  }
])

// 练习建议
const activeCollapse = ref(['1'])
const suggestions = ref([
  {
    id: '1',
    title: '动作改进建议',
    content: '建议加强手臂的协调性训练，可以通过慢动作练习来提高准确度。'
  },
  {
    id: '2',
    title: '节奏训练建议',
    content: '可以先不跟音乐，单独练习基本步伐，熟练后再配合音乐。'
  },
  {
    id: '3',
    title: '体能建议',
    content: '目前运动强度适中，建议每次练习时间控制在45分钟以内。'
  }
])

// 练习历史
const practiceHistory = ref([
  {
    date: '2025-03-28 15:30',
    duration: '30分钟',
    dance: '广场舞基础步伐',
    score: 85,
    improvement: '手臂动作需要更加协调'
  },
  {
    date: '2025-03-27 16:00',
    duration: '45分钟',
    dance: '民族舞基础',
    score: 92,
    improvement: '节奏把握得很好，继续保持'
  },
  {
    date: '2025-03-26 14:30',
    duration: '20分钟',
    dance: '健身舞基础',
    score: 78,
    improvement: '需要加强重心的稳定性'
  }
])

// 开始摄像头
const startCamera = () => {
  // 实现摄像头启动逻辑
  console.log('启动摄像头')
}
</script>

<style scoped>
.ai-coach {
  padding: 20px;
  padding-bottom: 40px;
  margin-bottom: 60px;
}

.page-title {
  font-size: 32px;
  text-align: center;
  margin: 40px 0;
  color: var(--primary-color);
}

.section-subtitle {
  text-align: center;
  margin-bottom: 30px;
  color: #666;
}

.video-container {
  height: 400px;
  background-color: #f5f7fa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-placeholder {
  text-align: center;
  color: #909399;
}

.video-placeholder .el-icon {
  margin-bottom: 20px;
}

.video-controls {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.score-section {
  height: 100%;
}

.score-item {
  text-align: center;
}

.progress-label {
  font-size: 18px;
  color: #606266;
  line-height: 1.4;
}

.percentage {
  font-size: 20px;
  font-weight: bold;
  color: var(--primary-color);
}

.guidance-section, .suggestions-section {
  height: 100%;
  margin-bottom: 20px;
}

.feedback-container {
  margin-bottom: 15px;
}

.feedback-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.feedback-item .el-icon {
  margin-right: 8px;
}

.feedback-item.success {
  background-color: #f0f9eb;
  color: var(--success-color);
}

.feedback-item.warning {
  background-color: #fdf6ec;
  color: var(--warning-color);
}

.feedback-item.info {
  background-color: #f4f4f5;
  color: var(--info-color);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 自定义工具类 */
.mt-1 { margin-top: 0.25rem !important; }
.mt-2 { margin-top: 0.5rem !important; }
.mt-3 { margin-top: 1rem !important; }
.mt-4 { margin-top: 1.5rem !important; }
.mt-5 { margin-top: 3rem !important; }

.history-section {
  margin-bottom: 80px;
}

@media (max-width: 992px) {
  .video-container {
    height: 300px;
  }
  
  .ai-coach {
    margin-bottom: 60px;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 26px;
  }
  
  .video-container {
    height: 250px;
  }
  
  .score-item {
    margin-bottom: 20px;
  }
}
</style> 