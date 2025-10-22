import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import { ElMessage, ElLoading } from 'element-plus'

// 定义环境变量接口（可选）已移除未使用声明

// 定义响应数据接口
interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
  total?: number
  page?: number
  limit?: number
}

// 定义请求配置接口
interface RequestConfig extends InternalAxiosRequestConfig {
  retry?: boolean
  retryCount?: number
  loading?: boolean
  showError?: boolean
  customErrorHandler?: (error: any) => void
}

// 重试配置
const RETRY_CONFIG = {
  maxRetries: 3,
  retryDelay: 1000,
  retryCodes: [408, 429, 500, 502, 503, 504]
}

// API 前缀统一为 /api/v1（与后端保持一致）
const API_PREFIX = '/api/v1'
const envBase: string | undefined = (import.meta.env as any).VITE_API_BASE_URL
// 如果设置了绝对地址，则确保包含 /api/v1；否则使用相对的 /api/v1 通过本地代理
const computedBaseURL = envBase
  ? (envBase.replace(/\/$/, '').endsWith(API_PREFIX)
      ? envBase.replace(/\/$/, '')
      : `${envBase.replace(/\/$/, '')}${API_PREFIX}`)
  : API_PREFIX

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: computedBaseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Loading实例管理
let loadingInstance: any = null
let loadingCount = 0

// 显示Loading
const showLoading = (text = '加载中...') => {
  if (loadingCount === 0) {
    loadingInstance = ElLoading.service({
      lock: true,
      text,
      background: 'rgba(0, 0, 0, 0.7)',
      spinner: 'el-icon-loading'
    })
  }
  loadingCount++
}

// 隐藏Loading
const hideLoading = () => {
  loadingCount--
  if (loadingCount <= 0) {
    loadingInstance?.close()
    loadingInstance = null
    loadingCount = 0
  }
}

// 延迟函数
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

// 重试请求
const retryRequest = async (
  config: RequestConfig,
  error: AxiosError,
  retryCount: number = 0
): Promise<any> => {
  if (!config.retry || retryCount >= RETRY_CONFIG.maxRetries) {
    return Promise.reject(error)
  }
  
  const retryCodes = RETRY_CONFIG.retryCodes
  const statusCode = error.response?.status
  
  if (!statusCode || !retryCodes.includes(statusCode)) {
    return Promise.reject(error)
  }
  
  // 指数退避延迟
  const delayTime = RETRY_CONFIG.retryDelay * Math.pow(2, retryCount)
  await delay(delayTime)
  
  const newConfig = { ...config, retryCount: retryCount + 1 }
  return service(newConfig)
}

