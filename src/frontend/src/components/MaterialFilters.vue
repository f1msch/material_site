<template>
  <div class="material-filters">
    <div class="filter-section">
      <h3>筛选条件</h3>

      <!-- 搜索框 -->
      <div class="form-group">
        <input
          v-model="localFilters.search"
          type="text"
          placeholder="搜索素材..."
          class="form-input"
          @input="handleSearchInput"
        />
      </div>

      <!-- 分类选择 -->
      <div class="form-group">
        <label class="form-label">分类</label>
        <select v-model="localFilters.category" class="form-input form-select" @change="updateFilters">
          <option value="">所有分类</option>
          <option
            v-for="category in materialStore.categories"
            :key="category.id"
            :value="category.slug"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <!-- 素材类型 -->
      <div class="form-group">
        <label class="form-label">素材类型</label>
        <select v-model="localFilters.material_type" class="form-input form-select" @change="updateFilters">
          <option value="">所有类型</option>
          <option value="image">图片</option>
          <option value="vector">矢量图</option>
          <option value="video">视频</option>
          <option value="audio">音频</option>
          <option value="template">模板</option>
          <option value="font">字体</option>
          <option value="other">其他</option>
        </select>
      </div>

      <!-- 许可类型 -->
      <div class="form-group">
        <label class="form-label">许可类型</label>
        <select v-model="localFilters.license_type" class="form-input form-select" @change="updateFilters">
          <option value="">所有许可</option>
          <option value="free">免费</option>
          <option value="premium">付费</option>
          <option value="cc-by">CC BY</option>
          <option value="cc-by-sa">CC BY-SA</option>
        </select>
      </div>

      <!-- 价格范围 -->
      <div class="form-group">
        <label class="form-label">价格范围</label>
        <div class="price-range">
          <input
            v-model.number="localFilters.min_price"
            type="number"
            placeholder="最低价"
            class="form-input"
            @change="updateFilters"
          />
          <span class="price-separator">-</span>
          <input
            v-model.number="localFilters.max_price"
            type="number"
            placeholder="最高价"
            class="form-input"
            @change="updateFilters"
          />
        </div>
      </div>

      <!-- 标签选择 -->
      <div class="form-group">
        <label class="form-label">标签</label>
        <div class="tags-container">
          <span
            v-for="tag in materialStore.tags"
            :key="tag.id"
            :class="['tag', { active: localFilters.tags.includes(tag.slug) }]"
            :style="{ backgroundColor: tag.color }"
            @click="toggleTag(tag.slug)"
          >
            {{ tag.name }}
          </span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="filter-actions">
        <button @click="clearFilters" class="btn btn-outline">清除筛选</button>
        <button @click="applyFilters" class="btn btn-primary">应用筛选</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useMaterialStore } from '@/stores/material_site'
import { debounce } from '@/utils/helpers'

const materialStore = useMaterialStore()

const localFilters = ref({
  search: '',
  category: '',
  tags: [],
  material_type: '',
  license_type: '',
  min_price: null,
  max_price: null
})

// 初始化时同步store的筛选条件
localFilters.value = { ...materialStore.filters }

// 防抖搜索
const handleSearchInput = debounce(() => {
  updateFilters()
}, 500)

const updateFilters = () => {
  materialStore.updateFilters(localFilters.value)
}

const applyFilters = () => {
  materialStore.fetchMaterials(1)
}

const clearFilters = () => {
  localFilters.value = {
    search: '',
    category: '',
    tags: [],
    material_type: '',
    license_type: '',
    min_price: null,
    max_price: null
  }
  materialStore.clearFilters()
  materialStore.fetchMaterials(1)
}

const toggleTag = (tagSlug) => {
  const index = localFilters.value.tags.indexOf(tagSlug)
  if (index > -1) {
    localFilters.value.tags.splice(index, 1)
  } else {
    localFilters.value.tags.push(tagSlug)
  }
  updateFilters()
}

// 监听store的filters变化（比如从其他组件修改）
watch(
  () => materialStore.filters,
  (newFilters) => {
    localFilters.value = { ...newFilters }
  },
  { deep: true }
)
</script>

<style scoped>
.material-filters {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.filter-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-range .form-input {
  flex: 1;
}

.price-separator {
  color: #6c757d;
  font-weight: 500;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.tag.active {
  border-color: #2c3e50;
  transform: scale(1.05);
}

.filter-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.filter-actions .btn {
  flex: 1;
}

@media (max-width: 768px) {
  .price-range {
    flex-direction: column;
  }

  .price-separator {
    display: none;
  }

  .filter-actions {
    flex-direction: column;
  }
}
</style>