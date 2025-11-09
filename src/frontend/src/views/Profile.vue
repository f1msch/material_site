<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-header">
        <h1>个人中心</h1>
        <p>管理你的个人信息和素材</p>
      </div>

      <div class="profile-layout">
        <!-- 侧边栏 -->
        <aside class="profile-sidebar">
          <div class="user-card">
            <div class="user-avatar">
              <img
                v-if="userStore.user?.avatar"
                :src="userStore.user.avatar"
                :alt="userStore.user.username"
                class="avatar-image"
              />
              <div v-else class="avatar-placeholder">
                {{ userStore.user?.username?.charAt(0).toUpperCase() }}
              </div>
            </div>
            <div class="user-info">
              <h3>{{ userStore.user?.username }}</h3>
              <p class="user-email">{{ userStore.user?.email }}</p>
              <p class="user-credits">积分: {{ userStore.user?.credits || 0 }}</p>
            </div>
          </div>

          <nav class="profile-nav">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="['nav-item', { active: activeTab === tab.id }]"
              @click="activeTab = tab.id"
            >
              <span class="nav-icon">{{ tab.icon }}</span>
              <span class="nav-text">{{ tab.name }}</span>
            </button>
          </nav>
        </aside>

        <!-- 主要内容 -->
        <main class="profile-content">
          <!-- 个人信息 -->
          <div v-if="activeTab === 'profile'" class="tab-content">
            <div class="content-header">
              <h2>个人信息</h2>
              <p>管理你的个人资料和设置</p>
            </div>

            <form @submit.prevent="updateProfile" class="profile-form">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">用户名</label>
                  <input
                    v-model="profileForm.username"
                    type="text"
                    class="form-input"
                    disabled
                  />
                  <p class="form-help">用户名不可修改</p>
                </div>

                <div class="form-group">
                  <label class="form-label">邮箱</label>
                  <input
                    v-model="profileForm.email"
                    type="email"
                    class="form-input"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">个人简介</label>
                <textarea
                  v-model="profileForm.bio"
                  placeholder="介绍一下你自己..."
                  class="form-input form-textarea"
                  rows="4"
                ></textarea>
              </div>

              <div class="form-group">
                <label class="form-label">个人网站</label>
                <input
                  v-model="profileForm.website"
                  type="url"
                  placeholder="https://example.com"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label class="form-label">头像</label>
                <div class="avatar-upload">
                  <div class="avatar-preview">
                    <img
                      v-if="avatarPreview"
                      :src="avatarPreview"
                      alt="头像预览"
                      class="preview-image"
                    />
                    <div v-else class="avatar-placeholder large">
                      {{ userStore.user?.username?.charAt(0).toUpperCase() }}
                    </div>
                  </div>
                  <div class="upload-controls">
                    <input
                      type="file"
                      ref="avatarInput"
                      @change="handleAvatarSelect"
                      accept="image/*"
                      class="file-input"
                    />
                    <button type="button" @click="$refs.avatarInput.click()" class="btn btn-outline">
                      选择图片
                    </button>
                    <p class="form-help">支持 JPG、PNG 格式，最大 2MB</p>
                  </div>
                </div>
              </div>

              <div class="form-actions">
                <button
                  type="submit"
                  :disabled="updatingProfile"
                  class="btn btn-primary"
                >
                  {{ updatingProfile ? '保存中...' : '保存更改' }}
                </button>
              </div>
            </form>
          </div>

          <!-- 我的素材 -->
          <div v-if="activeTab === 'materials'" class="tab-content">
            <div class="content-header">
              <h2>我的素材</h2>
              <p>管理你上传的所有素材</p>
            </div>

            <div class="materials-stats">
              <div class="stat-card">
                <div class="stat-number">{{ userStore.user?.materials_count || 0 }}</div>
                <div class="stat-label">总素材数</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">{{ userStore.user?.downloads_count || 0 }}</div>
                <div class="stat-label">被下载次数</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">{{ totalLikes }}</div>
                <div class="stat-label">总点赞数</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">{{ totalFavorites }}</div>
                <div class="stat-label">总收藏数</div>
              </div>
            </div>

            <div class="materials-tabs">
              <button
                :class="['tab-btn', { active: materialsTab === 'published' }]"
                @click="materialsTab = 'published'"
              >
                已发布 ({{ publishedMaterials.length }})
              </button>
              <button
                :class="['tab-btn', { active: materialsTab === 'drafts' }]"
                @click="materialsTab = 'drafts'"
              >
                草稿 ({{ draftMaterials.length }})
              </button>
              <button
                :class="['tab-btn', { active: materialsTab === 'pending' }]"
                @click="materialsTab = 'pending'"
              >
                待审核 ({{ pendingMaterials.length }})
              </button>
            </div>

            <div v-if="loadingMaterials" class="loading">
              <div class="loading-spinner"></div>
              <p>加载中...</p>
            </div>

            <div v-else class="materials-list">
              <div
                v-for="material in currentMaterials"
                :key="material.id"
                class="material-item"
              >
                <div class="material-preview">
                  <img
                    :src="material.thumbnail || material.preview_image || '/placeholder-image.jpg'"
                    :alt="material.title"
                    class="preview-image"
                  />
                </div>
                <div class="material-info">
                  <h4 class="material-title">{{ material.title }}</h4>
                  <div class="material-meta">
                    <span class="material-type">{{ material.material_type }}</span>
                    <span class="material-status" :class="material.status">
                      {{ getStatusText(material.status) }}
                    </span>
                    <span class="material-date">{{ formatDate(material.created_at) }}</span>
                  </div>
                  <div class="material-stats">
                    <span>浏览: {{ material.view_count }}</span>
                    <span>下载: {{ material.download_count }}</span>
                    <span>点赞: {{ material.like_count }}</span>
                  </div>
                </div>
                <div class="material-actions">
                  <router-link
                    :to="`/materials/${material.id}`"
                    class="btn btn-outline btn-small"
                  >
                    查看
                  </router-link>
                  <button
                    @click="editMaterial(material.id)"
                    class="btn btn-outline btn-small"
                  >
                    编辑
                  </button>
                  <button
                    @click="deleteMaterial(material.id)"
                    class="btn btn-danger btn-small"
                  >
                    删除
                  </button>
                </div>
              </div>
            </div>

            <div v-if="!loadingMaterials && currentMaterials.length === 0" class="empty-state">
              <p>暂无素材</p>
              <router-link to="/upload" class="btn btn-primary">上传第一个素材</router-link>
            </div>
          </div>

          <!-- 收藏的素材 -->
          <div v-if="activeTab === 'favorites'" class="tab-content">
            <div class="content-header">
              <h2>收藏的素材</h2>
              <p>你收藏的所有素材</p>
            </div>

            <div v-if="favorites.length === 0" class="empty-state">
              <p>还没有收藏任何素材</p>
              <router-link to="/materials" class="btn btn-primary">去发现素材</router-link>
            </div>

            <div v-else class="materials-grid">
              <MaterialCard
                v-for="favorite in favorites"
                :key="favorite.id"
                :material="favorite.material"
              />
            </div>
          </div>

          <!-- 账户设置 -->
          <div v-if="activeTab === 'settings'" class="tab-content">
            <div class="content-header">
              <h2>账户设置</h2>
              <p>管理你的账户和安全设置</p>
            </div>

            <div class="settings-section">
              <h3>安全设置</h3>
              <div class="setting-item">
                <div class="setting-info">
                  <h4>修改密码</h4>
                  <p>定期修改密码保护账户安全</p>
                </div>
                <button class="btn btn-outline">修改密码</button>
              </div>

              <div class="setting-item">
                <div class="setting-info">
                  <h4>账户注销</h4>
                  <p>永久删除你的账户和所有数据</p>
                </div>
                <button class="btn btn-danger">注销账户</button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { useMaterialStore } from '@/stores/material_site'
