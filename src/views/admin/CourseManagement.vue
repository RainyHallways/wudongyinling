<template>
  <div class="course-container admin-responsive">
    <!-- 搜索和筛选栏 -->
    <div class="search-filter-bar">
      <div class="search-filter-item search-input">
        <el-input 
          v-model="searchKeyword" 
          placeholder="搜索课程名称、描述、教练"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="search-filter-item">
        <el-select v-model="difficultyFilter" placeholder="难度筛选" clearable @change="handleSearch">
          <el-option label="全部" value="" />
          <el-option label="初级" value="beginner" />
          <el-option label="中级" value="intermediate" />
          <el-option label="高级" value="advanced" />
        </el-select>
      </div>
      <div class="search-filter-actions">
        <el-button type="primary" @click="handleSearch" class="touch-friendly">搜索</el-button>
        <el-button @click="handleReset" class="touch-friendly">重置</el-button>
        <el-button type="success" @click="handleAdd" class="touch-friendly desktop-only">添加课程</el-button>
      </div>
    </div>

    <!-- 浮动添加按钮（移动端） -->
    <div class="floating-action-button mobile-only">
      <el-button type="success" circle size="large" @click="handleAdd">
        <el-icon><Plus /></el-icon>
      </el-button>
    </div>

    <!-- 桌面端表格 -->
    <el-card class="desktop-table">
      <div class="table-container">
        <el-table v-loading="loading" :data="courses" border style="width: 100%">
          <el-table-column prop="title" label="课程名称" min-width="150" show-overflow-tooltip />
          <el-table-column prop="description" label="课程描述" min-width="200" show-overflow-tooltip />
          <el-table-column prop="difficulty" label="难度等级" width="100">
            <template #default="{ row }">
              <el-tag :type="getDifficultyType(row.difficulty)">
                {{ getDifficultyText(row.difficulty) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="duration" label="时长" width="100">
            <template #default="{ row }">
              {{ row.duration }}分钟
            </template>
          </el-table-column>
          <el-table-column label="封面图片" width="120">
            <template #default="{ row }">
              <el-image
                v-if="row.cover_url"
                :src="row.cover_url"
                :preview-src-list="[row.cover_url]"
                fit="cover"
                style="width: 50px; height: 50px; border-radius: 4px;"
              />
              <span v-else class="text-gray">暂无封面</span>
            </template>
          </el-table-column>
          <el-table-column label="课程视频" width="120">
            <template #default="{ row }">
              <el-button v-if="row.video_url" type="primary" link @click="handlePreviewVideo(row)">
                预览视频
              </el-button>
              <span v-else class="text-gray">暂无视频</span>
            </template>
          </el-table-column>
          <el-table-column prop="instructor" label="教练" width="100" show-overflow-tooltip />
          <el-table-column label="操作" width="160" fixed="right">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 移动端卡片列表 -->
    <div class="mobile-table-cards">
      <div v-for="course in courses" :key="course.id" class="mobile-card-item" v-loading="loading">
        <div class="mobile-card-header">
          <div class="mobile-card-title">
            <el-image
              v-if="course.cover_url"
              :src="course.cover_url"
              fit="cover"
              style="width: 40px; height: 40px; border-radius: 4px; margin-right: 12px;"
            />
            <div class="course-title-info">
              <span class="course-name">{{ course.title }}</span>
              <el-tag :type="getDifficultyType(course.difficulty)" size="small">
                {{ getDifficultyText(course.difficulty) }}
              </el-tag>
            </div>
          </div>
          <div class="mobile-card-status">
            <span class="duration">{{ course.duration }}分钟</span>
          </div>
        </div>
        
        <div class="mobile-card-content">
          <div class="mobile-card-field" v-if="course.description">
            <span class="mobile-card-label">课程描述：</span>
            <span class="mobile-card-value mobile-wrap">{{ course.description }}</span>
          </div>
          <div class="mobile-card-field" v-if="course.instructor">
            <span class="mobile-card-label">教练：</span>
            <span class="mobile-card-value">{{ course.instructor }}</span>
          </div>
          <div class="mobile-card-field">
            <span class="mobile-card-label">视频资源：</span>
            <span class="mobile-card-value">
              <el-button v-if="course.video_url" type="primary" size="small" @click="handlePreviewVideo(course)">
                预览视频
              </el-button>
              <span v-else class="text-gray">暂无视频</span>
            </span>
          </div>
        </div>
        
        <div class="mobile-card-actions">
          <el-button type="primary" size="small" @click="handleEdit(course)" class="touch-friendly">
            <el-icon><Edit /></el-icon> 编辑
          </el-button>
          <el-button type="danger" size="small" @click="handleDelete(course.id)" class="touch-friendly">
            <el-icon><Delete /></el-icon> 删除
          </el-button>
        </div>
      </div>
    </div>

    <!-- 添加/编辑课程对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      :width="dialogWidth"
      class="dialog-responsive"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="form-responsive"
      >
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="课程描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入课程描述"
          />
        </el-form-item>
        <el-form-item label="难度等级" prop="difficulty">
          <el-select v-model="form.difficulty" placeholder="请选择难度等级" style="width: 100%">
            <el-option label="初级" value="beginner" />
            <el-option label="中级" value="intermediate" />
            <el-option label="高级" value="advanced" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程时长" prop="duration">
          <div style="display: flex; align-items: center; gap: 8px;">
            <el-input-number v-model="form.duration" :min="1" :max="360" placeholder="课程时长" />
            <span class="unit">分钟</span>
          </div>
        </el-form-item>
        <el-form-item label="教练" prop="instructor">
          <el-input v-model="form.instructor" placeholder="请输入教练姓名" />
        </el-form-item>
        <el-form-item label="封面图片" prop="cover_url">
          <div class="file-input-container">
            <el-input 
              v-model="form.cover_url" 
              placeholder="请输入封面图片URL或选择文件上传"
              clearable
              class="file-input"
            />
            <el-upload
              class="file-upload-btn"
              action="/api/upload/image"
              :headers="uploadHeaders"
              :show-file-list="false"
              :on-success="handleCoverSuccess"
              :on-error="handleUploadError"
              accept="image/*"
            >
              <el-button type="default" class="upload-trigger">
                <el-icon><FolderOpened /></el-icon>
                浏览文件
              </el-button>
            </el-upload>
          </div>
          <div v-if="form.cover_url" class="image-preview">
            <el-image
              :src="form.cover_url"
              fit="cover"
              style="width: 100px; height: 100px; border-radius: 4px;"
              :preview-src-list="[form.cover_url]"
            />
          </div>
        </el-form-item>
        <el-form-item label="课程视频" prop="video_url">
          <div class="file-input-container">
            <el-input 
              v-model="form.video_url" 
              placeholder="请输入视频URL或选择文件上传"
              clearable
              class="file-input"
            />
            <el-upload
              class="file-upload-btn"
              :action="uploadUrl"
              :headers="uploadHeaders"
              :show-file-list="false"
              :on-success="handleVideoSuccess"
              :on-error="handleUploadError"
              :before-upload="beforeVideoUpload"
              accept="video/*"
            >
              <el-button type="default" class="upload-trigger">
                <el-icon><FolderOpened /></el-icon>
                浏览文件
              </el-button>
            </el-upload>
          </div>
          <div v-if="form.video_url" class="video-preview">
            <video :src="form.video_url" controls style="width: 200px; max-width: 100%; border-radius: 4px;"></video>
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false" class="touch-friendly">取消</el-button>
          <el-button type="primary" @click="handleSubmit(formRef)" :loading="submitting" class="touch-friendly">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 视频预览对话框 -->
    <el-dialog v-model="previewVisible" title="视频预览" :width="videoDialogWidth" class="dialog-responsive">
      <video v-if="previewVideoUrl" :src="previewVideoUrl" controls style="width: 100%; border-radius: 4px;"></video>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Edit, Delete, FolderOpened } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'

// 修改导入方式
import { courseApi } from '@/api/course'

const userStore = useUserStore()
const loading = ref(false)
const submitting = ref(false)
const courses = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()
const previewVisible = ref(false)
const previewVideoUrl = ref('')

// 搜索和筛选
const searchKeyword = ref('')
const difficultyFilter = ref('')

// 响应式相关
const isMobile = ref(false)

// 计算对话框宽度
const dialogWidth = computed(() => {
  return isMobile.value ? '95vw' : '600px'
})

const videoDialogWidth = computed(() => {
  return isMobile.value ? '95vw' : '800px'
})

// 检测移动端
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

const uploadUrl = `${import.meta.env.VITE_API_BASE_URL || ''}/api/v1/courses/upload-video`
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

interface CourseForm {
  id?: string | number
  title: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  duration: number
  cover_url: string
  video_url: string
  instructor?: string
}

const form = ref<CourseForm>({
  title: '',
  description: '',
  difficulty: 'beginner',
  duration: 60,
  cover_url: '',
  video_url: '',
  instructor: ''
})

const rules = reactive<FormRules>({
  title: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入课程描述', trigger: 'blur' }],
  difficulty: [{ required: true, message: '请选择难度等级', trigger: 'change' }],
  duration: [{ required: true, message: '请输入课程时长', trigger: 'blur' }]
})

// 获取难度标签类型
const getDifficultyType = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner':
      return 'success'
    case 'intermediate':
      return 'warning'
    case 'advanced':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取难度文本
const getDifficultyText = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner':
      return '初级'
    case 'intermediate':
      return '中级'
    case 'advanced':
      return '高级'
    default:
      return '未知'
  }
}

