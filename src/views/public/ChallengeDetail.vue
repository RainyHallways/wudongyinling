<template>
  <div class="challenge-detail">
    <PageHeader />
    
    <div class="container">
      <div class="challenge-hero" v-if="challenge">
        <div class="hero-content">
          <div class="challenge-status">
            <el-tag :type="getStatusType(challenge.status)" size="large">
              {{ getStatusText(challenge.status) }}
            </el-tag>
          </div>
          
          <h1 class="challenge-title">{{ challenge.title }}</h1>
          <p class="challenge-description">{{ challenge.description }}</p>
          
          <div class="challenge-stats">
            <div class="stat-item">
              <div class="stat-number">{{ challenge.participants }}</div>
              <div class="stat-label">参与人数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ challenge.days }}</div>
              <div class="stat-label">挑战天数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ challenge.currentDay }}</div>
              <div class="stat-label">已打卡天数</div>
            </div>
          </div>
          
          <div class="challenge-progress">
            <div class="progress-info">
              <span>完成进度</span>
              <span>{{ Math.round(challenge.currentDay / challenge.days * 100) }}%</span>
            </div>
            <el-progress 
              :percentage="challenge.currentDay / challenge.days * 100"
              :stroke-width="8"
              :status="challenge.currentDay === challenge.days ? 'success' : undefined"
            />
          </div>
          
          <div class="challenge-actions">
            <el-button 
              v-if="!isParticipating"
              type="primary" 
              size="large"
              @click="joinChallenge"
              :loading="joining"
            >
              参加挑战
            </el-button>
            <el-button 
              v-else-if="canCheckIn"
              type="success" 
              size="large"
              @click="checkIn"
              :loading="checkingIn"
            >
              今日打卡
            </el-button>
            <el-button 
              v-else
              size="large"
              disabled
            >
              今日已打卡
            </el-button>
          </div>
        </div>
        
        <div class="hero-image">
          <el-image 
            :src="challenge.image_url || '/images/challenge-default.png'"
            fit="cover"
            class="challenge-image"
          />
        </div>
      </div>
      
      <!-- 挑战详情内容 -->
      <div class="challenge-content" v-if="challenge">
        <el-row :gutter="24">
          <el-col :xs="24" :lg="16">
            <!-- 挑战说明 -->
            <el-card class="content-card">
              <template #header>
                <h3>挑战说明</h3>
              </template>
              <div class="challenge-rules">
                <h4>挑战规则</h4>
                <ul>
                  <li>每天完成指定的舞蹈练习</li>
                  <li>练习时长不少于15分钟</li>
                  <li>需要提交练习视频或照片作为打卡凭证</li>
                  <li>连续打卡可获得额外奖励</li>
                </ul>
                
                <h4>奖励机制</h4>
                <ul>
                  <li>完成挑战可获得专属徽章</li>
                  <li>连续打卡7天获得"坚持者"称号</li>
                  <li>完成挑战获得"挑战达人"称号</li>
                  <li>表现优秀者可获得精美舞蹈装备</li>
                </ul>
              </div>
            </el-card>
            
            <!-- 打卡记录 -->
            <el-card class="content-card">
              <template #header>
                <h3>我的打卡记录</h3>
              </template>
              <div class="checkin-calendar">
                <div class="calendar-grid">
                  <div 
                    v-for="day in challenge.days" 
                    :key="day"
                    class="calendar-day"
                    :class="{
                      'checked': day <= challenge.currentDay,
                      'today': day === challenge.currentDay + 1,
                      'future': day > challenge.currentDay + 1
                    }"
                  >
                    <span>{{ day }}</span>
                    <el-icon v-if="day <= challenge.currentDay" class="check-icon">
                      <Check />
                    </el-icon>
                  </div>
                </div>
              </div>
            </el-card>
            
            <!-- 参与者动态 -->
            <el-card class="content-card">
              <template #header>
                <h3>参与者动态</h3>
              </template>
              <div class="participant-posts">
                <div 
                  v-for="post in participantPosts" 
                  :key="post.id"
                  class="post-item"
                >
                  <div class="post-header">
                    <el-avatar :src="post.user_avatar" :size="32" />
                    <div class="post-user-info">
                      <div class="username">{{ post.username }}</div>
                      <div class="post-time">{{ formatTime(post.created_at) }}</div>
                    </div>
                  </div>
                  <div class="post-content">
                    <p>{{ post.content }}</p>
                    <el-image 
                      v-if="post.image_url"
                      :src="post.image_url"
                      fit="cover"
                      class="post-image"
                    />
                  </div>
                  <div class="post-actions">
                    <el-button text size="small">
                      <el-icon><Heart /></el-icon>
                      {{ post.likes }}
                    </el-button>
                    <el-button text size="small">
                      <el-icon><ChatDotRound /></el-icon>
                      {{ post.comments }}
                    </el-button>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="24" :lg="8">
            <!-- 排行榜 -->
            <el-card class="sidebar-card">
              <template #header>
                <h3>排行榜</h3>
              </template>
              <div class="leaderboard">
                <div 
                  v-for="(user, index) in leaderboard" 
                  :key="user.id"
                  class="leaderboard-item"
                  :class="{ 'is-me': user.id === userStore.userInfo.id }"
                >
                  <div class="rank">
                    <el-tag 
                      v-if="index < 3"
                      :type="['warning', 'info', 'success'][index]"
                      size="small"
                    >
                      {{ index + 1 }}
                    </el-tag>
                    <span v-else class="rank-number">{{ index + 1 }}</span>
                  </div>
                  <el-avatar :src="user.avatar" :size="32" />
                  <div class="user-info">
                    <div class="username">{{ user.username }}</div>
                    <div class="checkin-days">{{ user.checkinDays }}天</div>
                  </div>
                </div>
              </div>
            </el-card>
            
            <!-- 相关挑战 -->
            <el-card class="sidebar-card">
              <template #header>
                <h3>相关挑战</h3>
              </template>
              <div class="related-challenges">
                <div 
                  v-for="relatedChallenge in relatedChallenges" 
                  :key="relatedChallenge.id"
                  class="related-item"
                  @click="$router.push(`/challenge/${relatedChallenge.id}`)"
                >
                  <el-image 
                    :src="relatedChallenge.image_url"
                    fit="cover"
                    class="related-image"
                  />
                  <div class="related-info">
                    <div class="related-title">{{ relatedChallenge.title }}</div>
                    <div class="related-participants">
                      {{ relatedChallenge.participants }}人参与
                    </div>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 加载状态 -->
      <div v-else class="loading-container">
        <el-loading-icon />
        <p>加载中...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check, Heart, ChatDotRound } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const userStore = useUserStore()

