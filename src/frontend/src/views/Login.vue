<template>
  <div class="login-page">
    <div class="container">
      <div class="login-card">
        <div class="login-header">
          <h1>登录</h1>
          <p>欢迎回到素材网站</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">用户名或邮箱</label>
            <input
              v-model="loginData.username"
              type="text"
              placeholder="请输入用户名或邮箱"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">密码</label>
            <input
              v-model="loginData.password"
              type="password"
              placeholder="请输入密码"
              class="form-input"
              required
            />
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input v-model="rememberMe" type="checkbox" class="checkbox" />
              <span>记住我</span>
            </label>
            <router-link to="/forgot-password" class="forgot-link">忘记密码？</router-link>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="btn btn-primary btn-large login-btn"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>

          <div class="login-divider">
            <span>或</span>
          </div>

          <div class="register-link">
            还没有账号？
            <router-link to="/register" class="link">立即注册</router-link>
          </div>
        </form>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useUserStore} from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref<boolean>(false)
const error = ref<string>('')
const rememberMe = ref<boolean>(false)

const loginData = ref({
  username: '',
  password: ''
})

const handleLogin = async (): Promise<void> => {
  if (loading.value) return

  loading.value = true
  error.value = ''

  try {
    await userStore.login(loginData.value)

    // 登录成功，跳转到首页或来源页面
    const redirect = router.currentRoute.value.query.redirect || '/'
    router.push(redirect)

  } catch (err) {
    error.value = err.detail || err.message || '登录失败，请检查用户名和密码'
    console.error('登录失败:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #6c757d;
  margin: 0;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #6c757d;
}

.checkbox {
  width: 1.1rem;
  height: 1.1rem;
}

.forgot-link {
  color: #3498db;
  text-decoration: none;
  font-size: 0.9rem;
}

.forgot-link:hover {
  text-decoration: underline;
}

.login-btn {
  width: 100%;
  margin-bottom: 1.5rem;
}

.login-divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
  color: #6c757d;
}

.login-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #ecf0f1;
}

.login-divider span {
  background: white;
  padding: 0 1rem;
  position: relative;
}

.register-link {
  text-align: center;
  color: #6c757d;
}

.link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  margin-left: 0.5rem;
}

.link:hover {
  text-decoration: underline;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #f5c6cb;
  text-align: center;
  font-size: 0.9rem;
}

@media (max-width: 480px) {
  .login-page {
    padding: 1rem;
  }

  .login-card {
    padding: 2rem;
  }

  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>