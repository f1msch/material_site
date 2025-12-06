import $api from "@/api/index"
import type {Category, Material, MaterialFilters, PaginatedResponse, Tag} from '@/types'
import type {AxiosResponse} from 'axios'

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

export const uploadMaterialFileApi = async (formData: FormData, onProgress?: (progress: number) => void): Promise<AxiosResponse<Material>> => {
    return $api.post('/api/materials/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent): void => {
            const progress = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
            )
            if (onProgress) onProgress(progress)
        }
    })
}

export const uploadFileApi = async (fileData: FormData): Promise<AxiosResponse<any>> => {
    return $api.post('/api/upload/', fileData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}


