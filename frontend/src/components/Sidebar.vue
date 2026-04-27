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
  width: 200px;
  background-color: #fff;
  border-right: 1px solid var(--el-border-color);
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 50px;
}
</style>