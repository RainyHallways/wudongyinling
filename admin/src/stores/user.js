import { defineStore } from 'pinia'
import { userApi } from '@/api'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}')
  }),

  actions: {
    async login(data) {
      try {
        const res = await userApi.login(data)
        this.token = res.access_token
        localStorage.setItem('token', res.access_token)
        return true
      } catch (error) {
        ElMessage.error('登录失败')
        return false
      }
    },

    async getUserInfo() {
      try {
        const res = await userApi.getUserInfo()
        this.userInfo = res
        localStorage.setItem('userInfo', JSON.stringify(res))
      } catch (error) {
        ElMessage.error('获取用户信息失败')
      }
    },

    logout() {
      this.token = ''
      this.userInfo = {}
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  }
}) 