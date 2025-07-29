import { RouteRecordRaw } from 'vue-router'
import PublicLayout from '../layouts/PublicLayout.vue'

const publicRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    component: PublicLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/public/Home.vue'),
        meta: {
          title: '首页',
          keepAlive: true
        }
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('../views/public/About.vue'),
        meta: {
          title: '关于我们'
        }
      },
      {
        path: 'dance-courses',
        name: 'DanceCourses',
        component: () => import('../views/public/DanceCourses.vue'),
        meta: {
          title: '舞蹈课程'
        }
      },
      {
        path: 'course/:id',
        name: 'CourseDetail',
        component: () => import('../views/public/CourseDetail.vue'),
        meta: {
          title: '课程详情'
        }
      },
      {
        path: 'my-courses',
        name: 'MyCourses',
        component: () => import('../views/public/MyCourses.vue'),
        meta: {
          title: '我的课程',
          requiresAuth: true
        }
      },
      {
        path: 'favorites',
        name: 'Favorites',
        component: () => import('../views/public/Favorites.vue'),
        meta: {
          title: '我的收藏',
          requiresAuth: true
        }
      },
      {
        path: 'ai-coach',
        name: 'AICoach',
        component: () => import('../views/public/AICoach.vue'),
        meta: {
          title: 'AI教练',
          requiresAuth: true
        }
      },
      {
        path: 'health-management',
        name: 'HealthManagement',
        component: () => import('../views/public/HealthManagement.vue'),
        meta: {
          title: '健康管理',
          requiresAuth: true
        }
      },
      {
        path: 'social-platform',
        name: 'SocialPlatform',
        component: () => import('../views/public/SocialPlatform.vue'),
        meta: {
          title: '社交平台',
          requiresAuth: true
        }
      },
      {
        path: 'contact',
        name: 'Contact',
        component: () => import('../views/public/Contact.vue'),
        meta: {
          title: '联系我们'
        }
      },
      {
        path: 'faq',
        name: 'FAQ',
        component: () => import('../views/public/FAQ.vue'),
        meta: {
          title: '常见问题'
        }
      },
      {
        path: 'login',
        name: 'Login',
        component: () => import('../views/public/Login.vue'),
        meta: {
          title: '用户登录'
        }
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('../views/public/Register.vue'),
        meta: {
          title: '用户注册'
        }
      },
      {
        path: 'user-profile',
        name: 'UserProfile',
        component: () => import('../views/public/UserProfile.vue'),
        meta: {
          title: '个人中心',
          requiresAuth: true
        }
      },
      {
        path: 'policy',
        children: [
          {
            path: 'original-license-agreement',
            name: 'OriginalLicenseAgreement',
            component: () => import('../views/public/policy/OriginalLicenseAgreement.vue'),
            meta: {
              title: '原创作品授权协议'
            }
          },
          {
            path: 'user-agreement',
            name: 'UserAgreement',
            component: () => import('../views/public/policy/UserAgreement.vue'),
            meta: {
              title: '网站协议'
            }
          },
          {
            path: 'user-originality-guarantee',
            name: 'UserOriginalityGuarantee',
            component: () => import('../views/public/policy/UserOriginalityGuarantee.vue'),
            meta: {
              title: '原创性保证书'
            }
          },
          {
            path: 'privacy-policy',
            name: 'PrivacyPolicy',
            component: () => import('../views/public/policy/PrivacyPolicy.vue'),
            meta: {
              title: '隐私保护协议'
            }
          }
        ]
      },
      {
        path: 'not-found',
        name: 'NotFound',
        component: () => import('../views/public/NotFound.vue'),
        meta: {
          title: '页面未找到'
        }
      }
    ]
  }
]

export default publicRoutes 