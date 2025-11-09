<template>
  <div class="upload-page">
    <div class="container">
      <div class="page-header">
        <h1>上传素材</h1>
        <p>分享你的创意作品，让更多人发现</p>
      </div>

      <UploadProgress
        :is-uploading="uploadStore.isUploading"
        :progress="uploadStore.uploadProgress"
      />

      <div class="upload-form">
        <form @submit.prevent="handleSubmit">
          <!-- 文件选择 -->
          <div class="form-section">
            <h3>文件信息</h3>

            <div class="form-group">
              <label class="form-label">选择文件 *</label>
              <div class="file-upload">
                <input
                  type="file"
                  ref="fileInput"
                  @change="handleFileSelect"
                  :accept="getAcceptTypes(formData.material_type)"
                  class="file-input"
                />
                <div class="file-dropzone" @click="$refs.fileInput.click()">
                  <div v-if="!selectedFile" class="dropzone-content">
                    <div class="upload-icon">📁</div>
                    <p>点击选择文件或拖拽文件到这里</p>
                    <span class="file-types">支持 {{ getFileTypeText(formData.material_type) }} 文件</span>
                  </div>
                  <div v-else class="file-info">
                    <div class="file-name">{{ selectedFile.name }}</div>
                    <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
                    <button type="button" @click.stop="removeFile" class="btn btn-danger btn-small">
                      移除
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">素材类型 *</label>
              <select v-model="formData.material_type" class="form-input form-select">
                <option value="image">图片</option>
                <option value="vector">矢量图</option>
                <option value="video">视频</option>
                <option value="audio">音频</option>
                <option value="template">模板</option>
                <option value="font">字体</option>
                <option value="other">其他</option>
              </select>
            </div>
          </div>

          <!-- 基本信息 -->
          <div class="form-section">
            <h3>基本信息</h3>

            <div class="form-group">
              <label class="form-label">标题 *</label>
              <input
                v-model="formData.title"
                type="text"
                placeholder="请输入素材标题"
                class="form-input"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">描述</label>
              <textarea
                v-model="formData.description"
                placeholder="描述你的素材内容、特点和使用场景..."
                class="form-input form-textarea"
                rows="4"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">分类</label>
              <select v-model="formData.category" class="form-input form-select">
                <option value="">选择分类</option>
                <option
                  v-for="category in materialStore.categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">标签</label>
              <div class="tags-input">
                <input
                  v-model="tagInput"
                  type="text"
                  placeholder="输入标签后按回车添加"
                  class="form-input"
                  @keydown.enter="addTag"
                />
                <div class="tags-list">
                  <span
                    v-for="(tag, index) in formData.tags"
                    :key="index"
                    class="tag"
                    @click="removeTag(index)"
                  >
                    {{ tag }} ×
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 权限和设置 -->
          <div class="form-section">
            <h3>权限和设置</h3>

            <div class="form-group">
              <label class="form-label">许可类型</label>
              <select v-model="formData.license_type" class="form-input form-select">
                <option value="free">免费</option>
                <option value="premium">付费</option>
                <option value="cc-by">CC BY</option>
                <option value="cc-by-sa">CC BY-SA</option>
              </select>
            </div>

            <div class="form-group" v-if="formData.license_type === 'premium'">
              <label class="form-label">价格 (¥)</label>
              <input
                v-model.number="formData.price"
                type="number"
                min="0"
                step="0.01"
                placeholder="0.00"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label class="checkbox-label">
                <input
                  v-model="formData.is_featured"
                  type="checkbox"
                  class="checkbox"
                />
                <span>设为推荐素材</span>
              </label>
            </div>
          </div>

          <!-- 预览图（可选） -->
          <div class="form-section">
            <h3>预览设置</h3>

            <div class="form-group">
              <label class="form-label">缩略图</label>
              <input
                type="file"
                @change="handleThumbnailSelect"
                accept="image/*"
                class="form-input"
              />
              <div v-if="thumbnailPreview" class="image-preview">
                <img :src="thumbnailPreview" alt="缩略图预览" class="preview-image" />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">预览图</label>
              <input
                type="file"
                @change="handlePreviewSelect"
                accept="image/*"
                class="form-input"
              />
              <div v-if="previewImagePreview" class="image-preview">
                <img :src="previewImagePreview" alt="预览图预览" class="preview-image" />
              </div>
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="form-actions">
            <button
              type="submit"
              :disabled="!canSubmit || uploadStore.isUploading"
              class="btn btn-primary btn-large"
            >
              {{ uploadStore.isUploading ? '上传中...' : '发布素材' }}
            </button>
            <button
              type="button"
              @click="resetForm"
              class="btn btn-outline"
            >
              重置表单
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMaterialStore } from '@/stores/material_site'
import { useUploadStore } from '@/stores/upload'
import UploadProgress from '@/components/UploadProgress.vue'
import { formatFileSize } from '@/utils/helpers'
import { FILE_ACCEPT_TYPES, MAX_FILE_SIZE } from '@/utils/constants'

