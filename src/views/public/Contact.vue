<script setup lang="ts">
import { ref } from 'vue'
import { Message, Phone, Location, ElementPlus, Share, ChatDotRound } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PageHeader from '@/components/common/PageHeader.vue'

interface ContactForm {
  name: string
  email: string
  phone: string
  subject: string
  message: string
}

const form = ref<ContactForm>({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const submitForm = (): void => {
  // 这里可以添加表单验证逻辑
  // 模拟提交成功
  ElMessage({
    message: '您的留言已提交，我们会尽快与您联系！',
    type: 'success'
  })
  
  // 清空表单
  form.value = {
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  }
}
</script>

<template>
  <div class="contact-page page-with-nav">
    <PageHeader title="联系我们" subtitle="感谢您对舞动银龄平台的关注和支持" />
    
    <ElCard class="contact-content">
      <p class="intro">如果您有任何问题、建议或合作意向，欢迎通过以下方式与我们联系。我们将尽快回复您的咨询。</p>
      
      <div class="contact-grid">
        <div class="contact-item">
          <div class="contact-icon">
            <el-icon><Message /></el-icon>
          </div>
          <h3>电子邮件</h3>
          <p>contact@wdyl.cnies.org</p>
          <p>工作日回复时间：24小时内</p>
        </div>
        
        <div class="contact-item">
          <div class="contact-icon">
            <el-icon><Phone /></el-icon>
          </div>
          <h3>客服热线</h3>
          <p>400-888-XXXX</p>
          <p>服务时间：周一至周五 9:00-18:00</p>
        </div>
        
        <div class="contact-item">
          <div class="contact-icon">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <h3>在线客服</h3>
          <p>点击网站右下角的客服图标</p>
          <p>服务时间：每日 9:00-22:00</p>
        </div>
        
        <div class="contact-item">
          <div class="contact-icon">
            <el-icon><Location /></el-icon>
          </div>
          <h3>办公地址</h3>
          <p>山东省济南市</p>
          <p>（仅接待预约访客）</p>
        </div>
      </div>
      
      <div class="section">
        <h2>留言咨询</h2>
        <p>您也可以通过以下表单向我们发送消息，我们会尽快与您联系。</p>
        
        <ElForm :model="form" label-width="80px" class="contact-form">
          <ElFormItem label="姓名">
            <ElInput v-model="form.name" placeholder="请输入您的姓名"></ElInput>
          </ElFormItem>
          
          <ElFormItem label="邮箱">
            <ElInput v-model="form.email" placeholder="请输入您的邮箱地址"></ElInput>
          </ElFormItem>
          
          <ElFormItem label="电话">
            <ElInput v-model="form.phone" placeholder="请输入您的联系电话"></ElInput>
          </ElFormItem>
          
          <ElFormItem label="主题">
            <ElSelect v-model="form.subject" placeholder="请选择咨询主题" style="width: 100%">
              <ElOption label="产品咨询" value="product"></ElOption>
              <ElOption label="技术支持" value="support"></ElOption>
              <ElOption label="合作洽谈" value="cooperation"></ElOption>
              <ElOption label="投诉建议" value="complaint"></ElOption>
              <ElOption label="其他" value="other"></ElOption>
            </ElSelect>
          </ElFormItem>
          
          <ElFormItem label="留言内容">
            <ElInput v-model="form.message" type="textarea" :rows="6" placeholder="请详细描述您的问题或建议"></ElInput>
          </ElFormItem>
          
          <ElFormItem>
            <ElButton type="primary" @click="submitForm">提交留言</ElButton>
          </ElFormItem>
        </ElForm>
      </div>
      
      <div class="section">
        <h2>关注我们</h2>
        <p>关注我们的社交媒体账号，获取最新动态和活动信息。</p>
        
        <div class="social-links">
          <a href="#" class="social-link">
            <el-icon><ElementPlus /></el-icon>
            <span>微信公众号</span>
          </a>
          
          <a href="#" class="social-link">
            <el-icon><Share /></el-icon>
            <span>微博</span>
          </a>
          
          <a href="#" class="social-link">
            <el-icon><ChatDotRound /></el-icon>
            <span>抖音</span>
          </a>
        </div>
      </div>
    </ElCard>
  </div>
</template>

<style scoped>
.contact-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 60px;
}

.contact-content {
  margin-bottom: 40px;
}

.intro {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 30px;
  color: #666;
  text-align: center;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.contact-item {
  text-align: center;
  padding: 30px 20px;
  border-radius: 8px;
  background-color: var(--el-fill-color-light);
  transition: transform 0.3s, box-shadow 0.3s;
}

.contact-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.contact-icon {
  margin-bottom: 15px;
}

.contact-icon .el-icon {
  font-size: 40px;
  color: var(--el-color-primary);
}

.contact-item h3 {
  font-size: 20px;
  margin-bottom: 10px;
  color: var(--el-text-color-primary);
}

.contact-item p {
  color: var(--el-text-color-regular);
  margin-bottom: 5px;
}

.section {
  margin-bottom: 30px;
}

.section h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: var(--el-text-color-primary);
  position: relative;
  padding-bottom: 10px;
}

.section h2:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background-color: var(--el-color-primary);
}

