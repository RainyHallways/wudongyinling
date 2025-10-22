<template>
  <div class="policy-page page-with-nav">
    <page-header title="网站协议" subtitle="了解平台使用规则与用户权益"></page-header>
    
    <el-card class="policy-content">
      <div class="policy-document space-y-4 leading-7">
          <p>尊敬的用户，欢迎您使用本网站。在使用本网站前，请仔细阅读以下协议内容。如果您同意以下条款，请点击“同意并继续”按钮，进入本网站。如果您不同意以下条款，请勿使用本网站。</p>
          <h2 class="text-xl font-semibold">一、协议概述</h2>
          <p>1. 本协议是您与网站开发商（以下简称“我们”）之间关于您使用本网站所达成的协议。</p>
          <p>2. 本协议内容包括协议正文及所有我们发布的各类规则。所有规则为本协议不可分割的一部分，与协议正文具有同等法律效力。</p>
          <h2 class="text-xl font-semibold">二、网站使用许可</h2>
          <p>1. 我们授予您一项有限的、非独占的、不可转让的、可撤销的使用本网站的权利。</p>
          <p>2. 您可以在一台或多台设备上安装、使用、显示、运行本网站。</p>
          <p>3. 您不得对本网站进行逆向工程、反编译、反汇编或试图以其他方式发现本网站的源代码。</p>
          <h2 class="text-xl font-semibold">三、用户行为规范</h2>
          <p>1. 您在使用本网站时，应遵守法律法规，不得利用本网站从事违法活动。</p>
          <p>2. 您不得侵犯我们的知识产权，不得传播、上传、发布含有侵权内容的文件。</p>
          <p>3. 您应确保账号和密码的安全，对使用账号和密码所产生的一切后果承担法律责任。</p>
          <h2 class="text-xl font-semibold">四、隐私政策</h2>
          <p>1. 我们尊重您的隐私，承诺不会泄露您的个人信息。</p>
          <p>2. 我们可能会收集和使用您的非个人信息，以优化网站功能和用户体验。</p>
          <p>3. 在特定情况下，我们可能会根据法律法规要求，向有权机关提供您的相关信息。</p>
          <h2 class="text-xl font-semibold">五、免责声明</h2>
          <p>1. 本网站按“现状”提供，我们不承诺本网站的适用性、准确性、可靠性等。</p>
          <p>2. 我们不对因使用本网站导致的任何损失承担责任，包括但不限于直接、间接、偶然、特殊损害。</p>
          <h2 class="text-xl font-semibold">六、协议变更与终止</h2>
          <p>1. 我们有权随时修改本协议，修改后的协议在公布后立即生效。</p>
          <p>2. 在协议变更后，您继续使用本网站即视为同意新的协议内容。</p>
          <p>3. 我们有权在必要时终止本协议，届时您应停止使用本网站。</p>
          <p class="mt-6 text-center font-semibold">请您仔细阅读本协议，点击“同意并继续”按钮表示您已充分了解并接受本协议的全部内容。感谢您的使用！</p>
          <div class="flex justify-center gap-6 mt-4">
            <el-button type="danger" @click="rejectAgreement">拒绝</el-button>
            <el-button type="primary" @click="acceptAgreement">同意并继续</el-button>
          </div>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { useTitle } from '@vueuse/core'

useTitle('网站协议 - 舞动银龄')

const router = useRouter()

const printPolicy = () => {
  window.print()
  ElMessage.success('正在准备打印...')
}

const downloadPolicy = () => {
  // 模拟下载功能
  ElMessage.success('正在准备下载...')
}

const acceptAgreement = () => {
  ElMessageBox.confirm(
    '您确定同意本网站协议吗？',
    '确认同意',
    {
      confirmButtonText: '确认同意',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    ElMessage.success('感谢您的同意！')
    router.push('/')
  }).catch(() => {
    // 用户取消
  })
}

const rejectAgreement = () => {
  ElMessageBox.confirm(
    '如果您不同意本网站协议，将无法使用本平台服务。确定要拒绝吗？',
    '确认拒绝',
    {
      confirmButtonText: '确认拒绝',
      cancelButtonText: '重新考虑',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.info('感谢您的关注，期待您的下次访问！')
    router.push('/')
  }).catch(() => {
    // 用户取消
  })
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

.text-2xl {
  font-size: 1.5rem;
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