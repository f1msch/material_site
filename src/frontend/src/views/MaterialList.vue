<template>
  <div class="material-list">
    <div class="row mb-4">
      <div class="col-md-8">
        <h2>素材库</h2>
        <p class="text-muted">发现优质设计素材，提升创作效率</p>
      </div>
      <div class="col-md-4">
        <div class="input-group">
          <input
            v-model="searchQuery"
            type="text"
            class="form-control"
            placeholder="搜索素材..."
            @input="handleSearch"
          >
        </div>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="row mb-3">
      <div class="col-12">
        <div class="alert alert-info">
          <strong>数据状态:</strong>
          {{ materials.length > 0 ? `已加载 ${materials.length} 个素材` : '正在加载数据...' }}
          <span v-if="apiError" class="text-danger"> | API连接失败，使用模拟数据</span>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2 text-muted">正在从服务器加载数据...</p>
    </div>

    <!-- 素材列表 -->
    <div v-else class="row">
      <div
        v-for="material in materials"
        :key="material.id"
        class="col-lg-3 col-md-4 col-sm-6 mb-4"
      >
        <div class="card h-100 material-card">
          <div class="position-relative">
            <img
              :src="getImageUrl(material.image_preview)"
              class="card-img-top material-image"
              :alt="material.title"
              @error="handleImageError"
            >
            <span class="position-absolute top-0 end-0 m-2 badge"
                  :class="material.is_free ? 'bg-success' : 'bg-warning text-dark'">
              {{ material.is_free ? '免费' : `¥${material.price}` }}
            </span>
            <span class="position-absolute top-0 start-0 m-2 badge bg-dark">
              {{ getTypeLabel(material.material_type) }}
            </span>
          </div>
          <div class="card-body">
            <h6 class="card-title">{{ material.title }}</h6>
            <p class="card-text small text-muted">{{ material.description }}</p>

            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-primary">{{ material.category.name }}</span>
              <small class="text-muted">{{ formatFileSize(material.file_size) }}</small>
            </div>

            <div class="mb-2">
              <span
                v-for="tag in material.tags"
                :key="tag.name"
                class="badge bg-secondary me-1 mb-1"
              >
                {{ tag.name }}
              </span>
            </div>

            <div class="material-stats d-flex justify-content-between text-muted small">
              <span>📥 {{ material.downloads }} 下载</span>
              <span>❤️ {{ material.likes }} 收藏</span>
            </div>
          </div>
          <div class="card-footer bg-transparent">
            <div class="d-flex justify-content-between align-items-center">
              <small class="text-muted">{{ formatTime(material.created_at) }}</small>
              <div>
                <button class="btn btn-sm btn-outline-primary me-1"
                        @click="likeMaterial(material)"
                        :title="`收藏 ${material.title}`">
                  ❤️ {{ material.likes }}
                </button>
                <button class="btn btn-sm btn-primary"
                        @click="downloadMaterial(material)"
                        :title="`下载 ${material.title}`">
                  📥 下载
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && materials.length === 0 && !apiError" class="text-center py-5">
      <div class="empty-state">
        <h4 class="mt-3">暂无素材</h4>
        <p class="text-muted">没有找到素材数据</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'MaterialList',
  setup() {
    const materials = ref([])
    const categories = ref([])
    const searchQuery = ref('')
    const loading = ref(false)
    const apiError = ref(false)
    let searchTimeout = null

    const filters = reactive({
      category: '',
      material_type: '',
      ordering: '-created_at'
    })

    // 模拟数据（备用）
    const mockMaterials = [
      {
        id: 1,
        title: '测试素材 - 请检查API连接',
        description: '如果看到这个素材，说明Vue前端没有正确连接到Django API',
        category: { id: 1, name: '测试分类' },
        material_type: 'image',
        image_preview: 'https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=API连接失败',
        file_size: 1024000,
        downloads: 0,
        likes: 0,
        price: 0,
        is_free: true,
        tags: [{ name: '测试' }, { name: 'API' }],
        created_at: '2024-01-01T00:00:00Z'
      }
    ]

    const fetchMaterials = async () => {
      loading.value = true
      apiError.value = false

      try {
        console.log('正在从API获取素材数据...')

        // 尝试从Django API获取数据
        const response = await axios.get('http://localhost:8000/api/materials/')
        console.log('API响应:', response.data)

        if (response.data && (response.data.results || response.data.length > 0)) {
          materials.value = response.data.results || response.data
          console.log(`成功加载 ${materials.value.length} 个素材`)
        } else {
          throw new Error('API返回空数据')
        }

      } catch (error) {
        console.error('API请求失败:', error)
        apiError.value = true
        // 使用模拟数据作为备用
        materials.value = mockMaterials
        console.log('已切换到模拟数据')
      } finally {
        loading.value = false
      }
    }

    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/categories/')
        categories.value = response.data
      } catch (error) {
        console.error('获取分类失败:', error)
        categories.value = [{ id: 1, name: '默认分类' }]
      }
    }

    const handleSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        fetchMaterials()
      }, 500)
    }

    const likeMaterial = async (material) => {
      try {
        await axios.post(`http://localhost:8000/api/materials/${material.id}/like/`)
        material.likes += 1
      } catch (error) {
        console.error('点赞失败:', error)
        material.likes += 1 // 前端模拟
      }
    }

    const downloadMaterial = async (material) => {
      try {
        await axios.post(`http://localhost:8000/api/materials/${material.id}/download/`)
        material.downloads += 1
        alert(`开始下载: ${material.title}`)
      } catch (error) {
        console.error('下载失败:', error)
        material.downloads += 1 // 前端模拟
        alert(`开始下载: ${material.title} (模拟)`)
      }
    }

    const formatFileSize = (bytes) => {
      if (!bytes) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const formatTime = (timeString) => {
      return new Date(timeString).toLocaleDateString('zh-CN')
    }

    const getTypeLabel = (type) => {
      const typeMap = {
        'image': '图片',
        'vector': '矢量',
        'psd': 'PSD',
        'video': '视频',
        'audio': '音频'
      }
      return typeMap[type] || type
    }

    const getImageUrl = (url) => {
      if (!url) return 'https://via.placeholder.com/300x200/CCCCCC/FFFFFF?text=暂无图片'
      if (url.startsWith('http')) return url
      return `http://localhost:8000${url}`
    }

    const handleImageError = (event) => {
      event.target.src = 'https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=图片加载失败'
    }

    onMounted(() => {
      console.log('组件挂载，开始获取数据...')
      fetchCategories()
      fetchMaterials()
    })

    return {
      materials,
      categories,
      searchQuery,
      filters,
      loading,
      apiError,
      fetchMaterials,
      handleSearch,
      likeMaterial,
      downloadMaterial,
      formatFileSize,
      formatTime,
      getTypeLabel,
      getImageUrl,
      handleImageError
    }
  }
}
</script>

<style scoped>
.material-image {
  height: 200px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}

.material-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.material-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.card-title {
  font-weight: 600;
  color: #2c3e50;
}

.card-text {
  font-size: 0.875rem;
  line-height: 1.4;
}

.material-stats {
  font-size: 0.8rem;
}

.badge {
  font-size: 0.75rem;
}
</style>