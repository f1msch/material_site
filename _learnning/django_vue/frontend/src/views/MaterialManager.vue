<template>
  <div class="material-manager">
    <!-- 上传区域 -->
    <div class="upload-section">
      <h2>上传新素材</h2>
      <div class="upload-form">
        <div class="form-group">
          <label>素材标题 *</label>
          <input
            type="text"
            v-model="uploadForm.title"
            placeholder="输入素材标题"
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label>素材描述</label>
          <textarea
            v-model="uploadForm.description"
            placeholder="输入素材描述"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>分类 *</label>
            <select v-model="uploadForm.category" class="form-select">
              <option value="">选择分类</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>素材类型 *</label>
            <select v-model="uploadForm.material_type" class="form-select">
              <option value="">选择类型</option>
              <option value="image">图片</option>
              <option value="vector">矢量图</option>
              <option value="psd">PSD模板</option>
              <option value="video">视频</option>
              <option value="audio">音频</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>预览图 *</label>
            <div class="file-upload-area" @click="triggerFileInput('preview')">
              <div v-if="!uploadForm.previewFile" class="upload-placeholder">
                <span>点击选择预览图</span>
                <small>支持 JPG, PNG, GIF 格式</small>
              </div>
              <div v-else class="file-preview">
                <img v-if="isImageFile(uploadForm.previewFile)" :src="getFilePreview(uploadForm.previewFile)" class="preview-thumb">
                <div v-else class="file-info">
                  <span>{{ uploadForm.previewFile.name }}</span>
                  <small>{{ formatFileSize(uploadForm.previewFile.size) }}</small>
                </div>
                <button @click.stop="removeFile('preview')" class="remove-btn">×</button>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>素材文件 *</label>
            <div class="file-upload-area" @click="triggerFileInput('file')">
              <div v-if="!uploadForm.materialFile" class="upload-placeholder">
                <span>点击选择素材文件</span>
                <small>支持多种格式</small>
              </div>
              <div v-else class="file-preview">
                <div class="file-info">
                  <span>{{ uploadForm.materialFile.name }}</span>
                  <small>{{ formatFileSize(uploadForm.materialFile.size) }}</small>
                  <small class="file-type">{{ uploadForm.material_type }}</small>
                </div>
                <button @click.stop="removeFile('file')" class="remove-btn">×</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 文件预览 -->
        <div v-if="uploadForm.previewFile && isImageFile(uploadForm.previewFile)" class="image-preview">
          <h4>预览图效果:</h4>
          <img :src="getFilePreview(uploadForm.previewFile)" class="preview-image-large">
        </div>

        <div class="form-actions">
          <button
            @click="uploadMaterial"
            :disabled="!canUpload || uploading"
            class="btn-upload"
          >
            <span v-if="uploading">上传中...</span>
            <span v-else>上传素材</span>
          </button>
          <button @click="resetUploadForm" class="btn-cancel">取消</button>
        </div>
      </div>
    </div>

    <!-- 筛选和搜索 -->
    <div class="filter-section">
      <h2>素材列表</h2>
      <div class="filter-controls">
        <select v-model="filters.type" @change="loadMaterials">
          <option value="">所有类型</option>
          <option value="image">图片</option>
          <option value="vector">矢量图</option>
          <option value="psd">PSD模板</option>
          <option value="video">视频</option>
          <option value="audio">音频</option>
        </select>

        <select v-model="filters.category" @change="loadMaterials">
          <option value="">所有分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>

        <input
          type="text"
          v-model="filters.search"
          placeholder="搜索素材..."
          @input="onSearchInput"
          class="search-input"
        >
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      加载中...
    </div>

    <!-- 素材列表 -->
    <div v-else-if="materials.length > 0" class="materials-grid">
      <div
        v-for="material in materials"
        :key="material.id"
        class="material-card"
        :class="`type-${material.material_type}`"
      >
        <!-- 预览图 -->
        <div class="preview-container">
          <img
            :src="getPreviewUrl(material)"
            :alt="material.title"
            class="preview-image"
            @click="showPreview(material)"
          >
          <div class="material-badge">{{ material.material_type_display }}</div>
        </div>

        <!-- 素材信息 -->
        <div class="material-info">
          <h3 class="material-title">{{ material.title }}</h3>
          <p class="material-description">{{ material.description }}</p>

          <!-- 图片信息 -->
          <div v-if="material.material_type === 'image' && material.image_info" class="image-info">
            <span>尺寸: {{ material.image_info.size }}</span>
            <span>大小: {{ material.image_info.file_size }}</span>
          </div>

          <div class="material-meta">
            <span>下载: {{ material.downloads }}次</span>
            <span>分类: {{ material.category_name }}</span>
            <span>上传: {{ formatDate(material.created_at) }}</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button @click="downloadFile(material.id)" class="btn-primary">
            下载文件
          </button>

          <button
            v-if="material.material_type === 'image'"
            @click="previewImage(material.id)"
            class="btn-secondary"
          >
            预览原图
          </button>

          <button
            v-if="material.thumbnail_url"
            @click="downloadThumbnail(material.id)"
            class="btn-outline"
          >
            下载缩略图
          </button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">📁</div>
      <h3>暂无素材数据</h3>
      <p>点击上方上传区域添加第一个素材</p>
    </div>

    <!-- 图片预览模态框 -->
    <div v-if="showImagePreview" class="preview-modal" @click="closePreview">
      <div class="preview-content" @click.stop>
        <img :src="previewImageUrl" class="preview-image-large">
        <button @click="closePreview" class="close-btn">×</button>
      </div>
    </div>

    <!-- 隐藏的文件输入 -->
    <input
      type="file"
      ref="previewInput"
      @change="onPreviewFileSelect"
      accept="image/*"
      style="display: none"
    >
    <input
      type="file"
      ref="materialInput"
      @change="onMaterialFileSelect"
      :accept="getFileAccept"
      style="display: none"
    >
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MaterialManager',
  data() {
    return {
      materials: [],
      categories: [],
      filters: {
        type: '',
        category: '',
        search: ''
      },
      showImagePreview: false,
      previewImageUrl: '',
      searchTimeout: null,
      loading: false,
      uploading: false,
      error: null,

      // 上传表单数据
      uploadForm: {
        title: '',
        description: '',
        category: '',
        material_type: '',
        previewFile: null,
        materialFile: null
      }
    };
  },
  computed: {
    canUpload() {
      return (
        this.uploadForm.title &&
        this.uploadForm.category &&
        this.uploadForm.material_type &&
        this.uploadForm.previewFile &&
        this.uploadForm.materialFile
      );
    },
    getFileAccept() {
      const acceptMap = {
        image: 'image/*',
        vector: '.ai,.eps,.svg',
        psd: '.psd',
        video: 'video/*',
        audio: 'audio/*'
      };
      return acceptMap[this.uploadForm.material_type] || '*';
    }
  },
  mounted() {
    this.loadMaterials();
    this.loadCategories();
  },
  methods: {
    async loadMaterials() {
      this.loading = true;
      this.error = null;
      console.log('开始加载素材列表...');

      try {
        const params = {
          page_size: 1000  // 确保获取所有数据
        };
        if (this.filters.type) params.type = this.filters.type;
        if (this.filters.category) params.category = this.filters.category;
        if (this.filters.search) params.search = this.filters.search;

        console.log('请求参数:', params);
        const response = await axios.get('/api/materials/', { params });
        console.log('素材列表API响应:', response);
        console.log('响应数据:', response.data);

        // 处理分页数据
        let materialsData = response.data;

        // 如果启用了分页，数据可能在 results 字段中
        if (response.data && response.data.results) {
          materialsData = response.data.results;
          console.log('从分页结果中获取数据:', materialsData);
        }

        // 确保数据是数组且包含必需的字段
        this.materials = Array.isArray(materialsData)
          ? materialsData.filter(material => material && material.id)
          : [];

        console.log('处理后的素材数据:', this.materials);
        console.log('素材数量:', this.materials.length);

      } catch (error) {
        console.error('加载素材失败:', error);
        console.error('错误详情:', error.response);

        if (error.response) {
          this.error = `错误: ${error.response.status} - ${error.response.statusText}`;
        } else {
          this.error = `错误: ${error.message}`;
        }

        this.materials = [];
      } finally {
        this.loading = false;
      }
    },


    async loadCategories() {
      try {
        console.log('开始加载分类数据...');
        const response = await axios.get('/api/categories/');
        console.log('分类API响应:', response);
        console.log('响应状态:', response.status);
        console.log('响应数据:', response.data);

        // 确保数据是数组且包含必需的字段
        this.categories = Array.isArray(response.data.results)
          ? response.data.results.filter(category => category && category.id)
          : [];

        console.log('处理后的分类数据:', this.categories);
        console.log('分类数量:', this.categories.length);
      } catch (error) {
        console.error('加载分类失败:', error);
        this.categories = [];
      }
    },

    triggerFileInput(type) {
      if (type === 'preview') {
        this.$refs.previewInput.click();
      } else {
        this.$refs.materialInput.click();
      }
    },

    onPreviewFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        if (!this.isImageFile(file)) {
          alert('请选择图片文件作为预览图');
          return;
        }
        this.uploadForm.previewFile = file;
      }
      event.target.value = ''; // 重置input
    },

    onMaterialFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.uploadForm.materialFile = file;
      }
      event.target.value = ''; // 重置input
    },

    removeFile(type) {
      if (type === 'preview') {
        this.uploadForm.previewFile = null;
      } else {
        this.uploadForm.materialFile = null;
      }
    },

    isImageFile(file) {
      return file && file.type.startsWith('image/');
    },

    getFilePreview(file) {
      return URL.createObjectURL(file);
    },

    async uploadMaterial() {
      if (!this.canUpload) return;

      this.uploading = true;

      try {
        const formData = new FormData();
        formData.append('title', this.uploadForm.title);
        formData.append('description', this.uploadForm.description);
        formData.append('category', this.uploadForm.category);
        formData.append('material_type', this.uploadForm.material_type);
        formData.append('image_preview', this.uploadForm.previewFile);
        formData.append('file', this.uploadForm.materialFile);

        await axios.post('/api/materials/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        // 上传成功
        this.resetUploadForm();
        this.loadMaterials(); // 重新加载列表

        alert('素材上传成功！');

      } catch (error) {
        console.error('上传失败:', error);
        let errorMessage = '上传失败，请重试';

        if (error.response && error.response.data) {
          // 显示后端返回的错误信息
          const errors = error.response.data;
          if (typeof errors === 'object') {
            errorMessage = Object.values(errors).flat().join(', ');
          } else {
            errorMessage = errors;
          }
        }

        alert(errorMessage);
      } finally {
        this.uploading = false;
      }
    },

    resetUploadForm() {
      this.uploadForm = {
        title: '',
        description: '',
        category: '',
        material_type: '',
        previewFile: null,
        materialFile: null
      };
    },

    getPreviewUrl(material) {
      if (!material) return '';
      return material.thumbnail_url || material.preview_url || '';
    },

    onSearchInput() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadMaterials();
      }, 500);
    },

    async downloadFile(materialId) {
      if (!materialId) return;

      try {
        const response = await axios.get(
          `/api/materials/${materialId}/download_file/`,
          { responseType: 'blob' }
        );
        this.downloadBlob(response.data, `material_${materialId}`);
      } catch (error) {
        console.error('下载文件失败:', error);
        alert('下载失败，请重试');
      }
    },

    async downloadThumbnail(materialId) {
      if (!materialId) return;

      try {
        const response = await axios.get(
          `/api/materials/${materialId}/download_thumbnail/`,
          { responseType: 'blob' }
        );
        this.downloadBlob(response.data, `thumbnail_${materialId}`);
      } catch (error) {
        console.error('下载缩略图失败:', error);
        alert('下载缩略图失败，请重试');
      }
    },

    async previewImage(materialId) {
      if (!materialId) return;

      try {
        const response = await axios.get(
          `/api/materials/${materialId}/preview_image/`,
          { responseType: 'blob' }
        );

        const imageUrl = URL.createObjectURL(response.data);
        this.previewImageUrl = imageUrl;
        this.showImagePreview = true;
      } catch (error) {
        console.error('预览图片失败:', error);
        alert('预览图片失败，请重试');
      }
    },

    showPreview(material) {
      if (!material) return;

      const previewUrl = material.preview_url || material.thumbnail_url;
      if (previewUrl) {
        this.previewImageUrl = previewUrl;
        this.showImagePreview = true;
      }
    },

    closePreview() {
      this.showImagePreview = false;
      if (this.previewImageUrl.startsWith('blob:')) {
        URL.revokeObjectURL(this.previewImageUrl);
      }
      this.previewImageUrl = '';
    },

    downloadBlob(blob, filename) {
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.material-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.upload-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 30px;
  border: 2px dashed #dee2e6;
}