const router = useRouter()
const materialStore = useMaterialStore()
const uploadStore = useUploadStore()

const fileInput = ref(null)
const selectedFile = ref(null)
const tagInput = ref('')
const thumbnailPreview = ref('')
const previewImagePreview = ref('')

const formData = ref({
  title: '',
  description: '',
  material_type: 'image',
  category: '',
  tags: [],
  license_type: 'free',
  price: 0,
  is_featured: false
})

onMounted(() => {
  materialStore.fetchCategories()
})

const canSubmit = computed(() => {
  return selectedFile.value && formData.value.title.trim()
})

const getAcceptTypes = (type) => {
  return FILE_ACCEPT_TYPES[type] || '*'
}

const getFileTypeText = (type) => {
  const types = {
    image: '图片',
    vector: '矢量图',
    video: '视频',
    audio: '音频',
    template: '模板',
    font: '字体',
    other: '所有'
  }
  return types[type] || '所有'
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > MAX_FILE_SIZE) {
    alert('文件大小不能超过 100MB')
    return
  }

  selectedFile.value = file
}

const handleThumbnailSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      thumbnailPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handlePreviewSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const removeFile = () => {
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const addTag = (event) => {
  event.preventDefault()
  const tag = tagInput.value.trim()
  if (tag && !formData.value.tags.includes(tag)) {
    formData.value.tags.push(tag)
    tagInput.value = ''
  }
}

const removeTag = (index) => {
  formData.value.tags.splice(index, 1)
}

const handleSubmit = async () => {
  if (!canSubmit.value) return

  const uploadFormData = new FormData()

  // 添加文件
  uploadFormData.append('main_file', selectedFile.value)

  // 添加表单数据
  Object.keys(formData.value).forEach(key => {
    if (key === 'tags') {
      formData.value.tags.forEach(tag => {
        uploadFormData.append('tags', tag)
      })
    } else {
      uploadFormData.append(key, formData.value[key])
    }
  })

  // 添加预览文件
  if (thumbnailPreview.value) {
    const thumbnailFile = fileInput.value?.files[0]
    if (thumbnailFile) {
      uploadFormData.append('thumbnail', thumbnailFile)
    }
  }

  try {
    await uploadStore.uploadMaterial(uploadFormData)
    alert('上传成功！')
    resetForm()
    router.push('/materials')
  } catch (error) {
    console.error('上传失败:', error)
    alert('上传失败，请重试')
  }
}

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    material_type: 'image',
    category: '',
    tags: [],
    license_type: 'free',
    price: 0,
    is_featured: false
  }
  selectedFile.value = null
  tagInput.value = ''
  thumbnailPreview.value = ''
  previewImagePreview.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
.upload-page {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 2rem 0;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-header p {
  font-size: 1.1rem;
  color: #6c757d;
  margin: 0;
}

.upload-form {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.form-section {
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ecf0f1;
}

.form-section:last-child {
  border-bottom: none;
}

.form-section h3 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.3rem;
}

.file-upload {
  position: relative;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.file-dropzone {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-dropzone:hover {
  border-color: #3498db;
  background: #f8f9fa;
}

.dropzone-content .upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.dropzone-content p {
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.file-types {
  color: #6c757d;
  font-size: 0.9rem;
}

.file-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.file-name {
  font-weight: 500;
  color: #2c3e50;
}

.file-size {
  color: #6c757d;
  font-size: 0.9rem;
}

.btn-small {
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
}

.tags-input {
  position: relative;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tags-list .tag {
  background: #3498db;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.tags-list .tag:hover {
  background: #2980b9;
}

.image-preview {
  margin-top: 0.5rem;
}

.preview-image {
  max-width: 200px;
  max-height: 150px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox {
  width: 1.2rem;
  height: 1.2rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #ecf0f1;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .upload-form {
    padding: 1rem;
  }

  .file-info {
    flex-direction: column;
    text-align: center;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>