<template>
  <div class="material-detail">
    <div class="container" v-if="materialStore.currentMaterial">
      <!-- 面包屑导航 -->
      <nav class="breadcrumb">
        <router-link to="/materials">素材库</router-link>
        <span class="separator">/</span>
        <span>{{ materialStore.currentMaterial.title }}</span>
      </nav>

      <div class="material-layout">
        <!-- 左侧：素材预览 -->
        <div class="material-preview">
          <div class="preview-main">
            <img
                v-if="materialStore.currentMaterial.material_type === 'image'"
                :src="materialStore.currentMaterial.main_file"
                :alt="materialStore.currentMaterial.title"
                class="preview-image"
            />
            <div v-else class="preview-placeholder">
              <div class="file-icon">
                {{ getFileTypeIcon(materialStore.currentMaterial.material_type) }}
              </div>
              <p>{{ materialStore.currentMaterial.material_type }} 文件</p>
            </div>
          </div>

          <div class="preview-thumbnails" v-if="materialStore.currentMaterial.preview_image">
            <img
                :src="materialStore.currentMaterial.preview_image"
                :alt="materialStore.currentMaterial.title + '预览'"
                class="thumbnail"
            />
          </div>
        </div>

        <!-- 右侧：素材信息 -->
        <div class="material-info">
          <div class="material-header">
            <h1 class="material-title">{{ materialStore.currentMaterial.title }}</h1>
            <div class="material-actions">
              <button
                  class="btn btn-primary btn-large"
                  @click="handleDownload"
                  :disabled="downloading"
              >
                {{ downloading ? '下载中...' : '立即下载' }}
              </button>
              <button
                  class="btn favorite-btn"
                  :class="{ 'favorite': materialStore.currentMaterial.is_favorite }"
                  @click="handleFavorite"
              >
                ♡ {{ materialStore.currentMaterial.favorite_count }}
              </button>
              <button class="btn btn-outline" @click="handleLike">
                👍 {{ materialStore.currentMaterial.like_count }}
              </button>
            </div>
          </div>

          <div class="material-meta">
            <div class="meta-item">
              <strong>上传者:</strong>
              <span>{{ materialStore.currentMaterial.author.username }}</span>
            </div>
            <div class="meta-item">
              <strong>分类:</strong>
              <span>{{ materialStore.currentMaterial.category?.name || '未分类' }}</span>
            </div>
            <div class="meta-item">
              <strong>素材类型:</strong>
              <span>{{ materialStore.currentMaterial.material_type }}</span>
            </div>
            <div class="meta-item">
              <strong>文件大小:</strong>
              <span>{{ materialStore.currentMaterial.file_size_display }}</span>
            </div>
            <div v-if="materialStore.currentMaterial.dimensions" class="meta-item">
              <strong>尺寸:</strong>
              <span>{{ materialStore.currentMaterial.dimensions }}</span>
            </div>
            <div v-if="materialStore.currentMaterial.duration" class="meta-item">
              <strong>时长:</strong>
              <span>{{ formatDuration(materialStore.currentMaterial.duration) }}</span>
            </div>
            <div class="meta-item">
              <strong>许可类型:</strong>
              <span class="license-tag" :class="materialStore.currentMaterial.license_type">
                {{ materialStore.currentMaterial.license_type }}
              </span>
            </div>
            <div class="meta-item">
              <strong>价格:</strong>
              <span class="price" :class="{ 'free': materialStore.currentMaterial.license_type === 'free' }">
                {{
                  materialStore.currentMaterial.license_type === 'free' ? '免费' : `¥${materialStore.currentMaterial.price}`
                }}
              </span>
            </div>
          </div>

          <div class="material-description">
            <h3>素材描述</h3>
            <p>{{ materialStore.currentMaterial.description || '暂无描述' }}</p>
          </div>

          <div class="material-tags">
            <h3>标签</h3>
            <div class="tags-list">
              <span
                  v-for="tag in materialStore.currentMaterial.tags"
                  :key="tag.id"
                  class="tag"
                  :style="{ backgroundColor: tag.color }"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>

          <div class="material-stats">
            <div class="stat">
              <span class="stat-number">{{ materialStore.currentMaterial.view_count }}</span>
              <span class="stat-label">浏览</span>
            </div>
            <div class="stat">
              <span class="stat-number">{{ materialStore.currentMaterial.download_count }}</span>
              <span class="stat-label">下载</span>
            </div>
            <div class="stat">
              <span class="stat-number">{{ materialStore.currentMaterial.like_count }}</span>
              <span class="stat-label">点赞</span>
            </div>
            <div class="stat">
              <span class="stat-number">{{ materialStore.currentMaterial.favorite_count }}</span>
              <span class="stat-label">收藏</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 相关素材 -->
      <div class="related-materials" v-if="relatedMaterials.length > 0">
        <h2>相关素材</h2>
        <div class="materials-grid">
          <MaterialCard
              v-for="material in relatedMaterials"
              :key="material.id"
              :material="material"
          />
        </div>
      </div>
    </div>

    <div v-else-if="materialStore.loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else class="error-state">
      <h2>素材不存在</h2>
      <p>抱歉，您查找的素材不存在或已被删除</p>
      <router-link to="/materials" class="btn btn-primary">返回素材库</router-link>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useMaterialStore} from '@/stores/material_site'
