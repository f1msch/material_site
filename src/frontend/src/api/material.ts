import $api from "@/api/index"
import type {Category, Material, MaterialFilters, PaginatedResponse, Tag} from '@/types'
import type {AxiosProgressEvent, AxiosResponse} from 'axios'

export const postMaterialsApi = async (fromData: FormData): Promise<AxiosResponse<Material>> => {
    return $api.post('/api/materials/', fromData, {
        headers: {'Content-Type': 'multipart/form-data'}
    })
}

export const getMaterialsApi = async (params: MaterialFilters & {
    page?: number
}): Promise<AxiosResponse<PaginatedResponse<Material>>> => {
    return $api.get('/api/materials/', {params})
}

export const getMaterialIdApi = async (materialId: number): Promise<AxiosResponse<Material>> => {
    return $api.get(`/api/materials/${materialId}/`)
}

export const favoriteMaterialApi = async (materialId: number): Promise<AxiosResponse<void>> => {
    return $api.post(`/api/materials/${materialId}/favorite/`)
}

export const downloadMaterialApi = async (materialId: number): Promise<AxiosResponse<{ download_url: string }>> => {
    return $api.post(`/api/materials/${materialId}/download/`)
}

export const getCategoriesApi = async (): Promise<AxiosResponse<Category[]>> => {
    return $api.get('/api/categories/')
}

export const getTagsApi = async (): Promise<AxiosResponse<Tag[]>> => {
    return $api.get('/api/tags/')
}

const calculateProgress = (progressEvent: AxiosProgressEvent): number => {
    // 情况1：有确切的总大小
    if (progressEvent.total && progressEvent.total > 0) {
        return Math.round((progressEvent.loaded * 100) / progressEvent.total)
    }

    // 情况2：使用 axios 自带的 progress（0-1之间）
    if (progressEvent.progress !== undefined) {
        return Math.round(progressEvent.progress * 100)
    }

    // 情况3：使用估算（每1MB算5%）
    const mbUploaded = progressEvent.loaded / (1024 * 1024)
    return Math.min(Math.round(mbUploaded * 5), 99) // 最多99%
}

// 浏览器上传文件
export const uploadMaterialFileApi = async (formData: FormData, onProgress?: (progress: number) => void): Promise<AxiosResponse<Material>> => {
    return $api.post('/api/materials/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent: AxiosProgressEvent): void => {
            const progress = calculateProgress(progressEvent)
            if (onProgress && progress >= 0) onProgress(progress)
        }
    })
}