const fetchCourses = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      limit: pageSize.value
    }
    
    // 添加搜索和筛选参数
    if (searchKeyword.value.trim()) {
      params.search = searchKeyword.value.trim()
    }
    if (difficultyFilter.value) {
      params.difficulty = difficultyFilter.value
    }
    
    const res = await courseApi.getCourses(params)
    courses.value = res.items || []
    total.value = res.total || 0
  } catch (error) {
    ElMessage.error('获取课程列表失败')
    courses.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = async () => {
  currentPage.value = 1
  await fetchCourses()
}

// 重置搜索
const handleReset = () => {
  searchKeyword.value = ''
  difficultyFilter.value = ''
  handleSearch()
}

const handleAdd = () => {
  formMode.value = 'add'
  dialogTitle.value = '添加课程'
  form.value = {
    title: '',
    description: '',
    difficulty: 'beginner',
    duration: 60,
    cover_url: '',
    video_url: '',
    instructor: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row: CourseForm) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑课程'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id: string | number) => {
  ElMessageBox.confirm('确定要删除该课程吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await courseApi.deleteCourse(id)
      ElMessage.success('删除成功')
      fetchCourses()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        if (formMode.value === 'add') {
          await courseApi.createCourse(form.value)
          ElMessage.success('添加成功')
        } else {
          await courseApi.updateCourse(form.value.id!, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchCourses()
      } catch (error) {
        ElMessage.error(formMode.value === 'add' ? '添加失败' : '更新失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const beforeVideoUpload = (file: File) => {
  const isVideo = file.type.startsWith('video/')
  const isLt100M = file.size / 1024 / 1024 < 100

  if (!isVideo) {
    ElMessage.error('请上传视频文件！')
    return false
  }
  if (!isLt100M) {
    ElMessage.error('视频大小不能超过 100MB！')
    return false
  }
  return true
}

interface UploadResponse {
  url: string
}

const handleCoverSuccess = (response: UploadResponse) => {
  form.value.cover_url = response.url
  ElMessage.success('封面上传成功')
}

const handleVideoSuccess = (response: UploadResponse) => {
  form.value.video_url = response.url
  ElMessage.success('视频上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const handlePreviewVideo = (row: CourseForm) => {
  previewVideoUrl.value = row.video_url
  previewVisible.value = true
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchCourses()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchCourses()
}

onMounted(() => {
  fetchCourses()
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.course-container {
  padding: 16px;
  min-height: 100vh;
}

/* 搜索和筛选栏 */
.search-filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.search-filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 200px;
  flex: 1;
}

.search-filter-item.search-input {
  min-width: 250px;
  flex: 2;
}

.search-filter-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* 表格容器 */
.table-container {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
}

.table-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.table-actions .el-button {
  margin: 0;
  min-width: 60px;
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
  flex-wrap: wrap;
  gap: 12px;
}

/* 课程标题信息 */
.course-title-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.course-name {
  font-weight: 500;
  font-size: 14px;
  color: var(--text-primary);
}

.duration {
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-hover);
  padding: 2px 8px;
  border-radius: 12px;
}

.text-gray {
  color: var(--text-light);
}

/* 文件上传 */
.file-input-container {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.file-input {
  flex: 1;
  min-width: 200px;
}

.file-upload-btn {
  flex-shrink: 0;
}

.upload-trigger {
  display: flex;
  align-items: center;
  gap: 4px;
}

.image-preview,
.video-preview {
  margin-top: 12px;
  text-align: center;
}

.unit {
  color: var(--text-secondary);
  font-size: 14px;
}

/* 对话框样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 16px 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .course-container {
    padding: 12px;
  }
  
  .search-filter-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    padding: 12px;
  }
  
  .search-filter-item {
    width: 100%;
    min-width: auto;
    flex: none;
  }
  
  .search-filter-item.search-input {
    order: -1;
  }
  
  .search-filter-actions {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }
  
  .search-filter-actions .el-button {
    flex: 1;
    min-height: var(--mobile-button-height);
    font-size: 16px;
  }
  
  .file-input-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .file-input {
    min-width: auto;
    width: 100%;
  }
  
  .upload-trigger {
    justify-content: center;
    width: 100%;
  }
  
  .dialog-footer {
    flex-direction: column;
    padding: 12px 16px 0;
  }
  
  .dialog-footer .el-button {
    width: 100%;
    min-height: var(--mobile-button-height);
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .course-container {
    padding: 8px;
  }
  
  .search-filter-bar {
    padding: 10px;
  }
  
  .dialog-footer {
    gap: 6px;
  }
  
  .course-title-info {
    gap: 2px;
  }
  
  .course-name {
    font-size: 13px;
  }
  
  .duration {
    font-size: 11px;
  }
}
</style>