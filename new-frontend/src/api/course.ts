import { request } from '../utils/request'

// 定义接口
export interface Course {
  id: number
  title: string
  description: string
  coverImage: string
  videoUrl?: string
  category: string
  difficulty: string
  duration: number
  instructor: string
  createdAt: string
  updatedAt: string
  [key: string]: any
}

export interface CourseProgress {
  courseId: number
  progress: number
  lastUpdated: string
}

export interface CourseParams {
  page?: number
  limit?: number
  category?: string
  difficulty?: string
  search?: string
  [key: string]: any
}

/**
 * 获取课程列表
 * @param params - 查询参数
 * @returns 课程列表
 */
export function getCourses(params?: CourseParams) {
  return request.get<Course[]>('/courses', params)
}

/**
 * 获取课程详情
 * @param id - 课程ID
 * @returns 课程详情
 */
export function getCourseById(id: number | string) {
  return request.get<Course>(`/courses/${id}`)
}

/**
 * 获取收藏的课程
 * @returns 收藏的课程列表
 */
export function getFavoriteCourses() {
  return request.get<Course[]>('/courses/favorites')
}

/**
 * 收藏课程
 * @param id - 课程ID
 * @returns 操作结果
 */
export function favoriteCourse(id: number | string) {
  return request.post<{ success: boolean }>(`/courses/${id}/favorite`)
}

/**
 * 取消收藏课程
 * @param id - 课程ID
 * @returns 操作结果
 */
export function unfavoriteCourse(id: number | string) {
  return request.delete<{ success: boolean }>(`/courses/${id}/favorite`)
}

/**
 * 获取课程进度
 * @returns 所有课程的进度
 */
export function getCourseProgress() {
  return request.get<CourseProgress[]>('/courses/progress')
}

/**
 * 更新课程进度
 * @param id - 课程ID
 * @param progress - 进度百分比
 * @returns 更新后的进度
 */
export function updateCourseProgress(id: number | string, progress: number) {
  return request.post<CourseProgress>(`/courses/${id}/progress`, { progress })
} 