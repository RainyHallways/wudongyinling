<template>
  <div class="post-management">
    <PageHeader title="动态管理" subtitle="管理用户发布的动态内容" />
    
    <!-- 筛选工具栏 -->
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-select v-model="filters.postType" placeholder="选择动态类型" clearable>
            <el-option label="全部" value="" />
            <el-option label="文字动态" value="text" />
            <el-option label="图片动态" value="image" />
            <el-option label="视频动态" value="video" />
            <el-option label="舞蹈分享" value="dance" />
            <el-option label="非遗传承" value="heritage" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filters.userRole" placeholder="选择用户角色" clearable>
            <el-option label="全部" value="" />
            <el-option label="老年人" value="elderly" />
            <el-option label="子女" value="child" />
            <el-option label="志愿者" value="volunteer" />
            <el-option label="教师" value="teacher" />
            <el-option label="医生" value="doctor" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="filters.dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="searchPosts">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 动态列表 -->
    <el-card>
      <el-table :data="posts" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="用户信息" width="150">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :src="row.user.avatar" :size="40">
                {{ row.user.nickname?.[0] || row.user.username[0] }}
              </el-avatar>
              <div class="user-details">
                <div class="username">{{ row.user.nickname || row.user.username }}</div>
                <el-tag :type="getRoleTagType(row.user.role)" size="small">
                  {{ getRoleText(row.user.role) }}
                </el-tag>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="动态内容" min-width="300">
          <template #default="{ row }">
            <div class="post-content">
              <div v-if="row.title" class="post-title">{{ row.title }}</div>
              <div class="post-text">{{ row.content }}</div>
              <div v-if="row.media_url" class="post-media">
                <img v-if="row.post_type === 'image'" :src="row.media_url" class="media-preview" />
                <video v-else-if="row.post_type === 'video'" :src="row.media_url" class="media-preview" controls />
              </div>
              <el-tag :type="getPostTypeTagType(row.post_type)" size="small">
                {{ getPostTypeText(row.post_type) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="互动数据" width="120">
          <template #default="{ row }">
            <div class="interaction-stats">
              <div><el-icon><Star /></el-icon> {{ row.likes_count }}</div>
              <div><el-icon><ChatDotSquare /></el-icon> {{ row.comments_count }}</div>
              <div><el-icon><Share /></el-icon> {{ row.shares_count }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_public ? 'success' : 'warning'">
              {{ row.is_public ? '公开' : '私密' }}
            </el-tag>
            <el-tag v-if="row.is_featured" type="danger" size="small">精选</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="viewPost(row)">查看</el-button>
              <el-button 
                size="small" 
                :type="row.is_featured ? 'warning' : 'success'"
                @click="toggleFeatured(row)"
              >
                {{ row.is_featured ? '取消精选' : '设为精选' }}
              </el-button>
              <el-button 
                size="small" 
                :type="row.is_public ? 'warning' : 'primary'"
                @click="toggleVisibility(row)"
              >
                {{ row.is_public ? '设为私密' : '设为公开' }}
              </el-button>
              <el-button size="small" type="danger" @click="deletePost(row)">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 查看动态详情弹窗 -->
    <el-dialog v-model="showPostDetail" title="动态详情" width="800px">
      <div v-if="currentPost" class="post-detail">
        <div class="post-header">
          <el-avatar :src="currentPost.user.avatar" :size="50">
            {{ currentPost.user.nickname?.[0] || currentPost.user.username[0] }}
          </el-avatar>
          <div class="post-info">
            <div class="user-name">{{ currentPost.user.nickname || currentPost.user.username }}</div>
            <div class="post-time">{{ currentPost.created_at }}</div>
          </div>
        </div>
        <div class="post-body">
          <h3 v-if="currentPost.title">{{ currentPost.title }}</h3>
          <p>{{ currentPost.content }}</p>
          <div v-if="currentPost.media_url" class="post-media">
            <img v-if="currentPost.post_type === 'image'" :src="currentPost.media_url" />
            <video v-else-if="currentPost.post_type === 'video'" :src="currentPost.media_url" controls />
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Star, ChatDotSquare, Share } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'

interface Post {
  id: number
  user: {
    id: number
    username: string
    nickname?: string
    avatar?: string
    role: string
  }
  title?: string
  content: string
  post_type: string
  media_url?: string
  thumbnail_url?: string
  likes_count: number
  comments_count: number
  shares_count: number
  is_public: boolean
  is_featured: boolean
  created_at: string
  updated_at: string
}

const loading = ref(false)
const posts = ref<Post[]>([])
const showPostDetail = ref(false)
const currentPost = ref<Post | null>(null)

const filters = reactive({
  postType: '',
  userRole: '',
  dateRange: null as any
})

const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

const getRoleText = (role: string) => {
  const roleMap: Record<string, string> = {
    elderly: '老年人',
    child: '子女',
    volunteer: '志愿者', 
    teacher: '教师',
    doctor: '医生',
    admin: '管理员'
  }
  return roleMap[role] || role
}

const getRoleTagType = (role: string) => {
  const typeMap: Record<string, string> = {
    elderly: 'success',
    child: 'primary',
    volunteer: 'warning',
    teacher: 'info',
    doctor: 'danger',
    admin: 'danger'
  }
  return typeMap[role] || ''
}

const getPostTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    text: '文字',
    image: '图片',
    video: '视频',
    dance: '舞蹈',
    heritage: '非遗'
  }
  return typeMap[type] || type
}

