<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Share, Document, Monitor, Calendar, Heart, Trophy, Apple } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'

// 当前激活的标签页
const activeTab = ref('prescription')

// 标签页选项
interface TabOption {
  name: string
  label: string
}

const tabOptions: TabOption[] = [
  { name: 'prescription', label: '运动处方' },
  { name: 'monitor', label: '健康监测' },
  { name: 'chronic', label: '慢性病训练' }
]

// 健康卡片数据
interface HealthCard {
  id: number
  icon: string
  title: string
  description: string
  buttonText: string
  target: string
}

const healthCards = ref<HealthCard[]>([
  {
    id: 1,
    icon: 'Document',
    title: '运动处方',
    description: '根据您的健康状况和体能水平，生成个性化的舞蹈训练计划。',
    buttonText: '查看处方',
    target: 'prescription'
  },
  {
    id: 2,
    icon: 'Monitor',
    title: '健康监测',
    description: '实时监测您的血压、心率等健康数据，确保舞蹈训练安全。',
    buttonText: '查看数据',
    target: 'monitor'
  },
  {
    id: 3,
    icon: 'Calendar',
    title: '慢性病训练',
    description: '针对高血压、糖尿病等慢性病设计的专项舞蹈训练方案。',
    buttonText: '查看方案',
    target: 'chronic'
  }
])

// 运动处方数据
interface PrescriptionItem {
  label: string
  content: string
}

const prescription = ref<PrescriptionItem[]>([
  { label: '训练频率', content: '每周3-5次舞蹈训练' },
  { label: '单次时长', content: '每次训练时间30-45分钟' },
  { label: '运动强度', content: '以中低强度广场舞为主' },
  { label: '注意事项', content: '训练前后各5分钟热身和放松' }
])

// 运动建议
interface ExerciseAdvice {
  type: string
  content: string
}

const exerciseAdvice = ref<ExerciseAdvice[]>([
  { type: 'primary', content: '选择平坦、安全的场地进行舞蹈训练' },
  { type: 'success', content: '穿着舒适的运动鞋和宽松衣物' },
  { type: 'warning', content: '训练前后适量补充水分' },
  { type: 'danger', content: '如感到不适，立即停止训练' },
  { type: 'info', content: '定期监测血压和心率变化' }
])

// 健康指标数据
interface HealthMetric {
  id: number
  value: string
  label: string
  status: {
    type: string
    text: string
  }
}

const healthMetrics = ref<HealthMetric[]>([
  {
    id: 1,
    value: '125/82',
    label: '血压 (mmHg)',
    status: { type: 'success', text: '正常' }
  },
  {
    id: 2,
    value: '78',
    label: '心率 (次/分)',
    status: { type: 'success', text: '正常' }
  },
  {
    id: 3,
    value: '6.2',
    label: '血糖 (mmol/L)',
    status: { type: 'warning', text: '偏高' }
  }
])

// 健康记录
interface HealthRecord {
  time: string
  bp: string
  hr: string
  bs: string
  activityState: string
  dietState: string
}

const healthRecords = ref<HealthRecord[]>([])
let healthUpdateInterval: number | null = null

// 生成指定范围内的随机整数
const getRandomInt = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

// 生成指定范围内的随机浮点数
const getRandomFloat = (min: number, max: number, decimals: number): string => {
  const factor = Math.pow(10, decimals)
  return (Math.random() * (max - min) + min).toFixed(decimals)
}

// 生成随机血压值
const getRandomBP = (): string => {
  const systolic = getRandomInt(130, 150)
  const diastolic = getRandomInt(70, 90)
  return `${systolic}/${diastolic}`
}

// 生成随机心率值
const getRandomHR = (): number => {
  return getRandomInt(60, 100)
}

// 生成随机血糖值 (简化处理，4.4 ~ 10.0)
const getRandomBS = (): string => {
  return getRandomFloat(4.4, 10.0, 1)
}

// 判断血压状态
const getBPStatus = (bp: string): { type: string; text: string } => {
  const [systolic, diastolic] = bp.split('/').map(Number)
  if (systolic < 130 && diastolic < 85) return { type: 'success', text: '理想' }
  if (systolic <= 140 && diastolic <= 90) return { type: 'success', text: '正常' }
  if (systolic <= 160 && diastolic <= 100) return { type: 'warning', text: '偏高' }
  return { type: 'danger', text: '过高' }
}

// 判断心率状态
const getHRStatus = (hr: number): { type: string; text: string } => {
  if (hr >= 60 && hr <= 100) return { type: 'success', text: '正常' }
  if (hr < 60) return { type: 'warning', text: '偏低' }
  return { type: 'warning', text: '偏快' }
}

