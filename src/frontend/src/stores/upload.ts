import {defineStore} from 'pinia'
import {ref} from 'vue'
import {uploadFileApi, uploadMaterialFileApi} from '@/api/material'

export const useUploadStore = defineStore('upload', () => {
    const uploadProgress = ref(0)
    const isUploading = ref(false)
    const uploadQueue = ref<any[]>([])
    const uploadedMaterials = ref<any[]>([])

    const uploadMaterial = async (formData: FormData, onProgress: ((progress: number) => void) | null = null): Promise<any> => {
        isUploading.value = true
        uploadProgress.value = 0

        try {
            const response = await uploadMaterialFileApi(formData, (progress) => {
                uploadProgress.value = progress
                if (onProgress) onProgress(progress)
            })

            await uploadFileHandler(formData.main_file)

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

    const handleFileUpload = (event: Event): void => {
        // 可以在这里添加文件类型、大小校验
    }

    const uploadFileHandler = async (fileUrl: FormData | string): Promise<any> => {
        try {
            const response = await uploadFileApi(fileUrl as FormData)
            return response.data
        } catch (error) {
            console.error('上传失败:', error)
        }
    }

    const addToQueue = (file: File): void => {
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