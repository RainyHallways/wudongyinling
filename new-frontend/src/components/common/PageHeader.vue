<template>
  <div class="page-header">
    <div class="container">
      <h1 class="page-title">{{ title }}</h1>
      <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts" setup>
defineProps({
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
  }
})
</script>

<style scoped>
.page-header {
  @apply py-12 mb-10 bg-gradient-to-r from-blue-50 to-indigo-50 text-center;
}

.container {
  @apply max-w-4xl mx-auto px-4;
}

.page-title {
  @apply text-3xl md:text-4xl font-bold text-blue-600 mb-4;
}

.page-subtitle {
  @apply text-lg text-gray-600 max-w-2xl mx-auto;
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
}

/* 为小屏幕优化显示 */
@media (max-width: 640px) {
  .page-header {
    @apply py-8;
  }
}
</style> 