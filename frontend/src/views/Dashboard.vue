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
  max-width: var(--content-max-width);
  margin: 0 auto;
}

.dashboard-layout {
  display: flex;
  min-height: calc(100vh - var(--navbar-height));
}

.dashboard-content {
  flex: 1;
  padding: var(--spacing-lg);
  background-color: var(--bg-page);
}
</style>