<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/">素材网站</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/materials">素材库</router-link>
        <router-link to="/upload" v-if="userStore.isAuthenticated">上传</router-link>
        <router-link to="/profile" v-if="userStore.isAuthenticated">个人中心</router-link>
        <router-link to="/login" v-if="!userStore.isAuthenticated">登录</router-link>
        <button v-else @click="handleLogout" class="logout-btn">退出</button>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; 2024 素材网站. All rights reserved.</p>
    </footer>
  </div>
</template>

<script lang="ts" setup>
import {onMounted} from 'vue'
import {useUserStore} from '@/stores/user'
import {useRouter} from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

onMounted(() => {
  // 检查用户登录状态
  if (localStorage.getItem('auth_token')) {
    userStore.fetchProfile()
  }
})

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3498db;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-links a {
  color: #333;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background-color: #3498db;
  color: white;
}

.logout-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background: #c0392b;
}

.main-content {
  min-height: calc(100vh - 120px);
  padding: 2rem;
}

.footer {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  color: #666;
}
</style>