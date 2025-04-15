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
      title: '舞动银龄 - 首页',
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
    path: '/user-agreement',
    name: 'UserAgreement',
    component: () => import('@/views/UserAgreement.vue'),
    meta: {
      title: '用户协议 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/privacy-policy',
    name: 'PrivacyPolicy',
    component: () => import('@/views/PrivacyPolicy.vue'),
    meta: {
      title: '隐私政策 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/originality-guarantee',
    name: 'OriginalityGuarantee',
    component: () => import('@/views/UserOriginalityGuarantee.vue'),
    meta: {
      title: '原创性保证 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/original-license',
    name: 'OriginalLicense',
    component: () => import('@/views/OriginalLicenseAgreement.vue'),
    meta: {
      title: '原创授权协议 - 舞动银龄',
      requiresAuth: false
    }
  },
  {
    path: '/faq',
    name: 'FAQ',
    component: () => import('@/views/FAQ.vue'),
    meta: {
      title: '常见问题 - 舞动银龄',
      requiresAuth: false
    }
  },

  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/Contact.vue'),
    meta: {
      title: '联系我们 - 舞动银龄',
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