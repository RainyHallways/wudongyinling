// icons.js - 统一管理图标组件
import { markRaw } from 'vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 创建一个对象，包含所有 Element Plus 图标，并用 markRaw 包装它们
export const Icons = {}

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  Icons[key] = markRaw(component)
}

export default Icons 