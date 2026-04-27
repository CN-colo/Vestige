<template>
  <div class="dashboard-page">
    <div class="dashboard-layout">
      <Sidebar />
      <div class="dashboard-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue'
</script>

<style scoped>
.dashboard-page {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-layout {
  display: flex;
  min-height: calc(100vh - 100px);
}

.dashboard-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
}
</style>