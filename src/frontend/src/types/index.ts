/**
 * API类型定义
 * 所有API接口使用的类型定义
 */

// ========== 基础类型 ==========
export interface ApiResponse<T = any> {
    data: T
    status: number
    statusText: string
    headers: Record<string, string>
}

export interface PaginatedResponse<T> {
    count: number
    next: string | null
    previous: string | null
    results: T[]
}

export interface ErrorResponse {
    error: boolean
    message: string
    code: string
    timestamp?: number
    debug?: {
        exception_type: string
        traceback: string[]
    }
}

// ========== 用户相关 ==========
export interface User {
    id: number
    username: string
    email: string
    first_name?: string
    last_name?: string
    avatar?: string
    bio?: string
    website?: string
    credits: number
    materials_count: number
    downloads_count: number
    is_premium: boolean
    date_joined: string
    created_at?: string
    updated_at?: string
}

export interface LoginForm {
    username: string
    password: string
}

export interface RegisterForm {
    username: string
    email: string
    password: string
    password_confirm: string
}

export interface UpdateProfileData {
    email?: string
    bio?: string
    website?: string
    avatar?: File
}

// ========== 素材相关 ==========
export interface Material {
    id: number
    title: string
    description: string
    slug: string
    material_type: 'image' | 'vector' | 'video' | 'audio' | 'template' | 'font' | 'other'
    main_file: string
    thumbnail?: string
    preview_image?: string
    file_size: number
    file_size_display: string
    dimensions?: string
    duration?: number
    category?: Category
    tags: Tag[]
    author: User
    price: number
    license_type: 'free' | 'premium' | 'cc-by' | 'cc-by-sa'
    view_count: number
    download_count: number
    like_count: number
    favorite_count: number
    is_favorite: boolean
    is_featured: boolean
    status: 'draft' | 'pending' | 'approved' | 'rejected'
    created_at: string
    updated_at: string
    published_at?: string
}

export interface Category {
    id: number
    name: string
    slug: string
    description?: string
    parent?: Category
    icon?: string
    is_active: boolean
    material_count?: number
    created_at: string
}

export interface Tag {
    id: number
    name: string
    slug: string
    color?: string
    created_at: string
}

// ========== 素材筛选 ==========
export interface MaterialFilters {
    category?: string
    tags?: string[]
    material_type?: string
    license_type?: string
    search?: string
    min_price?: number | null
    max_price?: number | null
    is_featured?: boolean
    ordering?: string
}

export interface PaginationParams {
    current?: number
    total?: number
    pageSize?: number
}

// ========== 上传相关 ==========
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

export interface CreateMaterialData {
    title: string
    description?: string
    material_type: string
    category?: string
    tags: string[]
    license_type: string
    price?: number
    is_featured?: boolean
}

// ========== 收藏相关 ==========
export interface Favorite {
    id: number
    material: Material
    created_at: string
}

// ========== 下载相关 ==========
export interface DownloadResponse {
    download_url: string
    download_count: number
}

// ========== 路由相关 ==========
export interface RouteMetaCustom {
    title?: string
    requiresAuth?: boolean
    layout?: string
}

// ========== Store状态 ==========
export interface MaterialState {
    materials: Material[]
    currentMaterial: Material | null
    categories: Category[]
    tags: Tag[]
    loading: boolean
    pagination: PaginationParams
    filters: MaterialFilters
}

export interface UserState {
    user: User | null
    token: string | null
    isAuthenticated: boolean
    loading: boolean
}

export interface UploadState {
    uploadProgress: number
    isUploading: boolean
    uploadQueue: UploadFile[]
    uploadedMaterials: Material[]
}

// ========== 常量类型 ==========
export const MATERIAL_TYPES = ['image', 'vector', 'video', 'audio', 'template', 'font', 'other'] as const
export const LICENSE_TYPES = ['free', 'premium', 'cc-by', 'cc-by-sa'] as const
export const MATERIAL_STATUS = ['draft', 'pending', 'approved', 'rejected'] as const

export type MaterialType = typeof MATERIAL_TYPES[number]
export type LicenseType = typeof LICENSE_TYPES[number]
export type MaterialStatus = typeof MATERIAL_STATUS[number]