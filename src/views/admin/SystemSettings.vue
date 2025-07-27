<template>
  <div class="system-settings-container">
    <page-header title="系统设置" subtitle="管理平台全局设置"></page-header>
    
    <el-card class="main-card">
      <el-tabs>
        <!-- 基础设置 -->
        <el-tab-pane label="基础设置">
          <el-form :model="basicSettings" label-width="120px" label-position="left">
            <el-form-item label="平台名称">
              <el-input v-model="basicSettings.siteName"></el-input>
            </el-form-item>
            
            <el-form-item label="平台简介">
              <el-input 
                v-model="basicSettings.siteDescription" 
                type="textarea" 
                :rows="3">
              </el-input>
            </el-form-item>
            
            <el-form-item label="联系邮箱">
              <el-input v-model="basicSettings.contactEmail"></el-input>
            </el-form-item>
            
            <el-form-item label="联系电话">
              <el-input v-model="basicSettings.contactPhone"></el-input>
            </el-form-item>
            
            <el-form-item label="备案号">
              <el-input v-model="basicSettings.icp"></el-input>
            </el-form-item>
            
            <el-form-item label="版权信息">
              <el-input v-model="basicSettings.copyright"></el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 功能开关 -->
        <el-tab-pane label="功能开关">
          <el-form label-width="120px" label-position="left">
            <el-form-item label="用户注册">
              <el-switch v-model="featureSettings.enableRegistration"></el-switch>
            </el-form-item>
            
            <el-form-item label="AI课程功能">
              <el-switch v-model="featureSettings.enableAICoach"></el-switch>
            </el-form-item>
            
            <el-form-item label="健康管理">
              <el-switch v-model="featureSettings.enableHealthManagement"></el-switch>
            </el-form-item>
            
            <el-form-item label="社交功能">
              <el-switch v-model="featureSettings.enableSocialPlatform"></el-switch>
            </el-form-item>
            
            <el-form-item label="课程评论">
              <el-switch v-model="featureSettings.enableCourseComments"></el-switch>
            </el-form-item>
            
            <el-form-item label="课程评分">
              <el-switch v-model="featureSettings.enableCourseRating"></el-switch>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveFeatureSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 安全设置 -->
        <el-tab-pane label="安全设置">
          <el-form label-width="180px" label-position="left">
            <el-form-item label="密码最小长度">
              <el-input-number v-model="securitySettings.passwordMinLength" :min="6" :max="20"></el-input-number>
            </el-form-item>
            
            <el-form-item label="要求密码包含特殊字符">
              <el-switch v-model="securitySettings.requireSpecialChar"></el-switch>
            </el-form-item>
            
            <el-form-item label="要求密码包含数字">
              <el-switch v-model="securitySettings.requireNumber"></el-switch>
            </el-form-item>
            
            <el-form-item label="要求密码包含大写字母">
              <el-switch v-model="securitySettings.requireUppercase"></el-switch>
            </el-form-item>
            
            <el-form-item label="登录尝试失败锁定次数">
              <el-input-number v-model="securitySettings.loginAttempts" :min="3" :max="10"></el-input-number>
            </el-form-item>
            
            <el-form-item label="锁定时长（分钟）">
              <el-input-number v-model="securitySettings.lockDuration" :min="5" :max="60"></el-input-number>
            </el-form-item>
            
            <el-form-item label="会话超时时间（分钟）">
              <el-input-number v-model="securitySettings.sessionTimeout" :min="10" :max="1440"></el-input-number>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSecuritySettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 文件存储 -->
        <el-tab-pane label="文件存储">
          <el-form label-width="150px" label-position="left">
            <el-form-item label="存储方式">
              <el-radio-group v-model="storageSettings.storageType">
                <el-radio label="local">本地存储</el-radio>
                <el-radio label="oss">阿里云OSS</el-radio>
                <el-radio label="cos">腾讯云COS</el-radio>
                <el-radio label="qiniu">七牛云</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <template v-if="storageSettings.storageType !== 'local'">
              <el-form-item label="AccessKey">
                <el-input v-model="storageSettings.accessKey"></el-input>
              </el-form-item>
              
              <el-form-item label="SecretKey">
                <el-input v-model="storageSettings.secretKey" type="password" show-password></el-input>
              </el-form-item>
              
              <el-form-item label="Bucket">
                <el-input v-model="storageSettings.bucket"></el-input>
              </el-form-item>
              
              <el-form-item label="Region">
                <el-input v-model="storageSettings.region"></el-input>
              </el-form-item>
              
              <el-form-item label="Endpoint">
                <el-input v-model="storageSettings.endpoint"></el-input>
              </el-form-item>
              
              <el-form-item label="自定义域名">
                <el-input v-model="storageSettings.domain"></el-input>
              </el-form-item>
            </template>
            
            <el-form-item label="上传文件大小限制(MB)">
              <el-input-number v-model="storageSettings.maxFileSize" :min="1" :max="500"></el-input-number>
            </el-form-item>
            
            <el-form-item label="允许的文件类型">
              <el-select
                v-model="storageSettings.allowedTypes"
                multiple
                filterable
                allow-create
                default-first-option
                placeholder="请选择或添加允许的文件类型"
              >
                <el-option label="图片(jpg,jpeg,png,gif)" value="image"></el-option>
                <el-option label="视频(mp4,avi,mov)" value="video"></el-option>
                <el-option label="文档(pdf,doc,docx)" value="document"></el-option>
                <el-option label="音频(mp3,wav)" value="audio"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveStorageSettings">保存设置</el-button>
              <el-button type="success" @click="testStorageConnection">测试连接</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 缓存设置 -->
        <el-tab-pane label="缓存设置">
          <el-form label-width="150px" label-position="left">
            <el-form-item label="启用页面缓存">
              <el-switch v-model="cacheSettings.enablePageCache"></el-switch>
            </el-form-item>
            
            <el-form-item label="页面缓存时间(分钟)">
              <el-input-number 
                v-model="cacheSettings.pageCacheDuration" 
                :min="1" 
                :max="1440"
                :disabled="!cacheSettings.enablePageCache"
              ></el-input-number>
            </el-form-item>
            
            <el-form-item label="启用API缓存">
              <el-switch v-model="cacheSettings.enableApiCache"></el-switch>
            </el-form-item>
            
            <el-form-item label="API缓存时间(分钟)">
              <el-input-number 
                v-model="cacheSettings.apiCacheDuration" 
                :min="1" 
                :max="1440"
                :disabled="!cacheSettings.enableApiCache"
              ></el-input-number>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveCacheSettings">保存设置</el-button>
              <el-button type="danger" @click="clearAllCache">清除所有缓存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 日志设置 -->
        <el-tab-pane label="日志设置">
          <el-form label-width="150px" label-position="left">
            <el-form-item label="记录登录日志">
              <el-switch v-model="logSettings.enableLoginLog"></el-switch>
            </el-form-item>
            
            <el-form-item label="记录操作日志">
              <el-switch v-model="logSettings.enableOperationLog"></el-switch>
            </el-form-item>
            
            <el-form-item label="记录错误日志">
              <el-switch v-model="logSettings.enableErrorLog"></el-switch>
            </el-form-item>
            
            <el-form-item label="日志保留天数">
              <el-input-number v-model="logSettings.logRetentionDays" :min="7" :max="365"></el-input-number>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveLogSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
          
          <el-divider content-position="center">日志管理</el-divider>
          
          <div class="log-actions">
            <el-button @click="viewLoginLogs">查看登录日志</el-button>
            <el-button @click="viewOperationLogs">查看操作日志</el-button>
            <el-button @click="viewErrorLogs">查看错误日志</el-button>
            <el-button type="danger" @click="clearAllLogs">清除所有日志</el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import PageHeader from '../../components/common/PageHeader.vue';

