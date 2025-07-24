import request from '@/utils/request'

export interface Course {
  id: string
  title: string
  description: string
  coverImage: string
  category: string
  difficulty: string
  duration: number
  instructor: string
  videoUrl: string
  isFavorite?: boolean
}

export interface CourseCategory {
  value: string
  label: string
}

export interface CourseDifficulty {
  value: string
  label: string
}

export interface CourseDuration {
  value: string
  label: string
  min?: number
  max?: number
}

export interface CourseParams {
  page?: number
  limit?: number
  keyword?: string
  category?: string
  difficulty?: string
  duration?: string
  featured?: boolean
}

// 获取课程列表
export function getCourses(params: CourseParams) {
  return request({
    url: '/api/courses',
    method: 'get',
    params
  })
}

// 获取课程详情
export function getCourseById(id: string) {
  return request({
    url: `/api/courses/${id}`,
    method: 'get'
  })
}

// 收藏课程
export function favoriteCourse(id: string) {
  return request({
    url: `/api/courses/${id}/favorite`,
    method: 'post'
  })
}

// 取消收藏课程
export function unfavoriteCourse(id: string) {
  return request({
    url: `/api/courses/${id}/favorite`,
    method: 'delete'
  })
}

// 更新学习进度
export function updateProgress(id: string, progress: number) {
  return request({
    url: `/api/courses/${id}/progress`,
    method: 'post',
    data: { progress }
  })
}

// 获取课程分类
export function getCourseCategories() {
  return request({
    url: '/api/courses/categories',
    method: 'get'
  })
}

// 获取难度级别
export function getCourseDifficulties() {
  return request({
    url: '/api/courses/difficulties',
    method: 'get'
  })
}

// 获取课程时长选项
export function getCourseDurations() {
  return request({
    url: '/api/courses/durations',
    method: 'get'
  })
} 