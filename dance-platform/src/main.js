import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import 'element-plus/dist/index.css'
import '@fortawesome/fontawesome-free/css/all.css'
import './styles/index.css'
import './styles/utilities.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})

// 为测试方便，添加默认的用户令牌
if (!localStorage.getItem('user-token')) {
  localStorage.setItem('user-token', 'demo-token')
  localStorage.setItem('user-info', JSON.stringify({
    username: 'demo用户',
    role: 'user'
  }))
  console.log('已自动添加测试用户登录状态')
}

app.mount('#app') 