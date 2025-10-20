<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElButton, ElCard, ElTag, ElIcon, ElImage, ElDivider, ElRow, ElCol, ElRate } from 'element-plus'
import { VideoPlay, Star, StarFilled, Clock, User, Trophy } from '@element-plus/icons-vue'
import { courseApi } from '@/api/course'
import type { Course } from '@/api/course'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const course = ref<Course | null>(null)
const loading = ref(false)
const isEnrolled = ref(false)
const isFavorited = ref(false)
const enrollLoading = ref(false)
const favoriteLoading = ref(false)

const courseId = computed(() => parseInt(route.params.id as string))

// 获取课程详情
const fetchCourseDetail = async () => {
  loading.value = true
  try {
    course.value = await courseApi.getCourseById(courseId.value)
  } catch (error) {
    ElMessage.error('获取课程详情失败')
    router.push('/dance-courses')
  } finally {
    loading.value = false
  }
}

// 报名课程
const handleEnroll = async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  enrollLoading.value = true
  try {
    await courseApi.enrollCourse({ course_id: courseId.value })
    isEnrolled.value = true
    ElMessage.success('报名成功！')
  } catch (error) {
    ElMessage.error('报名失败')
  } finally {
    enrollLoading.value = false
  }
}

// 收藏/取消收藏
const handleFavorite = async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  favoriteLoading.value = true
  try {
    // 这里需要实现收藏API
    isFavorited.value = !isFavorited.value
    ElMessage.success(isFavorited.value ? '收藏成功！' : '取消收藏成功！')
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    favoriteLoading.value = false
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

// 获取难度文本
const getDifficultyText = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return '初级'
    case 'intermediate': return '中级'
    case 'advanced': return '高级'
    default: return '未知'
  }
}

onMounted(() => {
  fetchCourseDetail()
})
</script>

<template>
  <div class="course-detail page-with-nav" v-loading="loading">
    <div v-if="course" class="course-content">
      <!-- 课程头部信息 -->
      <ElCard class="course-header">
        <ElRow :gutter="24">
          <ElCol :xs="24" :md="12">
            <div class="course-cover">
              <ElImage 
                :src="course.cover_url || '/images/default-course.png'"
                fit="cover"
                class="cover-image"
              />
              <div class="play-overlay" v-if="course.video_url" @click="$router.push(`/course/${course.id}/video`)">
                <ElIcon size="48" color="white">
                  <VideoPlay />
                </ElIcon>
              </div>
            </div>
          </ElCol>
          <ElCol :xs="24" :md="12">
            <div class="course-info">
              <h1 class="course-title">{{ course.title }}</h1>
              
              <div class="course-meta">
                <ElTag :type="getDifficultyType(course.difficulty)" size="large">
                  {{ getDifficultyText(course.difficulty) }}
                </ElTag>
                
                <div class="meta-item">
                  <ElIcon><Clock /></ElIcon>
                  <span>{{ course.duration }}分钟</span>
                </div>
                
                <div class="meta-item" v-if="course.instructor_name">
                  <ElIcon><User /></ElIcon>
                  <span>{{ course.instructor_name }}</span>
                </div>
                
                <div class="meta-item" v-if="course.enrolled_count">
                  <ElIcon><Trophy /></ElIcon>
                  <span>{{ course.enrolled_count }}人已学习</span>
                </div>
              </div>
              
              <div class="course-rating" v-if="course.rating">
                <ElRate v-model="course.rating" disabled show-score />
              </div>
              
              <p class="course-description">{{ course.description }}</p>
              
              <div class="course-actions">
                <ElButton 
                  v-if="!isEnrolled"
                  type="primary" 
                  size="large"
                  :loading="enrollLoading"
                  @click="handleEnroll"
                >
                  立即报名
                </ElButton>
                <ElButton 
                  v-else
                  type="success" 
                  size="large"
                  @click="$router.push(`/course/${course.id}/learn`)"
                >
                  开始学习
                </ElButton>
                
                <ElButton 
                  :type="isFavorited ? 'warning' : 'default'"
                  size="large"
                  :loading="favoriteLoading"
                  @click="handleFavorite"
                >
                  <ElIcon>
                    <StarFilled v-if="isFavorited" />
                    <Star v-else />
                  </ElIcon>
                  {{ isFavorited ? '已收藏' : '收藏' }}
                </ElButton>
              </div>
            </div>
          </ElCol>
        </ElRow>
      </ElCard>
      
      <!-- 课程详细内容 -->
      <ElCard class="course-details" header="课程详情">
        <div class="course-content-section">
          <h3>课程介绍</h3>
          <p>{{ course.description }}</p>
          
          <!-- 这里可以添加更多课程内容，如课程大纲、学习目标等 -->
        </div>
      </ElCard>
      
      <!-- 相关课程推荐 -->
      <ElCard class="related-courses" header="相关推荐">
        <div class="coming-soon">
          <p>更多精彩课程敬请期待...</p>
        </div>
      </ElCard>
    </div>
  </div>
</template>

<style scoped>
.course-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.course-header {
  margin-bottom: 20px;
}

.course-cover {
  position: relative;
  width: 100%;
  height: 300px;
  border-radius: 8px;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s;
}

.play-overlay:hover {
  background: rgba(0, 0, 0, 0.5);
}

.course-info {
  padding: 20px 0;
}

.course-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #303133;
}

.course-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
  font-size: 14px;
}

.course-rating {
  margin-bottom: 16px;
}

.course-description {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 24px;
}

.course-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.course-details {
  margin-bottom: 20px;
}

.course-content-section h3 {
  color: #303133;
  margin-bottom: 12px;
}

.related-courses .coming-soon {
  text-align: center;
  padding: 40px;
  color: #909399;
}

@media (max-width: 768px) {
  .course-detail {
    padding: 10px;
  }
  
  .course-title {
    font-size: 24px;
  }
  
  .course-actions {
    flex-direction: column;
  }
  
  .course-actions .el-button {
    width: 100%;
  }
}
</style> 
 