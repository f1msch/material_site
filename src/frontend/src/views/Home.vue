<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero">
      <div class="hero-content">
        <h1>发现创意素材</h1>
        <p>高质量图片、视频、音频和设计资源，为你的创意项目提供灵感</p>
        <div class="hero-actions">
          <router-link to="/materials" class="btn btn-primary btn-large">
            浏览素材
          </router-link>
          <router-link to="/upload" class="btn btn-outline btn-large" v-if="userStore.isAuthenticated">
            上传素材
          </router-link>
          <router-link to="/login" class="btn btn-outline btn-large" v-else>
            立即登录
          </router-link>
          <router-link to="/payment" class="btn btn-primary btn-large">
            支付
          </router-link>
        </div>
      </div>
    </section>

    <!-- 特色分类 -->
    <section class="featured-categories">
      <div class="container">
        <h2>热门分类</h2>
        <div class="categories-grid">
          <div
            v-for="category in featuredCategories"
            :key="category.id"
            class="category-card"
            @click="$router.push(`/materials?category=${category.slug}`)"
          >
            <div class="category-icon">
              <span>{{ category.icon || '📁' }}</span>
            </div>
            <h3>{{ category.name }}</h3>
            <p>{{ category.material_count || 0 }} 个素材</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 推荐素材 -->
    <section class="featured-materials">
      <div class="container">
        <div class="section-header">
          <h2>精选素材</h2>
          <router-link to="/materials" class="view-all">查看全部 →</router-link>
        </div>

        <div v-if="materialStore.loading" class="loading">
          <div class="loading-spinner"></div>
        </div>

        <div v-else class="materials-grid">
          <MaterialCard
            v-for="material in featuredMaterials"
            :key="material.id"
            :material="material"
          />
        </div>

        <div v-if="!materialStore.loading && featuredMaterials.length === 0" class="empty-state">
          <p>暂无素材</p>
          <router-link to="/upload" class="btn btn-primary" v-if="userStore.isAuthenticated">
            上传第一个素材
          </router-link>
        </div>
      </div>
    </section>

    <!-- 数据统计 -->
    <section class="stats">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">{{ stats.totalMaterials || 0 }}</div>
            <div class="stat-label">总素材数</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.totalDownloads || 0 }}</div>
            <div class="stat-label">总下载量</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.totalUsers || 0 }}</div>
            <div class="stat-label">注册用户</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ stats.featuredMaterials || 0 }}</div>
            <div class="stat-label">精选素材</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import {computed, onMounted, ref} from 'vue'
import {useMaterialStore} from '@/stores/material_site'
import {useUserStore} from '@/stores/user'
import MaterialCard from '@/components/MaterialCard.vue'

const materialStore = useMaterialStore()
const userStore = useUserStore()

const featuredCategories = ref<any[]>([])
const stats = ref({
  totalMaterials: 0,
  totalDownloads: 0,
  totalUsers: 0,
  featuredMaterials: 0
})

const featuredMaterials = computed(() => {
  return materialStore.materials.slice(0, 8)
})

onMounted(async () => {
  await Promise.all([
    materialStore.fetchMaterials(1),
    materialStore.fetchCategories(),
  ])
  await loadFeaturedData()
})

const loadFeaturedData = async () => {
  try {
    // 这里可以调用API获取特色分类和统计数据
    // 暂时使用模拟数据
    featuredCategories.value = materialStore.categories.slice(0, 6)
    console.log('featuredCategories.value is ', featuredCategories.value)

    // 模拟统计数据
    stats.value = {
      totalMaterials: 1234,
      totalDownloads: 5678,
      totalUsers: 432,
      featuredMaterials: 56
    }
    console.log('stats.value 已设置:', stats.value)
    console.log('loadFeaturedData 执行完成')
  } catch (error) {
    console.error('加载特色数据失败:', error)
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6rem 2rem;
  text-align: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.featured-categories {
  padding: 4rem 0;
  background: white;
}

.featured-categories h2 {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2.5rem;
  color: #2c3e50;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.category-card {
  text-align: center;
  padding: 2rem 1rem;
  border-radius: 12px;
  background: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  background: white;
}

.category-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.category-card h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.category-card p {
  color: #6c757d;
  margin: 0;
}

.featured-materials {
  padding: 4rem 0;
  background: #f8f9fa;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0;
}

.view-all {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.view-all:hover {
  text-decoration: underline;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.stats {
  padding: 4rem 0;
  background: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  text-align: center;
}

.stat-item {
  padding: 2rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: #3498db;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  color: #6c757d;
  font-weight: 500;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .categories-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .materials-grid {
    grid-template-columns: 1fr;
  }
}
</style>