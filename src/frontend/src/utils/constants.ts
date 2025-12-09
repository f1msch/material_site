/**
 * 应用常量定义
 * 包含素材类型、文件类型、许可类型等常量
 */

// ========== 素材类型 ==========
export const MATERIAL_TYPES = {
    image: { value: 'image', label: '图片', icon: '🖼️' },
    vector: { value: 'vector', label: '矢量图', icon: '📐' },
    video: { value: 'video', label: '视频', icon: '🎬' },
    audio: { value: 'audio', label: '音频', icon: '🎵' },
    template: { value: 'template', label: '模板', icon: '📄' },
    font: { value: 'font', label: '字体', icon: '🔤' },
    other: { value: 'other', label: '其他', icon: '📎' }
} as const

// ========== 许可类型 ==========
export const LICENSE_TYPES = {
    free: { value: 'free', label: '免费', color: 'green' },
    premium: { value: 'premium', label: '付费', color: 'orange' },
    'cc-by': { value: 'cc-by', label: 'CC BY', color: 'blue' },
    'cc-by-sa': { value: 'cc-by-sa', label: 'CC BY-SA', color: 'purple' }
} as const

// ========== 素材状态 ==========
export const MATERIAL_STATUS = {
    draft: { value: 'draft', label: '草稿', color: 'gray' },
    pending: { value: 'pending', label: '待审核', color: 'yellow' },
    approved: { value: 'approved', label: '已发布', color: 'green' },
    rejected: { value: 'rejected', label: '已拒绝', color: 'red' }
} as const

// ========== 文件类型接受格式 ==========
export const FILE_ACCEPT_TYPES: Record<string, string> = {
    image: 'image/*',
    vector: '.svg,.ai,.eps,.pdf',
    video: 'video/*',
    audio: 'audio/*',
    template: '.psd,.xd,.sketch,.fig,.indd',
    font: '.ttf,.otf,.woff,.woff2',
    other: '*'
}

// ========== 文件大小限制 ==========
export const MAX_FILE_SIZE = 100 * 1024 * 1024 // 100MB
export const MAX_IMAGE_SIZE = 10 * 1024 * 1024 // 10MB
export const MAX_THUMBNAIL_SIZE = 2 * 1024 * 1024 // 2MB

// ========== 分页配置 ==========
export const PAGINATION_CONFIG = {
    DEFAULT_PAGE_SIZE: 12,
    PAGE_SIZE_OPTIONS: [12, 24, 48, 96],
    MAX_PAGE_SIZE: 100
}

// ========== 上传配置 ==========
export const UPLOAD_CONFIG = {
    MAX_CONCURRENT_UPLOADS: 3,
    RETRY_COUNT: 3,
    RETRY_DELAY: 1000 // 1秒
}

// ========== 错误码 ==========
export const ERROR_CODES = {
    VALIDATION_ERROR: 'validation_error',
    AUTHENTICATION_ERROR: 'authentication_failed',
    PERMISSION_ERROR: 'permission_denied',
    NOT_FOUND: 'not_found',
    SERVER_ERROR: 'server_error',
    NETWORK_ERROR: 'network_error',
    TIMEOUT_ERROR: 'timeout_error'
} as const

// ========== API配置 ==========
export const API_CONFIG = {
    TIMEOUT: 30000,
    BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    UPLOAD_TIMEOUT: 60000
} as const

// ========== 路由配置 ==========
export const ROUTES = {
    HOME: '/',
    MATERIALS: '/materials',
    MATERIAL_DETAIL: '/materials/:id',
    UPLOAD: '/upload',
    PROFILE: '/profile',
    LOGIN: '/login',
    REGISTER: '/register'
} as const