.section p {
  font-size: 16px;
  line-height: 1.6;
  color: var(--el-text-color-regular);
  margin-bottom: 20px;
}

.contact-form {
  max-width: 600px;
  margin: 0 auto;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 20px;
}

.social-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--el-text-color-regular);
  text-decoration: none;
  transition: color 0.3s;
}

.social-link:hover {
  color: var(--el-color-primary);
}

.social-link .el-icon {
  font-size: 36px;
  margin-bottom: 10px;
}

.social-link span {
  font-size: 16px;
}

@media (max-width: 992px) {
  .contact-page {
    padding: 20px 15px;
    padding-bottom: 80px; /* 为底部导航添加安全区域 */
  }

  .contact-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .contact-item {
    padding: 25px 15px;
  }

  .contact-icon .el-icon {
    font-size: 36px;
  }

  .contact-item h3 {
    font-size: 18px;
  }

  .contact-item p {
    font-size: 14px;
  }

  .section h2 {
    font-size: 20px;
  }

  .section p {
    font-size: 15px;
  }

  .contact-form {
    max-width: 100%;
  }

  .contact-form :deep(.el-form-item__label) {
    font-size: 14px;
  }

  .contact-form :deep(.el-input__inner) {
    font-size: 16px; /* 防止iOS缩放 */
    height: 44px;
  }

  .contact-form :deep(.el-textarea__inner) {
    font-size: 16px;
    padding: 8px 12px;
  }

  .contact-form :deep(.el-button) {
    height: 44px;
    font-size: 16px;
  }
}

@media (max-width: 768px) {
  .contact-page {
    padding: 15px 10px;
    padding-bottom: 80px;
  }

  .intro {
    font-size: 16px;
    padding: 0 10px;
    margin-bottom: 25px;
  }

  .contact-grid {
    gap: 12px;
  }

  .contact-item {
    padding: 20px 12px;
  }

  .contact-icon .el-icon {
    font-size: 32px;
  }

  .contact-item h3 {
    font-size: 16px;
  }

  .contact-item p {
    font-size: 13px;
  }

  .section h2 {
    font-size: 18px;
    margin-bottom: 15px;
  }

  .section p {
    font-size: 14px;
  }

  .contact-form :deep(.el-form-item__label) {
    font-size: 13px;
  }

  .contact-form :deep(.el-input__inner) {
    height: 40px;
  }

  .contact-form :deep(.el-button) {
    height: 40px;
    font-size: 15px;
  }
}

@media (max-width: 576px) {
  .contact-page {
    padding: 10px 8px;
    padding-bottom: 80px;
  }

  .intro {
    font-size: 15px;
    padding: 0 5px;
    margin-bottom: 20px;
  }

  .contact-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .contact-item {
    padding: 20px 10px;
  }

  .contact-icon .el-icon {
    font-size: 28px;
  }

  .contact-item h3 {
    font-size: 15px;
    margin-bottom: 8px;
  }

  .contact-item p {
    font-size: 12px;
    margin-bottom: 3px;
  }

  .section {
    margin-bottom: 25px;
  }

  .section h2 {
    font-size: 17px;
    margin-bottom: 12px;
  }

  .section h2:after {
    width: 40px;
    height: 2px;
  }

  .section p {
    font-size: 13px;
    margin-bottom: 15px;
  }

  .contact-form :deep(.el-form-item) {
    margin-bottom: 18px;
  }

  .contact-form :deep(.el-form-item__label) {
    font-size: 12px;
    margin-bottom: 8px;
  }

  .contact-form :deep(.el-input__inner),
  .contact-form :deep(.el-select__wrapper) {
    height: 40px;
    font-size: 16px; /* 防止iOS缩放 */
  }

  .contact-form :deep(.el-textarea__inner) {
    font-size: 16px;
    padding: 6px 10px;
    min-height: 80px;
  }

  .contact-form :deep(.el-button) {
    height: 44px;
    font-size: 15px;
  }

  .social-links {
    flex-direction: column;
    align-items: center;
    gap: 15px;
    margin-top: 15px;
  }

  .social-link {
    padding: 15px;
    border-radius: 12px;
    min-width: 200px;
    background-color: var(--el-fill-color-light);
    transition: transform 0.3s ease;
  }

  .social-link:hover {
    transform: translateY(-2px);
  }

  .social-link .el-icon {
    font-size: 32px;
    margin-bottom: 8px;
  }

  .social-link span {
    font-size: 14px;
  }
}
</style> 