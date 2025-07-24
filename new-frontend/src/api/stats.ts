import { request } from '../utils/request'

// 仪表盘统计数据接口
export interface DashboardStats {
  totalCourses: number
  totalUsers: number
  totalChallenges?: number
  activeUsers?: number
  completedCourses?: number
  [key: string]: any
}

// 用户统计数据接口
export interface UserStats {
  registrations: {
    date: string
    count: number
  }[]
  roles: {
    role: string
    count: number
  }[]
  activity: {
    date: string
    activeUsers: number
  }[]
  [key: string]: any
}

// 课程统计数据接口
export interface CourseStats {
  popular: {
    id: number
    title: string
    enrollments: number
  }[]
  categories: {
    category: string
    count: number
  }[]
  completions: {
    date: string
    count: number
  }[]
  [key: string]: any
}

// 挑战统计数据接口
export interface ChallengeStats {
  active: number
  completed: number
  participants: {
    challengeId: number
    challengeName: string
    count: number
  }[]
  [key: string]: any
}

/**
 * 统计数据API
 */
export const statsApi = {
  /**
   * 获取仪表盘统计数据
   */
  getDashboardStats() {
    return request.get<DashboardStats>('/stats/dashboard')
  },

  /**
   * 获取用户统计数据
   */
  getUserStats() {
    return request.get<UserStats>('/stats/users')
  },

  /**
   * 获取课程统计数据
   */
  getCourseStats() {
    return request.get<CourseStats>('/stats/courses')
  },

  /**
   * 获取挑战统计数据
   */
  getChallengeStats() {
    return request.get<ChallengeStats>('/stats/challenges')
  }
} 