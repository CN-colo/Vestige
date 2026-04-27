<template>
  <el-button 
    v-if="userId && userId > 0 && !isNaN(userId)"
    :type="isFollowing ? 'default' : 'primary'"
    :loading="loading"
    :disabled="disabled"
    @click="handleClick"
  >
    {{ buttonText }}
  </el-button>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useFollowStore } from '@/stores/follow'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  userId: number
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'change', isFollowing: boolean): void
}>()

const followStore = useFollowStore()
const userStore = useUserStore()
const loading = ref(false)
const isFollowing = ref(false)
const followersCount = ref(0)

// 计算按钮文字
const buttonText = computed(() => {
  if (isFollowing.value) {
    return '已关注'
  }
  return '关注'
})

// 检查是否是当前用户自己
const isSelf = computed(() => {
  return userStore.user?.id === props.userId
})

// 加载关注状态
const loadFollowStatus = async () => {
  // 检查 userId 是否有效
  if (!props.userId || props.userId <= 0 || isNaN(props.userId)) return
  if (!userStore.isLoggedIn || isSelf.value) return
  
  try {
    const info = await followStore.getUserFollowInfo(props.userId)
    isFollowing.value = info.is_following
    followersCount.value = info.followers_count
  } catch (error) {
    console.error('Failed to load follow status:', error)
  }
}

// 处理点击
const handleClick = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  if (isSelf.value) {
    ElMessage.warning('不能关注自己')
    return
  }
  
  loading.value = true
  try {
    const newState = await followStore.toggleFollow(props.userId)
    isFollowing.value = newState
    followersCount.value = newState ? followersCount.value + 1 : followersCount.value - 1
    emit('change', newState)
    ElMessage.success(newState ? '关注成功' : '已取消关注')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

// 监听 userId 变化
watch(() => props.userId, () => {
  loadFollowStatus()
})

onMounted(() => {
  loadFollowStatus()
})
</script>