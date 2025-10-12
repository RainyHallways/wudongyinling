<template>
  <div class="search-box" :class="{ 'focused': focused }">
    <!-- 搜索输入框 -->
    <div class="search-input-wrapper">
      <el-icon class="search-icon">
        <Search />
      </el-icon>
      
      <el-input
        ref="inputRef"
        :model-value="modelValue"
        @update:model-value="handleInput"
        :placeholder="placeholder"
        :clearable="clearable"
        :size="size"
        :disabled="disabled"
        class="search-input"
        @focus="handleFocus"
        @blur="handleBlur"
        @keyup.enter="handleSearch"
        @keyup.esc="handleClear"
      >
        <template #suffix v-if="showSearchButton">
          <el-button
            type="primary"
            :size="size"
            @click="handleSearch"
            :loading="loading"
          >
            搜索
          </el-button>
        </template>
      </el-input>
      
      <!-- 清空按钮 -->
      <el-icon
        v-if="modelValue && clearable"
        class="clear-icon"
        @click="handleClear"
      >
        <Close />
      </el-icon>
    </div>
    
    <!-- 搜索建议下拉框 -->
    <div v-if="showSuggestions && suggestions.length > 0" class="search-suggestions">
      <div class="suggestions-header" v-if="suggestionsTitle">
        {{ suggestionsTitle }}
      </div>
      <div
        v-for="(suggestion, index) in suggestions"
        :key="index"
        class="suggestion-item"
        :class="{ 'selected': selectedIndex === index }"
        @click="selectSuggestion(suggestion)"
        @mouseenter="selectedIndex = index"
      >
        <el-icon v-if="suggestion.icon" class="suggestion-icon">
          <component :is="suggestion.icon" />
        </el-icon>
        <div class="suggestion-content">
          <div class="suggestion-label" v-html="highlightMatch(suggestion.label)"></div>
          <div v-if="suggestion.description" class="suggestion-description">
            {{ suggestion.description }}
          </div>
        </div>
        <div v-if="suggestion.count" class="suggestion-count">
          {{ suggestion.count }}
        </div>
      </div>
    </div>
    
    <!-- 搜索历史 -->
    <div v-if="showHistory && searchHistory.length > 0 && !modelValue" class="search-history">
      <div class="history-header">
        <span>搜索历史</span>
        <el-button type="text" size="small" @click="clearHistory">
          清空
        </el-button>
      </div>
      <div class="history-items">
        <el-tag
          v-for="(item, index) in searchHistory"
          :key="index"
          class="history-tag"
          closable
          @close="removeHistoryItem(index)"
          @click="handleHistoryClick(item)"
        >
          {{ item }}
        </el-tag>
      </div>
    </div>
    
    <!-- 快捷搜索 -->
    <div v-if="showQuickSearch && quickSearchItems.length > 0 && !modelValue" class="quick-search">
      <div class="quick-search-header">快捷搜索</div>
      <div class="quick-search-items">
        <el-button
          v-for="(item, index) in quickSearchItems"
          :key="index"
          size="small"
          :type="item.type || 'default'"
          @click="handleQuickSearch(item)"
        >
          {{ item.label }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { Search, Close } from '@element-plus/icons-vue'
import { ElInput } from 'element-plus'

interface SearchSuggestion {
  label: string
  description?: string
  value?: string
  icon?: any
  count?: number
}

interface QuickSearchItem {
  label: string
  value: string
  type?: 'primary' | 'success' | 'warning' | 'danger' | 'info'
}

interface Props {
  modelValue: string
  placeholder?: string
  size?: 'large' | 'default' | 'small'
  clearable?: boolean
  disabled?: boolean
  loading?: boolean
  showSearchButton?: boolean
  showSuggestions?: boolean
  suggestions?: SearchSuggestion[]
  suggestionsTitle?: string
  showHistory?: boolean
  searchHistory?: string[]
  maxHistoryItems?: number
  showQuickSearch?: boolean
  quickSearchItems?: QuickSearchItem[]
  debounceDelay?: number
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请输入搜索内容',
  size: 'default',
  clearable: true,
  showSearchButton: false,
  showSuggestions: false,
  suggestions: () => [],
  maxHistoryItems: 10,
  showQuickSearch: false,
  quickSearchItems: () => [],
  debounceDelay: 300
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  search: [value: string]
  clear: []
  select: [suggestion: SearchSuggestion]
  'history-clear': []
  'history-item-remove': [index: number]
  'history-item-click': [item: string]
}>()

const inputRef = ref<InstanceType<typeof ElInput>>()
const focused = ref(false)
const selectedIndex = ref(-1)
const debounceTimer = ref<number>()

// 处理输入
const handleInput = (value: string) => {
  emit('update:modelValue', value)
  selectedIndex.value = -1
  
  // 防抖处理
  if (debounceTimer.value) {
    clearTimeout(debounceTimer.value)
  }
  
  debounceTimer.value = setTimeout(() => {
    // 可以在这里触发搜索建议的获取
  }, props.debounceDelay)
}

// 处理搜索
const handleSearch = () => {
  const value = props.modelValue.trim()
  if (value) {
    emit('search', value)
  }
}

// 处理清空
const handleClear = () => {
  emit('update:modelValue', '')
  emit('clear')
  selectedIndex.value = -1
}

// 处理焦点事件
const handleFocus = () => {
  focused.value = true
}

const handleBlur = () => {
  setTimeout(() => {
    focused.value = false
    selectedIndex.value = -1
  }, 200)
}

// 选择搜索建议
const selectSuggestion = (suggestion: SearchSuggestion) => {
  const value = suggestion.value || suggestion.label
  emit('update:modelValue', value)
  emit('select', suggestion)
  emit('search', value)
}

// 处理历史记录点击
const handleHistoryClick = (item: string) => {
  emit('update:modelValue', item)
  emit('history-item-click', item)
  emit('search', item)
}

// 处理快捷搜索
const handleQuickSearch = (item: QuickSearchItem) => {
  emit('update:modelValue', item.value)
  emit('search', item.value)
}

// 清空历史记录
const clearHistory = () => {
  emit('history-clear')
}

// 删除历史记录项
const removeHistoryItem = (index: number) => {
  emit('history-item-remove', index)
}

// 高亮匹配文本
const highlightMatch = (text: string): string => {
  if (!props.modelValue) return text
  
  const regex = new RegExp(`(${props.modelValue})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

// 键盘导航
const handleKeyNavigation = (event: KeyboardEvent) => {
  if (!props.showSuggestions || props.suggestions.length === 0) return
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      selectedIndex.value = Math.min(selectedIndex.value + 1, props.suggestions.length - 1)
      break
    case 'ArrowUp':
      event.preventDefault()
      selectedIndex.value = Math.max(selectedIndex.value - 1, -1)
      break
    case 'Enter':
      if (selectedIndex.value >= 0) {
        event.preventDefault()
        selectSuggestion(props.suggestions[selectedIndex.value])
      } else {
        handleSearch()
      }
      break
  }
}

// 监听键盘事件
watch(() => props.modelValue, () => {
  nextTick(() => {
    if (inputRef.value?.input) {
      inputRef.value.input.addEventListener('keydown', handleKeyNavigation)
    }
  })
})

// 暴露方法
defineExpose({
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur(),
  clear: handleClear
})
</script>

<style scoped>
.search-box {
  position: relative;
  width: 100%;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--el-text-color-placeholder);
  z-index: 10;
}

.clear-icon {
  position: absolute;
  right: 12px;
  color: var(--el-text-color-placeholder);
  cursor: pointer;
  z-index: 10;
  transition: color 0.2s;
}

.clear-icon:hover {
  color: var(--el-text-color-regular);
}

.search-input {
  width: 100%;
}

.search-input :deep(.el-input__inner) {
  padding-left: 35px;
  padding-right: 80px;
}

.search-input :deep(.el-input__suffix) {
  right: 8px;
}

.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
}

.suggestions-header {
  padding: 8px 16px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover,
.suggestion-item.selected {
  background: var(--el-fill-color-light);
}

.suggestion-icon {
  margin-right: 12px;
  color: var(--el-text-color-secondary);
}

.suggestion-content {
  flex: 1;
  min-width: 0;
}

.suggestion-label {
  font-size: 14px;
  color: var(--el-text-color-primary);
  margin-bottom: 2px;
}

.suggestion-label :deep(mark) {
  background: #fff2e8;
  color: var(--el-color-primary);
  padding: 0 2px;
  border-radius: 2px;
}

.suggestion-description {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.suggestion-count {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  background: var(--el-fill-color);
  padding: 2px 6px;
  border-radius: 10px;
}

.search-history {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
  margin-top: 4px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.history-items {
  padding: 12px 16px;
}

.history-tag {
  margin: 4px 8px 4px 0;
  cursor: pointer;
}

.quick-search {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
  margin-top: 4px;
}

.quick-search-header {
  padding: 8px 16px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.quick-search-items {
  padding: 12px 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.focused .search-icon {
  color: var(--el-color-primary);
}

@media (max-width: 768px) {
  .search-input :deep(.el-input__inner) {
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  .suggestion-item {
    padding: 16px;
  }
  
  .history-items,
  .quick-search-items {
    padding: 16px;
  }
}
</style>