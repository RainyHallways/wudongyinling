<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'

// API 导入
import { getCourses, createCourse, updateCourse, deleteCourse } from '@/api/course'

const userStore = useUserStore()
const loading = ref(false)
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

const uploadUrl = `${import.meta.env.VITE_API_BASE_URL}/api/v1/courses/upload-video`
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
  video_url: ''
})

const rules = reactive<FormRules>({
  title: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入课程描述', trigger: 'blur' }],
  difficulty: [{ required: true, message: '请选择难度等级', trigger: 'change' }],
  duration: [{ required: true, message: '请输入课程时长', trigger: 'blur' }]
})

const fetchCourses = async () => {
  loading.value = true
  try {
    const res = await getCourses({
      page: currentPage.value,
      limit: pageSize.value
    })
    courses.value = res.items
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
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
    video_url: ''
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
      await deleteCourse(id)
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
        if (formMode.value === 'add') {
          await createCourse(form.value)
          ElMessage.success('添加成功')
        } else {
          await updateCourse(form.value.id!, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchCourses()
      } catch (error) {
        ElMessage.error(formMode.value === 'add' ? '添加失败' : '更新失败')
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
})
</script>

<template>
  <div class="course-container">
    <div class="header">
      <h2>课程管理</h2>
      <ElButton type="primary" @click="handleAdd">添加课程</ElButton>
    </div>

    <ElTable v-loading="loading" :data="courses" border style="width: 100%">
      <ElTableColumn prop="title" label="课程名称" />
      <ElTableColumn prop="description" label="课程描述" show-overflow-tooltip />
      <ElTableColumn prop="difficulty" label="难度等级">
        <template #default="{ row }">
          <ElTag :type="row.difficulty === 'beginner' ? 'success' : row.difficulty === 'intermediate' ? 'warning' : 'danger'">
            {{ row.difficulty === 'beginner' ? '初级' : row.difficulty === 'intermediate' ? '中级' : '高级' }}
          </ElTag>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="duration" label="时长">
        <template #default="{ row }">
          {{ row.duration }}分钟
        </template>
      </ElTableColumn>
      <ElTableColumn label="封面图片" width="120">
        <template #default="{ row }">
          <ElImage
            v-if="row.cover_url"
            :src="row.cover_url"
            :preview-src-list="[row.cover_url]"
            fit="cover"
            style="width: 50px; height: 50px"
          />
          <span v-else>暂无封面</span>
        </template>
      </ElTableColumn>
      <ElTableColumn label="课程视频" width="120">
        <template #default="{ row }">
          <ElButton v-if="row.video_url" type="primary" link @click="handlePreviewVideo(row)">
            预览视频
          </ElButton>
          <span v-else>暂无视频</span>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="instructor" label="教练" />
      <ElTableColumn label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <ElButtonGroup>
            <ElButton type="primary" @click="handleEdit(row)">编辑</ElButton>
            <ElButton type="danger" @click="handleDelete(row.id)">删除</ElButton>
          </ElButtonGroup>
        </template>
      </ElTableColumn>
    </ElTable>

    <div class="pagination">
      <ElPagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <ElDialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <ElForm
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <ElFormItem label="课程名称" prop="title">
          <ElInput v-model="form.title" />
        </ElFormItem>
        <ElFormItem label="课程描述" prop="description">
          <ElInput v-model="form.description" type="textarea" :rows="3" />
        </ElFormItem>
        <ElFormItem label="难度等级" prop="difficulty">
          <ElSelect v-model="form.difficulty" style="width: 100%">
            <ElOption label="初级" value="beginner" />
            <ElOption label="中级" value="intermediate" />
            <ElOption label="高级" value="advanced" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="课程时长" prop="duration">
          <ElInputNumber v-model="form.duration" :min="1" :max="360" />
          <span class="unit">分钟</span>
        </ElFormItem>
        <ElFormItem label="封面图片" prop="cover_url">
          <ElUpload
            class="cover-uploader"
            action="/api/upload/image"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleCoverSuccess"
            :on-error="handleUploadError"
            accept="image/*"
          >
            <ElImage
              v-if="form.cover_url"
              :src="form.cover_url"
              fit="cover"
              class="cover-preview"
            />
            <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
          </ElUpload>
        </ElFormItem>
        <ElFormItem label="课程视频" prop="video_url">
          <ElUpload
            class="video-uploader"
            action="/api/upload/video"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleVideoSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeVideoUpload"
            accept="video/*"
          >
            <div v-if="form.video_url" class="video-preview">
              <video :src="form.video_url" controls width="200"></video>
            </div>
            <el-icon v-else class="video-uploader-icon"><Plus /></el-icon>
          </ElUpload>
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="handleSubmit(formRef)">确定</ElButton>
        </span>
      </template>
    </ElDialog>

    <ElDialog v-model="previewVisible" title="视频预览" width="800px">
      <video v-if="previewVideoUrl" :src="previewVideoUrl" controls width="100%"></video>
    </ElDialog>
  </div>
</template>

<style scoped>
.course-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.cover-uploader,
.video-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}

.cover-uploader:hover,
.video-uploader:hover {
  border-color: var(--el-color-primary);
}

.cover-uploader-icon,
.video-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-preview {
  width: 100px;
  height: 100px;
  display: block;
}

.video-preview {
  width: 200px;
}

.unit {
  margin-left: 10px;
}
</style> 