// 基础设置
const basicSettings = reactive({
  siteName: '舞动银龄',
  siteDescription: '为中老年人打造的舞蹈学习与健康管理平台',
  contactEmail: 'contact@example.com',
  contactPhone: '400-123-4567',
  icp: '京ICP备12345678号',
  copyright: '© 2023 舞动银龄 版权所有'
});

// 功能开关设置
const featureSettings = reactive({
  enableRegistration: true,
  enableAICoach: true,
  enableHealthManagement: true,
  enableSocialPlatform: true,
  enableCourseComments: true,
  enableCourseRating: true
});

// 安全设置
const securitySettings = reactive({
  passwordMinLength: 8,
  requireSpecialChar: true,
  requireNumber: true,
  requireUppercase: true,
  loginAttempts: 5,
  lockDuration: 30,
  sessionTimeout: 60
});

// 存储设置
const storageSettings = reactive({
  storageType: 'local',
  accessKey: '',
  secretKey: '',
  bucket: '',
  region: '',
  endpoint: '',
  domain: '',
  maxFileSize: 50,
  allowedTypes: ['image', 'video', 'document']
});

// 缓存设置
const cacheSettings = reactive({
  enablePageCache: true,
  pageCacheDuration: 60,
  enableApiCache: true,
  apiCacheDuration: 30
});

