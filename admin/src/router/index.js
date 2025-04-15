import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('../layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/dashboard/index.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/users/index.vue')
      },
      {
        path: 'courses',
        name: 'Courses',
        component: () => import('../views/courses/index.vue')
      },
      {
        path: 'prescriptions',
        name: 'Prescriptions',
        component: () => import('../views/prescriptions/index.vue')
      },
      {
        path: 'health-records',
        name: 'HealthRecords',
        component: () => import('../views/health-records/index.vue')
      },
      {
        path: 'challenges',
        name: 'Challenges',
        component: () => import('../views/challenges/index.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router 