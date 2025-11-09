import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import $api from '@/services/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token'))

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials) => {
    try {
      const response = await $api.post('/api/auth/login/', credentials)
      const { user: userData, access } = response.data

      user.value = userData
      token.value = access
      localStorage.setItem('auth_token', access)

      return userData
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const register = async (userData) => {
    try {
      const response = await $api.post('/api/auth/register/', userData)
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const fetchProfile = async () => {
    try {
      const response = await $api.get('/api/auth/profile/')
      user.value = response.data
      return response.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await $api.patch('/api/auth/profile/', profileData)
      user.value = response.data
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    fetchProfile,
    updateProfile
  }
})