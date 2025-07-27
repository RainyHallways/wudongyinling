<template>
  <div class="user-profile-container">
    <page-header title="个人中心" subtitle="管理您的账户信息和舞蹈历程"></page-header>
    
    <el-row :gutter="20">
      <!-- 左侧信息卡 -->
      <el-col :xs="24" :md="8">
        <el-card class="profile-card" shadow="hover">
          <div class="user-avatar-wrapper">
            <el-avatar :size="120" :src="userInfo.avatar || defaultAvatar"></el-avatar>
            <div class="edit-avatar">
              <el-button size="small" type="primary" circle>
                <el-icon><Edit /></el-icon>
              </el-button>
            </div>
          </div>
          
          <h2 class="user-name">{{ userInfo.nickname || '未设置昵称' }}</h2>
          <p class="user-email">{{ userInfo.email }}</p>
          
          <div class="user-stats">
            <div class="stat-item">
              <div class="stat-value">{{ userStats.danceHours || 0 }}</div>
              <div class="stat-label">舞蹈时长</div>
            </div>
            <el-divider direction="vertical" />
            <div class="stat-item">
              <div class="stat-value">{{ userStats.completedCourses || 0 }}</div>
              <div class="stat-label">完成课程</div>
            </div>
            <el-divider direction="vertical" />
            <div class="stat-item">
              <div class="stat-value">{{ userStats.achievements || 0 }}</div>
              <div class="stat-label">获得成就</div>
            </div>
          </div>
          
          <div class="user-level">
            <div class="level-text">
              <span class="level-label">当前等级:</span>
              <span class="level-value">{{ userLevel.name || '初学者' }}</span>
            </div>
            <el-progress :percentage="userLevel.progress || 0" :format="() => `${userLevel.currentExp || 0}/${userLevel.nextLevelExp || 100}`"></el-progress>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧选项卡 -->
      <el-col :xs="24" :md="16">
        <el-card shadow="hover">
          <el-tabs>
            <el-tab-pane label="基本信息">
              <el-form :model="userForm" label-width="100px">
                <el-form-item label="用户昵称">
                  <el-input v-model="userForm.nickname" placeholder="请输入昵称"></el-input>
                </el-form-item>
                
                <el-form-item label="性别">
                  <el-radio-group v-model="userForm.gender">
                    <el-radio :label="1">男</el-radio>
                    <el-radio :label="2">女</el-radio>
                    <el-radio :label="0">保密</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="年龄">
                  <el-input-number v-model="userForm.age" :min="1" :max="120"></el-input-number>
                </el-form-item>
                
                <el-form-item label="手机号码">
                  <el-input v-model="userForm.phone" placeholder="请输入手机号码"></el-input>
                </el-form-item>
                
                <el-form-item label="个人简介">
                  <el-input 
                    v-model="userForm.bio" 
                    type="textarea" 
                    placeholder="介绍一下自己吧" 
                    :rows="4">
                  </el-input>
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="saveUserInfo">保存信息</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <el-tab-pane label="舞蹈历程">
              <el-empty v-if="danceHistory.length === 0" description="暂无舞蹈历程记录"></el-empty>
              <el-timeline v-else>
                <el-timeline-item
                  v-for="(history, index) in danceHistory"
                  :key="index"
                  :timestamp="history.date"
                  :type="history.type"
                >
                  {{ history.content }}
                </el-timeline-item>
              </el-timeline>
            </el-tab-pane>
            
            <el-tab-pane label="我的收藏">
              <el-empty v-if="favoriteCourses.length === 0" description="暂无收藏的课程"></el-empty>
              <div v-else class="course-grid">
                <el-card 
                  v-for="course in favoriteCourses" 
                  :key="course.id" 
                  class="course-card" 
                  shadow="hover"
                  @click="viewCourse(course.id)"
                >
                  <img :src="course.coverImg" class="course-cover" />
                  <div class="course-info">
                    <h3 class="course-title">{{ course.title }}</h3>
                    <div class="course-meta">
                      <el-tag size="small">{{ course.category }}</el-tag>
                      <div class="course-stats">
                        <span><el-icon><View /></el-icon> {{ course.viewCount }}</span>
                        <span><el-icon><Star /></el-icon> {{ course.favoriteCount }}</span>
                      </div>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="账号安全">
              <el-form label-width="100px">
                <el-form-item label="修改密码">
                  <el-button type="primary" @click="showChangePasswordDialog">修改密码</el-button>
                </el-form-item>
                
                <el-form-item label="绑定手机">
                  <div class="bind-status">
                    <span v-if="userInfo.phone">{{ maskPhone(userInfo.phone) }}</span>
                    <span v-else>未绑定</span>
                    <el-button type="primary" link @click="showBindPhoneDialog">
                      {{ userInfo.phone ? '更换' : '绑定' }}
                    </el-button>
                  </div>
                </el-form-item>
                
                <el-form-item label="绑定邮箱">
                  <div class="bind-status">
                    <span v-if="userInfo.email">{{ maskEmail(userInfo.email) }}</span>
                    <span v-else>未绑定</span>
                    <el-button type="primary" link @click="showBindEmailDialog">
                      {{ userInfo.email ? '更换' : '绑定' }}
                    </el-button>
                  </div>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="changePasswordDialog"
      title="修改密码"
      width="500px"
    >
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="当前密码">
          <el-input v-model="passwordForm.currentPassword" type="password"></el-input>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="passwordForm.confirmPassword" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="changePasswordDialog = false">取消</el-button>
          <el-button type="primary" @click="changePassword">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import PageHeader from '../../components/common/PageHeader.vue';
