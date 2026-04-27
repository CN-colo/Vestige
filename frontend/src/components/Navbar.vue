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
  background-color: #fff;
  border-bottom: 1px solid var(--el-border-color);
  height: 60px;
  padding: 0 20px;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1200px;
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
}

.brand-text {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.brand-subtitle {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin-left: 8px;
}

.navbar-menu {
  flex: 1;
  margin-left: 40px;
  border-bottom: none;
}

.navbar-menu .el-menu-item {
  padding: 0 20px;
}

.navbar-menu .el-menu-item a {
  text-decoration: none;
  color: inherit;
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  color: var(--el-text-color-primary);
}

.el-dropdown-menu a {
  text-decoration: none;
  color: inherit;
}
</style>