// 响应式数据
const challenge = ref<any>(null)
const loading = ref(true)
const joining = ref(false)
const checkingIn = ref(false)
const isParticipating = ref(false)
const canCheckIn = ref(true)

// 模拟数据
const participantPosts = ref([
  {
    id: 1,
    username: '张玉梅',
    user_avatar: '/images/zym.png',
    content: '今天的练习完成了！感觉动作越来越熟练了',
    image_url: '/images/zym-2.png',
    likes: 12,
    comments: 3,
    created_at: '2024-01-15T10:30:00Z'
  },
  {
    id: 2,
    username: '陈淑芬',
    user_avatar: '/images/csf.png',
    content: '坚持第10天打卡，身体感觉更有活力了！',
    image_url: '/images/csf-2.png',
    likes: 8,
    comments: 2,
    created_at: '2024-01-15T09:15:00Z'
  }
])

const leaderboard = ref([
  { id: 1, username: '王德福', avatar: '/images/wdf.png', checkinDays: 21 },
  { id: 2, username: '张玉梅', avatar: '/images/zym.png', checkinDays: 20 },
  { id: 3, username: '陈淑芬', avatar: '/images/csf.png', checkinDays: 18 },
  { id: 4, username: '李明华', avatar: '/images/default-avatar.png', checkinDays: 15 },
  { id: 5, username: '王小红', avatar: '/images/default-avatar.png', checkinDays: 12 }
])

const relatedChallenges = ref([
  {
    id: 2,
    title: '太极拳基础动作',
    participants: 89,
    image_url: '/images/taiji.png'
  },
  {
    id: 3,
    title: '民族舞入门',
    participants: 156,
    image_url: '/images/minzu.png'
  }
])

// 计算属性
const challengeId = computed(() => parseInt(route.params.id as string))

// 生命周期
onMounted(() => {
  loadChallengeDetail()
})

// 加载挑战详情
const loadChallengeDetail = async () => {
  try {
    loading.value = true
    
    // 模拟API调用
    setTimeout(() => {
      challenge.value = {
        id: challengeId.value,
        title: challengeId.value === 1 ? '30天广场舞打卡挑战' : '太极拳基础动作',
        description: challengeId.value === 1 ? 
          '连续30天打卡广场舞练习，提升身体协调性和健康水平' : 
          '学习太极拳24式基础动作，提升身心健康',
        participants: challengeId.value === 1 ? 156 : 89,
        days: challengeId.value === 1 ? 30 : 21,
        currentDay: challengeId.value === 1 ? 15 : 8,
        status: 'ongoing',
        image_url: challengeId.value === 1 ? '/images/guangchangwu.png' : '/images/taiji.png'
      }
      
      // 检查用户是否已参与
      isParticipating.value = true
      
      loading.value = false
    }, 1000)
  } catch (error) {
    console.error('Failed to load challenge detail:', error)
    ElMessage.error('加载挑战详情失败')
    loading.value = false
  }
}

