<template>
  <div class="login-page">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>登录</h2>
          <p>欢迎回到 Vestige</p>
        </div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%">
            登录
          </el-button>
        </el-form-item>

        <div class="footer-links">
          <span>还没有账号？</span>
          <router-link to="/register">立即注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await userStore.login(form.value)
        ElMessage.success('登录成功')
        const redirect = route.query.redirect as string || '/dashboard'
        router.push(redirect)
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '登录失败')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 100px);
  padding: var(--spacing-lg);
  background: var(--bg-page);
}

.login-card {
  width: 400px;
  max-width: 100%;
  border-radius: var(--radius-xl);
  border: none;
  box-shadow: var(--shadow-md);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.card-header p {
  margin: var(--spacing-sm) 0 0 0;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.footer-links {
  text-align: center;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.footer-links a {
  color: var(--primary-color);
  margin-left: var(--spacing-xs);
  font-weight: var(--font-weight-medium);
  transition: color var(--transition-fast);
}

.footer-links a:hover {
  color: var(--primary-light);
}

/* 手机端适配 */
@media (max-width: 767px) {
  .login-page {
    min-height: calc(100vh - 60px);
    padding: var(--spacing-sm);
  }

  .login-card {
    width: 100%;
  }

  .card-header h2 {
    font-size: var(--font-size-xl);
  }
}
</style>