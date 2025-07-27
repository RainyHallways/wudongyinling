<template>
  <div class="statistics-container">
    <page-header title="数据统计" subtitle="查看平台的关键统计数据"></page-header>

    <el-card class="main-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <el-icon><User /></el-icon>
                <span>用户总数</span>
              </div>
            </template>
            <div class="stat-value">{{ totalUsers }}</div>
            <div class="stat-change">
              <el-tag type="success" size="small">
                <el-icon><ArrowUp /></el-icon> {{ userGrowth }}%
              </el-tag>
              <span class="period">本月</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <el-icon><VideoCameraFilled /></el-icon>
                <span>课程总数</span>
              </div>
            </template>
            <div class="stat-value">{{ totalCourses }}</div>
            <div class="stat-change">
              <el-tag type="success" size="small">
                <el-icon><ArrowUp /></el-icon> {{ courseGrowth }}%
              </el-tag>
              <span class="period">本月</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <el-icon><View /></el-icon>
                <span>总访问量</span>
              </div>
            </template>
            <div class="stat-value">{{ totalVisits }}</div>
            <div class="stat-change">
              <el-tag type="success" size="small">
                <el-icon><ArrowUp /></el-icon> {{ visitGrowth }}%
              </el-tag>
              <span class="period">本月</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <el-icon><ChatDotRound /></el-icon>
                <span>互动总数</span>
              </div>
            </template>
            <div class="stat-value">{{ totalInteractions }}</div>
            <div class="stat-change">
              <el-tag type="success" size="small">
                <el-icon><ArrowUp /></el-icon> {{ interactionGrowth }}%
              </el-tag>
              <span class="period">本月</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 图表区域 -->
      <el-row :gutter="20" class="chart-row">
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>用户增长趋势</span>
              </div>
            </template>
            <div class="chart-placeholder">图表区域 - 用户增长趋势</div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>课程参与度</span>
              </div>
            </template>
            <div class="chart-placeholder">图表区域 - 课程参与度</div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="chart-row">
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>用户年龄分布</span>
              </div>
            </template>
            <div class="chart-placeholder">图表区域 - 用户年龄分布</div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>热门舞蹈类型</span>
              </div>
            </template>
            <div class="chart-placeholder">图表区域 - 热门舞蹈类型</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import PageHeader from '../../components/common/PageHeader.vue';
import { User, VideoCameraFilled, View, ChatDotRound, ArrowUp } from '@element-plus/icons-vue';

// 模拟数据
const totalUsers = ref(2450);
const userGrowth = ref(12.5);
const totalCourses = ref(178);
const courseGrowth = ref(8.3);
const totalVisits = ref(38650);
const visitGrowth = ref(15.2);
const totalInteractions = ref(9824);
const interactionGrowth = ref(10.7);

onMounted(() => {
  // 这里可以添加实际的API调用来获取统计数据
  fetchStatistics();
});

const fetchStatistics = () => {
  // 模拟API调用
  console.log('获取统计数据...');
  // 实际项目中应该调用API获取真实数据
  // statsApi.getStatistics().then(response => { ... })
};
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.main-card {
  margin-top: 20px;
}

.stat-card {
  text-align: center;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin: 10px 0;
  color: #409EFF;
}

.stat-change {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.period {
  font-size: 12px;
  color: #909399;
}

.chart-row {
  margin-top: 20px;
}

.chart-card {
  height: 350px;
  margin-bottom: 20px;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 4px;
  color: #909399;
}
</style> 