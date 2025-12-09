/**
 * Axios实例配置和拦截器
 * 统一处理请求和响应，包含错误处理
 */

import type { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import axios from 'axios'
import type { ErrorResponse } from '@/types'

// 创建axios实例
const $api: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    timeout: 30000, // 30秒超时
    headers: {
        'Content-Type': 'application/json',
    },
})

// ========== 请求拦截器 ==========
$api.interceptors.request.use(
    (config: AxiosRequestConfig) => {
        // 添加认证token
        const token = localStorage.getItem('auth_token')
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`
        }

        // 记录请求日志（开发环境）
        if (import.meta.env.DEV) {
            console.log(`📡 API Request: ${config.method?.toUpperCase()} ${config.url}`, {
                params: config.params,
                data: config.data,
            })
        }

        return config
    },
    (error: AxiosError) => {
        // 请求配置错误
        console.error('❌ Request config error:', error)
        return Promise.reject(error)
    }
)

// ========== 响应拦截器 ==========
$api.interceptors.response.use(
    (response: AxiosResponse) => {
        // 记录响应日志（开发环境）
        if (import.meta.env.DEV) {
            console.log(`✅ API Response: ${response.status} ${response.config.url}`, {
                data: response.data,
                headers: response.headers,
            })
        }
        return response
    },
    (error: AxiosError<ErrorResponse>) => {
        // 统一错误处理
        const response = error.response
        const config = error.config

        console.error('❌ API Error:', {
            url: config?.url,
            method: config?.method,
            status: response?.status,
            data: response?.data,
            message: error.message,
        })

        // 处理不同状态码
        if (response) {
            switch (response.status) {
                case 400:
                    console.error('请求参数错误:', response.data)
                    break
                case 401:
                    // Token过期或无效
                    localStorage.removeItem('auth_token')
                    window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname)
                    break
                case 403:
                    console.error('权限不足:', response.data)
                    break
                case 404:
                    console.error('资源不存在:', response.data)
                    break
                case 422:
                    console.error('数据验证失败:', response.data)
                    break
                case 429:
                    console.error('请求过于频繁，请稍后重试')
                    break
                case 500:
                case 502:
                case 503:
                case 504:
                    console.error('服务器错误:', response.data)
                    break
                default:
                    console.error('未知错误:', response.data)
            }

            // 显示错误提示（根据环境）
            if (import.meta.env.DEV) {
                const errorData = response.data as ErrorResponse
                const errorMsg = errorData.message || '请求失败'
                alert(`错误: ${errorMsg}`)
            }
        } else if (error.code === 'ECONNABORTED') {
            console.error('请求超时，请检查网络连接')
            alert('请求超时，请检查网络连接')
        } else if (error.code === 'NETWORK_ERROR') {
            console.error('网络错误，请检查网络连接')
            alert('网络错误，请检查网络连接')
        } else {
            console.error('未知网络错误:', error.message)
        }

        return Promise.reject(error)
    }
)

export default $api