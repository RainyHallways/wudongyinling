<template>
  <div class="home">
    <!-- 头部横幅 -->
    <div class="banner">
      <div class="banner-content">
        <h1>欢迎来到舞蹈平台</h1>
        <p>探索舞蹈的魅力，享受运动的快乐</p>
        <el-button type="primary" size="large" @click="startLearning">
          开始学习
        </el-button>
      </div>
    </div>

    <!-- 功能特点展示 -->
    <div class="features section">
      <div class="container">
        <h2 class="section-title">平台特色</h2>
        <el-row :gutter="30">
          <el-col :span="8" v-for="feature in features" :key="feature.title">
            <el-card class="feature-card">
              <el-icon :size="40" class="feature-icon">
                <component :is="feature.icon" />
              </el-icon>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 热门课程 -->
    <div class="popular-courses container">
      <h2 class="section-title">热门课程</h2>
      <el-row :gutter="20">
        <el-col :span="6" v-for="course in popularCourses" :key="course.id">
          <el-card class="course-card" :body-style="{ padding: '0px' }">
            <img :src="course.image" class="course-image">
            <div class="course-info">
              <h3>{{ course.title }}</h3>
              <p>{{ course.description }}</p>
              <div class="course-footer">
                <span>{{ course.duration }}</span>
                <el-button type="primary" link>
                  立即学习
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 学习统计 -->
    <div class="statistics">
      <div class="container">
        <el-row :gutter="30">
          <el-col :span="6" v-for="stat in statistics" :key="stat.label">
            <div class="stat-item">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const features = ref([
  {
    icon: 'VideoCameraFilled',
    title: 'AI 智能教练',
    description: '实时动作识别和纠正，为您提供专业指导'
  },
  {
    icon: 'UserFilled',
    title: '社交平台',
    description: '结识志同道合的舞伴，分享舞蹈心得'
  },
  {
    icon: 'DataLine',
    title: '健康管理',
    description: '科学的运动数据追踪，合理规划训练'
  }
])

const popularCourses = ref([
  {
    id: 1,
    title: '街舞入门课程',
    description: '零基础学习街舞的最佳选择',
    image: '/images/courses/street-dance.jpg',
    duration: '12课时'
  },
  {
    id: 2,
    title: '现代舞基础',
    description: '体验现代舞的艺术魅力',
    image: '/images/courses/modern-dance.jpg',
    duration: '10课时'
  },
  {
    id: 3,
    title: '拉丁舞初级',
    description: '热情奔放的拉丁舞蹈',
    image: '/images/courses/latin-dance.jpg',
    duration: '15课时'
  },
  {
    id: 4,
    title: '中国古典舞',
    description: '传统文化的优美展现',
    image: '/images/courses/classical-dance.jpg',
    duration: '8课时'
  }
])

const statistics = ref([
  { value: '100,000+', label: '注册用户' },
  { value: '500+', label: '精品课程' },
  { value: '50+', label: '专业导师' },
  { value: '98%', label: '学员好评' }
])

const startLearning = () => {
  router.push('/coach')
}
</script>

<style scoped>
.banner {
  height: 500px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.banner-content h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.banner-content p {
  font-size: 20px;
  margin-bottom: 30px;
}

.feature-card {
  text-align: center;
  padding: 30px;
  height: 100%;
}

.feature-icon {
  color: var(--primary-color);
  margin-bottom: 20px;
}

.feature-card h3 {
  margin: 15px 0;
  font-size: 20px;
}

.popular-courses {
  margin-bottom: 60px;
}

.course-card {
  height: 100%;
}

.course-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.course-info {
  padding: 15px;
}

.course-info h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.course-info p {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.statistics {
  background-color: #f8f9fa;
  padding: 60px 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 10px;
}

.stat-label {
  color: #666;
  font-size: 16px;
}

@media (max-width: 768px) {
  .banner {
    height: 400px;
  }

  .banner-content h1 {
    font-size: 36px;
  }

  .banner-content p {
    font-size: 18px;
  }
}
</style> 