<template>
  <div class="policy-page page-with-nav">
    <page-header title="原创作品授权协议" subtitle="了解作品授权的详细条款与条件"></page-header>
    
    <el-card class="policy-content">
      <div class="policy-document space-y-4 leading-7">
          <p>甲方（网站提供者）：舞动银龄</p>
          <p>乙方（原创作品作者）：__________________</p>
          <h2 class="text-xl font-semibold">一、协议目的</h2>
          <p>1. 本协议旨在明确甲乙双方在原创作品展播、分享、下载等环节的权利义务关系。</p>
          <p>2. 乙方授权甲方在其平台上展播乙方原创作品，甲方为乙方提供作品展示和推广服务。</p>
          <h2 class="text-xl font-semibold">二、授权内容</h2>
          <p>1. 乙方同意将其原创作品（以下简称"作品"）授权给甲方，甲方有权在以下范围内使用乙方的作品：</p>
          <p>（1）在甲方平台上展示乙方的作品；</p>
          <p>（2）对乙方的作品进行推广、宣传；</p>
          <p>（3）允许用户浏览、下载乙方的作品；</p>
          <p>（4）其他经乙方同意的使用方式。</p>
          <p>2. 乙方授权甲方使用作品的期限为：自本协议签订之日起至乙方书面通知甲方解除授权之日止。</p>
          <h2 class="text-xl font-semibold">三、乙方权利与义务</h2>
          <p>1. 乙方保证其作品为原创作品，拥有完整的知识产权，且未侵犯任何第三方的合法权益。</p>
          <p>2. 乙方同意甲方在协议约定的范围内使用其作品，并保证不将作品授权给其他第三方使用。</p>
          <p>3. 乙方有权要求甲方支付作品使用费，具体费用及支付方式由双方另行约定。</p>
          <p>4. 乙方应确保作品内容符合法律法规，不含有违法、违规信息。</p>
          <h2 class="text-xl font-semibold">四、甲方权利与义务</h2>
          <p>1. 甲方应确保乙方作品在平台上的安全，采取措施防止作品被未经授权的第三方下载、传播。</p>
          <p>2. 甲方有权对乙方作品进行审核，如发现作品不符合本协议规定，甲方有权拒绝展播或删除作品。</p>
          <p>3. 甲方应尊重乙方的知识产权，不得擅自修改、歪曲乙方作品。</p>
          <h2 class="text-xl font-semibold">五、协议的变更与终止</h2>
          <p>1. 双方同意，本协议的变更、解除、终止等事宜，应以书面形式确认。</p>
          <p>2. 乙方有权在提前通知甲方的情况下，解除本协议。协议解除后，甲方应停止使用乙方的作品。</p>
          <h2 class="text-xl font-semibold">六、争议解决</h2>
          <p>1. 本协议的签订、履行、解释及争议解决均适用中华人民共和国法律法规。</p>
          <p>2. 如双方在协议履行过程中发生争议，应首先通过友好协商解决；协商不成的，任何一方均有权向甲方所在地人民法院提起诉讼。</p>
          <p class="mt-4">乙方签字（或盖章）：____________________</p>
          <p>签订日期：______________________________</p>
          <p class="mt-4">请乙方下载本协议文件，签字或盖章后上传至甲方平台。甲方审核通过后，乙方即可上传作品。感谢您的支持与合作！</p>
          <p class="mt-4">甲方（网站提供者）：舞动银龄</p>
          <p>地址：______________________________</p>
          <p>联系人：______________________________</p>
          <p>联系电话：______________________________</p>
          <p>电子邮箱：______________________________</p>
      </div>
      
      <!-- 操作按钮 -->
      <div class="policy-actions">
        <el-button type="primary" @click="printPolicy">
          <el-icon><Printer /></el-icon> 打印协议
        </el-button>
        <el-button @click="downloadPolicy">
          <el-icon><Download /></el-icon> 下载协议
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { Printer, Download } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import { ElMessage } from 'element-plus'

const printPolicy = () => {
  window.print()
  ElMessage.success('正在准备打印...')
}

const downloadPolicy = () => {
  // 模拟下载功能
  ElMessage.success('正在准备下载...')
}
</script>

<style scoped>
.policy-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.policy-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
}

.policy-content:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.policy-document {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.space-y-4 > * + * {
  margin-top: 1.5rem;
}

.leading-7 {
  line-height: 1.8;
  font-size: 16px;
  color: var(--el-text-color-regular);
}

.text-xl {
  font-size: 1.3rem;
  color: var(--el-text-color-primary);
  margin: 2rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--el-color-primary-light-7);
  position: relative;
}

.text-xl::before {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 60px;
  height: 2px;
  background: var(--el-color-primary);
}

.font-semibold {
  font-weight: 600;
}

.font-bold {
  font-weight: 700;
}

.text-center {
  text-align: center;
}

.mb-6 {
  margin-bottom: 2rem;
}

.mt-4 {
  margin-top: 1.5rem;
}

.policy-actions {
  padding: 20px 40px;
  background: var(--el-fill-color-lighter);
  border-top: 1px solid var(--el-border-color-light);
  display: flex;
  justify-content: center;
  gap: 15px;
}

.policy-actions .el-button {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.policy-actions .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .policy-page {
    padding: 15px;
  }
  
  .policy-document {
    padding: 25px 20px;
  }
  
  .leading-7 {
    font-size: 15px;
  }
  
  .text-xl {
    font-size: 1.2rem;
    margin: 1.5rem 0 0.8rem 0;
  }
  
  .policy-actions {
    padding: 15px 20px;
    flex-direction: column;
    gap: 10px;
  }
  
  .policy-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .policy-page {
    padding: 10px;
  }
  
  .policy-document {
    padding: 20px 15px;
  }
  
  .leading-7 {
    font-size: 14px;
    line-height: 1.7;
  }
  
  .text-xl {
    font-size: 1.1rem;
  }
}

/* 打印样式 */
@media print {
  .policy-page {
    padding: 0;
  }
  
  .policy-content {
    box-shadow: none;
    border: 1px solid #ddd;
  }
  
  .policy-document {
    padding: 20px;
    max-width: none;
  }
  
  .policy-actions {
    display: none;
  }
  
  .text-xl {
    color: #000 !important;
    border-bottom-color: #000 !important;
  }
  
  .text-xl::before {
    background: #000 !important;
  }
}
</style> 