// 判断血糖状态
const getBSStatus = (bs: number): { type: string; text: string } => {
  if (bs >= 4.4 && bs <= 7.0) return { type: 'success', text: '正常' } // 空腹范围
  if (bs > 7.0 && bs <= 10.0) return { type: 'warning', text: '餐后偏高' } // 餐后范围
  if (bs > 10.0) return { type: 'danger', text: '过高' }
  return { type: 'danger', text: '过低' } // < 4.4
}

// 更新健康指标
const updateHealthMetrics = (): void => {
  const newBP = getRandomBP()
  const newHR = getRandomHR()
  const newBS = getRandomBS()

  healthMetrics.value = [
    { id: 1, value: newBP, label: '血压 (mmHg)', status: getBPStatus(newBP) },
    { id: 2, value: newHR.toString(), label: '心率 (次/分)', status: getHRStatus(newHR) },
    { id: 3, value: newBS.toString(), label: '血糖 (mmol/L)', status: getBSStatus(parseFloat(newBS)) }
  ]
}

// 添加健康记录
const addHealthRecord = (): void => {
  const now = new Date()
  const currentTime = now.toLocaleString('zh-CN', { hour12: false })
  const currentBP = healthMetrics.value.find(m => m.id === 1)?.value || '-'
  const currentHR = healthMetrics.value.find(m => m.id === 2)?.value || '-'
  const currentBS = healthMetrics.value.find(m => m.id === 3)?.value || '-'

  healthRecords.value.unshift({ // 使用 unshift 在开头添加新纪录
    time: currentTime,
    bp: currentBP,
    hr: currentHR,
    bs: currentBS,
    activityState: '静息', // 默认值
    dietState: '空腹' // 默认值
  })
}

// 分享给医生
const shareWithDoctor = (): void => {
  // 这里可以添加实际的分享逻辑，例如调用API
  ElMessage.success('分享成功')
}

// 启动定时器
onMounted(() => {
  updateHealthMetrics() // 立即更新一次
  healthUpdateInterval = window.setInterval(updateHealthMetrics, 2000)
})

// 清除定时器
onUnmounted(() => {
  if (healthUpdateInterval) {
    clearInterval(healthUpdateInterval)
  }
})

// 格式化日期为 YYYY年M月D日 周X
const formatDate = (date: Date): string => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekDay = ['日', '一', '二', '三', '四', '五', '六'][date.getDay()]
  return `${year}年${month}月${day}日 周${weekDay}`
}

// 训练计划数据
interface TrainingPlan {
  date: string
  type: string
  category: string
  content: string
  duration: string
  notes: string
}

const trainingPlans = ref<TrainingPlan[]>([
  {
    date: '2025年3月28日 周五',
    type: 'primary',
    category: '高血压专项',
    content: '舒缓型民族舞基础训练',
    duration: '30分钟 (含5分钟热身和放松)',
    notes: '训练前后测量血压，避免头部快速转动动作'
  },
  {
    date: '2025年3月30日 周天',
    type: 'success',
    category: '糖尿病专项',
    content: '中低强度健身舞',
    duration: '35分钟 (含5分钟热身和放松)',
    notes: '训练前后测量血糖，准备糖果预防低血糖'
  },
  {
    date: '2025年4月1日 周二',
    type: 'warning',
    category: '关节保健',
    content: '水中舞蹈基础训练',
    duration: '25分钟 (含5分钟热身和放松)',
    notes: '水温保持在28-30℃，避免剧烈动作'
  }
])

// 生成下周训练计划
const generateNextWeekPlan = (): void => {
  const today = new Date()
  const nextPlans: TrainingPlan[] = []

  // 创建原始计划的副本以避免直接修改
  const originalPlans = JSON.parse(JSON.stringify(trainingPlans.value))

  // 计算并更新日期
  let currentDate = new Date(today)
  originalPlans.forEach((plan: TrainingPlan, index: number) => {
    if (index > 0) {
      currentDate.setDate(currentDate.getDate() + 2) // 后续计划日期加2天
    }
    nextPlans.push({
      ...plan,
      date: formatDate(currentDate)
    })
  })

  trainingPlans.value = nextPlans
  ElMessage.success('下周训练计划已生成')
}

// 健康小贴士
interface HealthTip {
  id: number
  icon: string
  iconColor: string
  title: string
  type: string
  items: string[]
}

