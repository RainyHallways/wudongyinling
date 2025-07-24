import request from '@/utils/request'

export const courseApi = {
  // 获取课程列表
  getCourses: (params) => {
    return request({
      url: '/api/v1/courses',
      method: 'get',
      params
    })
  },

  // 获取单个课程详情
  getCourse: (id) => {
    return request({
      url: `/api/v1/courses/${id}`,
      method: 'get'
    })
  },

  // 创建课程
  createCourse: (data) => {
    return request({
      url: '/api/v1/courses',
      method: 'post',
      data
    })
  },

  // 更新课程
  updateCourse: (id, data) => {
    return request({
      url: `/api/v1/courses/${id}`,
      method: 'put',
      data
    })
  },

  // 删除课程
  deleteCourse: (id) => {
    return request({
      url: `/api/v1/courses/${id}`,
      method: 'delete'
    })
  }
}

export default courseApi 