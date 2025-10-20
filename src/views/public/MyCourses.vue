<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElCard, ElEmpty, ElButton, ElImage, ElProgress, ElTag, ElIcon, ElRow, ElCol } from 'element-plus'
import { VideoPlay, Clock, Trophy } from '@element-plus/icons-vue'
import { courseApi } from '@/api/course'
import type { Course } from '@/api/course'

const router = useRouter()

const courses = ref<Course[]>([])
const loading = ref(false)

// 获取我的课程
const fetchMyCourses = async () => {
  loading.value = true
  try {
    courses.value = await courseApi.getUserCourses()
  } catch (error) {
    console.error('获取我的课程失败:', error)
  } finally {
    loading.value = false
  }
}

// 继续学习
const continueLearning = (course: Course) => {
  router.push(`/course/${course.id}/learn`)
}

// 查看详情
const viewDetail = (course: Course) => {
  router.push(`/course/${course.id}`)
}

// 获取难度文本
const getDifficultyText = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return '初级'
    case 'intermediate': return '中级'
    case 'advanced': return '高级'
    default: return '未知'
  }
}

// 获取难度标签类型
const getDifficultyType = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return 'success'
    case 'intermediate': return 'warning'
    case 'advanced': return 'danger'
    default: return 'info'
  }
}

onMounted(() => {
  fetchMyCourses()
})
</script>

<template>
  <div class="my-courses page-with-nav">
    <div class="page-header">
      <h1>我的课程</h1>
      <p>继续您的舞蹈学习之旅</p>
    </div>

    <div v-loading="loading" class="courses-container">
      <ElEmpty v-if="!loading && courses.length === 0" description="您还没有报名任何课程">
        <ElButton type="primary" @click="$router.push('/dance-courses')">
          去选课
        </ElButton>
      </ElEmpty>

      <ElRow v-else :gutter="20">
        <ElCol v-for="course in courses" :key="course.id" :xs="24" :sm="12" :md="8" :lg="6">
          <ElCard class="course-card" shadow="hover">
            <div class="course-cover">
              <ElImage 
                :src="course.cover_url || '/images/default-course.png'"
                fit="cover"
                class="cover-image"
              />
              <div class="course-overlay">
                <ElButton 
                  type="primary" 
                  :icon="VideoPlay"
                  circle
                  size="large"
                  @click="continueLearning(course)"
                />
              </div>
            </div>
            
            <div class="course-info">
              <h3 class="course-title" @click="viewDetail(course)">{{ course.title }}</h3>
              
              <div class="course-meta">
                <ElTag :type="getDifficultyType(course.difficulty)" size="small">
                  {{ getDifficultyText(course.difficulty) }}
                </ElTag>
                
                <div class="meta-item">
                  <ElIcon size="14"><Clock /></ElIcon>
                  <span>{{ course.duration }}分钟</span>
                </div>
              </div>
              
              <!-- 学习进度 -->
              <div class="course-progress">
                <div class="progress-info">
                  <span>学习进度</span>
                  <span>{{ Math.round((course.progress || 0)) }}%</span>
                </div>
                <ElProgress 
                  :percentage="Math.round((course.progress || 0))" 
                  :stroke-width="6"
                  :show-text="false"
                />
              </div>
              
              <div class="course-actions">
                <ElButton 
                  type="primary" 
                  size="small"
                  @click="continueLearning(course)"
                >
                  {{ (course.progress || 0) > 0 ? '继续学习' : '开始学习' }}
                </ElButton>
                <ElButton 
                  type="default" 
                  size="small"
                  @click="viewDetail(course)"
                >
                  查看详情
                </ElButton>
              </div>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<style scoped>
.my-courses {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 8px;
}

.page-header p {
  color: #606266;
  font-size: 16px;
}

.courses-container {
  min-height: 400px;
}

.course-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-2px);
}

.course-cover {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 16px;
}

.cover-image {
  width: 100%;
  height: 100%;
}

.course-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.course-card:hover .course-overlay {
  opacity: 1;
}

.course-info {
  padding: 0 4px;
}

.course-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
  cursor: pointer;
  transition: color 0.3s;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-title:hover {
  color: #409EFF;
}

.course-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
  font-size: 12px;
}

.course-progress {
  margin-bottom: 16px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.course-actions {
  display: flex;
  gap: 8px;
}

.course-actions .el-button {
  flex: 1;
}

@media (max-width: 768px) {
  .my-courses {
    padding: 10px;
  }
  
  .page-header h1 {
    font-size: 24px;
  }
  
  .course-actions {
    flex-direction: column;
  }
}
</style> 
 