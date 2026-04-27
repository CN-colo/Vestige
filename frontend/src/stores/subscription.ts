import { defineStore } from 'pinia'
import { ref } from 'vue'
import { subscriptionsApi } from '@/api/subscriptions'
import type { SubscriptionFeed } from '@/types'

export const useSubscriptionStore = defineStore('subscription', () => {
  const subscriptions = ref<string[]>([])
  const feed = ref<SubscriptionFeed | null>(null)
  const popularTags = ref<{ tag: string; count: number }[]>([])
  const loading = ref(false)

  // 订阅标签
  const subscribeTag = async (tag: string) => {
    const normalizedTag = tag.trim().toLowerCase()
    await subscriptionsApi.subscribe({ tag: normalizedTag })
    if (!subscriptions.value.includes(normalizedTag)) {
      subscriptions.value.push(normalizedTag)
    }
  }

  // 取消订阅
  const unsubscribeTag = async (tag: string) => {
    const normalizedTag = tag.trim().toLowerCase()
    await subscriptionsApi.unsubscribe(normalizedTag)
    subscriptions.value = subscriptions.value.filter(t => t !== normalizedTag)
  }

  // 加载订阅列表
  const loadSubscriptions = async () => {
    loading.value = true
    try {
      const result = await subscriptionsApi.getSubscriptions()
      subscriptions.value = result.tags
    } finally {
      loading.value = false
    }
  }

  // 加载订阅推送内容
  const loadFeed = async (page = 1, pageSize = 10) => {
    loading.value = true
    try {
      feed.value = await subscriptionsApi.getFeed(page, pageSize)
    } finally {
      loading.value = false
    }
  }

  // 加载热门标签
  const loadPopularTags = async (limit = 20) => {
    popularTags.value = await subscriptionsApi.getPopularTags(limit)
  }

  // 检查是否订阅了某个标签
  const isSubscribed = (tag: string): boolean => {
    const normalizedTag = tag.trim().toLowerCase()
    return subscriptions.value.includes(normalizedTag)
  }

  // 切换订阅状态
  const toggleSubscription = async (tag: string): Promise<boolean> => {
    const normalizedTag = tag.trim().toLowerCase()
    if (isSubscribed(normalizedTag)) {
      await unsubscribeTag(normalizedTag)
      return false
    } else {
      await subscribeTag(normalizedTag)
      return true
    }
  }

  return {
    subscriptions,
    feed,
    popularTags,
    loading,
    subscribeTag,
    unsubscribeTag,
    loadSubscriptions,
    loadFeed,
    loadPopularTags,
    isSubscribed,
    toggleSubscription
  }
})