.upload-section h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.5em;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-input,
.form-textarea,
.form-select {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.file-upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-upload-area:hover {
  border-color: #007bff;
  background: #f8fbff;
}

.upload-placeholder {
  color: #666;
}

.upload-placeholder span {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.upload-placeholder small {
  color: #999;
}

.file-preview {
  position: relative;
  width: 100%;
}

.preview-thumb {
  max-width: 100%;
  max-height: 100px;
  border-radius: 4px;
}

.file-info {
  text-align: left;
}

.file-info span {
  display: block;
  font-weight: 500;
  margin-bottom: 4px;
}

.file-info small {
  color: #666;
  display: block;
}

.file-type {
  background: #007bff;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7em;
}

.remove-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-preview {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.image-preview h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.preview-image-large {
  max-width: 300px;
  max-height: 200px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

.btn-upload {
  background: #28a745;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-upload:hover:not(:disabled) {
  background: #218838;
}

.btn-upload:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.btn-cancel {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.btn-cancel:hover {
  background: #5a6268;
}

.filter-section {
  margin-bottom: 30px;
}

.filter-section h2 {
  margin: 0 0 15px 0;
  color: #333;
}

.filter-controls {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.filter-controls select,
.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4em;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.empty-state p {
  margin: 0;
  color: #999;
}

/* 其余样式保持不变... */
.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.material-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  transition: transform 0.2s, box-shadow 0.2s;
}

.material-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.preview-container {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

.material-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
}

.material-info {
  padding: 15px;
}

.material-title {
  margin: 0 0 10px 0;
  font-size: 1.1em;
  color: #333;
}

.material-description {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 0.9em;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.image-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.8em;
  color: #888;
}

.material-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.8em;
  color: #999;
}

.action-buttons {
  padding: 0 15px 15px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-outline {
  background: transparent;
  color: #007bff;
  border: 1px solid #007bff;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.preview-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.close-btn {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 2em;
  cursor: pointer;
}

/* 不同类型素材的样式 */
.material-card.type-image {
  border-left: 4px solid #28a745;
}

.material-card.type-vector {
  border-left: 4px solid #17a2b8;
}

.material-card.type-psd {
  border-left: 4px solid #ffc107;
}

.material-card.type-video {
  border-left: 4px solid #dc3545;
}

.material-card.type-audio {
  border-left: 4px solid #6f42c1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .filter-controls {
    flex-direction: column;
  }

  .materials-grid {
    grid-template-columns: 1fr;
  }
}
</style>