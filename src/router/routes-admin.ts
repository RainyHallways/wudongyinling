import { RouteRecordRaw } from 'vue-router'
import AdminLayout from '../layouts/AdminLayout.vue'

const adminRoutes: RouteRecordRaw[] = [
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/admin/Dashboard.vue'),
        meta: { 
          title: '仪表盘',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-odometer'
        }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('../views/admin/UserManagement.vue'),
        meta: { 
          title: '用户管理',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-user'
        }
      },
      {
        path: 'courses',
        name: 'CourseManagement',
        component: () => import('../views/admin/CourseManagement.vue'),
        meta: { 
          title: '课程管理',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-reading'
        }
      },
      {
        path: 'challenges',
        name: 'ChallengeManagement',
        component: () => import('../views/admin/ChallengeManagement.vue'),
        meta: { 
          title: '挑战活动',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-trophy'
        }
      },
      {
        path: 'health-records',
        name: 'HealthRecords',
        component: () => import('../views/admin/HealthRecords.vue'),
        meta: { 
          title: '健康记录',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-first-aid-kit'
        }
      },
      {
        path: 'prescriptions',
        name: 'PrescriptionManagement',
        component: () => import('../views/admin/PrescriptionManagement.vue'),
        meta: { 
          title: '处方管理',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-list'
        }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('../views/admin/Statistics.vue'),
        meta: { 
          title: '数据统计',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-data-line'
        }
      },
      {
        path: 'system',
        name: 'SystemSettings',
        component: () => import('../views/admin/SystemSettings.vue'),
        meta: { 
          title: '系统设置',
          requiresAuth: true, 
          role: 'admin',
          icon: 'el-icon-setting'
        }
      }
    ]
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/Login.vue'),
    meta: {
      title: '管理员登录'
    }
  }
]

export default adminRoutes 