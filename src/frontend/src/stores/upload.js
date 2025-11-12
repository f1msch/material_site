import { defineStore } from 'pinia'
import { ref } from 'vue'
import $api from '@/services/api'

export const useUploadStore = defineStore('upload', () => {
  const uploadProgress = ref(0)
  const isUploading = ref(false)
  const uploadQueue = ref([])
  const uploadedMaterials = ref([])

  const uploadMaterial = async (formData, onProgress = null) => {
    isUploading.value = true
    uploadProgress.value = 0

    try {
      const response = await $api.post('/api/material_site/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          uploadProgress.value = progress
          if (onProgress) onProgress(progress)
        }
      })

      uploadedMaterials.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('上传失败:', error)
      throw error
    } finally {
      isUploading.value = false
      uploadProgress.value = 0
    }
  }

  const addToQueue = (file) => {
    uploadQueue.value.push({
      id: Date.now(),
      file,
      status: 'pending',
      progress: 0
    })
  }

  const clearQueue = () => {
    uploadQueue.value = []
  }

  const clearUploaded = () => {
    uploadedMaterials.value = []
  }

  return {
    uploadProgress,
    isUploading,
    uploadQueue,
    uploadedMaterials,
    uploadMaterial,
    addToQueue,
    clearQueue,
    clearUploaded
  }
})