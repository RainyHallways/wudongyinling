<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  StarFilled, 
  ChatDotRound, 
  Share, 
  Promotion, 
  Sunrise, 
  Star, 
  Trophy, 
  Clock,
  Plus,
  Like,
  MessageBox,
  Loading
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageHeader from '@/components/common/PageHeader.vue'
import { postApi, heritageProjectApi, heritageInheritorApi, type Post, type HeritageProject, type HeritageInheritor } from '@/api/social'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 当前激活的标签页
const activeTab = ref('feed')

// 标签选项
interface TabOption {
  name: string
  label: string
}

const tabOptions: TabOption[] = [
  { name: 'feed', label: '动态广场' },
  { name: 'challenge', label: '打卡挑战' },
  { name: 'heritage', label: '非遗传承' },
  { name: 'message', label: '私信聊天' }
]

// 动态广场数据
const posts = ref<Post[]>([])
const postsLoading = ref(false)
const postsPagination = ref({
  page: 1,
  page_size: 10,
  total: 0
})

// 发布动态数据
const newPost = ref({
  content: '',
  post_type: 'text' as 'text' | 'image' | 'video' | 'dance' | 'heritage',
  media_url: '',
  is_public: true
})
const showCreatePost = ref(false)
const publishLoading = ref(false)
const showFilters = ref(false)

// 非遗传承数据
const heritageProjects = ref<HeritageProject[]>([])
const heritageInheritors = ref<HeritageInheritor[]>([])
const heritageLoading = ref(false)

// 挑战数据
const challenges = ref([
  {
    id: 1,
    title: '30天广场舞打卡挑战',
    description: '连续30天打卡广场舞练习',
    participants: 156,
    days: 30,
    currentDay: 15,
    status: 'ongoing'
  },
  {
    id: 2,
    title: '太极拳基础动作',
    description: '学习太极拳24式基础动作',
    participants: 89,
    days: 21,
    currentDay: 8,
    status: 'ongoing'
  }
])

// 过滤选项
const feedFilters = ref({
  post_type: '',
  user_role: '',
  is_featured: undefined as boolean | undefined
})

// 计算属性
const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    if (feedFilters.value.post_type && post.post_type !== feedFilters.value.post_type) {
      return false
    }
    if (feedFilters.value.is_featured !== undefined && post.is_featured !== feedFilters.value.is_featured) {
      return false
    }
    return true
  })
})

// 生命周期
onMounted(() => {
  loadFeedData()
  loadHeritageData()
})

// 加载动态数据
const loadFeedData = async () => {
  try {
    postsLoading.value = true
    const response = await postApi.getPosts({
      page: postsPagination.value.page,
      page_size: postsPagination.value.page_size,
      ...feedFilters.value
    })
    
    if (response.code === 200) {
      posts.value = response.data.items || []
      postsPagination.value.total = response.data.total || 0
    }
  } catch (error) {
    console.error('Failed to load posts:', error)
    ElMessage.error('加载动态失败')
  } finally {
    postsLoading.value = false
  }
}

// 加载非遗数据
const loadHeritageData = async () => {
  try {
    heritageLoading.value = true
    
    const [projectsResponse, inheritorsResponse] = await Promise.all([
      heritageProjectApi.getProjects({ page: 1, page_size: 6 }),
      heritageInheritorApi.getInheritors({ page: 1, page_size: 6 })
    ])
    
    if (projectsResponse.code === 200) {
      heritageProjects.value = projectsResponse.data.items || []
    }
    
    if (inheritorsResponse.code === 200) {
      heritageInheritors.value = inheritorsResponse.data.items || []
    }
  } catch (error) {
    console.error('Failed to load heritage data:', error)
    ElMessage.error('加载非遗数据失败')
  } finally {
    heritageLoading.value = false
  }
}

// 发布动态
const publishPost = async () => {
  if (!newPost.value.content.trim()) {
    ElMessage.warning('请输入动态内容')
    return
  }

  try {
    publishLoading.value = true
    const response = await postApi.createPost({
      content: newPost.value.content.trim(),
      post_type: newPost.value.post_type,
      media_url: newPost.value.media_url || undefined,
      is_public: newPost.value.is_public
    })

    if (response.code === 200) {
      ElMessage.success('发布成功')
      showCreatePost.value = false
      newPost.value = {
        content: '',
        post_type: 'text',
        media_url: '',
        is_public: true
      }
      loadFeedData() // 重新加载动态列表
    } else {
      ElMessage.error(response.message || '发布失败')
    }
  } catch (error) {
    console.error('Failed to publish post:', error)
    ElMessage.error('发布失败')
  } finally {
    publishLoading.value = false
  }
}

