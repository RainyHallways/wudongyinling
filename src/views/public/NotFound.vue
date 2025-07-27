<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <el-result
        icon="error"
        title="404"
        sub-title="很抱歉，您访问的页面不存在"
      >
        <template #extra>
          <el-button type="primary" @click="router.push('/')">返回首页</el-button>
        </template>
      </el-result>
      
      <div class="not-found-suggestions">
        <h3>您可能想要访问：</h3>
        <el-space direction="vertical" size="large" alignment="flex-start">
          <el-link type="primary" @click="router.push('/dance-courses')">
            <el-icon><VideoCameraFilled /></el-icon> 舞蹈课程
          </el-link>
          
          <el-link type="primary" @click="router.push('/ai-coach')">
            <el-icon><Cpu /></el-icon> AI教练
          </el-link>
          
          <el-link type="primary" @click="router.push('/about')">
            <el-icon><InfoFilled /></el-icon> 关于我们
          </el-link>
          
          <el-link type="primary" @click="router.push('/contact')">
            <el-icon><Phone /></el-icon> 联系我们
          </el-link>
        </el-space>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { VideoCameraFilled, Cpu, InfoFilled, Phone } from '@element-plus/icons-vue';

const router = useRouter();
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.not-found-content {
  max-width: 600px;
  width: 100%;
  text-align: center;
}

.not-found-suggestions {
  margin-top: 30px;
  padding: 20px;
  border-top: 1px solid #ebeef5;
  text-align: left;
}

.not-found-suggestions h3 {
  margin-bottom: 15px;
  color: #606266;
}
</style> 