const healthTips = ref<HealthTip[]>([
  {
    id: 1,
    icon: 'Heart',
    iconColor: '#f56c6c',
    title: '心血管健康',
    type: 'danger',
    items: [
      '训练前后测量血压和心率',
      '避免突然剧烈运动',
      '保持均匀呼吸，不要憋气'
    ]
  },
  {
    id: 2,
    icon: 'Trophy',
    iconColor: '#409eff',
    title: '骨骼关节',
    type: 'primary',
    items: [
      '选择低冲击舞蹈动作',
      '避免过度扭转关节',
      '穿有良好支撑的运动鞋'
    ]
  },
  {
    id: 3,
    icon: 'Apple',
    iconColor: '#67c23a',
    title: '营养补充',
    type: 'success',
    items: [
      '训练前后适量补充水分',
      '可携带少量糖果预防低血糖',
      '训练后补充蛋白质'
    ]
  }
])

// 滚动到指定区域
const scrollToSection = (section: string): void => {
  activeTab.value = section
  // 滚动到标签页顶部比较合适
  const element = document.querySelector('.custom-tabs')
  if (element) {
    // 可以添加平滑滚动效果，但简单起见先直接跳转
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

<template>
  <div class="health-management">
    <PageHeader title="健康管理" subtitle="关注您的健康数据，科学安排舞蹈训练" />

    <!-- 健康卡片区域 -->
    <ElRow :gutter="20">
      <ElCol :xs="24" :sm="24" :md="8" :lg="8" v-for="card in healthCards" :key="card.id">
        <ElCard class="health-card">
          <div class="health-icon">
            <el-icon :size="40">
              <component :is="card.icon" />
            </el-icon>
          </div>
          <h3 class="health-title">{{ card.title }}</h3>
          <p>{{ card.description }}</p>
          <ElButton type="primary" link @click="scrollToSection(card.target)">
            {{ card.buttonText }}
          </ElButton>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 标签页区域 -->
    <div class="custom-tabs">
      <!-- 自定义标签页按钮 -->
      <div class="tabs-container">
        <button 
          v-for="tab in tabOptions" 
          :key="tab.name"
          :class="['tab-button', { active: activeTab === tab.name }]"
          @click="activeTab = tab.name"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- 运动处方 -->
      <div v-show="activeTab === 'prescription'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="24" :md="12">
            <ElCard>
              <template #header>
                <div class="card-header">
                  <span>您的运动处方</span>
                </div>
              </template>
              <p>根据您的健康评估结果，为您推荐以下舞蹈训练计划：</p>
              <ElDescriptions :column="1" border>
                <ElDescriptionsItem v-for="(item, index) in prescription" 
                  :key="index" 
                  :label="item.label">
                  {{ item.content }}
                </ElDescriptionsItem>
              </ElDescriptions>
              <ElButton type="primary" class="mt-3">生成新处方</ElButton>
            </ElCard>
          </ElCol>
          <ElCol :xs="24" :sm="24" :md="12">
            <ElCard>
              <template #header>
                <div class="card-header">
                  <span>运动建议</span>
                </div>
              </template>
              <ElAlert
                type="success"
                :closable="false"
                show-icon>
                您的当前运动量适中，继续保持！
              </ElAlert>
              <ElTimeline class="mt-3">
                <ElTimelineItem
                  v-for="(advice, index) in exerciseAdvice"
                  :key="index"
                  :type="advice.type">
                  {{ advice.content }}
                </ElTimelineItem>
              </ElTimeline>
            </ElCard>
          </ElCol>
        </ElRow>
      </div>

      <!-- 健康监测 -->
      <div v-show="activeTab === 'monitor'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="8" v-for="metric in healthMetrics" :key="metric.id">
            <ElCard class="text-center health-metric-card">
              <div class="data-value">{{ metric.value }}</div>
              <div class="data-label">{{ metric.label }}</div>
              <ElTag :type="metric.status.type" class="mt-2">
                {{ metric.status.text }}
              </ElTag>
            </ElCard>
          </ElCol>
        </ElRow>
        <ElCard class="mt-4">
          <template #header>
            <div class="card-header">
              <span>健康数据记录</span>
            </div>
          </template>
          <div class="button-group">
            <ElButton type="primary" @click="addHealthRecord">
              <el-icon><Plus /></el-icon>
              添加记录
            </ElButton>
            <ElButton @click="shareWithDoctor">
              <el-icon><Share /></el-icon>
              分享给医生
            </ElButton>
          </div>
          <!-- 健康记录表格 -->
          <ElTable :data="healthRecords" stripe class="mt-4 record-table">
            <ElTableColumn prop="time" label="时间" width="180" class-name="first-column" />
            <ElTableColumn prop="bp" label="血压 (mmHg)" />
            <ElTableColumn prop="hr" label="心率 (次/分)" />
            <ElTableColumn prop="bs" label="血糖 (mmol/L)" />
            <ElTableColumn prop="activityState" label="活动状态" />
            <ElTableColumn prop="dietState" label="饮食状态" />
          </ElTable>
        </ElCard>
      </div>

      <!-- 慢性病训练 -->
      <div v-show="activeTab === 'chronic'" class="tab-content">
        <ElAlert
          type="info"
          show-icon
          :closable="false"
          class="mb-4">
          以下是为您量身定制的慢性病专项训练方案，请根据身体状况调整训练强度。
        </ElAlert>

        <div v-for="plan in trainingPlans" :key="plan.date" class="mb-4">
          <ElCard>
            <div class="d-flex justify-content-between align-items-center plan-header">
              <div class="plan-date">{{ plan.date }}</div>
              <ElTag :type="plan.type">{{ plan.category }}</ElTag>
            </div>
            <ElDescriptions class="mt-3" :column="1" border>
              <ElDescriptionsItem label="训练内容">
                {{ plan.content }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="训练时长">
                {{ plan.duration }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="注意事项">
                {{ plan.notes }}
              </ElDescriptionsItem>
            </ElDescriptions>
          </ElCard>
        </div>

        <div class="text-center mt-4">
          <ElButton type="primary" size="large" @click="generateNextWeekPlan">
            生成下周训练计划
          </ElButton>
        </div>
      </div>
    </div>

    <!-- 健康小贴士 -->
    <div class="health-tips mt-5">
      <h2 class="section-title">健康小贴士</h2>
      <p class="section-subtitle">老年人舞蹈训练注意事项</p>
      
      <ElRow :gutter="20">
        <ElCol :xs="24" :sm="24" :md="8" v-for="tip in healthTips" :key="tip.id">
          <ElCard class="health-tip-card">
            <template #header>
              <div class="d-flex align-items-center">
                <el-icon :size="24" :color="tip.iconColor">
                  <component :is="tip.icon" />
                </el-icon>
                <span class="ms-2">{{ tip.title }}</span>
              </div>
            </template>
            <ElTimeline>
              <ElTimelineItem
                v-for="(item, index) in tip.items"
                :key="index"
                :type="tip.type">
                {{ item }}
              </ElTimelineItem>
            </ElTimeline>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<style scoped>
.health-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 60px;
}

.health-card {
  height: 100%;
  text-align: center;
  padding: 25px;
  margin-bottom: 20px;
}

.health-icon {
  color: var(--el-color-primary);
  margin-bottom: 20px;
}

.health-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
  color: var(--el-color-primary);
}

.data-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--el-color-primary);
}

