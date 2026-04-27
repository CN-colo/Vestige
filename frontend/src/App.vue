<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <Navbar />
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Navbar from '@/components/Navbar.vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isInitialized = ref(false)

// 初始化用户状态
onMounted(async () => {
  await userStore.initUser()
  isInitialized.value = true
})
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
</style>