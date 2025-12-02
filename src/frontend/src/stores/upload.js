import {defineStore} from 'pinia'
import {ref} from 'vue'
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
            const response = await $api.post('/api/materials/', formData, {
                headers: {'Content-Type': 'multipart/form-data'},
                onUploadProgress: (progressEvent) => {
                    const progress = Math.round(
                        (progressEvent.loaded * 100) / progressEvent.total
                    )
                    uploadProgress.value = progress
                    if (onProgress) onProgress(progress)
                }
            })

            await uploadFile(formData.main_file)

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

    const handleFileUpload = (event) => {
        // 可以在这里添加文件类型、大小校验
    }

    const uploadFile = async (fileUrl) => {
        try {
            const response = await $api.post('/api/upload/', fileUrl, {
                headers: {'Content-Type': 'multipart/form-data'}
            })
        } catch (error) {
            console.error('上传失败:', error)
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