import { Edit, View, Star } from '@element-plus/icons-vue';

const defaultAvatar = '/public/images/default-avatar.png'; // 默认头像路径

// 用户信息
const userInfo = ref({
  id: 1,
  username: 'user123',
  nickname: '舞动爱好者',
  email: 'user123@example.com',
  phone: '13800138000',
  avatar: null,
  gender: 1,
  age: 65,
  bio: '退休后爱上了舞蹈，希望通过舞蹈保持健康活力！'
});

// 用户表单数据
const userForm = reactive({
  nickname: userInfo.value.nickname,
  gender: userInfo.value.gender,
  age: userInfo.value.age,
  phone: userInfo.value.phone,
  bio: userInfo.value.bio
});

// 用户统计数据
const userStats = ref({
  danceHours: 32,
  completedCourses: 8,
  achievements: 5
});

// 用户等级信息
const userLevel = ref({
  name: '舞蹈新手',
  currentExp: 75,
  nextLevelExp: 100,
  progress: 75
});

// 舞蹈历程
const danceHistory = ref([
  {
    date: '2023-05-10',
    type: 'success',
    content: '完成了第一个基础舞蹈课程《舞动基础入门》'
  },
  {
    date: '2023-06-01',
    type: 'primary',
    content: '参加了线上舞蹈挑战，获得"初级舞者"称号'
  },
  {
    date: '2023-07-15',
    type: 'success',
    content: '完成了《中国古典舞基础》课程，达到初级水平'
  }
]);

// 收藏的课程
const favoriteCourses = ref([
  {
    id: 1,
    title: '太极舞基础入门',
    coverImg: '/public/images/dance1.jpg',
    category: '太极舞',
    viewCount: 1253,
    favoriteCount: 328
  },
  {
    id: 2,
    title: '广场舞健身课程',
    coverImg: '/public/images/dance2.jpg',
    category: '广场舞',
    viewCount: 2156,
    favoriteCount: 512
  },
  {
    id: 3,
    title: '民族舞蹈欣赏',
    coverImg: '/public/images/dance3.jpg',
    category: '民族舞',
    viewCount: 1855,
    favoriteCount: 423
  }
]);

// 修改密码相关
const changePasswordDialog = ref(false);
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// 页面加载时获取用户数据
onMounted(() => {
  fetchUserData();
});

// 获取用户数据
const fetchUserData = () => {
  // 模拟API调用
  console.log('获取用户数据...');
  // 实际项目中应该调用API获取数据
  // userApi.getUserProfile().then(response => { ... })
};

// 保存用户信息
const saveUserInfo = () => {
  // 模拟API调用
  console.log('保存用户信息:', userForm);
  
  // 更新本地userInfo数据
  userInfo.value = {
    ...userInfo.value,
    ...userForm
  };
  
  ElMessage({
    type: 'success',
    message: '个人信息保存成功'
  });
  
  // 实际项目中应该调用API保存数据
  // userApi.updateUserProfile(userForm).then(response => { ... })
};

// 查看课程详情
const viewCourse = (courseId) => {
  console.log('查看课程详情:', courseId);
  // 实际项目中应该跳转到课程详情页
  // router.push(`/course/${courseId}`);
};

// 显示修改密码对话框
const showChangePasswordDialog = () => {
  changePasswordDialog.value = true;
  // 重置表单
  passwordForm.currentPassword = '';
  passwordForm.newPassword = '';
  passwordForm.confirmPassword = '';
};

// 修改密码
const changePassword = () => {
  // 表单验证
  if (!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    ElMessage.error('请填写完整密码信息');
    return;
  }
  
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的新密码不一致');
    return;
  }
  
  // 模拟API调用
  console.log('修改密码:', passwordForm);
  
  // 关闭对话框
  changePasswordDialog.value = false;
  
  ElMessage({
    type: 'success',
    message: '密码修改成功'
  });
  
  // 实际项目中应该调用API修改密码
  // userApi.changePassword(passwordForm).then(response => { ... })
};

// 显示绑定手机对话框
const showBindPhoneDialog = () => {
  console.log('显示绑定手机对话框');
  // 实现绑定手机逻辑
};

// 显示绑定邮箱对话框
const showBindEmailDialog = () => {
  console.log('显示绑定邮箱对话框');
  // 实现绑定邮箱逻辑
};

// 手机号脱敏
const maskPhone = (phone) => {
  if (!phone) return '';
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
};

// 邮箱脱敏
const maskEmail = (email) => {
  if (!email) return '';
  const [username, domain] = email.split('@');
  return `${username.charAt(0)}***@${domain}`;
};
</script>

<style scoped>
.user-profile-container {
  padding: 20px;
}

.profile-card {
  text-align: center;
  padding: 20px;
}

.user-avatar-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
}

.edit-avatar {
  position: absolute;
  right: 0;
  bottom: 0;
}

.user-name {
  margin: 10px 0 5px 0;
  font-size: 24px;
  font-weight: bold;
}

.user-email {
  color: #909399;
  margin-bottom: 20px;
}

.user-stats {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.stat-item {
  padding: 0 20px;
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.user-level {
  margin: 20px 0;
  text-align: left;
}

.level-text {
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
}

.level-label {
  color: #909399;
}

.level-value {
  font-weight: bold;
  color: #67C23A;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.course-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-cover {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.course-info {
  padding: 10px 0;
}

.course-title {
  margin: 5px 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
}

.course-stats {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #909399;
}

.bind-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 