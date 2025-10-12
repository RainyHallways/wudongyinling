<template>
  <div class="page-header">
    <div class="container">
      <!-- 面包屑导航 -->
      <div v-if="showBreadcrumb && breadcrumbs.length > 0" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item 
            v-for="(item, index) in breadcrumbs" 
            :key="index"
            :to="item.to"
            :class="{ 'is-current': index === breadcrumbs.length - 1 }"
          >
            <el-icon v-if="item.icon" class="breadcrumb-icon">
              <component :is="item.icon" />
            </el-icon>
            {{ item.label }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">{{ title }}</h1>
          <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
        </div>
        
        <div v-if="$slots.actions" class="actions-section">
          <slot name="actions"></slot>
        </div>
      </div>
      
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

interface BreadcrumbItem {
  label: string
  to?: string
  icon?: any
}

const props = defineProps({
  /**
   * 页面标题
   */
  title: {
    type: String,
    required: true
  },
  /**
   * 页面副标题
   */
  subtitle: {
    type: String,
    default: ''
  },
  /**
   * 是否显示面包屑导航
   */
  showBreadcrumb: {
    type: Boolean,
    default: true
  },
  /**
   * 自定义面包屑导航
   */
  customBreadcrumbs: {
    type: Array as () => BreadcrumbItem[],
    default: () => []
  },
  /**
   * 是否自动生成面包屑
   */
  autoBreadcrumb: {
    type: Boolean,
    default: true
  }
})

const route = useRoute()

// 自动生成面包屑导航
const breadcrumbs = computed(() => {
  if (props.customBreadcrumbs.length > 0) {
    return props.customBreadcrumbs
  }
  
  if (!props.autoBreadcrumb) {
    return []
  }
  
  const crumbs: BreadcrumbItem[] = []
  const pathSegments = route.path.split('/').filter(segment => segment)
  
  // 添加首页
  crumbs.push({
    label: '首页',
    to: '/',
    icon: 'House'
  })
  
  // 根据路径生成面包屑
  let currentPath = ''
  const routeMap: Record<string, string> = {
    'dance-courses': '舞蹈课程',
    'my-courses': '我的课程',
    'ai-coach': 'AI教练',
    'health-management': '健康管理',
    'social-platform': '社交平台',
    'user-profile': '个人资料',
    'favorites': '我的收藏',
    'chat-room': '聊天室',
    'about': '关于我们',
    'contact': '联系我们',
    'faq': '常见问题',
    'login': '登录',
    'register': '注册',
    'admin': '管理后台',
    'dashboard': '仪表盘',
    'user-management': '用户管理',
    'course-management': '课程管理',
    'health-records': '健康记录',
    'statistics': '数据统计',
    'system-settings': '系统设置'
  }
  
  pathSegments.forEach((segment, index) => {
    currentPath += `/${segment}`
    const isLast = index === pathSegments.length - 1
    
    if (routeMap[segment]) {
      crumbs.push({
        label: routeMap[segment],
        to: isLast ? undefined : currentPath
      })
    }
  })
  
  return crumbs
})
</script>

<style scoped>
.page-header {
  @apply py-12 mb-10 bg-gradient-to-r from-blue-50 to-indigo-50;
}

.container {
  @apply max-w-4xl mx-auto px-4;
}

.breadcrumb-container {
  @apply mb-6;
}

.breadcrumb-icon {
  @apply mr-1;
}

:deep(.el-breadcrumb) {
  @apply justify-center;
}

:deep(.el-breadcrumb__item) {
  @apply text-sm;
}

:deep(.el-breadcrumb__item.is-current) {
  @apply text-blue-600 font-medium;
}

.header-content {
  @apply flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6;
}

.title-section {
  @apply flex-1 text-center lg:text-left;
}

.actions-section {
  @apply flex-shrink-0;
}

.page-title {
  @apply text-3xl md:text-4xl font-bold text-blue-600 mb-4;
}

.page-subtitle {
  @apply text-lg text-gray-600 max-w-2xl mx-auto lg:mx-0;
}

/* 为大屏幕优化显示 */
@media (min-width: 1024px) {
  .page-header {
    @apply py-16;
  }
  
  .page-title {
    @apply text-5xl;
  }
  
  .page-subtitle {
    @apply text-xl;
  }
  
  :deep(.el-breadcrumb) {
    @apply justify-start;
  }
}

/* 为小屏幕优化显示 */
@media (max-width: 640px) {
  .page-header {
    @apply py-8;
  }
  
  .breadcrumb-container {
    @apply mb-4;
  }
  
  :deep(.el-breadcrumb) {
    @apply text-xs;
  }
  
  .header-content {
    @apply gap-4;
  }
}

/* 响应式面包屑 */
@media (max-width: 768px) {
  :deep(.el-breadcrumb__item:not(:first-child):not(:last-child)) {
    @apply hidden;
  }
  
  :deep(.el-breadcrumb__item:nth-last-child(2))::before {
    content: "...";
    @apply mx-2 text-gray-400;
  }
}
</style> 