<template>
  <div class="image-upload">
    <el-upload
      ref="uploadRef"
      :action="uploadUrl"
      :headers="headers"
      :data="uploadData"
      :multiple="multiple"
      :accept="acceptTypes"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-progress="handleProgress"
      :on-remove="handleRemove"
      :on-exceed="handleExceed"
      :on-preview="handlePreview"
      :file-list="fileList"
      :limit="limit"
      :disabled="disabled || loading"
      :list-type="listType"
      :show-file-list="showFileList"
      :drag="drag"
      :auto-upload="autoUpload"
      class="upload-container"
    >
      <!-- 拖拽上传区域 -->
      <div v-if="drag" class="upload-dragger">
        <el-icon class="upload-icon" :size="48">
          <UploadFilled />
        </el-icon>
        <div class="upload-text">
          <p class="upload-title">将图片拖拽到此处，或<em>点击上传</em></p>
          <p class="upload-hint" v-if="hint">{{ hint }}</p>
          <p class="upload-limit" v-if="limit > 1">
            最多上传 {{ limit }} 个文件
          </p>
        </div>
      </div>
      
      <!-- 普通上传按钮 -->
      <div v-else class="upload-button">
        <el-button type="primary" :loading="loading" :disabled="disabled">
          <el-icon><Upload /></el-icon>
          {{ buttonText }}
        </el-button>
        <div class="upload-hint" v-if="hint">{{ hint }}</div>
      </div>
      
      <!-- 自定义插槽 -->
      <template v-if="$slots.default" #default>
        <slot></slot>
      </template>
      
      <!-- 文件列表 -->
      <template v-if="showFileList" #file="{ file }">
        <div class="upload-file-item">
          <img
            v-if="file.url"
            :src="file.url"
            :alt="file.name"
            class="upload-file-image"
            @click="handlePreview(file)"
          />
          <div v-else class="upload-file-icon">
            <el-icon><Picture /></el-icon>
          </div>
          
          <div class="upload-file-info">
            <div class="file-name" :title="file.name">{{ file.name }}</div>
            <div class="file-size">{{ formatFileSize(file.size) }}</div>
            <el-progress
              v-if="file.status === 'uploading'"
              :percentage="file.percentage || 0"
              :show-text="false"
              class="upload-progress"
            />
          </div>
          
          <div class="upload-file-actions">
            <el-button
              v-if="file.status === 'success'"
              type="text"
              @click="handlePreview(file)"
            >
              <el-icon><View /></el-icon>
            </el-button>
            <el-button
              v-if="!disabled"
              type="text"
              @click="handleRemove(file)"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
      </template>
    </el-upload>
    
    <!-- 图片预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="图片预览"
      width="80%"
      :append-to-body="true"
      class="preview-dialog"
    >
      <div class="preview-container">
        <img
          v-if="previewUrl"
          :src="previewUrl"
          alt="预览图片"
          class="preview-image"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Upload, UploadFilled, Picture, View, Delete } from '@element-plus/icons-vue'
import type { UploadInstance, UploadProps, UploadUserFile } from 'element-plus'

interface Props {
  modelValue?: string | string[]
  uploadUrl?: string
  headers?: Record<string, string>
  uploadData?: Record<string, any>
  multiple?: boolean
  acceptTypes?: string
  maxSize?: number // MB
  limit?: number
  disabled?: boolean
  loading?: boolean
  listType?: 'text' | 'picture' | 'picture-card'
  showFileList?: boolean
  drag?: boolean
  autoUpload?: boolean
  buttonText?: string
  hint?: string
  compress?: boolean
  quality?: number // 0-1
  maxWidth?: number
  maxHeight?: number
}

const props = withDefaults(defineProps<Props>(), {
  uploadUrl: '/api/v1/upload/image',
  headers: () => ({}),
  uploadData: () => ({}),
  multiple: false,
  acceptTypes: 'image/jpeg,image/jpg,image/png,image/gif,image/webp',
  maxSize: 5, // 5MB
  limit: 1,
  disabled: false,
  loading: false,
  listType: 'picture-card',
  showFileList: true,
  drag: false,
  autoUpload: true,
  buttonText: '上传图片',
  hint: '支持 JPG、PNG、GIF 格式，文件大小不超过 5MB',
  compress: true,
  quality: 0.8,
  maxWidth: 1920,
  maxHeight: 1080
})

const emit = defineEmits<{
  'update:modelValue': [value: string | string[]]
  success: [response: any, file: UploadUserFile]
  error: [error: any, file: UploadUserFile]
  progress: [event: any, file: UploadUserFile]
  remove: [file: UploadUserFile]
  exceed: [files: UploadUserFile[], fileList: UploadUserFile[]]
  change: [fileList: UploadUserFile[]]
}>()

const uploadRef = ref<UploadInstance>()
const fileList = ref<UploadUserFile[]>([])
const previewVisible = ref(false)
const previewUrl = ref('')

// 处理 modelValue 变化
watch(() => props.modelValue, (newVal) => {
  if (!newVal) {
    fileList.value = []
    return
  }
  
  const urls = Array.isArray(newVal) ? newVal : [newVal]
  fileList.value = urls.map((url, index) => ({
    name: `image_${index + 1}`,
    url,
    uid: Date.now() + index,
    status: 'success'
  } as UploadUserFile))
}, { immediate: true })

// 格式化文件大小
const formatFileSize = (size: number): string => {
  if (!size) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let unitIndex = 0
  let fileSize = size
  
  while (fileSize >= 1024 && unitIndex < units.length - 1) {
    fileSize /= 1024
    unitIndex++
  }
  
  return `${fileSize.toFixed(1)} ${units[unitIndex]}`
}

