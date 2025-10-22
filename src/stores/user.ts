import { defineStore } from 'pinia'
// 动态引入以避免循环依赖
let request: typeof import('../utils/request').request | null = null
async function getRequest() {
  if (!request) {
    const mod = await import('../utils/request')
    request = mod.request
  }
  return request
}
// 动态引入路由，避免循环依赖
async function getRouter() {
  const { default: router } = await import('../router')
  return router
}
import { ElMessage } from 'element-plus'

// 定义接口
interface UserInfo {
  id: number
  username: string
  nickname?: string
  avatar?: string
  email?: string
  phone?: string
  [key: string]: any
}

interface UserState {
  token: string
  userInfo: UserInfo
  roles: string[]
  loading: boolean
  error: string | null
  isDemo: boolean  // 标记是否为演示账号
}

interface LoginCredentials {
  username: string
  password: string
  isAdmin?: boolean
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    roles: JSON.parse(localStorage.getItem('roles') || '[]'),
    loading: false,
    error: null,
    isDemo: localStorage.getItem('isDemo') === 'true'
  }),
  
  getters: {
    isLoggedIn: (state): boolean => !!state.token,
    isAdmin: (state): boolean => state.roles.includes('admin'),
    username: (state): string => state.userInfo?.username || '',
    nickname: (state): string => state.userInfo?.nickname || state.userInfo?.username || ''
  },
  
  actions: {
    /**
     * 登录操作
     * @param credentials 登录凭证
     */
    async login(credentials: LoginCredentials) {
      try {
        this.loading = true
        this.error = null
        
        // 统一使用一个登录接口
        const req = await getRequest()
        const data = await req.post('/v1/auth/login', {
          username: credentials.username,
          password: credentials.password
        })
        
        // 保存登录信息
        this.setToken(data.access_token)
        this.setUserInfo(data.user)
        
        // 根据用户的is_admin属性设置角色
        const roles = data.user.is_admin ? ['admin'] : ['user']
        this.setRoles(roles)
        
        // 真实账号登录，清除演示标记
        this.isDemo = false
        localStorage.removeItem('isDemo')
        
        ElMessage.success('登录成功')
        
        // 根据用户类型和登录意图进行跳转
        const router = await getRouter()
        if (credentials.isAdmin && data.user.is_admin) {
          router.push('/admin')
        } else if (credentials.isAdmin && !data.user.is_admin) {
          ElMessage.error('您没有管理员权限')
          this.resetState()
          return
        } else {
          router.push('/')
        }
        
        return data
      } catch (error: any) {
        this.error = error.message || '登录失败'
        ElMessage.error(this.error || '登录失败')
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 获取用户信息
     */
    async getUserInfo() {
      try {
        this.loading = true
        this.error = null
        
        // 判断是否是管理员
        const req = await getRequest()
        const data = await req.get('/v1/users/me')
        this.setUserInfo(data)
        
        // 更新角色信息
        if (data.roles) {
          this.setRoles(data.roles)
        }
        
        return data
      } catch (error: any) {
        this.error = error.message || '获取用户信息失败'
        ElMessage.error(this.error || '获取用户信息失败')
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 管理员登录
     */
    async adminLogin(credentials: Omit<LoginCredentials, 'isAdmin'>) {
      return this.login({
        ...credentials,
        isAdmin: true
      })
    },
    
    /**
     * 演示账号登录（前端模拟，不调用服务器）
     */
    demoLogin() {
      try {
        // 生成模拟的 token
        const mockToken = 'demo_token_' + Date.now()
        
        // 创建模拟用户信息
        const mockUser: UserInfo = {
          id: 999,
          username: 'demo_user',
          nickname: '演示用户',
          avatar: '/images/default-avatar.png',
          email: 'demo@example.com',
          phone: '13800138000'
        }
        
        // 设置登录状态
        this.setToken(mockToken)
        this.setUserInfo(mockUser)
        this.setRoles(['user'])
        
        // 标记为演示账号
        this.isDemo = true
        localStorage.setItem('isDemo', 'true')
        
        ElMessage.success('演示账号登录成功（仅前端模拟，部分功能可能不可用）')
        return true
      } catch (error: any) {
        ElMessage.error('演示登录失败')
        console.error(error)
        return false
      }
    },
    
    /**
     * 退出登录
     */
    async logout() {
      try {
        // 演示账号直接退出，不调用服务器
        if (!this.isDemo) {
          const req = await getRequest()
          await req.post('/v1/auth/logout')
        }
        ElMessage.success('已退出登录')
      } catch (error) {
        console.error('退出登录失败', error)
      } finally {
        this.resetState()
        
        // 根据当前路径判断跳转目标
        const router = await getRouter()
        if (router.currentRoute.value.path.startsWith('/admin')) {
          router.push('/admin/login')
        } else {
          router.push('/login')
        }
      }
    },
    
    /**
     * 重置状态
     */
    resetState() {
      this.token = ''
      this.userInfo = {} as UserInfo
      this.roles = []
      this.isDemo = false
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('roles')
      localStorage.removeItem('isDemo')
    },
    
    /**
     * 设置token
     */
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    /**
     * 设置用户信息
     */
    setUserInfo(userInfo: UserInfo) {
      this.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    
    /**
     * 设置角色
     */
    setRoles(roles: string[]) {
      this.roles = roles
      localStorage.setItem('roles', JSON.stringify(roles))
    },
    
    /**
     * 更新用户信息
     */
    async updateUserInfo(userData: Partial<UserInfo>) {
      try {
        this.loading = true
        this.error = null
        
        const isAdmin = this.roles.includes('admin')
        const endpoint = isAdmin ? `/v1/users/${this.userInfo.id}` : '/v1/users/me'
        const req = await getRequest()
        const data = await req.put(endpoint, userData)
        this.setUserInfo({ ...this.userInfo, ...data })
        
        ElMessage.success('用户信息更新成功')
        return data
      } catch (error: any) {
        this.error = error.message || '更新用户信息失败'
        ElMessage.error(this.error || '更新用户信息失败')
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 检查是否有权限
     */
    hasPermission(requiredRole: string): boolean {
      if (!this.token) return false
      if (requiredRole === 'admin') return this.roles.includes('admin')
      return true
    }
  }
}) 