<template>
  <div class="dashboard-container admin-responsive">
    <!-- 统计卡片 -->
    <div class="dashboard-stats">
      <div class="stat-card-responsive">
        <div class="stat-card-header">
          <span class="stat-card-title">总课程数</span>
          <el-icon class="stat-card-icon"><VideoCamera /></el-icon>
        </div>
        <div class="stat-card-value">{{ stats.totalCourses || 0 }}</div>
      </div>
      
      <div class="stat-card-responsive">
        <div class="stat-card-header">
          <span class="stat-card-title">总用户数</span>
          <el-icon class="stat-card-icon"><User /></el-icon>
        </div>
        <div class="stat-card-value">{{ stats.totalUsers || 0 }}</div>
      </div>
      
      <div class="stat-card-responsive">
        <div class="stat-card-header">
          <span class="stat-card-title">活跃用户</span>
          <el-icon class="stat-card-icon"><UserFilled /></el-icon>
        </div>
        <div class="stat-card-value">{{ stats.activeUsers || 0 }}</div>
      </div>
      
      <div class="stat-card-responsive">
        <div class="stat-card-header">
          <span class="stat-card-title">总挑战数</span>
          <el-icon class="stat-card-icon"><Trophy /></el-icon>
        </div>
        <div class="stat-card-value">{{ stats.totalChallenges || 0 }}</div>
      </div>
    </div>
    
    <!-- 页面标题和刷新按钮 -->
    <div class="page-header">
      <h1 class="page-title">仪表盘</h1>
      <el-button type="primary" @click="refreshStats" class="touch-friendly">
        <el-icon><Refresh /></el-icon>
        <span class="mobile-hide">刷新数据</span>
      </el-button>
    </div>
    
    <!-- 系统状态卡片 -->
    <el-card shadow="hover" class="system-card">
      <template #header>
        <div class="card-header">
          <h3>系统状态</h3>
        </div>
      </template>
      
      <el-descriptions :column="desktopColumns" border>
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
        <el-button type="primary" @click="$router.push('/admin/users')" class="quick-action-btn">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-button>
        
        <el-button type="success" @click="$router.push('/admin/courses')" class="quick-action-btn">
          <el-icon><VideoCamera /></el-icon>
          <span>课程管理</span>
        </el-button>
        
        <el-button type="warning" @click="$router.push('/admin/challenges')" class="quick-action-btn">
          <el-icon><Trophy /></el-icon>
          <span>挑战活动</span>
        </el-button>
        
        <el-button type="info" @click="$router.push('/admin/health-records')" class="quick-action-btn">
          <el-icon><Suitcase /></el-icon>
          <span>健康记录</span>
        </el-button>
        
        <el-button type="primary" plain @click="$router.push('/admin/prescriptions')" class="quick-action-btn">
          <el-icon><Document /></el-icon>
          <span>处方管理</span>
        </el-button>
        
        <el-button type="success" plain @click="$router.push('/admin/posts')" class="quick-action-btn">
          <el-icon><ChatDotRound /></el-icon>
          <span>动态广场</span>
        </el-button>
        
        <el-button type="warning" plain @click="$router.push('/admin/heritage')" class="quick-action-btn">
          <el-icon><Compass /></el-icon>
          <span>非遗传承</span>
        </el-button>
        
        <el-button type="info" plain @click="$router.push('/admin/statistics')" class="quick-action-btn">
          <el-icon><DataLine /></el-icon>
          <span>数据统计</span>
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { statsApi, type DashboardStats } from '@/api/stats'
import { 
  User, 
  UserFilled, 
  VideoCamera, 
  Trophy, 
  Suitcase,
  Document,
  ChatDotRound,
  Compass,
  DataLine,
  Refresh
} from '@element-plus/icons-vue'

// 统计数据
const stats = ref<DashboardStats>({
  totalCourses: 0,
  totalUsers: 0,
  totalChallenges: 0,
  totalHealthRecords: 0,
  activeUsers: 0,
  coursesByDifficulty: {}
})

const loading = ref(false)

// 响应式相关
const isMobile = ref(false)

// 计算桌面端列数
const desktopColumns = computed(() => {
  return isMobile.value ? 1 : 2
})

// 检测移动端
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

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
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.dashboard-container {
  padding: 16px;
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
}

/* 系统状态卡片 */
.system-card {
  margin-bottom: 24px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-weight: 500;
  color: var(--text-primary);
}

/* 快捷操作区域 */
.quick-actions-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.quick-action-btn {
  display: flex !important;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100px;
  padding: 16px;
  border-radius: 12px;
  box-shadow: var(--shadow-light);
  transition: all 0.3s ease;
  gap: 8px;
  font-weight: 500;
}

.quick-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.quick-action-btn .el-icon {
  font-size: 28px;
  margin: 0;
}

.quick-action-btn span {
  font-size: 14px;
  text-align: center;
  line-height: 1.2;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .quick-actions-content {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 12px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
    text-align: center;
  }
  
  .page-title {
    font-size: 20px;
  }
  
  .quick-actions-content {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .quick-action-btn {
    height: 90px;
    padding: 12px;
  }
  
  .quick-action-btn .el-icon {
    font-size: 24px;
  }
  
  .quick-action-btn span {
    font-size: 13px;
  }
  
  .mobile-hide {
    display: none;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 8px;
  }
  
  .page-header {
    padding: 12px 16px;
  }
  
  .quick-actions-content {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .quick-action-btn {
    height: 70px;
    flex-direction: row;
    justify-content: flex-start;
    padding: 12px 16px;
  }
  
  .quick-action-btn .el-icon {
    font-size: 20px;
    margin-right: 12px;
    margin-bottom: 0;
  }
  
  .quick-action-btn span {
    font-size: 14px;
    text-align: left;
  }
}

/* 加载状态 */
.dashboard-container.v-loading {
  position: relative;
}

/* 描述列表优化 */
.system-card .el-descriptions {
  margin: 0;
}

.system-card .el-descriptions-item__label {
  font-weight: 500;
  color: var(--text-secondary);
}

.system-card .el-descriptions-item__content {
  color: var(--text-primary);
}

/* 标签优化 */
.system-card .el-tag {
  border-radius: 16px;
  font-weight: 500;
}

/* 按钮响应式 */
.touch-friendly {
  min-height: var(--mobile-button-height);
  padding: 12px 20px;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.touch-friendly .el-icon {
  font-size: 18px;
}
</style> 