// 上传前检查
const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  // 检查文件类型
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  
  // 检查文件大小
  const isLtMaxSize = file.size / 1024 / 1024 < props.maxSize
  if (!isLtMaxSize) {
    ElMessage.error(`图片大小不能超过 ${props.maxSize}MB！`)
    return false
  }
  
  // 图片压缩
  if (props.compress && props.autoUpload) {
    return compressImage(file)
  }
  
  return true
}

// 图片压缩
const compressImage = (file: File): Promise<File> => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')!
        
        // 计算压缩后的尺寸
        let { width, height } = img
        const maxWidth = props.maxWidth
        const maxHeight = props.maxHeight
        
        if (width > maxWidth || height > maxHeight) {
          const ratio = Math.min(maxWidth / width, maxHeight / height)
          width *= ratio
          height *= ratio
        }
        
        canvas.width = width
        canvas.height = height
        
        // 绘制压缩后的图片
        ctx.drawImage(img, 0, 0, width, height)
        
        // 转换为 Blob
        canvas.toBlob((blob) => {
          if (blob) {
            const compressedFile = new File([blob], file.name, {
              type: file.type,
              lastModified: Date.now()
            })
            resolve(compressedFile)
          } else {
            resolve(file)
          }
        }, file.type, props.quality)
      }
      img.src = e.target?.result as string
    }
    reader.readAsDataURL(file)
  })
}

// 上传成功
const handleSuccess: UploadProps['onSuccess'] = (response, file) => {
  ElMessage.success('上传成功')
  emit('success', response, file)
  
  // 更新 modelValue
  if (response.url) {
    const newUrl = response.url
    if (props.multiple) {
      const urls = fileList.value
        .filter(f => f.url && f.status === 'success')
        .map(f => f.url!)
      if (!urls.includes(newUrl)) {
        urls.push(newUrl)
      }
      emit('update:modelValue', urls)
    } else {
      emit('update:modelValue', newUrl)
    }
  }
}

// 上传失败
const handleError: UploadProps['onError'] = (error, file) => {
  ElMessage.error('上传失败')
  emit('error', error, file)
}

// 上传进度
const handleProgress: UploadProps['onProgress'] = (event, file) => {
  emit('progress', event, file)
}

// 移除文件
const handleRemove: UploadProps['onRemove'] = (file) => {
  emit('remove', file)
  
  // 更新 modelValue
  if (file.url) {
    if (props.multiple) {
      const urls = fileList.value
        .filter(f => f.url && f.status === 'success' && f.uid !== file.uid)
        .map(f => f.url!)
      emit('update:modelValue', urls)
    } else {
      emit('update:modelValue', '')
    }
  }
}

// 文件数量超限
const handleExceed: UploadProps['onExceed'] = (files, fileList) => {
  ElMessage.warning(`最多只能上传 ${props.limit} 个文件`)
  emit('exceed', files, fileList)
}

// 预览图片
const handlePreview: UploadProps['onPreview'] = (file) => {
  previewUrl.value = file.url || ''
  previewVisible.value = true
}

// 手动上传
const submit = () => {
  uploadRef.value?.submit()
}

// 清空文件列表
const clearFiles = () => {
  uploadRef.value?.clearFiles()
  fileList.value = []
  emit('update:modelValue', props.multiple ? [] : '')
}

// 暴露方法
defineExpose({
  submit,
  clearFiles,
  uploadRef
})
</script>

<style scoped>
.image-upload {
  width: 100%;
}

.upload-container {
  width: 100%;
}

.upload-dragger {
  padding: 40px;
  text-align: center;
  border: 2px dashed var(--el-border-color-light);
  border-radius: 8px;
  background: var(--el-fill-color-lighter);
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-dragger:hover {
  border-color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}

.upload-icon {
  color: var(--el-color-primary);
  margin-bottom: 16px;
}

.upload-text {
  color: var(--el-text-color-regular);
}

.upload-title {
  font-size: 16px;
  margin: 0 0 8px 0;
  color: var(--el-text-color-primary);
}

.upload-title em {
  color: var(--el-color-primary);
  font-style: normal;
}

.upload-hint {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin: 4px 0 0 0;
}

.upload-limit {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  margin: 8px 0 0 0;
}

.upload-button {
  text-align: center;
}

.upload-hint {
  margin-top: 8px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.upload-file-item {
  display: flex;
  align-items: center;
  padding: 8px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  margin-bottom: 8px;
  background: white;
  transition: all 0.3s ease;
}

.upload-file-item:hover {
  border-color: var(--el-color-primary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.upload-file-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 12px;
  cursor: pointer;
}

.upload-file-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--el-fill-color-light);
  border-radius: 4px;
  margin-right: 12px;
  color: var(--el-text-color-placeholder);
}

.upload-file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 14px;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-bottom: 4px;
}

.upload-progress {
  margin-top: 4px;
}

.upload-file-actions {
  display: flex;
  gap: 4px;
}

.preview-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.preview-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  background: #f5f5f5;
}

.preview-image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .upload-dragger {
    padding: 20px;
  }
  
  .upload-icon {
    font-size: 36px;
    margin-bottom: 12px;
  }
  
  .upload-title {
    font-size: 14px;
  }
  
  .upload-file-item {
    padding: 6px;
  }
  
  .upload-file-image,
  .upload-file-icon {
    width: 50px;
    height: 50px;
  }
  
  .file-name {
    font-size: 13px;
  }
  
  .file-size {
    font-size: 11px;
  }
}
</style>