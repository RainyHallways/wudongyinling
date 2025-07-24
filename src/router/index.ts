import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import publicRoutes from './routes-public'
import adminRoutes from './routes-admin'

// 合并所有路由
const routes: RouteRecordRaw[] = [
  ...publicRoutes,
  ...adminRoutes,
  {
    path: '/:pathMatch(.*)*',
    redirect: '/not-found'
  }
]

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

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 舞蹈艺术平台` : '舞蹈艺术平台'
  
  // 获取用户信息
  const userStore = useUserStore()
  const { token, roles } = userStore
  
  // 判断是否需要登录权限
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // 判断是否需要管理员权限
  const requiresAdmin = to.matched.some(record => record.meta.role === 'admin')
  
  // 不需要登录权限，直接放行
  if (!requiresAuth) {
    next()
    return
  }
  
  // 需要登录权限但没有token，跳转到登录页
  if (requiresAuth && !token) {
    ElMessage.error('请先登录')
    if (to.path.startsWith('/admin')) {
      next({ name: 'AdminLogin' })
    } else {
      next({ name: 'Login' })
    }
    return
  }
  
  // 需要管理员权限但不是管理员，跳转到首页
  if (requiresAdmin && !roles.includes('admin')) {
    ElMessage.error('没有管理员权限')
    next({ name: 'Home' })
    return
  }
  
  // 已登录且有权限，放行
  next()
})

export default router 