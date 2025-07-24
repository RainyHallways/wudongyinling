<template>
  <div class="dashboard-container">
    <el-card shadow="hover" class="header-card">
      <template #header>
        <div class="card-header">
          <h2>仪表盘</h2>
          <el-button type="primary" @click="refreshStats">刷新数据</el-button>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <span>总课程数</span>
                <el-icon><VideoCamera /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h3>{{ stats.totalCourses || 0 }}</h3>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <span>总用户数</span>
                <el-icon><User /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h3>{{ stats.totalUsers || 0 }}</h3>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <span>活跃用户</span>
                <el-icon><UserFilled /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h3>{{ stats.activeUsers || 0 }}</h3>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <span>总挑战数</span>
                <el-icon><Trophy /></el-icon>
              </div>
            </template>
            <div class="card-content">
              <h3>{{ stats.totalChallenges || 0 }}</h3>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 系统状态卡片 -->
    <el-card shadow="hover" class="system-card mt-20">
      <template #header>
        <div class="card-header">
          <h3>系统状态</h3>
        </div>
      </template>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="系统版本">1.0.0</el-descriptions-item>
        <el-descriptions-item label="Node版本">16.x</el-descriptions-item>
        <el-descriptions-item label="服务器状态">
          <el-tag type="success">运行中</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="数据库状态">
          <el-tag type="success">连接正常</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <!-- 快捷操作区 -->
    <el-card shadow="hover" class="quick-actions mt-20">
      <template #header>
        <div class="card-header">
          <h3>快捷操作</h3>
        </div>
      </template>
      
      <div class="quick-actions-content">
        <el-button type="primary" @click="$router.push('/admin/users')">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-button>
        
        <el-button type="success" @click="$router.push('/admin/courses')">
          <el-icon><VideoCamera /></el-icon>
          <span>课程管理</span>
        </el-button>
        
        <el-button type="warning" @click="$router.push('/admin/challenges')">
          <el-icon><Trophy /></el-icon>
          <span>挑战活动</span>
        </el-button>
        
        <el-button type="info" @click="$router.push('/admin/health-records')">
          <el-icon><Suitcase /></el-icon>
          <span>健康记录</span>
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { statsApi, type DashboardStats } from '@/api/stats'
import { 
  User, 
  UserFilled, 
  VideoCamera, 
  Trophy, 
  Suitcase 
} from '@element-plus/icons-vue'

// 统计数据
const stats = ref<DashboardStats>({
  totalCourses: 0,
  totalUsers: 0,
  totalChallenges: 0,
  activeUsers: 0,
  completedCourses: 0
})

const loading = ref(false)

// 获取统计数据
const fetchStats = async () => {
  loading.value = true
  try {
    const data = await statsApi.getDashboardStats()
    stats.value = data
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新统计数据
const refreshStats = () => {
  fetchStats()
  ElMessage.success('数据已刷新')
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2, .card-header h3 {
  margin: 0;
  font-weight: 500;
}

.stat-card {
  height: 100%;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.card-content h3 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #409EFF;
}

.quick-actions-content {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.quick-actions-content .el-button {
  display: flex;
  flex-direction: column;
  height: 90px;
  width: 110px;
  justify-content: center;
  padding: 15px;
}

.quick-actions-content .el-button .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 10px;
  }
  
  .quick-actions-content .el-button {
    height: 80px;
    width: calc(50% - 8px);
  }
}
</style> 