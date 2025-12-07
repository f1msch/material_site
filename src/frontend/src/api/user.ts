import $api from "@/api/index"
import type {LoginForm, RegisterForm, User} from '@/types'
import type {AxiosResponse} from 'axios'

export const login = async (credentials: LoginForm): Promise<AxiosResponse<{
    access: string;
    refresh: string;
    user: User
}>> => {
    return $api.post('/api/auth/login/', credentials)
}

export const register = async (userData: RegisterForm): Promise<AxiosResponse<{ user: User; message: string }>> => {
    return $api.post('/api/auth/register/', userData)
}

export const logout = async (): Promise<AxiosResponse<{ message: string }>> => {
    return $api.post('/api/auth/logout/')
}

export const refreshToken = async (refresh: string): Promise<AxiosResponse<{ access: string }>> => {
    return $api.post('/api/auth/refresh/', {refresh})
}

export const getCurrentUser = async (): Promise<AxiosResponse<User>> => {
    return $api.get('/api/auth/user/')
}

export const updateProfile = async (userData: Partial<User>): Promise<AxiosResponse<User>> => {
    return $api.put('/api/auth/profile/', userData)
}

export const changePassword = async (data: { old_password: string; new_password: string }): Promise<AxiosResponse<{
    message: string
}>> => {
    return $api.post('/api/auth/change-password/', data)
}