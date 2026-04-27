import { defineStore } from 'pinia'
import { ref } from 'vue'
import { followsApi } from '@/api/follows'
import type { FollowStats, UserWithFollowStatus } from '@/types'

export const useFollowStore = defineStore('follow', () => {
  const following = ref<UserWithFollowStatus[]>([])
  const followers = ref<UserWithFollowStatus[]>([])
  const stats = ref<FollowStats>({ following_count: 0, followers_count: 0 })
  const loading = ref(false)

  // 关注用户
  const followUser = async (userId: number): Promise<UserWithFollowStatus> => {
    const result = await followsApi.follow({ user_id: userId })
    // 更新本地状态
    stats.value.following_count++
    return result
  }

  // 取消关注
  const unfollowUser = async (userId: number) => {
    await followsApi.unfollow(userId)
    // 更新本地状态
    stats.value.following_count--
    following.value = following.value.filter(u => u.id !== userId)
  }

  // 加载关注列表
  const loadFollowing = async () => {
    loading.value = true
    try {
      following.value = await followsApi.getFollowing()
    } finally {
      loading.value = false
    }
  }

  // 加载粉丝列表
  const loadFollowers = async () => {
    loading.value = true
    try {
      followers.value = await followsApi.getFollowers()
    } finally {
      loading.value = false
    }
  }

  // 加载关注统计
  const loadStats = async () => {
    stats.value = await followsApi.getStats()
  }

  // 获取指定用户的关注信息
  const getUserFollowInfo = async (userId: number): Promise<UserWithFollowStatus> => {
    return await followsApi.getUserFollowInfo(userId)
  }

  // 检查是否关注了指定用户
  const checkFollowing = async (userId: number): Promise<boolean> => {
    const result = await followsApi.checkFollowing(userId)
    return result.is_following
  }

  // 切换关注状态
  const toggleFollow = async (userId: number): Promise<boolean> => {
    const isFollowing = await checkFollowing(userId)
    if (isFollowing) {
      await unfollowUser(userId)
      return false
    } else {
      await followUser(userId)
      return true
    }
  }

  return {
    following,
    followers,
    stats,
    loading,
    followUser,
    unfollowUser,
    loadFollowing,
    loadFollowers,
    loadStats,
    getUserFollowInfo,
    checkFollowing,
    toggleFollow
  }
})