import MaterialCard from '@/components/MaterialCard.vue'

const route = useRoute()
const router = useRouter()
const materialStore = useMaterialStore()

const downloading = ref<boolean>(false)
const relatedMaterials = ref<any[]>([])

onMounted(async () => {
  await materialStore.fetchMaterialDetail(Number(route.params.id))
  await loadRelatedMaterials()
})

const getFileTypeIcon = (type: string): string => {
  const icons: Record<string, string> = {
    image: '🖼️',
    vector: '📐',
    video: '🎬',
    audio: '🎵',
    template: '📄',
    font: '🔤',
    other: '📎'
  }
  return icons[type] || '📎'
}

const formatDuration = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const handleDownload = async () => {
  if (downloading.value) return

  downloading.value = true
  try {
    if (materialStore.currentMaterial) {
      const response = await materialStore.downloadMaterial(materialStore.currentMaterial.id)
      if (response) {
        // 创建下载链接
        const link = document.createElement('a')
        link.href = response.download_url
        link.download = materialStore.currentMaterial.title
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }
    }
  } catch (error) {
    console.error('下载失败:', error)
    alert('下载失败，请重试')
  } finally {
    downloading.value = false
  }
}

const handleFavorite = async () => {
  try {
    if (materialStore.currentMaterial) {
      await materialStore.favoriteMaterial(materialStore.currentMaterial.id)
    }
  } catch (error) {
    console.error('收藏失败:', error)
  }
}

const handleLike = async () => {
  try {
    if (materialStore.currentMaterial) {
      // 这里可以调用点赞API
      materialStore.currentMaterial.like_count += 1
    }
  } catch (error) {
    console.error('点赞失败:', error)
  }
}

const loadRelatedMaterials = async () => {
  // 模拟相关素材数据
  relatedMaterials.value = materialStore.materials
      .filter(m => materialStore.currentMaterial && m.id !== materialStore.currentMaterial.id)
      .slice(0, 4)
}
</script>

<style scoped>
.material-detail {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 2rem 0;
}

.breadcrumb {
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: #6c757d;
}

.breadcrumb a {
  color: #3498db;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.separator {
  margin: 0 0.5rem;
}

.material-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 3rem;
  margin-bottom: 4rem;
}

.material-preview {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.preview-main {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 1rem;
  overflow: hidden;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.preview-placeholder {
  text-align: center;
  color: #6c757d;
}

.file-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.preview-thumbnails {
  display: flex;
  gap: 1rem;
}

.thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  border: 2px solid transparent;
}

.thumbnail:hover {
  border-color: #3498db;
}

.material-info {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.material-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.material-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.material-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  flex: 1;
}

.favorite-btn {
  background: white;
  border: 1px solid #ddd;
}

.favorite-btn.favorited {
  background: #e74c3c;
  color: white;
  border-color: #e74c3c;
}

.material-meta {
  margin-bottom: 2rem;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.meta-item:last-child {
  border-bottom: none;
}

.license-tag {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.license-tag.free {
  background: #d4edda;
  color: #155724;
}

.license-tag.premium {
  background: #fff3cd;
  color: #856404;
}

.price {
  font-weight: 600;
  font-size: 1.1rem;
}

.price.free {
  color: #28a745;
}

.material-description,
.material-tags {
  margin-bottom: 2rem;
}

.material-description h3,
.material-tags h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: white;
}

.material-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  text-align: center;
}

.stat {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #3498db;
}

.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.related-materials {
  margin-top: 4rem;
}

.related-materials h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.loading,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 2rem auto;
  max-width: 600px;
}

.error-state h2 {
  color: #e74c3c;
  margin-bottom: 1rem;
}

@media (max-width: 1024px) {
  .material-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .material-info {
    order: -1;
  }
}

@media (max-width: 768px) {
  .material-actions {
    flex-direction: column;
  }

  .material-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .materials-grid {
    grid-template-columns: 1fr;
  }
}
</style>