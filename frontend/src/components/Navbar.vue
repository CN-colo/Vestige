<template>
  <el-header class="navbar">
    <div class="navbar-content">
      <div class="navbar-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-text">Vestige</span>
          <span class="brand-subtitle">古墟</span>
        </router-link>
      </div>

      <el-menu
        :default-active="activeMenu"
        class="navbar-menu"
        mode="horizontal"
        :ellipsis="false"
      >
        <el-menu-item index="/">
          <router-link to="/">广场</router-link>
        </el-menu-item>

        <el-menu-item v-if="isLoggedIn" index="/dashboard">
          <router-link to="/dashboard">我的</router-link>
        </el-menu-item>
      </el-menu>

      <div class="navbar-user">
        <template v-if="isLoggedIn">
          <el-dropdown trigger="click">
            <span class="user-dropdown">
              <el-avatar v-if="user?.avatar" :src="user.avatar" :size="32" />
              <el-avatar v-else :size="32">
                {{ user?.username?.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ user?.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <router-link to="/dashboard">仪表盘</router-link>
                </el-dropdown-item>
                <el-dropdown-item>
                  <router-link to="/dashboard/settings">设置</router-link>
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  登出
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" size="small" @click="$router.push('/login')">
            登录
          </el-button>
          <el-button size="small" @click="$router.push('/register')">
            注册
          </el-button>
        </template>
      </div>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)
const isLoggedIn = computed(() => userStore.isLoggedIn)
const activeMenu = computed(() => route.path.split('/')[1] || '/')

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: none;
  box-shadow: var(--shadow-sm);
  height: var(--navbar-height);
  padding: 0 var(--spacing-lg);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: var(--content-max-width);
  margin: 0 auto;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: baseline;
  text-decoration: none;
  transition: opacity var(--transition-fast);
}

.brand-link:hover {
  opacity: 0.85;
}

.brand-text {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
  letter-spacing: -0.5px;
}

.brand-subtitle {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-left: var(--spacing-xs);
  font-weight: var(--font-weight-medium);
}

.navbar-menu {
  flex: 1;
  margin-left: var(--spacing-xl);
  border-bottom: none;
  background-color: transparent;
}

.navbar-menu .el-menu-item {
  padding: 0 var(--spacing-lg);
  height: var(--navbar-height);
  line-height: var(--navbar-height);
  border-radius: 0;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.navbar-menu .el-menu-item:hover {
  background-color: transparent;
  color: var(--primary-color);
}

.navbar-menu .el-menu-item.is-active {
  background-color: transparent;
  border-bottom: 2px solid var(--primary-color);
  color: var(--primary-color);
}

.navbar-menu .el-menu-item a {
  text-decoration: none;
  color: inherit;
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.user-dropdown:hover {
  background-color: var(--gray-50);
}

.username {
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.el-dropdown-menu a {
  text-decoration: none;
  color: inherit;
}
</style>