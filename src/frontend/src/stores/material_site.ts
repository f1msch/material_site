import {defineStore} from 'pinia'
import {computed, ref, type Ref} from 'vue'
import {
    downloadMaterialApi as downloadMaterialApi,
    favoriteMaterialApi,
    getCategoriesApi,
    getMaterialIdApi,
    getMaterialsApi,
    getTagsApi,
    postMaterialsApi
} from "@/api/material";
import type {Category, Material, MaterialFilters, PaginationParams, Tag} from '@/types'

export const useMaterialStore = defineStore('materials', () => {
    const materials = ref<Material[]>([])
    const currentMaterial: Ref<Material | null> = ref<Material | null>(null)
    const categories = ref<Category[]>([])
    const tags = ref<Tag[]>([])
    const loading = ref<boolean>(false)

    const pagination = ref<PaginationParams>({
        current: 1,
        total: 0,
        pageSize: 12
    })

    const filters = ref<MaterialFilters>({
        category: '',
        tags: [],
        material_type: '',
        license_type: '',
        search: '',
        min_price: null,
        max_price: null
    })

    const filteredMaterials = computed<Material[]>(() => {
        return materials.value
    })

    const searchQuery = computed<string>(() => filters.value.search || '')

    const fetchMaterials = async (page: number = 1): Promise<void> => {
        loading.value = true
        try {
            const params: Record<string, any> = {
                page,
                ...filters.value,
                tags: filters.value.tags?.join(',')
            }

            Object.keys(params).forEach(key => {
                if (params[key] === '' || params[key] === null || params[key] === undefined || (Array.isArray(params[key]) && params[key].length === 0)) {
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
        } catch (error) {
            console.error('获取素材失败:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    const fetchMaterialDetail = async (materialId: number): Promise<Material> => {
        loading.value = true
        try {
            const response = await getMaterialIdApi(materialId)
            currentMaterial.value = response.data
            return response.data
        } catch (error) {
            console.error('获取素材详情失败:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    const uploadMaterial = async (formData: FormData): Promise<Material> => {
        try {
            const response = await postMaterialsApi(formData)

            materials.value.unshift(response.data)
            return response.data
        } catch (error) {
            console.error('上传素材失败:', error)
            throw error
        }
    }

    const favoriteMaterial = async (materialId: number): Promise<void> => {
        try {
            await favoriteMaterialApi(materialId)

            const material = materials.value.find((m: Material) => m.id === materialId)
            if (material) {
                material.is_favorite = !material.is_favorite
                material.favorite_count += material.is_favorite ? 1 : -1
            }

            if (currentMaterial.value && currentMaterial.value.id === materialId) {
                currentMaterial.value.is_favorite = !currentMaterial.value.is_favorite
                currentMaterial.value.favorite_count += currentMaterial.value.is_favorite ? 1 : -1
            }
        } catch (error) {
            console.error('收藏操作失败:', error)
            throw error
        }
    }

    const downloadMaterial = async (materialId: number): Promise<{ download_url: string }> => {
        try {
            const response = await downloadMaterialApi(materialId)

            return response.data
        } catch (error) {
            console.error('下载失败:', error)
            throw error
        }
    }

    const updateFilters = (newFilters: Partial<MaterialFilters>): void => {
        filters.value = {...filters.value, ...newFilters}
        pagination.value.current = 1
    }

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

    const fetchCategories = async (): Promise<void> => {
        try {
            const response = await getCategoriesApi()
            categories.value = response.data
            console.log('categories.value is ', categories.value)
        } catch (error) {
            console.error('获取分类失败:', error)
            throw error
        }
    }

    const fetchTags = async (): Promise<void> => {
        try {
            const response = await getTagsApi()
            tags.value = response.data
        } catch (error) {
            console.error('获取标签失败:', error)
            throw error
        }
    }

    return {
        materials,
        currentMaterial,
        categories,
        tags,
        loading,
        pagination,
        filters,
        filteredMaterials,
        searchQuery,
        fetchMaterials,
        fetchMaterialDetail,
        uploadMaterial,
        favoriteMaterial,
        downloadMaterial,
        updateFilters,
        clearFilters,
        fetchCategories,
        fetchTags
    }
})