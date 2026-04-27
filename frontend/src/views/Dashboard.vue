<template>
  <div class="dashboard-page">
    <div class="dashboard-layout">
      <!-- 桌面端固定侧边栏 -->
      <div class="desktop-sidebar">
        <Sidebar />
      </div>
      
      <!-- 移动端抽屉侧边栏 -->
      <el-drawer
        v-model="sidebarVisible"
        direction="ltr"
        size="70%"
        class="mobile-sidebar-drawer"
      >
        <Sidebar />
      </el-drawer>
      
      <div class="dashboard-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const route = useRoute()

// 从 App.vue 获取侧边栏状态
const sidebarVisible = inject('sidebarVisible') as any

// 路由变化时关闭抽屉
watch(() => route.path, () => {
  if (sidebarVisible?.value) {
    sidebarVisible.value = false
  }
})

// 监听屏幕宽度变化
const checkScreenWidth = () => {
  if (window.innerWidth >= 1024 && sidebarVisible?.value) {
    sidebarVisible.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', checkScreenWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenWidth)
})
</script>

<style scoped>
.dashboard-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
}

.dashboard-layout {
  display: flex;
  min-height: calc(100vh - var(--navbar-height) - var(--spacing-lg) * 2);
}

/* 桌面端侧边栏 */
.desktop-sidebar {
  display: block;
}

/* 内容区域 */
.dashboard-content {
  flex: 1;
  min-width: 0;  /* 防止 flex 子元素被内容撑大 */
  overflow-x: hidden;  /* 防止横向溢出 */
  padding: var(--spacing-lg);
  background-color: var(--bg-page);
}

/* 手机端适配 */
@media (max-width: 1023px) {
  .dashboard-page {
    max-width: 100%;
  }

  .desktop-sidebar {
    display: none;
  }

  .dashboard-layout {
    flex-direction: column;
    min-height: calc(100vh - var(--navbar-height) - var(--spacing-sm) * 2);
  }

  .dashboard-content {
    padding: var(--spacing-sm);
  }
}

/* 抽屉样式 */
:deep(.mobile-sidebar-drawer) {
  .el-drawer__header {
    margin-bottom: 0;
    padding: var(--spacing-sm);
    border-bottom: 1px solid var(--border-light);
  }

  .el-drawer__body {
    padding: 0;
  }
}
</style>