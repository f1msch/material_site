/**
 * 用户Store
 * 管理用户认证和资料相关状态
 */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { LoginForm, RegisterForm, User } from '@/types'
import { loginApi, registerApi, logoutApi, getCurrentUserApi, updateProfileApi } from '@/api/user'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
    // ========== State ==========
    const user = ref<User | null>(null)
    const token = ref<string | null>(localStorage.getItem('auth_token'))
    const loading = ref<boolean>(false)
    const error = ref<string | null>(null)

    // ========== Getters ==========
    const isAuthenticated = computed<boolean>(() => !!token.value)

    // ========== Actions ==========
    /**
     * 用户登录
     * @param credentials - 登录凭证（用户名和密码）
     * @returns 用户数据
     */
    const login = async (credentials: LoginForm): Promise<User> => {
        if (loading.value) throw new Error('已有请求在进行中')

        loading.value = true
        error.value = null

        try {
            const response = await loginApi(credentials)
            const { user: userData, access } = response.data

            // 更新状态
            user.value = userData
            token.value = access

            // 保存token到本地存储
            localStorage.setItem('auth_token', access)

            return userData
        } catch (err: any) {
            error.value = err.response?.data?.message || '登录失败'
            console.error('登录失败:', err)
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 用户注册
     * @param userData - 注册信息
     * @returns 注册结果
     */
    const register = async (userData: RegisterForm): Promise<{ user: User; message: string }> => {
        if (loading.value) throw new Error('已有请求在进行中')

        loading.value = true
        error.value = null

        try {
            const response = await registerApi(userData)
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '注册失败'
            console.error('注册失败:', err)
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 用户登出
     */
    const logout = (): void => {
        try {
            // 调用登出API（可选）
            logoutApi().catch(() => {
                // 忽略登出API错误，确保本地登出成功
            })

            // 清除本地状态
            user.value = null
            token.value = null
            localStorage.removeItem('auth_token')

            // 跳转到登录页
            router.push('/login')
        } catch (err) {
            console.error('登出失败:', err)
            throw err
        }
    }

    /**
     * 获取当前用户资料
     * @returns 用户数据
     */
    const fetchProfile = async (): Promise<User> => {
        if (!token.value) {
            throw new Error('未登录')
        }

        if (loading.value) throw new Error('已有请求在进行中')

        loading.value = true
        error.value = null

        try {
            const response = await getCurrentUserApi()
            user.value = response.data
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '获取用户信息失败'

            // Token无效时清除本地状态
            if (err.response?.status === 401) {
                logout()
            }

            console.error('获取用户信息失败:', err)
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 更新用户资料
     * @param profileData - 要更新的资料数据
     * @returns 更新后的用户数据
     */
    const updateProfile = async (profileData: Partial<User>): Promise<User> => {
        if (!token.value) {
            throw new Error('未登录')
        }

        if (loading.value) throw new Error('已有请求在进行中')

        loading.value = true
        error.value = null

        try {
            const response = await updateProfileApi(profileData)
            user.value = response.data
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '更新个人信息失败'
            console.error('更新个人信息失败:', err)
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 检查登录状态
     * 如果本地有token但未获取用户信息，则自动获取
     */
    const checkAuth = async (): Promise<boolean> => {
        if (token.value && !user.value) {
            try {
                await fetchProfile()
                return true
            } catch {
                // 获取失败，清除无效token
                logout()
                return false
            }
        }
        return !!user.value
    }

    /**
     * 清除错误信息
     */
    const clearError = (): void => {
        error.value = null
    }

    return {
        // State
        user,
        token,
        loading,
        error,

        // Getters
        isAuthenticated,

        // Actions
        login,
        register,
        logout,
        fetchProfile,
        updateProfile,
        checkAuth,
        clearError
    }
})