const getPostTypeTagType = (type: string) => {
  const typeMap: Record<string, string> = {
    text: '',
    image: 'success',
    video: 'primary',
    dance: 'warning',
    heritage: 'danger'
  }
  return typeMap[type] || ''
}

const loadPosts = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/v1/social/posts?${new URLSearchParams({
      skip: ((pagination.page - 1) * pagination.size).toString(),
      limit: pagination.size.toString(),
      ...(filters.postType && { post_type: filters.postType }),
      ...(filters.userRole && { user_role: filters.userRole }),
      ...(filters.dateRange && filters.dateRange[0] && { start_date: filters.dateRange[0] }),
      ...(filters.dateRange && filters.dateRange[1] && { end_date: filters.dateRange[1] })
    })}`)
    
    if (!response.ok) {
      throw new Error('获取动态列表失败')
    }
    
    const data = await response.json()
    posts.value = data.data || []
    pagination.total = data.total || 0
  } catch (error) {
    ElMessage.error('加载动态列表失败')
    // 回退到模拟数据
    posts.value = [
      {
        id: 1,
        user: {
          id: 1,
          username: 'zhangsan',
          nickname: '张大爷',
          avatar: '',
          role: 'elderly'
        },
        title: '今日练功',
        content: '今天学了一段新的舞蹈，感觉身体轻松了很多！',
        post_type: 'text',
        likes_count: 15,
        comments_count: 8,
        shares_count: 3,
        is_public: true,
        is_featured: false,
        created_at: '2024-01-20 09:30:00',
        updated_at: '2024-01-20 09:30:00'
      }
    ]
    pagination.total = 1
  } finally {
    loading.value = false
  }
}

const searchPosts = () => {
  pagination.page = 1
  loadPosts()
}

const resetFilters = () => {
  filters.postType = ''
  filters.userRole = ''
  filters.dateRange = null
  searchPosts()
}

const viewPost = (post: Post) => {
  currentPost.value = post
  showPostDetail.value = true
}

const toggleFeatured = async (post: Post) => {
  try {
    const response = await fetch(`/api/v1/social/posts/${post.id}/featured`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error('操作失败')
    }
    
    const data = await response.json()
    post.is_featured = data.data.is_featured
    ElMessage.success(post.is_featured ? '已设为精选' : '已取消精选')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const toggleVisibility = async (post: Post) => {
  try {
    const response = await fetch(`/api/v1/social/posts/${post.id}/visibility`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error('操作失败')
    }
    
    const data = await response.json()
    post.is_public = data.data.is_public
    ElMessage.success(post.is_public ? '已设为公开' : '已设为私密')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deletePost = async (post: Post) => {
  try {
    await ElMessageBox.confirm('确定要删除这条动态吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await fetch(`/api/v1/social/posts/${post.id}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) {
      throw new Error('删除失败')
    }
    
    ElMessage.success('删除成功')
    loadPosts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  loadPosts()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadPosts()
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.post-management {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.username {
  font-weight: 500;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.el-avatar {
  flex-shrink: 0;
}

.post-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.post-title {
  font-weight: 500;
  color: #333;
}

.post-text {
  color: #666;
  line-height: 1.4;
}

.media-preview {
  max-width: 100px;
  max-height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.interaction-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #666;
}

.interaction-stats > div {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.post-detail {
  padding: 20px;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.post-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name {
  font-weight: 500;
  font-size: 16px;
}

.post-time {
  color: #999;
  font-size: 12px;
}

.post-body h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.post-body p {
  margin: 0 0 15px 0;
  line-height: 1.6;
  color: #666;
}

.post-media img,
.post-media video {
  max-width: 100%;
  border-radius: 8px;
}
</style> 