import $api from "@/api/index"
import type {LoginForm, RegisterForm, User} from '@/types'
import type {AxiosResponse} from 'axios'

export const loginApi = async (credentials: LoginForm): Promise<AxiosResponse<{
    access: string;
    refresh: string;
    user: User
}>> => {
    return $api.post('/api/auth/login/', credentials)
}

export const registerApi = async (userData: RegisterForm): Promise<AxiosResponse<{ user: User; message: string }>> => {
    return $api.post('/api/auth/register/', userData)
}

export const logoutApi = async (): Promise<AxiosResponse<{ message: string }>> => {
    return $api.post('/api/auth/logout/')
}

export const refreshTokenApi = async (refresh: string): Promise<AxiosResponse<{ access: string }>> => {
    return $api.post('/api/auth/refresh/', {refresh})
}

export const getCurrentUserApi = async (): Promise<AxiosResponse<User>> => {
    return $api.get('/api/auth/user/')
}

export const updateProfileApi = async (userData: Partial<User>): Promise<AxiosResponse<User>> => {
    return $api.put('/api/auth/profile/', userData)
}

export const changePasswordApi = async (data: { old_password: string; new_password: string }): Promise<AxiosResponse<{
    message: string
}>> => {
    return $api.post('/api/auth/change-password/', data)
}