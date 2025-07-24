import { request } from '../utils/request'
import { Course } from './course'

// 轮播图接口
export interface Banner {
  id: number
  image: string
  title: string
  subtitle?: string
  link?: string
  sort_order?: number
}

// 新闻接口
export interface News {
  id: number
  title: string
  summary: string
  content?: string
  cover_image?: string
  publish_date: string
  view_count?: number
  author?: string
  tags?: string[]
}

// 首页信息接口
export interface HomeInfo {
  banners: Banner[]
  popularCourses: Course[]
  latestNews: News[]
  featuredEvents: any[]
  stats: {
    userCount: number
    courseCount: number
    completionRate: number
  }
}

/**
 * 首页相关API
 */
export const homeApi = {
  /**
   * 获取首页数据
   */
  getHomeInfo() {
    return request.get<HomeInfo>('/home')
  },
  
  /**
   * 获取轮播图列表
   */
  getBanners() {
    return request.get<Banner[]>('/home/banners')
  },
  
  /**
   * 获取推荐课程
   * @param limit 限制数量
   */
  getRecommendedCourses(limit: number = 6) {
    return request.get<Course[]>('/courses/recommended', { limit })
  },
  
  /**
   * 获取最新新闻
   * @param limit 限制数量
   */
  getLatestNews(limit: number = 3) {
    return request.get<News[]>('/news/latest', { limit })
  },
  
  /**
   * 获取首页统计数据
   */
  getHomeStats() {
    return request.get<HomeInfo['stats']>('/home/stats')
  }
} 