/**
 * 素材Store
 * 管理素材相关的状态和操作
 */

import { defineStore } from 'pinia'
import { computed, ref, type Ref } from 'vue'
import type { Category, Material, MaterialFilters, PaginationParams, Tag } from '@/types'
import {
    downloadMaterialApi,
    favoriteMaterialApi,
    getCategoriesApi,
    getMaterialIdApi,
    getMaterialsApi,
    getTagsApi,
    postMaterialsApi
} from "@/api/material"

export const useMaterialStore = defineStore('materials', () => {
    // ========== State ==========
    const materials: Ref<Material[]> = ref<Material[]>([])
    const currentMaterial: Ref<Material | null> = ref<Material | null>(null)
    const categories: Ref<Category[]> = ref<Category[]>([])
    const tags: Ref<Tag[]> = ref<Tag[]>([])
    const loading: Ref<boolean> = ref<boolean>(false)
    const error: Ref<string | null> = ref<string | null>(null)

    const pagination: Ref<PaginationParams> = ref<PaginationParams>({
        current: 1,
        total: 0,
        pageSize: 12
    })

    const filters: Ref<MaterialFilters> = ref<MaterialFilters>({
        category: '',
        tags: [],
        material_type: '',
        license_type: '',
        search: '',
        min_price: null,
        max_price: null
    })

    // ========== Getters ==========
    const filteredMaterials = computed<Material[]>(() => {
        return materials.value
    })

    const searchQuery = computed<string>(() => filters.value.search || '')

    // ========== Actions ==========
    /**
     * 获取素材列表
     * @param page - 页码，默认1
     */
    const fetchMaterials = async (page: number = 1): Promise<void> => {
        if (loading.value) return

        loading.value = true
        error.value = null

        try {
            const params: Record<string, any> = {
                page,
                ...filters.value,
                tags: filters.value.tags?.join(',')
            }

            // 清理空参数
            Object.keys(params).forEach(key => {
                if (params[key] === '' || params[key] === null || params[key] === undefined ||
                    (Array.isArray(params[key]) && params[key].length === 0)) {
                    delete params[key]
                }
            })

            const response = await getMaterialsApi(params)
            materials.value = response.data.results
            pagination.value = {
                current: page,
                total: response.data.count,
                pageSize: 12
            }
        } catch (err: any) {
            error.value = err.response?.data?.message || '获取素材失败'
            console.error('获取素材失败:', err)
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 获取素材详情
     * @param materialId - 素材ID
     * @returns 素材详情数据
     */
    const fetchMaterialDetail = async (materialId: number): Promise<Material> => {
        if (loading.value) throw new Error('已有请求在进行中')

        loading.value = true
        error.value = null

        try {
            const response = await getMaterialIdApi(materialId)
            currentMaterial.value = response.data
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '获取素材详情失败'
            console.error('获取素材详情失败:', err)
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 上传素材
     * @param formData - FormData对象，包含素材文件和信息
     * @returns 上传的素材数据
     */
    const uploadMaterial = async (formData: FormData): Promise<Material> => {
        try {
            const response = await postMaterialsApi(formData)

            // 添加到素材列表
            materials.value.unshift(response.data)

            // 更新分页总数
            if (pagination.value.total !== undefined) {
                pagination.value.total += 1
            }

            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '上传素材失败'
            console.error('上传素材失败:', err)
            throw err
        }
    }

    /**
     * 收藏/取消收藏素材
     * @param materialId - 素材ID
     */
    const favoriteMaterial = async (materialId: number): Promise<void> => {
        try {
            await favoriteMaterialApi(materialId)

            // 更新本地状态
            const material = materials.value.find((m: Material) => m.id === materialId)
            if (material) {
                material.is_favorite = !material.is_favorite
                material.favorite_count += material.is_favorite ? 1 : -1
            }

            if (currentMaterial.value && currentMaterial.value.id === materialId) {
                currentMaterial.value.is_favorite = !currentMaterial.value.is_favorite
                currentMaterial.value.favorite_count += currentMaterial.value.is_favorite ? 1 : -1
            }
        } catch (err: any) {
            error.value = err.response?.data?.message || '收藏操作失败'
            console.error('收藏操作失败:', err)
            throw err
        }
    }

    /**
     * 下载素材
     * @param materialId - 素材ID
     * @returns 下载URL
     */
    const downloadMaterial = async (materialId: number): Promise<{ download_url: string }> => {
        try {
            const response = await downloadMaterialApi(materialId)

            // 更新本地统计
            const material = materials.value.find((m: Material) => m.id === materialId)
            if (material) {
                material.download_count += 1
            }

            if (currentMaterial.value && currentMaterial.value.id === materialId) {
                currentMaterial.value.download_count += 1
            }

            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '下载失败'
            console.error('下载失败:', err)
            throw err
        }
    }

    /**
     * 更新筛选条件
     * @param newFilters - 新的筛选条件
     */
    const updateFilters = (newFilters: Partial<MaterialFilters>): void => {
        filters.value = { ...filters.value, ...newFilters }
        pagination.value.current = 1
    }

    /**
     * 清除筛选条件
     */
    const clearFilters = (): void => {
        filters.value = {
            category: '',
            tags: [],
            material_type: '',
            license_type: '',
            search: '',
            min_price: null,
            max_price: null
        }
        pagination.value.current = 1
    }

    /**
     * 获取分类列表
     */
    const fetchCategories = async (): Promise<void> => {
        try {
            const response = await getCategoriesApi()
            categories.value = response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '获取分类失败'
            console.error('获取分类失败:', err)
            throw err
        }
    }

    /**
     * 获取标签列表
     */
    const fetchTags = async (): Promise<void> => {
        try {
            const response = await getTagsApi()
            tags.value = response.data
        } catch (err: any) {
            error.value = err.response?.data?.message || '获取标签失败'
            console.error('获取标签失败:', err)
            throw err
        }
    }

    /**
     * 清除错误信息
     */
    const clearError = (): void => {
        error.value = null
    }

    return {
        // State
        materials,
        currentMaterial,
        categories,
        tags,
        loading,
        error,
        pagination,
        filters,

        // Getters
        filteredMaterials,
        searchQuery,

        // Actions
        fetchMaterials,
        fetchMaterialDetail,
        uploadMaterial,
        favoriteMaterial,
        downloadMaterial,
        updateFilters,
        clearFilters,
        fetchCategories,
        fetchTags,
        clearError
    }
})