// 请求拦截器
service.interceptors.request.use(
  async (config: RequestConfig): Promise<RequestConfig> => {
    // 显示Loading
    if (config.loading !== false) {
      showLoading(config.headers?.['X-Loading-Text'] as string)
    }
    
    // 确保 headers 存在
    if (!config.headers) {
      config.headers = {} as any
    }

    // 添加认证token（避免引入 store 造成循环，直接读取本地存储）
    const token = localStorage.getItem('token') || ''
    const isDemo = localStorage.getItem('isDemo') === 'true'
    
    // 如果是演示账号，静默错误提示
    if (isDemo && config.showError !== false) {
      config.showError = false
    }
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 添加请求ID用于追踪
    ;(config.headers as any)['X-Request-ID'] = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    // 添加时间戳防止缓存
    if (config.method?.toLowerCase() === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    // 默认开启重试
    if (config.retry === undefined) {
      config.retry = true
    }
    
    // 默认显示错误消息
    if (config.showError === undefined) {
      config.showError = true
    }
    
    return config
  },
  (error) => {
    hideLoading()
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  async (response: AxiosResponse<ApiResponse | any>): Promise<any> => {
    // 隐藏Loading
    const config = response.config as RequestConfig
    if (config.loading !== false) {
      hideLoading()
    }
    
    const res: any = response.data as any
    const requestConfig = response.config as RequestConfig
    
    // 业务逻辑错误处理
    if (res.code !== 0) {
      // 使用自定义错误处理器
      if (requestConfig.customErrorHandler) {
        requestConfig.customErrorHandler(res)
      } else if (requestConfig.showError !== false) {
        ElMessage({
          message: res.message || '服务器错误',
          type: 'error',
          duration: 5 * 1000
        })
      }
      
      // 401: Token失效，需要重新登录
      if (res.code === 401) {
        // 清理本地认证并重定向（不引入路由以避免循环）
        try {
          localStorage.removeItem('token')
          localStorage.removeItem('userInfo')
          localStorage.removeItem('roles')
          localStorage.removeItem('isDemo')
        } catch {}
        const path = window.location.pathname
        if (path.startsWith('/admin')) window.location.href = '/admin/login'
        else window.location.href = '/login'
      }
      
      return Promise.reject(new Error(res.message || '未知错误'))
    } else {
      // 如果响应包含分页信息，返回完整响应对象
      if ((res as any).hasOwnProperty('total') || (res as any).hasOwnProperty('page')) {
        return res
      }
      // 否则只返回data部分（保持向后兼容）
      return (res as any).data
    }
  },
  async (error: AxiosError) => {
    // 隐藏Loading
    const config = error.config as RequestConfig
    if (config?.loading !== false) {
      hideLoading()
    }
    
    // 如果是演示账号，静默处理所有错误（避免引入 store，读取本地存储）
    if (localStorage.getItem('isDemo') === 'true') {
      return Promise.reject(error)
    }
    
    // 重试机制
    if (config && config.retry) {
      try {
        const retryCount = config.retryCount || 0
        return await retryRequest(config, error, retryCount)
      } catch (retryError) {
        // 重试失败，继续执行错误处理
      }
    }
    
    const { response } = error
    let message = '请求错误'
    let customHandler = false
    
    if (response && response.status) {
      switch (response.status) {
        case 401:
          message = '未授权，请登录'
          try {
            localStorage.removeItem('token')
            localStorage.removeItem('userInfo')
            localStorage.removeItem('roles')
            localStorage.removeItem('isDemo')
          } catch {}
          // 直接根据路径判断跳转目标，避免引入路由
          if (window.location.pathname.startsWith('/admin')) {
            window.location.href = '/admin/login'
          } else {
            window.location.href = '/login'
          }
          break
        case 403:
          message = '拒绝访问，权限不足'
          break
        case 404:
          message = '请求的资源不存在'
          break
        case 408:
          message = '请求超时'
          break
        case 422:
          message = '请求参数错误'
          // 尝试从响应中获取详细错误信息
          {
            const data: any = (response as any).data
            if (data?.message) {
              message = data.message
            }
          }
          break
        case 429:
          message = '请求过于频繁，请稍后再试'
          break
        case 500:
          message = '服务器内部错误'
          break
        case 502:
          message = '网关错误'
          break
        case 503:
          message = '服务暂时不可用'
          break
        case 504:
          message = '网关超时'
          break
        default:
          message = `网络错误 ${response.status}`
      }
    } else if (error.code === 'NETWORK_ERROR') {
      message = '网络连接失败，请检查网络设置'
    } else if (error.code === 'ECONNABORTED') {
      message = '请求超时，请稍后重试'
    } else if (error.message) {
      message = error.message
    }
    
    // 使用自定义错误处理器
    if (config?.customErrorHandler) {
      config.customErrorHandler({ message, status: response?.status, data: response?.data })
      customHandler = true
    } else if (!config || config.showError !== false) {
      ElMessage({
        message,
        type: 'error',
        duration: 5 * 1000,
        showClose: true
      })
    }
    
    // 记录错误日志
    if (config?.headers?.['X-Request-ID']) {
      console.error(`Request Error [${config.headers['X-Request-ID']}]:`, {
        url: config.url,
        method: config.method,
        status: response?.status,
        message
      })
    }
    
    return Promise.reject(customHandler ? error : new Error(message))
  }
)

// 封装请求方法
export const request = {
  get<T = any>(url: string, params?: object, config?: RequestConfig): Promise<T> {
    return service.get(url, { params, ...config })
  },
  post<T = any>(url: string, data?: object, config?: RequestConfig): Promise<T> {
    return service.post(url, data, config)
  },
  put<T = any>(url: string, data?: object, config?: RequestConfig): Promise<T> {
    return service.put(url, data, config)
  },
  delete<T = any>(url: string, params?: object, config?: RequestConfig): Promise<T> {
    return service.delete(url, { params, ...config })
  },
  patch<T = any>(url: string, data?: object, config?: RequestConfig): Promise<T> {
    return service.patch(url, data, config)
  },
  
  // 文件上传
  upload<T = any>(url: string, formData: FormData, config?: RequestConfig): Promise<T> {
    return service.post(url, formData, {
      ...config,
      headers: {
        'Content-Type': 'multipart/form-data',
        ...config?.headers
      }
    })
  },
  
  // 下载文件
  download(url: string, params?: object, config?: RequestConfig): Promise<void> {
    return service.get(url, {
      params,
      ...config,
      responseType: 'blob'
    }).then((response) => {
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = config?.headers?.['X-Download-Filename'] || 'download'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    })
  },
  
  // 取消请求（留空实现，避免类型错误；如需使用请改为 AbortController）
}

// 导出axios实例和配置
export { service as axios, type RequestConfig }
export default request 