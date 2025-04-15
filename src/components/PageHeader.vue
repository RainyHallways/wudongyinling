<template>
  <div class="page-header">
    <h1 class="page-title">{{ title }}</h1>
    <p v-if="subtitle" class="section-subtitle">{{ subtitle }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  }
})
</script>

<style lang="scss" scoped>
.page-header {
  text-align: center;
  margin: 40px 0;

  .page-title {
    font-size: 32px;
    color: var(--primary-color);
    margin-bottom: 10px;
  }

  .section-subtitle {
    font-size: 18px;
    color: #666;
  }
}
</style> 