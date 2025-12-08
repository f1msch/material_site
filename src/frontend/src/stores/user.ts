import {defineStore} from 'pinia'
import {computed, ref} from 'vue'
import {loginApi, registerApi, updateProfileApi} from '@/api/user'
import type {LoginForm, RegisterForm} from '@/types'

export const useUserStore = defineStore('user', () => {
    const user = ref<User | null>(null)
    const token = ref<string | null>(localStorage.getItem('auth_token'))
    const loading = ref<boolean>(false)

    const isAuthenticated = computed<boolean>(() => !!token.value)

    const login = async (credentials: LoginForm): Promise<User> => {
        loading.value = true
        try {
            const response = await loginApi(credentials)
            const {user: userData, access} = response.data

            user.value = userData
            token.value = access
            localStorage.setItem('auth_token', access)

            return userData
        } catch (error: any) {
            throw error.response?.data || error
        } finally {
            loading.value = false
        }
    }

    const register = async (userData: RegisterForm): Promise<{ user: User; message: string }> => {
        loading.value = true
        try {
            const response = await registerApi(userData)
            return response.data
        } catch (error: AxiosError) {
            throw error.response?.data || error
        } finally {
            loading.value = false
        }
    }

    const logout = (): void => {
        user.value = null
        token.value = null
        localStorage.removeItem('auth_token')
    }

    const fetchProfile = async (): Promise<User> => {
        loading.value = true
        try {
            const response = await getCurrentUser()
            user.value = response.data
            return response.data
        } catch (error) {
            console.error('获取用户信息失败:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    const updateProfile = async (profileData: Partial<User>): Promise<User> => {
        loading.value = true
        try {
            const response = await updateProfileApi(profileData)
            user.value = response.data
            return response.data
        } catch (error: any) {
            throw error.response?.data || error
        } finally {
            loading.value = false
        }
    }

    return {
        user,
        token,
        loading,
        isAuthenticated,
        login,
        register,
        logout,
        fetchProfile,
        updateProfile
    }
})