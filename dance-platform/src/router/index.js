import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import Home from '../views/Home.vue'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue'),
    meta: {
      title: '关于我们 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/social',
    name: 'Social',
    component: () => import('@/views/SocialPlatform.vue'),
    meta: {
      title: '社交平台 - 舞动银龄',
      requiresAuth: true
    }
  },
  {
    path: '/health',
    name: 'Health',
    component: () => import('@/views/HealthManagement.vue'),
    meta: {
      title: '健康管理 - 舞动银龄',
      requiresAuth: true
    }
  },
  {
    path: '/coach',
    name: 'AICoach',
    component: () => import('@/views/AICoach.vue'),
    meta: {
      title: 'AI教练 - 舞动银龄',
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '用户登录 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/dance-courses',
    name: 'dance-courses',
    component: () => import('../views/DanceCourses.vue'),
    meta: {
      title: '舞蹈课程 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面未找到 - 舞动银龄',
      requiresAuth: false
    }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 更新页面标题
  document.title = to.meta.title || '舞动银龄'
  
  // 添加调试日志
  console.log(`正在跳转到路由: ${to.path}, 需要登录: ${to.meta.requiresAuth}`)
  
  // 检查是否需要登录权限
  if (to.meta.requiresAuth) {
    const isAuthenticated = localStorage.getItem('user-token')
    
    // 添加调试日志
    console.log(`用户认证状态: ${isAuthenticated ? '已登录' : '未登录'}`)
    
    if (!isAuthenticated) {
      ElMessage.warning('请先登录')
      next({ 
        name: 'Login', 
        query: { redirect: to.fullPath } 
      })
      return
    }
  }
  
  next()
})

// 全局后置钩子
router.afterEach((to, from) => {
  // 可以在这里添加页面访问统计等逻辑
  console.log(`从 ${from.name} 页面跳转到 ${to.name} 页面`)
})

export default router 