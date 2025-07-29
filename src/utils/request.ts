import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'
import { useUserStore } from '../stores/user'

// 定义环境变量接口
interface ViteEnv {
  VITE_API_BASE_URL?: string
  [key: string]: any
}

// 定义响应数据接口
interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: (import.meta.env as any).VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const userStore = useUserStore()
    const token = userStore.token
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>): any => {
    const res = response.data
    
    // 业务逻辑错误处理
    if (res.code !== 0) {
      ElMessage({
        message: res.message || '服务器错误',
        type: 'error',
        duration: 5 * 1000
      })
      
      // 401: Token失效，需要重新登录
      if (res.code === 401) {
        const userStore = useUserStore()
        userStore.resetState()
        
        // 判断当前路由是否需要登录权限
        if (router.currentRoute.value.meta.requiresAuth) {
          router.push('/login')
        }
      }
      
      return Promise.reject(new Error(res.message || '未知错误'))
    } else {
      // 如果响应包含分页信息，返回完整响应对象
      if (res.hasOwnProperty('total') || res.hasOwnProperty('page')) {
        return res
      }
      // 否则只返回data部分（保持向后兼容）
      return res.data
    }
  },
  (error) => {
    const { response } = error
    let message = '请求错误'
    
    if (response && response.status) {
      switch (response.status) {
        case 401:
          message = '未授权，请登录'
          const userStore = useUserStore()
          userStore.resetState()
          
          // 判断当前路由是否是管理员路由
          if (router.currentRoute.value.path.startsWith('/admin')) {
            router.push('/admin/login')
          } else if (router.currentRoute.value.meta.requiresAuth) {
            router.push('/login')
          }
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址错误'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = `连接错误${response.status}`
      }
    }
    
    ElMessage({
      message,
      type: 'error',
      duration: 5 * 1000
    })
    
    return Promise.reject(error)
  }
)

// 封装请求方法
export const request = {
  get<T = any>(url: string, params?: object): Promise<T> {
    return service.get(url, { params })
  },
  post<T = any>(url: string, data?: object): Promise<T> {
    return service.post(url, data)
  },
  put<T = any>(url: string, data?: object): Promise<T> {
    return service.put(url, data)
  },
  delete<T = any>(url: string, params?: object): Promise<T> {
    return service.delete(url, { params })
  },
  patch<T = any>(url: string, data?: object): Promise<T> {
    return service.patch(url, data)
  }
}

export default request 