import MaterialCard from '@/components/MaterialCard.vue'
import { formatDate } from '@/utils/helpers'

const userStore = useUserStore()
const materialStore = useMaterialStore()

const activeTab = ref('profile')
const materialsTab = ref('published')
const updatingProfile = ref(false)
const loadingMaterials = ref(false)
const avatarPreview = ref('')

const tabs = [
  { id: 'profile', name: '个人信息', icon: '👤' },
  { id: 'materials', name: '我的素材', icon: '📁' },
  { id: 'favorites', name: '我的收藏', icon: '❤️' },
  { id: 'settings', name: '账户设置', icon: '⚙️' }
]

const profileForm = reactive({
  username: userStore.user?.username || '',
  email: userStore.user?.email || '',
  bio: userStore.user?.bio || '',
  website: userStore.user?.website || ''
})

const publishedMaterials = ref([])
const draftMaterials = ref([])
const pendingMaterials = ref([])
const favorites = ref([])

const currentMaterials = computed(() => {
  switch (materialsTab.value) {
    case 'drafts':
      return draftMaterials.value
    case 'pending':
      return pendingMaterials.value
    default:
      return publishedMaterials.value
  }
})

const totalLikes = computed(() => {
  return publishedMaterials.value.reduce((sum, material) => sum + material.like_count, 0)
})

