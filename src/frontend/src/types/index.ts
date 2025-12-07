// API 响应通用类型
export interface ApiResponse<T = any> {
    data: T
    status: number
    statusText: string
    headers: Record<string, string>
}

// 分页响应类型
export interface PaginatedResponse<T> {
    count: number
    next: string | null
    previous: string | null
    results: T[]
}

// 用户相关类型
export interface User {
    id: number
    username: string
    email: string
    first_name: string
    last_name: string
    avatar?: string
    is_premium: boolean
    created_at: string
    updated_at: string
}

export interface LoginForm {
    username: string
    password: string
}

export interface RegisterForm {
    username: string
    email: string
    password: string
    password2: string
    first_name: string
    last_name: string
}

// 素材相关类型
export interface Material {
    id: number
    title: string
    description: string
    main_file: string
    thumbnail: string
    preview_image: string
    file_type: string
    file_size: number
    material_type: string
    dimensions: string
    duration: number
    file_size_display: number
    category: Category
    tags: Tag[]
    author: User
    price: number
    is_free: boolean
    license_type: string
    view_count: number
    download_count: number
    like_count: number
    favorite_count: number
    is_favorite: boolean
    status: string
    created_at: string
    updated_at: string
}

export interface Category {
    id: number
    slug: string
    name: string
    description?: string
    parent?: Category
    created_at: string
}

export interface Tag {
    id: number
    slug: string
    name: string
    color?: string
    created_at: string
}

// 素材筛选参数类型
export interface MaterialFilters {
    category?: string
    tags?: string[]
    material_type?: string
    license_type?: string
    search?: string
    min_price?: number | null
    max_price?: number | null
}

// 分页参数类型
export interface PaginationParams {
    current?: number
    total?: number
    pageSize?: number
}

// 上传相关类型
export interface UploadProgress {
    loaded: number
    total: number
    percentage: number
}

export interface UploadFile {
    file: File
    progress: UploadProgress
    status: 'pending' | 'uploading' | 'success' | 'error'
    error?: string
}

// 支付相关类型
export interface PaymentOrder {
    id: number
    order_id: string
    user: number | User
    material?: Material
    amount: number
    status: string
    payment_method: string
    payment_url?: string
    qr_code?: string
    created_at: string
    updated_at: string
}

export interface CreatePaymentData {
    user: string | number
    description: string
    material?: number
    plan?: string
    amount?: number
}

// 路由元数据类型
export interface RouteMetaCustom {
    title?: string
    requiresAuth?: boolean
    layout?: string
}

// 组件 Props 类型
export interface MaterialCardProps {
    material: Material
    loading?: boolean
}

export interface PaginationProps {
    current: number
    total: number
    pageSize: number
    loading?: boolean
}

export interface UploadProgressProps {
    progress: UploadProgress
    file: UploadFile
}

// Store 状态类型
export interface MaterialState {
    materials: Material[]
    currentMaterial: Material | null
    categories: Category[]
    tags: Tag[]
    loading: boolean
    pagination: {
        current: number
        total: number
        pageSize: number
    }
    filters: MaterialFilters
}

export interface UserState {
    user: User | null
    token: string | null
    isAuthenticated: boolean
    loading: boolean
}

export interface PaymentState {
    orders: PaymentOrder[]
    currentOrder: PaymentOrder | null
    loading: boolean
}

export interface UploadState {
    files: UploadFile[]
    isUploading: boolean
    progress: number
}

// 工具函数类型
export interface DownloadOptions {
    filename?: string
    openInNewTab?: boolean
}

// 表单验证规则类型
export interface FormRule {
    required?: boolean
    message?: string
    trigger?: string
    min?: number
    max?: number
    pattern?: RegExp
    validator?: (rule: any, value: any, callback: any) => void
}

export interface FormRules {
    [key: string]: FormRule | FormRule[]
}

// 常量类型
export const MATERIAL_TYPES = ['image', 'video', 'document', 'audio', 'other'] as const
export const LICENSE_TYPES = ['free', 'premium', 'commercial', 'personal'] as const
export const PAYMENT_METHODS = ['alipay', 'wechat', 'paypal'] as const

export type MaterialType = typeof MATERIAL_TYPES[number]
export type LicenseType = typeof LICENSE_TYPES[number]
export type PaymentMethod = typeof PAYMENT_METHODS[number]