// 点赞动态
const likePost = async (post: Post) => {
  try {
    const response = await postApi.likePost(post.id)
    if (response.code === 200) {
      // 更新本地数据
      const index = posts.value.findIndex(p => p.id === post.id)
      if (index !== -1) {
        posts.value[index].likes_count++
      }
    }
  } catch (error) {
    console.error('Failed to like post:', error)
    ElMessage.error('点赞失败')
  }
}

// 评论动态
const commentPost = async (post: Post) => {
  try {
    const { value: comment } = await ElMessageBox.prompt('请输入评论内容', '添加评论', {
      confirmButtonText: '发送',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputPlaceholder: '说点什么...'
    })

    if (comment && comment.trim()) {
      const response = await postApi.addComment(post.id, {
        content: comment.trim()
      })

      if (response.code === 200) {
        ElMessage.success('评论成功')
        // 更新本地数据
        const index = posts.value.findIndex(p => p.id === post.id)
        if (index !== -1) {
          posts.value[index].comments_count++
        }
      } else {
        ElMessage.error(response.message || '评论失败')
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to comment post:', error)
      ElMessage.error('评论失败')
    }
  }
}

// 分享动态
const sharePost = async (post: Post) => {
  try {
    // 创建分享链接
    const shareUrl = `${window.location.origin}/social/post/${post.id}`
    
    // 尝试使用 Web Share API
    if (navigator.share) {
      await navigator.share({
        title: '分享动态',
        text: post.content,
        url: shareUrl
      })
      ElMessage.success('分享成功')
    } else {
      // 如果不支持，则复制链接到剪贴板
      await navigator.clipboard.writeText(shareUrl)
      ElMessage.success('链接已复制到剪贴板')
    }
    
    // 更新分享计数（这里应该调用真实的API）
    const index = posts.value.findIndex(p => p.id === post.id)
    if (index !== -1) {
      posts.value[index].shares_count++
    }
  } catch (error) {
    console.error('Failed to share post:', error)
    ElMessage.error('分享失败')
  }
}

// 跳转到聊天页面
const goToChat = () => {
  router.push('/chat')
}

// 跳转到挑战详情
const goToChallengeDetail = (challengeId: number) => {
  router.push(`/challenge/${challengeId}`)
}

// 应用过滤器
const applyFilters = () => {
  postsPagination.value.page = 1
  loadFeedData()
}

// 重置过滤器
const resetFilters = () => {
  feedFilters.value = {
    post_type: '',
    user_role: '',
    is_featured: undefined
  }
  applyFilters()
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

// 默认头像
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
</script>

<template>
  <div class="social-platform">
    <PageHeader title="社交激励" subtitle="与舞友互动交流，共同进步" />
    
    <!-- 标签页 - 改用自定义样式取代el-tabs -->
    <div class="custom-tabs">
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
      
      <!-- 动态广场内容 -->
      <div v-show="activeTab === 'feed'" class="tab-content">
        <div class="social-cards">
          <ElCard v-for="post in posts" :key="post.id" class="social-card">
            <div class="d-flex">
              <ElAvatar :src="post.avatar || defaultAvatar" :size="50" class="me-3" />
              <div>
                <h5 class="mb-0">{{ post.username }}</h5>
                <p class="text-muted mb-0">{{ formatTime(post.created_at) }} · {{ post.location }}</p>
              </div>
            </div>
            <div class="post-content">
              <p>{{ post.content }}</p>
              <ElImage v-if="post.media_url" :src="post.media_url" class="post-image" fit="cover" />
            </div>
            <div class="post-actions">
              <ElButton text @click="likePost(post)">
                <el-icon><Like /></el-icon>
                点赞 ({{ post.likes_count }})
              </ElButton>
              <ElButton text @click="commentPost(post)">
                <el-icon><ChatDotRound /></el-icon>
                评论 ({{ post.comments_count }})
              </ElButton>
              <ElButton text @click="sharePost(post)">
                <el-icon><Share /></el-icon>
                分享
              </ElButton>
            </div>
          </ElCard>
          <div class="text-center mt-4">
            <ElButton type="primary" plain @click="showCreatePost = true">发布动态</ElButton>
          </div>
        </div>
        <ElPagination
          v-if="posts.length > 0"
          v-model:current-page="postsPagination.page"
          v-model:page-size="postsPagination.page_size"
          :total="postsPagination.total"
          @current-change="loadFeedData"
          @size-change="loadFeedData"
          class="mt-4"
        />
      </div>

      <!-- 打卡挑战内容 -->
      <div v-show="activeTab === 'challenge'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="12" :lg="12" v-for="challenge in challenges" :key="challenge.id">
            <ElCard class="challenge-card">
              <ElTag :type="challenge.status === 'ongoing' ? 'primary' : 'info'" class="challenge-badge">
                {{ challenge.status === 'ongoing' ? '进行中' : '已完成' }}
              </ElTag>
              <h3>{{ challenge.title }}</h3>
              <p>{{ challenge.description }}</p>
              <div class="d-flex justify-content-between">
                <span>已参与: {{ challenge.participants }}人</span>
                <span>已打卡: {{ challenge.currentDay }}/{{ challenge.days }}天</span>
              </div>
              <ElProgress 
                :percentage="challenge.currentDay / challenge.days * 100" 
                :status="challenge.currentDay / challenge.days * 100 === 100 ? 'success' : undefined"
              />
              <ElButton type="primary" class="w-100 mt-3" @click="goToChallengeDetail(challenge.id)">
                查看详情
              </ElButton>
            </ElCard>
          </ElCol>
        </ElRow>
      </div>

      <!-- 非遗传承内容 -->
      <div v-show="activeTab === 'heritage'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="8" :lg="8" v-for="project in heritageProjects" :key="project.id">
            <div class="heritage-card">
              <ElImage :src="project.image_url" fit="cover" class="heritage-image" />
              <div class="heritage-overlay">
                <h4>{{ project.title }}</h4>
                <p>{{ project.description }}</p>
              </div>
            </div>
          </ElCol>
        </ElRow>

        <ElCard class="mt-4">
          <h3>非遗舞蹈学习社区</h3>
          <p>加入我们的非遗舞蹈学习小组，与传承人互动交流，学习传统舞蹈文化。</p>
          <ElRow :gutter="20" class="mt-4">
            <ElCol :xs="24" :sm="24" :md="12" v-for="inheritor in heritageInheritors" :key="inheritor.id">
              <div class="d-flex align-items-center mb-3">
                <ElAvatar :src="inheritor.avatar_url" :size="60" class="me-3" />
                <div>
                  <h5 class="mb-0">{{ inheritor.name }}</h5>
                  <p class="text-muted mb-0">{{ inheritor.title }}</p>
                </div>
              </div>
              <p>{{ inheritor.description }}</p>
              <ElButton type="primary">加入学习小组</ElButton>
            </ElCol>
          </ElRow>
        </ElCard>
      </div>

      <!-- 私信聊天 -->
      <div v-show="activeTab === 'message'" class="tab-content">
        <div class="text-center py-5">
          <el-icon size="64" color="#409eff"><ChatDotRound /></el-icon>
          <h3 class="mt-3">开始聊天</h3>
          <p class="text-muted mb-4">与舞友们实时交流，分享学习心得</p>
          <el-button type="primary" size="large" @click="goToChat">
            <el-icon><MessageBox /></el-icon>
            进入聊天室
          </el-button>
        </div>
      </div>
    </div>

    <!-- 发布动态对话框 -->
    <el-dialog
      v-model="showCreatePost"
      title="发布动态"
      width="500px"
      :before-close="() => showCreatePost = false"
    >
      <el-form :model="newPost" label-width="80px">
        <el-form-item label="动态类型">
          <el-select v-model="newPost.post_type" placeholder="选择类型">
            <el-option label="文字" value="text" />
            <el-option label="图片" value="image" />
            <el-option label="视频" value="video" />
            <el-option label="舞蹈" value="dance" />
            <el-option label="非遗" value="heritage" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="内容">
          <el-input
            v-model="newPost.content"
            type="textarea"
            :rows="4"
            placeholder="分享你的想法..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="媒体链接" v-if="newPost.post_type !== 'text'">
          <el-input
            v-model="newPost.media_url"
            placeholder="请输入图片或视频链接"
          />
        </el-form-item>
        
        <el-form-item label="可见性">
          <el-switch
            v-model="newPost.is_public"
            active-text="公开"
            inactive-text="私密"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreatePost = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="publishPost"
            :loading="publishLoading"
          >
            发布
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 筛选器对话框 -->
    <el-dialog
      v-model="showFilters"
      title="筛选动态"
      width="400px"
    >
      <el-form :model="feedFilters" label-width="80px">
        <el-form-item label="动态类型">
          <el-select v-model="feedFilters.post_type" placeholder="全部类型" clearable>
            <el-option label="文字" value="text" />
            <el-option label="图片" value="image" />
            <el-option label="视频" value="video" />
            <el-option label="舞蹈" value="dance" />
            <el-option label="非遗" value="heritage" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="用户角色">
          <el-select v-model="feedFilters.user_role" placeholder="全部角色" clearable>
            <el-option label="老人" value="ELDERLY" />
            <el-option label="儿童" value="CHILD" />
            <el-option label="志愿者" value="VOLUNTEER" />
            <el-option label="教师" value="TEACHER" />
            <el-option label="医生" value="DOCTOR" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="精选内容">
          <el-select v-model="feedFilters.is_featured" placeholder="全部内容" clearable>
            <el-option label="精选内容" :value="true" />
            <el-option label="普通内容" :value="false" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetFilters">重置</el-button>
          <el-button type="primary" @click="applyFilters(); showFilters = false">
            应用筛选
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.social-platform {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 60px;
}

/* 自定义标签页样式，模仿HTML版本 */
.custom-tabs {
  margin-bottom: 40px;
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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

.social-card {
  margin-bottom: 20px;
}

.post-content {
  margin: 15px 0;
}

.post-image {
  width: 100%;
  max-height: 400px;
  border-radius: 10px;
  margin-bottom: 10px;
}

.post-actions {
  border-top: 1px solid var(--el-border-color-lighter);
  padding-top: 15px;
  display: flex;
  justify-content: flex-start;
  gap: 15px;
}

.challenge-card {
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}

.challenge-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  border-radius: 20px;
  padding: 5px 10px;
}

.heritage-card {
  position: relative;
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 20px;
  height: 250px;
}

.heritage-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.heritage-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  padding: 15px;
  color: white;
}

.message-list {
  max-height: 500px;
  overflow-y: auto;
  margin-bottom: 15px;
}

.message-item {
  padding: 10px 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  max-width: 80%;
}

.message-sender {
  background-color: #e3f2fd;
  margin-left: auto;
}

.message-receiver {
  background-color: var(--el-fill-color-light);
  margin-right: auto;
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

.mb-0 {
  margin-bottom: 0 !important;
}

.mb-3 {
  margin-bottom: 1rem !important;
}

.me-3 {
  margin-right: 1rem !important;
}

.mt-3 {
  margin-top: 1rem !important;
}

.mt-4 {
  margin-top: 1.5rem !important;
}

.w-100 {
  width: 100% !important;
}

.text-center {
  text-align: center;
}

.text-muted {
  color: var(--el-text-color-secondary);
}

.text-danger {
  color: var(--el-color-danger);
}

.text-warning {
  color: var(--el-color-warning);
}

.text-info {
  color: var(--el-color-info);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 768px) {
  .post-image {
    max-height: 300px;
  }
  
  .heritage-card {
    height: 200px;
  }
  
  .tab-button {
    flex: 1;
    padding: 10px 15px;
    min-width: 100px;
  }
}

/* 调整聊天列表项的内边距和垂直对齐 */
.el-menu-item {
  padding-top: 0 !important; /* 移除内边距，让 flex 对齐控制 */
  padding-bottom: 0 !important;
  display: flex !important; /* 确保 el-menu-item 是 flex 容器 */
  align-items: center !important; /* 垂直居中其直接子元素 (.d-flex) */
}

/* 确保内部的 d-flex 容器也垂直居中 */
.el-menu-item .d-flex {
  width: 100%; /* 确保占据可用宽度 */
  align-items: center !important; /* 垂直居中头像和文本块 */
}

/* 移除包裹 h6 和 small 的 div 的额外间距 */
.el-menu-item .d-flex > div:last-child {
  padding: 0 !important;
  margin: 0 !important;
}

/* 移除聊天列表 h6 的所有间距和减小行高 */
.el-menu-item .d-flex > div:last-child h6 {
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.2; /* 减小行高 */
  display: block;
}

/* 移除聊天列表 small 的所有间距和减小行高 */
.el-menu-item .d-flex > div:last-child small {
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.2; /* 减小行高 */
  display: block;
}
</style>