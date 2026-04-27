<template>
  <div class="like-button" @click.stop="handleClick">
    <el-icon :size="size" :color="isLiked ? '#f56c6c' : '#909399'" class="like-icon" :class="{ 'is-liked': isLiked }">
      <component :is="LikeIcon" />
    </el-icon>
    <span class="like-count" :class="{ 'is-liked': isLiked }" v-if="showCount">{{ likeCount }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, markRaw } from 'vue'
import { CaretTop } from '@element-plus/icons-vue'
import { useLikeStore } from '@/stores/like'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

// 导出图标供模板使用
const LikeIcon = markRaw(CaretTop)

const props = defineProps<{
  targetType: 'article' | 'project'
  targetId: number
  initialLikeCount?: number
  initialIsLiked?: boolean
  size?: number
  showCount?: boolean
}>()

const emit = defineEmits<{
  (e: 'change', isLiked: boolean, likeCount: number): void
}>()

const likeStore = useLikeStore()
const userStore = useUserStore()
const isLiked = ref(false)
const likeCount = ref(0)
const loading = ref(false)

// 加载点赞状态
const loadLikeStatus = async () => {
  if (props.initialIsLiked !== undefined && props.initialLikeCount !== undefined) {
    isLiked.value = props.initialIsLiked
    likeCount.value = props.initialLikeCount
    return
  }
  
  try {
    const status = await likeStore.getStatus(props.targetType, props.targetId)
    isLiked.value = status.is_liked
    likeCount.value = status.like_count
  } catch (error) {
    console.error('Failed to load like status:', error)
  }
}

// 处理点击
const handleClick = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  if (loading.value) return
  loading.value = true
  
  try {
    const newState = await likeStore.toggleLike(props.targetType, props.targetId)
    isLiked.value = newState
    likeCount.value = newState ? likeCount.value + 1 : Math.max(0, likeCount.value - 1)
    emit('change', newState, likeCount.value)
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

// 监听 targetId 变化
watch(() => props.targetId, () => {
  loadLikeStatus()
})

onMounted(() => {
  loadLikeStatus()
})
</script>

<style scoped>
.like-button {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  user-select: none;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.like-button:hover {
  background-color: rgba(245, 108, 108, 0.1);
}

.like-icon {
  transition: transform 0.2s;
}

.like-icon.is-liked {
  transform: scale(1.1);
}

.like-button:hover .like-icon {
  transform: scale(1.2);
}

.like-count {
  color: #909399;
  font-size: 12px;
}

.like-count.is-liked {
  color: #f56c6c;
  font-weight: 500;
}
</style>