const totalFavorites = computed(() => {
  return publishedMaterials.value.reduce((sum, material) => sum + material.favorite_count, 0)
})

onMounted(async () => {
  await loadUserMaterials()
  await loadFavorites()
})

const loadUserMaterials = async () => {
  loadingMaterials.value = true
  try {
    // 这里应该调用API获取用户素材
    // 暂时使用模拟数据
    publishedMaterials.value = materialStore.materials.filter(m => m.author?.id === userStore.user?.id)
    draftMaterials.value = []
    pendingMaterials.value = []
  } catch (error) {
    console.error('加载用户素材失败:', error)
  } finally {
    loadingMaterials.value = false
  }
}

const loadFavorites = async () => {
  try {
    // 这里应该调用API获取收藏列表
    // 暂时使用模拟数据
    favorites.value = materialStore.materials
      .filter(m => m.is_favorited)
      .map(material => ({ id: material.id, material }))
  } catch (error) {
    console.error('加载收藏失败:', error)
  }
}

const handleAvatarSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const updateProfile = async () => {
  if (updatingProfile.value) return

  updatingProfile.value = true
  try {
    await userStore.updateProfile(profileForm)
    alert('个人信息更新成功')
  } catch (error) {
    console.error('更新个人信息失败:', error)
    alert('更新失败，请重试')
  } finally {
    updatingProfile.value = false
  }
}

const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    pending: '待审核',
    approved: '已发布',
    rejected: '已拒绝'
  }
  return statusMap[status] || status
}

const editMaterial = (materialId) => {
  // 跳转到编辑页面
  console.log('编辑素材:', materialId)
}

const deleteMaterial = async (materialId) => {
  if (!confirm('确定要删除这个素材吗？此操作不可恢复。')) {
    return
  }

  try {
    // 这里调用删除API
    console.log('删除素材:', materialId)
    await loadUserMaterials() // 重新加载
  } catch (error) {
    console.error('删除素材失败:', error)
    alert('删除失败，请重试')
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 2rem 0;
}

.profile-header {
  text-align: center;
  margin-bottom: 3rem;
}

.profile-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.profile-header p {
  font-size: 1.1rem;
  color: #6c757d;
  margin: 0;
}

.profile-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.profile-sidebar {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  height: fit-content;
}

.user-card {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ecf0f1;
}

.user-avatar {
  margin-bottom: 1rem;
}

.avatar-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  margin: 0 auto;
}

.avatar-placeholder.large {
  width: 120px;
  height: 120px;
  font-size: 3rem;
}

.user-info h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.user-email {
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.user-credits {
  color: #3498db;
  font-weight: 500;
}

.profile-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: none;
  background: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.nav-item:hover {
  background: #f8f9fa;
}

.nav-item.active {
  background: #3498db;
  color: white;
}

.nav-icon {
  font-size: 1.2rem;
}

.nav-text {
  font-weight: 500;
}

.profile-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.content-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.content-header h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.content-header p {
  color: #6c757d;
  margin: 0;
}

.profile-form {
  max-width: 600px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-help {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 0.3rem;
}

.avatar-upload {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.avatar-preview {
  flex-shrink: 0;
}

.preview-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ecf0f1;
}

.upload-controls {
  flex: 1;
}

.file-input {
  display: none;
}

.form-actions {
  margin-top: 2rem;
}

.materials-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #3498db;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
}

.materials-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #ecf0f1;
  padding-bottom: 1rem;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-btn:hover {
  background: #f8f9fa;
}

.tab-btn.active {
  background: #3498db;
  color: white;
}

.materials-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.material-item {
  display: grid;
  grid-template-columns: 100px 1fr auto;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  align-items: center;
}

.material-preview {
  width: 100px;
  height: 80px;
}

.material-preview .preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.material-info {
  flex: 1;
}

.material-title {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.material-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.material-type,
.material-status,
.material-date {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  background: #f8f9fa;
  color: #6c757d;
}

.material-status.approved {
  background: #d4edda;
  color: #155724;
}

.material-status.pending {
  background: #fff3cd;
  color: #856404;
}

.material-status.draft {
  background: #e2e3e5;
  color: #383d41;
}

.material-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.material-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.settings-section {
  margin-bottom: 2rem;
}

.settings-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.setting-info h4 {
  margin-bottom: 0.3rem;
  color: #2c3e50;
}

.setting-info p {
  color: #6c757d;
  margin: 0;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-state p {
  margin-bottom: 1rem;
}

@media (max-width: 1024px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }

  .profile-sidebar {
    order: 2;
  }

  .profile-content {
    order: 1;
  }
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .materials-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .material-item {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .material-actions {
    justify-content: center;
  }

  .avatar-upload {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .setting-item {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>