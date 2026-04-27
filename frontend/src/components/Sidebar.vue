<template>
  <div class="sidebar">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      router
    >
      <el-menu-item index="/dashboard/articles">
        <el-icon><Document /></el-icon>
        <span>文章管理</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/projects">
        <el-icon><FolderOpened /></el-icon>
        <span>作品管理</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/favorites">
        <el-icon><Star /></el-icon>
        <span>我的收藏</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/follows">
        <el-icon><User /></el-icon>
        <span>关注/粉丝</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/subscriptions">
        <el-icon><Bell /></el-icon>
        <span>订阅推送</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/card">
        <el-icon><Postcard /></el-icon>
        <span>我的名片</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/keys">
        <el-icon><Key /></el-icon>
        <span>API Keys</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/settings">
        <el-icon><Setting /></el-icon>
        <span>设置</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Star, Postcard, User, Bell } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--bg-card);
  border-right: 1px solid var(--border-light);
  padding: var(--spacing-md) 0;
}

.sidebar-menu {
  border-right: none;
  background-color: transparent;
}

.sidebar-menu .el-menu-item {
  height: 44px;
  line-height: 44px;
  margin: 4px var(--spacing-sm);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.sidebar-menu .el-menu-item:hover {
  background-color: var(--gray-50);
}

.sidebar-menu .el-menu-item.is-active {
  background-color: var(--primary-lighter);
  color: var(--primary-color);
}

.sidebar-menu .el-menu-item .el-icon {
  font-size: 18px;
  margin-right: var(--spacing-sm);
}
</style>