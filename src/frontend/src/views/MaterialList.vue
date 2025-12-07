<template>
  <div class="material-list">
    <div class="container">
      <div class="page-header">
        <h1>素材库</h1>
        <p>发现高质量的创意素材资源</p>
      </div>

      <div class="layout">
        <!-- 筛选侧边栏 -->
        <aside class="sidebar">
          <MaterialFilters />
        </aside>

        <!-- 主要内容 -->
        <main class="main-content">
          <!-- 排序和显示选项 -->
          <div class="toolbar">
            <div class="sort-options">
              <label>排序:</label>
              <select v-model="sortBy" @change="handleSortChange" class="form-select">
                <option value="-created_at">最新发布</option>
                <option value="-view_count">最多浏览</option>
                <option value="-download_count">最多下载</option>
                <option value="-like_count">最多点赞</option>
                <option value="price">价格最低</option>
                <option value="-price">价格最高</option>
              </select>
            </div>

            <div class="display-options">
              <span class="results-count">
                找到 {{ materialStore.pagination.total }} 个素材
              </span>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="materialStore.loading" class="loading">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>

          <!-- 素材网格 -->
          <div v-else class="materials-grid">
            <MaterialCard
              v-for="material in materialStore.filteredMaterials"
              :key="material.id"
              :material="material"
            />
          </div>

          <!-- 空状态 -->
          <div v-if="!materialStore.loading && materialStore.materials.length === 0" class="empty-state">
            <div class="empty-icon">📁</div>
            <h3>暂无素材</h3>
            <p>没有找到符合条件的素材，尝试调整筛选条件</p>
            <button @click="materialStore.clearFilters()" class="btn btn-primary">
              清除筛选条件
            </button>
          </div>

          <!-- 分页 -->
          <Pagination
              v-if="(materialStore.pagination?.total ?? 0) > 0"
              :current="materialStore.pagination.current || 1"
              :page-size="materialStore.pagination.pageSize || 12"
              :total="materialStore.pagination.total || 0"
            @change="handlePageChange"
          />
        </main>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref, watch} from 'vue'
import {useMaterialStore} from '@/stores/material_site'
import * as MaterialFilters from '@/components/MaterialFilters.vue'
import MaterialCard from '@/components/MaterialCard.vue'
import * as Pagination from '@/components/Pagination.vue'

const materialStore = useMaterialStore()
const sortBy = ref('-created_at')

onMounted(async () => {
  await Promise.all([
    materialStore.fetchMaterials(),
    materialStore.fetchCategories(),
    materialStore.fetchTags()
  ])
})

const handlePageChange = (page: number): void => {
  materialStore.fetchMaterials(page)
}

const handleSortChange = (): void => {
  materialStore.fetchMaterials(1)
}

// 监听筛选条件变化，自动重新加载
watch(
  () => materialStore.filters,
  () => {
    materialStore.fetchMaterials(1)
  },
  { deep: true, immediate: false }
)
</script>

<style scoped>
.material-list {
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

.layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  align-items: start;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-options label {
  font-weight: 500;
  color: #2c3e50;
}

.form-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.results-count {
  color: #6c757d;
  font-weight: 500;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6c757d;
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.loading p {
  margin-top: 1rem;
  color: #6c757d;
}

@media (max-width: 1024px) {
  .layout {
    grid-template-columns: 250px 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    order: 2;
  }

  .main-content {
    order: 1;
  }

  .toolbar {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .sort-options {
    justify-content: space-between;
  }

  .materials-grid {
    grid-template-columns: 1fr;
  }
}
</style>