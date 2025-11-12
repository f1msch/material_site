<template>
  <div class="material-card">
    <div class="material-image">
      <img
        :src="material.thumbnail || material.preview_image || '/placeholder-image.jpg'"
        :alt="material.title"
        @click="$router.push(`/material_site/${material.id}`)"
      />
      <div class="material-overlay">
        <button class="btn btn-primary" @click="handleDownload">下载</button>
        <button
          class="btn btn-outline favorite-btn"
          :class="{ 'favorited': material.is_favorited }"
          @click="handleFavorite"
        >
          ♡ {{ material.favorite_count }}
        </button>
      </div>
    </div>

    <div class="material-info">
      <h3 class="material-title" @click="$router.push(`/material_site/${material.id}`)">
        {{ material.title }}
      </h3>

      <div class="material-meta">
        <span class="material-type">{{ material.material_type }}</span>
        <span class="material-size">{{ material.file_size_display }}</span>
        <span v-if="material.dimensions" class="material-dimensions">{{ material.dimensions }}</span>
      </div>

      <div class="material-stats">
        <span class="stat">
          <i>👁️</i> {{ material.view_count }}
        </span>
        <span class="stat">
          <i>⬇️</i> {{ material.download_count }}
        </span>
        <span class="stat">
          <i>👍</i> {{ material.like_count }}
        </span>
      </div>

      <div class="material-author">
        <span>by {{ material.author.username }}</span>
        <span class="material-price" :class="{ 'free': material.license_type === 'free' }">
          {{ material.license_type === 'free' ? '免费' : `¥${material.price}` }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useMaterialStore } from '@/stores/material_site'

const props = defineProps({
  material: {
    type: Object,
    required: true
  }
})

const materialStore = useMaterialStore()

const handleFavorite = async () => {
  try {
    await materialStore.favoriteMaterial(props.material.id)
  } catch (error) {
    console.error('收藏失败:', error)
  }
}

const handleDownload = async () => {
  try {
    const response = await materialStore.downloadMaterial(props.material.id)
    // 创建下载链接
    const link = document.createElement('a')
    link.href = response.download_url
    link.download = props.material.title
    link.click()
  } catch (error) {
    console.error('下载失败:', error)
  }
}
</script>

<style scoped>
.material-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.material-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.material-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.material-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

.material-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.material-image:hover .material-overlay {
  opacity: 1;
}

.favorite-btn {
  background: white;
}

.favorite-btn.favorited {
  background: #e74c3c;
  color: white;
}

.material-info {
  padding: 1rem;
}

.material-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  cursor: pointer;
  color: #2c3e50;
}

.material-title:hover {
  color: #3498db;
}

.material-meta {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.material-type,
.material-size,
.material-dimensions {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  color: #6c757d;
}

.material-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.material-author {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #6c757d;
}

.material-price {
  font-weight: 600;
  color: #27ae60;
}

.material-price.free {
  color: #3498db;
}
</style>