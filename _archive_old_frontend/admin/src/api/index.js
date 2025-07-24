import request from '@/utils/request'

// 用户相关API
export const userApi = {
  login: (data) => request.post('/auth/login', data),
  register: (data) => request.post('/auth/register', data),
  getUsers: (params) => request.get('/users', { params }),
  updateUser: (id, data) => request.put(`/users/${id}`, data),
  deleteUser: (id) => request.delete(`/users/${id}`)
}

// 课程相关API
export const courseApi = {
  getCourses: (params) => request.get('/courses', { params }),
  createCourse: (data) => request.post('/courses', data),
  updateCourse: (id, data) => request.put(`/courses/${id}`, data),
  deleteCourse: (id) => request.delete(`/courses/${id}`),
  uploadVideo: (data) => request.post('/courses/upload', data)
}

// 健康记录API
export const healthApi = {
  getRecords: (params) => request.get('/health', { params }),
  createRecord: (data) => request.post('/health', data),
  updateRecord: (id, data) => request.put(`/health/${id}`, data),
  deleteRecord: (id) => request.delete(`/health/${id}`),
  getRealtimeData: (userId) => `/health/ws/${userId}` // WebSocket URL
}

// 运动处方API
export const prescriptionApi = {
  getPrescriptions: (params) => request.get('/prescriptions', { params }),
  createPrescription: (data) => request.post('/prescriptions', data),
  updatePrescription: (id, data) => request.put(`/prescriptions/${id}`, data),
  deletePrescription: (id) => request.delete(`/prescriptions/${id}`)
}

// 打卡挑战API
export const challengeApi = {
  getChallenges: (params) => request.get('/challenges', { params }),
  createChallenge: (data) => request.post('/challenges', data),
  updateChallenge: (id, data) => request.put(`/challenges/${id}`, data),
  deleteChallenge: (id) => request.delete(`/challenges/${id}`),
  getRecords: (challengeId, params) => request.get(`/challenges/${challengeId}/records`, { params })
}

// AI分析API
export const aiApi = {
  analyzeVideo: (data) => request.post('/ai/analyze', data),
  getFeedback: (videoId) => request.get(`/ai/feedback/${videoId}`),
  compareVideos: (data) => request.post('/ai/compare', data),
  chatWithAI: (data) => request.post('/ai/chat', data)
}

// 统计数据API
export const statsApi = {
  getDashboardStats: () => request.get('/stats/dashboard'),
  getUserStats: () => request.get('/stats/users'),
  getCourseStats: () => request.get('/stats/courses'),
  getChallengeStats: () => request.get('/stats/challenges')
} 