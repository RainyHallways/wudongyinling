<template>
  <div class="agreement-page">
    <div class="container">
      <h1 class="page-title">联系我们</h1>
      
      <el-card class="agreement-content">
        <p class="intro">感谢您对舞动银龄平台的关注和支持。如果您有任何问题、建议或合作意向，欢迎通过以下方式与我们联系。我们将尽快回复您的咨询。</p>
        
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
          
          <el-form :model="form" label-width="80px" class="contact-form">
            <el-form-item label="姓名">
              <el-input v-model="form.name" placeholder="请输入您的姓名"></el-input>
            </el-form-item>
            
            <el-form-item label="邮箱">
              <el-input v-model="form.email" placeholder="请输入您的邮箱地址"></el-input>
            </el-form-item>
            
            <el-form-item label="电话">
              <el-input v-model="form.phone" placeholder="请输入您的联系电话"></el-input>
            </el-form-item>
            
            <el-form-item label="主题">
              <el-select v-model="form.subject" placeholder="请选择咨询主题" style="width: 100%">
                <el-option label="产品咨询" value="product"></el-option>
                <el-option label="技术支持" value="support"></el-option>
                <el-option label="合作洽谈" value="cooperation"></el-option>
                <el-option label="投诉建议" value="complaint"></el-option>
                <el-option label="其他" value="other"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="留言内容">
              <el-input v-model="form.message" type="textarea" rows="6" placeholder="请详细描述您的问题或建议"></el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="submitForm">提交留言</el-button>
            </el-form-item>
          </el-form>
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
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Message, Phone, Location, ElementPlus, Share, ChatDotRound } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const submitForm = () => {
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

<style lang="scss" scoped>
.agreement-page {
  padding: 40px 0;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .page-title {
    text-align: center;
    margin-bottom: 30px;
    color: var(--primary-color);
    font-size: 32px;
  }

  .agreement-content {
    padding: 30px;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

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

      @media (max-width: 992px) {
        grid-template-columns: repeat(2, 1fr);
      }

      @media (max-width: 576px) {
        grid-template-columns: 1fr;
      }
    }

    .contact-item {
      text-align: center;
      padding: 30px 20px;
      border-radius: 8px;
      background-color: #f9f9f9;
      transition: transform 0.3s, box-shadow 0.3s;

      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
      }

      .contact-icon {
        margin-bottom: 15px;
        
        .el-icon {
          font-size: 40px;
          color: var(--primary-color);
        }
      }

      h3 {
        font-size: 20px;
        margin-bottom: 10px;
        color: #333;
      }

      p {
        color: #666;
        margin-bottom: 5px;
      }
    }

    .section {
      margin-bottom: 30px;

      h2 {
        font-size: 24px;
        margin-bottom: 20px;
        color: #333;
        position: relative;
        padding-bottom: 10px;

        &:after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          width: 50px;
          height: 3px;
          background-color: var(--primary-color);
        }
      }

      p {
        font-size: 16px;
        line-height: 1.6;
        color: #666;
        margin-bottom: 20px;
      }
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

      .social-link {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #666;
        text-decoration: none;
        transition: color 0.3s;

        &:hover {
          color: var(--primary-color);
        }

        .el-icon {
          font-size: 36px;
          margin-bottom: 10px;
        }

        span {
          font-size: 16px;
        }
      }
    }
  }
}
</style>