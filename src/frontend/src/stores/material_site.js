import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import $api from '@/services/api'

export const useMaterialStore = defineStore('materials', () => {
  const materials = ref([])
  const currentMaterial = ref(null)
  const categories = ref([])
  const tags = ref([])
  const loading = ref(false)

  const pagination = ref({
    current: 1,
    total: 0,
    pageSize: 12
  })

  const filters = ref({
    category: '',
    tags: [],
    material_type: '',
    license_type: '',
    search: '',
    min_price: null,
    max_price: null
  })

  const filteredMaterials = computed(() => {
    return materials.value
  })

  const searchQuery = computed(() => filters.value.search)

  const fetchMaterials = async (page = 1) => {
    loading.value = true
    try {
      const params = {
        page,
        ...filters.value,
        tags: filters.value.tags.join(',')
      }

      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === null || params[key] === undefined || params[key].length === 0) {
          delete params[key]
        }
      })
      console.log('params is ', params)

      const response = await $api.get('/api/materials/', { params })
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

  const fetchMaterialDetail = async (materialId) => {
    loading.value = true
    try {
      const response = await $api.get(`/api/materials/${materialId}/`)
      currentMaterial.value = response.data
      return response.data
    } catch (error) {
      console.error('获取素材详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const uploadMaterial = async (formData) => {
    try {
      const response = await $api.post('/api/materials/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      materials.value.unshift(response.data)
      return response.data
    } catch (error) {
      console.error('上传素材失败:', error)
      throw error
    }
  }

  const favoriteMaterial = async (materialId) => {
    try {
      await $api.post(`/api/materials/${materialId}/favorite/`)

      const material = materials.value.find(m => m.id === materialId)
      if (material) {
        material.is_favorited = !material.is_favorited
        material.favorite_count += material.is_favorited ? 1 : -1
      }

      if (currentMaterial.value && currentMaterial.value.id === materialId) {
        currentMaterial.value.is_favorited = !currentMaterial.value.is_favorited
        currentMaterial.value.favorite_count += currentMaterial.value.is_favorited ? 1 : -1
      }
    } catch (error) {
      console.error('收藏操作失败:', error)
      throw error
    }
  }

  const downloadMaterial = async (materialId) => {
    try {
      const response = await $api.post(`/api/materials/${materialId}/download/`)

      const material = materials.value.find(m => m.id === materialId)
      if (material) {
        material.download_count += 1
      }

      return response.data
    } catch (error) {
      console.error('下载失败:', error)
      throw error
    }
  }

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.current = 1
  }

  const clearFilters = () => {
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

  const fetchCategories = async () => {
    try {
        const response = await $api.get('/api/categories/')
        categories.value = response.data
        console.log('categories.value is ', categories.value)
    } catch (error) {
      console.error('获取分类失败:', error)
      throw error
    }
  }

  const fetchTags = async () => {
    try {
      const response = await $api.get('/api/tags/')
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