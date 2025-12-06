<template>
  <div class="register-page">
    <div class="container">
      <div class="register-card">
        <div class="register-header">
          <h1>注册账号</h1>
          <p>加入我们，开始分享你的创意</p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label class="form-label">用户名 *</label>
            <input
              v-model="registerData.username"
              type="text"
              placeholder="请输入用户名"
              class="form-input"
              :class="{ error: errors.username }"
              required
            />
            <div v-if="errors.username" class="error-text">{{ errors.username }}</div>
          </div>

          <div class="form-group">
            <label class="form-label">邮箱 *</label>
            <input
              v-model="registerData.email"
              type="email"
              placeholder="请输入邮箱地址"
              class="form-input"
              :class="{ error: errors.email }"
              required
            />
            <div v-if="errors.email" class="error-text">{{ errors.email }}</div>
          </div>

          <div class="form-group">
            <label class="form-label">密码 *</label>
            <input
              v-model="registerData.password"
              type="password"
              placeholder="请输入密码（至少6位）"
              class="form-input"
              :class="{ error: errors.password }"
              required
            />
            <div v-if="errors.password" class="error-text">{{ errors.password }}</div>
          </div>

          <div class="form-group">
            <label class="form-label">确认密码 *</label>
            <input
              v-model="registerData.password_confirm"
              type="password"
              placeholder="请再次输入密码"
              class="form-input"
              :class="{ error: errors.password_confirm }"
              required
            />
            <div v-if="errors.password_confirm" class="error-text">{{ errors.password_confirm }}</div>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="agreeTerms" type="checkbox" class="checkbox" required />
              <span>我已阅读并同意</span>
            </label>
            <router-link to="/terms" class="terms-link">《用户协议》</router-link>
            和
            <router-link to="/privacy" class="terms-link">《隐私政策》</router-link>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="btn btn-primary btn-large register-btn"
          >
            {{ loading ? '注册中...' : '注册账号' }}
          </button>

          <div class="login-link">
            已有账号？
            <router-link to="/login" class="link">立即登录</router-link>
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
const agreeTerms = ref<boolean>(false)

const registerData = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const errors = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const validateForm = (): boolean => {
  let isValid = true
  errors.value = { username: '', email: '', password: '', password_confirm: '' }

  // 用户名验证
  if (registerData.value.username.length < 3) {
    errors.value.username = '用户名至少3个字符'
    isValid = false
  }

  // 邮箱验证
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(registerData.value.email)) {
    errors.value.email = '请输入有效的邮箱地址'
    isValid = false
  }

  // 密码验证
  if (registerData.value.password.length < 6) {
    errors.value.password = '密码至少6个字符'
    isValid = false
  }

  // 确认密码验证
  if (registerData.value.password !== registerData.value.password_confirm) {
    errors.value.password_confirm = '两次输入的密码不一致'
    isValid = false
  }

  // 协议同意验证
  if (!agreeTerms.value) {
    error.value = '请同意用户协议和隐私政策'
    isValid = false
  }

  return isValid
}

const handleRegister = async (): Promise<void> => {
  if (loading.value) return

  if (!validateForm()) {
    return
  }

  loading.value = true
  error.value = ''

  try {
    await userStore.register(registerData.value)

    // 注册成功，自动登录
    await userStore.login({
      username: registerData.value.username,
      password: registerData.value.password
    })

    // 跳转到首页
    router.push('/')

  } catch (err) {
    if (err.username) {
      errors.value.username = err.username[0]
    } else if (err.email) {
      errors.value.email = err.email[0]
    } else {
      error.value = err.detail || err.message || '注册失败，请重试'
    }
    console.error('注册失败:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-card {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 450px;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.register-header p {
  color: #6c757d;
  margin: 0;
}

.register-form {
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

.form-input.error {
  border-color: #e74c3c;
}

.error-text {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.3rem;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #6c757d;
  margin-right: 0.3rem;
}

.checkbox {
  width: 1.1rem;
  height: 1.1rem;
}

.terms-link {
  color: #3498db;
  text-decoration: none;
  font-size: 0.9rem;
}

.terms-link:hover {
  text-decoration: underline;
}

.register-btn {
  width: 100%;
  margin: 1.5rem 0;
}

.login-link {
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
  .register-page {
    padding: 1rem;
  }

  .register-card {
    padding: 2rem;
  }
}
</style>