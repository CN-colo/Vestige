<template>
  <el-header class="navbar">
    <div class="navbar-content">
      <!-- 移动端汉堡菜单按钮 -->
      <el-icon class="hamburger-btn" @click="toggleMobileSidebar" v-if="isLoggedIn">
        <Menu />
      </el-icon>

      <div class="navbar-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-text">Vestige</span>
          <span class="brand-subtitle">古墟</span>
        </router-link>
      </div>

      <!-- 桌面端菜单 -->
      <el-menu
        :default-active="activeMenu"
        class="navbar-menu desktop-menu"
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

      <!-- 桌面端用户区域 -->
      <div class="navbar-user desktop-user">
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

      <!-- 移动端用户区域 -->
      <div class="navbar-user mobile-user">
        <template v-if="isLoggedIn">
          <el-dropdown trigger="click">
            <el-avatar v-if="user?.avatar" :src="user.avatar" :size="32" />
            <el-avatar v-else :size="32">
              {{ user?.username?.charAt(0).toUpperCase() }}
            </el-avatar>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <router-link to="/">广场</router-link>
                </el-dropdown-item>
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
        </template>
      </div>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Menu } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const emit = defineEmits<{
  (e: 'toggleSidebar'): void
}>()

const user = computed(() => userStore.user)
const isLoggedIn = computed(() => userStore.isLoggedIn)
const activeMenu = computed(() => route.path.split('/')[1] || '/')

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

const toggleMobileSidebar = () => {
  emit('toggleSidebar')
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

/* 汉堡菜单按钮 */
.hamburger-btn {
  font-size: 20px;
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  transition: background-color var(--transition-fast);
  display: none; /* 默认隐藏，移动端显示 */
}

.hamburger-btn:hover {
  background-color: var(--gray-100);
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

/* 移动端用户区域默认隐藏 */
.mobile-user {
  display: none;
}

/* 桌面端用户区域默认显示 */
.desktop-user {
  display: flex;
}

/* 响应式：手机端 (< 1024px) */
@media (max-width: 1023px) {
  .navbar {
    padding: 0 var(--spacing-sm);
  }

  .hamburger-btn {
    display: flex;
    margin-right: var(--spacing-sm);
  }

  .desktop-menu {
    display: none;
  }

  .desktop-user {
    display: none;
  }

  .mobile-user {
    display: flex;
  }

  .brand-text {
    font-size: var(--font-size-lg);
  }

  .brand-subtitle {
    font-size: var(--font-size-xs);
  }
}
</style>