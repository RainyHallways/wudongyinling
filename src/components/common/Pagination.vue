<template>
  <div class="pagination">
    <div class="pagination-info">
      <span v-if="showTotal">
        共 {{ total }} 条记录，第 {{ currentPage }} / {{ totalPages }} 页
      </span>
    </div>
    
    <div class="pagination-controls">
      <!-- 首页 -->
      <el-button
        :disabled="currentPage <= 1"
        size="small"
        @click="handlePageChange(1)"
      >
        首页
      </el-button>
      
      <!-- 上一页 -->
      <el-button
        :disabled="currentPage <= 1"
        size="small"
        @click="handlePageChange(currentPage - 1)"
      >
        上一页
      </el-button>
      
      <!-- 页码 -->
      <div class="page-numbers">
        <el-button
          v-for="page in visiblePages"
          :key="page"
          :type="page === currentPage ? 'primary' : 'default'"
          size="small"
          :disabled="page === '...'"
          @click="typeof page === 'number' && handlePageChange(page)"
        >
          {{ page }}
        </el-button>
      </div>
      
      <!-- 下一页 -->
      <el-button
        :disabled="currentPage >= totalPages"
        size="small"
        @click="handlePageChange(currentPage + 1)"
      >
        下一页
      </el-button>
      
      <!-- 末页 -->
      <el-button
        :disabled="currentPage >= totalPages"
        size="small"
        @click="handlePageChange(totalPages)"
      >
        末页
      </el-button>
    </div>
    
    <!-- 每页条数选择 -->
    <div v-if="showSizes" class="page-size-selector">
      <span>每页显示</span>
      <el-select
        :model-value="pageSize"
        @update:model-value="handleSizeChange"
        size="small"
        style="width: 80px; margin: 0 8px;"
      >
        <el-option
          v-for="size in pageSizes"
          :key="size"
          :label="size"
          :value="size"
        />
      </el-select>
      <span>条</span>
    </div>
    
    <!-- 跳转 -->
    <div v-if="showJumper" class="page-jumper">
      <span>跳至</span>
      <el-input-number
        :model-value="jumpPage"
        @update:model-value="jumpPage = $event"
        :min="1"
        :max="totalPages"
        size="small"
        style="width: 60px; margin: 0 8px;"
        @keyup.enter="handleJump"
      />
      <span>页</span>
      <el-button size="small" @click="handleJump">确定</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Props {
  total: number
  currentPage: number
  pageSize: number
  pageSizes?: number[]
  showTotal?: boolean
  showSizes?: boolean
  showJumper?: boolean
  pagerCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  pageSizes: () => [10, 20, 50, 100],
  showTotal: true,
  showSizes: true,
  showJumper: true,
  pagerCount: 7
})

const emit = defineEmits<{
  'update:currentPage': [page: number]
  'update:pageSize': [size: number]
  change: [page: number, size: number]
}>()

const jumpPage = ref(props.currentPage)

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(props.total / props.pageSize)
})

// 计算可见页码
const visiblePages = computed(() => {
  const current = props.currentPage
  const total = totalPages.value
  const count = props.pagerCount
  
  if (total <= count) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  
  const half = Math.floor(count / 2)
  let start = Math.max(1, current - half)
  let end = Math.min(total, start + count - 1)
  
  // 调整起始位置，确保显示足够的页码
  if (end - start + 1 < count) {
    start = Math.max(1, end - count + 1)
  }
  
  const pages = Array.from({ length: end - start + 1 }, (_, i) => start + i)
  
  // 添加省略号
  if (start > 1) {
    if (start > 2) {
      pages.unshift('...')
    } else {
      pages.unshift(1)
    }
  }
  
  if (end < total) {
    if (end < total - 1) {
      pages.push('...')
    } else {
      pages.push(total)
    }
  }
  
  return pages
})

// 页码改变
const handlePageChange = (page: number) => {
  if (page < 1 || page > totalPages.value || page === props.currentPage) {
    return
  }
  
  emit('update:currentPage', page)
  emit('change', page, props.pageSize)
  jumpPage.value = page
}

// 每页条数改变
const handleSizeChange = (size: number) => {
  emit('update:pageSize', size)
  
  // 重新计算当前页码，确保不超出范围
  const newTotalPages = Math.ceil(props.total / size)
  const newCurrentPage = Math.min(props.currentPage, newTotalPages || 1)
  
  emit('update:currentPage', newCurrentPage)
  emit('change', newCurrentPage, size)
  jumpPage.value = newCurrentPage
}

// 跳转页面
const handleJump = () => {
  const page = Math.max(1, Math.min(jumpPage.value, totalPages.value))
  handlePageChange(page)
}

// 监听当前页变化，更新跳转输入框
watch(() => props.currentPage, (newPage) => {
  jumpPage.value = newPage
})
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px 0;
  flex-wrap: wrap;
}

.pagination-info {
  color: var(--el-text-color-regular);
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-size-selector {
  display: flex;
  align-items: center;
  color: var(--el-text-color-regular);
  font-size: 14px;
}

.page-jumper {
  display: flex;
  align-items: center;
  color: var(--el-text-color-regular);
  font-size: 14px;
  gap: 8px;
}

@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 15px;
  }
  
  .pagination-controls {
    order: 1;
  }
  
  .pagination-info {
    order: 2;
  }
  
  .page-size-selector,
  .page-jumper {
    order: 3;
  }
  
  .page-numbers {
    flex-wrap: wrap;
    justify-content: center;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .pagination-controls {
    flex-wrap: wrap;
    justify-content: center;
    max-width: 300px;
  }
  
  .page-numbers {
    order: -1;
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>