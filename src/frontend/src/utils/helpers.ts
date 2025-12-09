/**
 * 工具函数集合
 * 包含格式化、验证、防抖等常用函数
 */

/**
 * 格式化文件大小
 * @param bytes - 文件大小（字节）
 * @returns 格式化后的文件大小字符串
 */
export const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B'
    if (bytes < 0) return '无效大小'

    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

/**
 * 格式化日期
 * @param dateString - 日期字符串或Date对象
 * @param format - 格式模板
 * @returns 格式化后的日期字符串
 */
export const formatDate = (dateString: string | Date, format: string = 'YYYY-MM-DD'): string => {
    const date = new Date(dateString)

    if (isNaN(date.getTime())) {
        return '无效日期'
    }

    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')

    const formatMap: Record<string, string> = {
        'YYYY': String(year),
        'MM': month,
        'DD': day,
        'HH': hours,
        'mm': minutes,
        'ss': seconds
    }

    return format.replace(/YYYY|MM|DD|HH|mm|ss/g, match => formatMap[match])
}

/**
 * 防抖函数
 * @param func - 要执行的函数
 * @param wait - 等待时间（毫秒）
 * @returns 防抖后的函数
 */
export const debounce = <T extends (...args: any[]) => any>(func: T, wait: number): T => {
    let timeout: ReturnType<typeof setTimeout> | null = null

    return ((...args: Parameters<T>) => {
        if (timeout) clearTimeout(timeout)

        timeout = setTimeout(() => {
            func(...args)
            timeout = null
        }, wait)
    }) as T
}

/**
 * 节流函数
 * @param func - 要执行的函数
 * @param limit - 限制时间（毫秒）
 * @returns 节流后的函数
 */
export const throttle = <T extends (...args: any[]) => any>(func: T, limit: number): T => {
    let inThrottle: boolean = false

    return ((...args: Parameters<T>) => {
        if (!inThrottle) {
            func(...args)
            inThrottle = true

            setTimeout(() => {
                inThrottle = false
            }, limit)
        }
    }) as T
}

/**
 * 验证邮箱格式
 * @param email - 邮箱地址
 * @returns 是否有效
 */
export const isValidEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
}

/**
 * 验证URL格式
 * @param url - URL地址
 * @returns 是否有效
 */
export const isValidUrl = (url: string): boolean => {
    try {
        new URL(url)
        return true
    } catch {
        return false
    }
}

/**
 * 生成随机字符串
 * @param length - 字符串长度
 * @returns 随机字符串
 */
export const generateRandomString = (length: number = 8): string => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    let result = ''

    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
    }

    return result
}

/**
 * 深度克隆对象
 * @param obj - 要克隆的对象
 * @returns 克隆后的对象
 */
export const deepClone = <T>(obj: T): T => {
    if (obj === null || typeof obj !== 'object') {
        return obj
    }

    if (obj instanceof Date) {
        return new Date(obj.getTime()) as T
    }

    if (Array.isArray(obj)) {
        return obj.map(item => deepClone(item)) as T
    }

    if (typeof obj === 'object') {
        const clonedObj = {} as T
        for (const key in obj) {
            if (Object.prototype.hasOwnProperty.call(obj, key)) {
                clonedObj[key] = deepClone(obj[key])
            }
        }
        return clonedObj
    }

    return obj
}

/**
 * 安全获取对象属性
 * @param obj - 目标对象
 * @param path - 属性路径
 * @param defaultValue - 默认值
 * @returns 属性值或默认值
 */
export const getSafe = <T>(obj: any, path: string, defaultValue?: T): T | undefined => {
    const keys = path.split('.')
    let result = obj

    for (const key of keys) {
        if (result && typeof result === 'object' && key in result) {
            result = result[key]
        } else {
            return defaultValue
        }
    }

    return result as T
}

/**
 * 延迟执行
 * @param ms - 延迟时间（毫秒）
 * @returns Promise
 */
export const sleep = (ms: number): Promise<void> => {
    return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * 检查是否为空值
 * @param value - 要检查的值
 * @returns 是否为空
 */
export const isEmpty = (value: any): boolean => {
    if (value === null || value === undefined) {
        return true
    }

    if (typeof value === 'string' && value.trim() === '') {
        return true
    }

    if (Array.isArray(value) && value.length === 0) {
        return true
    }

    if (typeof value === 'object' && Object.keys(value).length === 0) {
        return true
    }

    return false
}

/**
 * 截断字符串
 * @param str - 原字符串
 * @param length - 最大长度
 * @param suffix - 后缀
 * @returns 截断后的字符串
 */
export const truncateString = (str: string, length: number, suffix: string = '...'): string => {
    if (str.length <= length) {
        return str
    }

    return str.slice(0, length) + suffix
}