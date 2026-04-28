<template>
  <el-tag 
    :type="isSubscribed ? 'primary' : 'info'"
    :effect="isSubscribed ? 'dark' : 'plain'"
    class="tag-subscribe-btn"
    @click.stop="handleClick"
  >
    {{ tag }}
    <el-icon v-if="loading" class="is-loading"><Loading /></el-icon>
    <el-icon v-else-if="isSubscribed"><Check /></el-icon>
    <el-icon v-else><Plus /></el-icon>
  </el-tag>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Check, Loading } from '@element-plus/icons-vue'
import { useSubscriptionStore } from '@/stores/subscription'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  tag: string
}>()

const emit = defineEmits<{
  (e: 'change', isSubscribed: boolean): void
}>()

const subscriptionStore = useSubscriptionStore()
const userStore = useUserStore()
const loading = ref(false)
const isSubscribed = ref(false)

// 检查订阅状态
const checkSubscription = async () => {
  if (!userStore.isLoggedIn) {
    isSubscribed.value = false
    return
  }
  
  // 确保已加载订阅列表
  if (subscriptionStore.subscriptions.length === 0) {
    await subscriptionStore.loadSubscriptions()
  }
  
  isSubscribed.value = subscriptionStore.isSubscribed(props.tag)
}

// 处理点击
const handleClick = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  loading.value = true
  try {
    const newState = await subscriptionStore.toggleSubscription(props.tag)
    isSubscribed.value = newState
    emit('change', newState)
    ElMessage.success(newState ? `已订阅标签 "${props.tag}"` : `已取消订阅标签 "${props.tag}"`)
  } catch (error: any) {
    ElMessage.error(error.userMessage || error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  checkSubscription()
})
</script>

<style scoped>
.tag-subscribe-btn {
  cursor: pointer;
  user-select: none;
}

.tag-subscribe-btn .el-icon {
  margin-left: 4px;
  font-size: 12px;
}

.is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>