.data-label {
  font-size: 1rem;
  color: #666;
  margin: 10px 0;
}

.health-metric-card {
  text-align: center;
  padding: 20px;
  margin-bottom: 20px;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plan-date {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--el-color-primary);
}

.button-group {
  display: flex;
  gap: 10px;
}

.health-tip-card {
  height: 100%;
}

.text-center {
  text-align: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: var(--el-color-primary);
  margin-bottom: 30px;
  text-align: center;
}

.section-subtitle {
  text-align: center;
  margin-bottom: 40px;
  color: #666;
}

/* 自定义标签页样式 */
.custom-tabs {
  margin: 40px 0;
}

.tabs-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.tab-button {
  padding: 12px 24px;
  background-color: #fff;
  color: var(--el-text-color-primary);
  border: none;
  border-radius: 50px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  min-width: 120px;
  text-align: center;
}

.tab-button.active {
  background-color: var(--el-color-primary);
  color: #fff;
}

.tab-content {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 自定义工具类 */
.d-flex {
  display: flex;
}

.justify-content-between {
  justify-content: space-between;
}

.align-items-center {
  align-items: center;
}

.mt-2 {
  margin-top: 0.5rem;
}

.mt-3 {
  margin-top: 1rem;
}

.mt-4 {
  margin-top: 1.5rem;
}

.mt-5 {
  margin-top: 3rem;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.ms-2 {
  margin-left: 0.5rem;
}

/* 健康记录表格样式 */
.record-table :deep(.el-table__header-wrapper th) {
  background-color: var(--el-color-primary-light-8);
  color: var(--el-color-primary);
  font-weight: bold;
}

.record-table :deep(td.first-column) {
  background-color: var(--el-color-primary-light-9);
  font-weight: bold;
  color: var(--el-text-color-primary);
}

@media (max-width: 768px) {
  .health-title {
    font-size: 1.2rem;
  }
  
  .data-value {
    font-size: 2rem;
  }
  
  .button-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .button-group .el-button {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .health-icon {
    margin-bottom: 15px;
  }
  
  .plan-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .health-tips .el-timeline {
    padding-left: 10px;
  }
  
  .tab-button {
    flex: 1;
    padding: 10px 15px;
    min-width: 100px;
    font-size: 16px;
  }
}
</style>