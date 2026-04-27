<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <Navbar @toggle-sidebar="toggleSidebar" />
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { onMounted, ref, provide } from 'vue'
import Navbar from '@/components/Navbar.vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isInitialized = ref(false)
const sidebarVisible = ref(false)

// 初始化用户状态
onMounted(async () => {
  await userStore.initUser()
  isInitialized.value = true
})

// 切换侧边栏
const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value
}

// 提供侧边栏状态给子组件
provide('sidebarVisible', sidebarVisible)
provide('toggleSidebar', toggleSidebar)
</script>

<style>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: var(--spacing-lg);
  background-color: var(--bg-page);
}

/* 手机端减少内边距 */
@media (max-width: 767px) {
  .main-content {
    padding: var(--spacing-sm);
  }
}
</style>