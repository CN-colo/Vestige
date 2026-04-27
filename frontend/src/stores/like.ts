import { defineStore } from 'pinia'
import { ref } from 'vue'
import { likesApi } from '@/api/likes'
import type { Like, LikeStatus } from '@/types'

export const useLikeStore = defineStore('like', () => {
  const myLikes = ref<Like[]>([])
  const loading = ref(false)
  // 缓存点赞状态
  const likeStatusCache = ref<Map<string, LikeStatus>>(new Map())

  // 点赞
  const like = async (targetType: 'article' | 'project', targetId: number): Promise<Like> => {
    const result = await likesApi.like({ target_type: targetType, target_id: targetId })
    // 更新缓存
    const key = `${targetType}_${targetId}`
    const current = likeStatusCache.value.get(key)
    if (current) {
      likeStatusCache.value.set(key, { is_liked: true, like_count: current.like_count + 1 })
    } else {
      likeStatusCache.value.set(key, { is_liked: true, like_count: 1 })
    }
    return result
  }

  // 取消点赞
  const unlike = async (targetType: 'article' | 'project', targetId: number) => {
    await likesApi.unlike(targetType, targetId)
    // 更新缓存
    const key = `${targetType}_${targetId}`
    const current = likeStatusCache.value.get(key)
    if (current) {
      likeStatusCache.value.set(key, { is_liked: false, like_count: Math.max(0, current.like_count - 1) })
    }
  }

  // 获取点赞状态
  const getStatus = async (targetType: 'article' | 'project', targetId: number): Promise<LikeStatus> => {
    const key = `${targetType}_${targetId}`
    // 如果有缓存，直接返回
    if (likeStatusCache.value.has(key)) {
      return likeStatusCache.value.get(key)!
    }
    // 否则请求服务器
    const status = await likesApi.getStatus(targetType, targetId)
    likeStatusCache.value.set(key, status)
    return status
  }

  // 加载我的点赞列表
  const loadMyLikes = async (targetType?: 'article' | 'project') => {
    loading.value = true
    try {
      myLikes.value = await likesApi.getMyLikes(targetType)
    } finally {
      loading.value = false
    }
  }

  // 获取点赞用户列表
  const getLikeUsers = async (targetType: 'article' | 'project', targetId: number, limit = 20) => {
    return await likesApi.getLikeUsers(targetType, targetId, limit)
  }

  // 切换点赞状态
  const toggleLike = async (targetType: 'article' | 'project', targetId: number): Promise<boolean> => {
    const status = await getStatus(targetType, targetId)
    if (status.is_liked) {
      await unlike(targetType, targetId)
      return false
    } else {
      await like(targetType, targetId)
      return true
    }
  }

  // 清除缓存（用于刷新数据）
  const clearCache = () => {
    likeStatusCache.value.clear()
  }

  return {
    myLikes,
    loading,
    likeStatusCache,
    like,
    unlike,
    getStatus,
    loadMyLikes,
    getLikeUsers,
    toggleLike,
    clearCache
  }
})