// 参加挑战
const joinChallenge = async () => {
  try {
    joining.value = true
    
    // 模拟API调用
    setTimeout(() => {
      isParticipating.value = true
      challenge.value.participants++
      ElMessage.success('成功参加挑战！')
      joining.value = false
    }, 1000)
  } catch (error) {
    console.error('Failed to join challenge:', error)
    ElMessage.error('参加挑战失败')
    joining.value = false
  }
}

// 打卡
const checkIn = async () => {
  try {
    checkingIn.value = true
    
    // 模拟API调用
    setTimeout(() => {
      challenge.value.currentDay++
      canCheckIn.value = false
      ElMessage.success('打卡成功！')
      checkingIn.value = false
    }, 1000)
  } catch (error) {
    console.error('Failed to check in:', error)
    ElMessage.error('打卡失败')
    checkingIn.value = false
  }
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    'ongoing': 'primary',
    'completed': 'success',
    'upcoming': 'warning'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    'ongoing': '进行中',
    'completed': '已完成',
    'upcoming': '即将开始'
  }
  return textMap[status] || '未知'
}

// 格式化时间
const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return '刚刚'
  if (diffMins < 60) return `${diffMins}分钟前`
  if (diffMins < 1440) return `${Math.floor(diffMins / 60)}小时前`
  
  return date.toLocaleDateString()
}
</script>

<style scoped>
.challenge-detail {
  min-height: 100vh;
  background: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.challenge-hero {
  display: flex;
  gap: 40px;
  align-items: center;
  background: white;
  padding: 40px;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.hero-content {
  flex: 1;
}

.challenge-status {
  margin-bottom: 16px;
}

.challenge-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #303133;
  margin: 0 0 16px;
}

.challenge-description {
  font-size: 1.1rem;
  color: #606266;
  margin-bottom: 30px;
  line-height: 1.6;
}

.challenge-stats {
  display: flex;
  gap: 40px;
  margin-bottom: 30px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #909399;
}

.challenge-progress {
  margin-bottom: 30px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-weight: 500;
}

.challenge-actions {
  display: flex;
  gap: 16px;
}

.hero-image {
  width: 300px;
  height: 200px;
}

.challenge-image {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.content-card, .sidebar-card {
  margin-bottom: 24px;
}

.challenge-rules h4 {
  color: #303133;
  margin: 20px 0 12px;
  font-size: 1.1rem;
}

.challenge-rules ul {
  margin: 0 0 20px;
  padding-left: 20px;
}

.challenge-rules li {
  margin-bottom: 8px;
  color: #606266;
  line-height: 1.5;
}

.checkin-calendar {
  padding: 20px 0;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  font-weight: 500;
  position: relative;
  transition: all 0.2s;
}

.calendar-day.checked {
  background: #f0f9ff;
  border-color: #409eff;
  color: #409eff;
}

.calendar-day.today {
  border-color: #67c23a;
  background: #f0f9ff;
}

.calendar-day.future {
  color: #c0c4cc;
}

.check-icon {
  position: absolute;
  bottom: 2px;
  right: 2px;
  color: #67c23a;
  font-size: 12px;
}

.participant-posts {
  max-height: 400px;
  overflow-y: auto;
}

.post-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.post-item:last-child {
  border-bottom: none;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.post-user-info .username {
  font-weight: 500;
  color: #303133;
}

.post-user-info .post-time {
  font-size: 0.8rem;
  color: #909399;
}

.post-content p {
  margin: 0 0 12px;
  color: #606266;
  line-height: 1.5;
}

.post-image {
  width: 100%;
  max-width: 200px;
  height: 120px;
  border-radius: 8px;
}

.post-actions {
  display: flex;
  gap: 16px;
}

.leaderboard {
  max-height: 300px;
  overflow-y: auto;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.leaderboard-item:last-child {
  border-bottom: none;
}

.leaderboard-item.is-me {
  background: #f0f9ff;
  margin: 0 -16px;
  padding: 12px 16px;
  border-radius: 8px;
}

.rank {
  width: 24px;
  text-align: center;
}

.rank-number {
  font-weight: 500;
  color: #909399;
}

.user-info {
  flex: 1;
}

.user-info .username {
  font-weight: 500;
  color: #303133;
  margin-bottom: 2px;
}

.user-info .checkin-days {
  font-size: 0.8rem;
  color: #909399;
}

.related-challenges {
  max-height: 300px;
  overflow-y: auto;
}

.related-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.related-item:hover {
  background: #f5f7fa;
  margin: 0 -16px;
  padding: 12px 16px;
  border-radius: 8px;
}

.related-item:last-child {
  border-bottom: none;
}

.related-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  flex-shrink: 0;
}

.related-info {
  flex: 1;
}

.related-title {
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.related-participants {
  font-size: 0.8rem;
  color: #909399;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .challenge-hero {
    flex-direction: column;
    padding: 20px;
    gap: 20px;
  }
  
  .hero-image {
    width: 100%;
    height: 200px;
  }
  
  .challenge-title {
    font-size: 1.8rem;
  }
  
  .challenge-stats {
    gap: 20px;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  .calendar-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}
</style> 