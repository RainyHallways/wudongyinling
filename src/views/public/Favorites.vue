<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElCard, ElEmpty, ElButton, ElImage, ElTag, ElIcon, ElRow, ElCol, ElMessage, ElMessageBox } from 'element-plus'
import { Star, StarFilled, Clock, Delete } from '@element-plus/icons-vue'
import { courseApi } from '@/api/course'
import type { Course } from '@/api/course'

const router = useRouter()

const favoritesCourses = ref<Course[]>([])
const loading = ref(false)

// 模拟收藏的课程数据
const mockFavorites: Course[] = [
  {
    id: 1,
    title: '古典舞基础入门',
    description: '学习古典舞的基本功和经典动作',
    cover_url: '/images/古典舞.jpg',
    difficulty: 'beginner',
    duration: 45,
    instructor_id: 1,
    instructor_name: '李老师',
    enrolled_count: 1200,
    rating: 4.8
  },
  {
    id: 2,
    title: '现代舞表演技巧',
    description: '提升现代舞的表现力和舞台感',
    cover_url: '/images/现代舞.jpg',
    difficulty: 'intermediate',
    duration: 60,
    instructor_id: 2,
    instructor_name: '王老师',
    enrolled_count: 800,
    rating: 4.6
  }
]

// 获取收藏的课程
const fetchFavorites = async () => {
  loading.value = true
  try {
    // 这里应该调用真实的收藏API
    // favoritesCourses.value = await courseApi.getFavoriteCourses()
    
    // 暂时使用模拟数据
    setTimeout(() => {
      favoritesCourses.value = mockFavorites
      loading.value = false
    }, 1000)
  } catch (error) {
    console.error('获取收藏课程失败:', error)
    loading.value = false
  }
}

// 取消收藏
const removeFavorite = async (course: Course) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消收藏《${course.title}》吗？`,
      '确认取消收藏',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 这里应该调用真实的取消收藏API
    // await courseApi.removeFavorite(course.id)
    
    // 从列表中移除
    favoritesCourses.value = favoritesCourses.value.filter(c => c.id !== course.id)
    ElMessage.success('取消收藏成功')
  } catch (error) {
    // 用户取消操作
  }
}

// 查看课程详情
const viewDetail = (course: Course) => {
  router.push(`/course/${course.id}`)
}

// 报名课程
const enrollCourse = (course: Course) => {
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
  fetchFavorites()
})
</script>

<template>
  <div class="favorites page-with-nav">
    <div class="page-header">
      <h1>我的收藏</h1>
      <p>您收藏的精彩课程</p>
    </div>

    <div v-loading="loading" class="favorites-container">
      <ElEmpty v-if="!loading && favoritesCourses.length === 0" description="您还没有收藏任何课程">
        <ElButton type="primary" @click="$router.push('/dance-courses')">
          去发现课程
        </ElButton>
      </ElEmpty>

      <ElRow v-else :gutter="20">
        <ElCol v-for="course in favoritesCourses" :key="course.id" :xs="24" :sm="12" :md="8" :lg="6">
          <ElCard class="course-card" shadow="hover">
            <div class="course-cover">
              <ElImage 
                :src="course.cover_url || '/images/default-course.png'"
                fit="cover"
                class="cover-image"
                @click="viewDetail(course)"
              />
              <div class="favorite-badge">
                <ElIcon color="#f56c6c" size="20">
                  <StarFilled />
                </ElIcon>
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
              
              <p class="course-description">{{ course.description }}</p>
              
              <div class="course-stats" v-if="course.enrolled_count || course.rating">
                <div v-if="course.enrolled_count" class="stat-item">
                  <span class="stat-value">{{ course.enrolled_count }}</span>
                  <span class="stat-label">人学习</span>
                </div>
                <div v-if="course.rating" class="stat-item">
                  <span class="stat-value">{{ course.rating }}</span>
                  <span class="stat-label">评分</span>
                </div>
              </div>
              
              <div class="course-actions">
                <ElButton 
                  type="primary" 
                  size="small"
                  @click="enrollCourse(course)"
                >
                  立即报名
                </ElButton>
                <ElButton 
                  type="danger" 
                  size="small"
                  :icon="Delete"
                  @click="removeFavorite(course)"
                >
                  取消收藏
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
.favorites {
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

.favorites-container {
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
  cursor: pointer;
}

.cover-image {
  width: 100%;
  height: 100%;
  transition: transform 0.3s;
}

.course-cover:hover .cover-image {
  transform: scale(1.05);
}

.favorite-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
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
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
  font-size: 12px;
}

.course-description {
  color: #606266;
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 12px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.course-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.course-actions {
  display: flex;
  gap: 8px;
}

.course-actions .el-button {
  flex: 1;
}

@media (max-width: 768px) {
  .favorites {
    padding: 10px;
    padding-bottom: 80px; /* 为底部导航添加安全区域 */
  }
  
  .page-header {
    margin-bottom: 30px;
  }
  
  .page-header h1 {
    font-size: 24px;
    margin-bottom: 5px;
  }
  
  .page-header p {
    font-size: 14px;
  }
  
  .course-card {
    margin-bottom: 15px;
  }

  .course-cover {
    height: 160px;
  }
  
  .course-info {
    padding: 0 0;
  }
  
  .course-title {
    font-size: 15px;
    margin-bottom: 8px;
    line-height: 1.3;
  }
  
  .course-meta {
    gap: 10px;
    margin-bottom: 12px;
  }
  
  .meta-item {
    font-size: 11px;
  }
  
  .course-description {
    font-size: 13px;
    line-height: 1.4;
    margin-bottom: 12px;
    -webkit-line-clamp: 3;
  }
  
  .course-stats {
    gap: 12px;
    margin-bottom: 12px;
  }
  
  .stat-value {
    font-size: 14px;
  }
  
  .stat-label {
    font-size: 10px;
  }
  
  .course-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .course-actions .el-button {
    font-size: 14px;
    height: 40px;
    min-height: 40px;
  }

  .favorite-badge {
    width: 28px;
    height: 28px;
  }
}

@media (max-width: 576px) {
  .favorites {
    padding: 8px 5px;
    padding-bottom: 80px;
  }
  
  .page-header h1 {
    font-size: 20px;
  }
  
  .page-header p {
    font-size: 13px;
  }
  
  .course-cover {
    height: 140px;
  }
  
  .course-title {
    font-size: 14px;
  }
  
  .course-meta {
    gap: 8px;
  }
  
  .meta-item {
    font-size: 10px;
  }
  
  .course-description {
    font-size: 12px;
    -webkit-line-clamp: 2;
  }
  
  .stat-value {
    font-size: 13px;
  }
  
  .stat-label {
    font-size: 9px;
  }
  
  .course-actions .el-button {
    font-size: 13px;
    height: 36px;
    min-height: 36px;
  }

  .favorite-badge {
    width: 24px;
    height: 24px;
  }

  .favorites-container {
    min-height: 300px;
  }
}
</style> 
 