// 日志设置
const logSettings = reactive({
  enableLoginLog: true,
  enableOperationLog: true,
  enableErrorLog: true,
  logRetentionDays: 30
});

// 页面加载时获取设置数据
onMounted(() => {
  fetchSettings();
});

// 获取设置数据
const fetchSettings = () => {
  // 模拟API调用
  console.log('获取系统设置...');
  // 实际项目中应该调用API获取数据
  // api.getSettings().then(response => { ... })
};

// 保存基础设置
const saveBasicSettings = () => {
  console.log('保存基础设置:', basicSettings);
  ElMessage.success('基础设置保存成功');
};

// 保存功能开关设置
const saveFeatureSettings = () => {
  console.log('保存功能开关设置:', featureSettings);
  ElMessage.success('功能设置保存成功');
};

// 保存安全设置
const saveSecuritySettings = () => {
  console.log('保存安全设置:', securitySettings);
  ElMessage.success('安全设置保存成功');
};

// 保存存储设置
const saveStorageSettings = () => {
  console.log('保存存储设置:', storageSettings);
  ElMessage.success('存储设置保存成功');
};

// 测试存储连接
const testStorageConnection = () => {
  if (storageSettings.storageType === 'local') {
    ElMessage.success('本地存储连接测试成功');
    return;
  }
  
  if (!storageSettings.accessKey || !storageSettings.secretKey || !storageSettings.bucket) {
    ElMessage.error('请填写完整的存储配置信息');
    return;
  }
  
  console.log('测试存储连接:', storageSettings);
  ElMessage.success('存储连接测试成功');
};

// 保存缓存设置
const saveCacheSettings = () => {
  console.log('保存缓存设置:', cacheSettings);
  ElMessage.success('缓存设置保存成功');
};

// 清除所有缓存
const clearAllCache = () => {
  console.log('清除所有缓存');
  ElMessage.success('所有缓存已清除');
};

// 保存日志设置
const saveLogSettings = () => {
  console.log('保存日志设置:', logSettings);
  ElMessage.success('日志设置保存成功');
};

// 查看各种日志
const viewLoginLogs = () => {
  console.log('查看登录日志');
};

const viewOperationLogs = () => {
  console.log('查看操作日志');
};

const viewErrorLogs = () => {
  console.log('查看错误日志');
};

// 清除所有日志
const clearAllLogs = () => {
  console.log('清除所有日志');
  ElMessage.success('所有日志已清除');
};
</script>

<style scoped>
.system-settings-container {
  padding: 20px;
}

.main-card {
  margin-top: 20px;
}

.log-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  flex-wrap: wrap;
}
</style> 